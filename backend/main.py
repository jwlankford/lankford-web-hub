import os
import sys

# Dynamic root patching for Python 3.14 worker threads
backend_root = os.path.dirname(os.path.abspath(__file__))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from database import init_db, get_async_session
# Import our new data models alongside the tenant helpers
from models import TenantDomain, BookMailingList, ResearchPaper, ResearchTag

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[SYSTEM] Executing database verification...")
    await init_db()
    print("[SYSTEM] Database tables synchronized successfully.")
    yield

app = FastAPI(title="Lankford Dual-Domain Core API", lifespan=lifespan)

# Configure CORS to accept requests from both frontends
origins = [
    "http://localhost:5173",          # Vite dev port 1
    "http://localhost:5174",          # Vite dev port 2
    "http://professional.localhost",
    "http://academic.localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def determine_tenant_middleware(request: Request, call_next):
    # Support explicit X-Tenant header override for API clients and dev environments
    x_tenant = request.headers.get("x-tenant", "").lower()
    host = request.headers.get("host", "").lower()
    clean_host = host.split(":")[0]
    port = host.split(":")[1] if ":" in host else ""
    
    if x_tenant in ["professional", "academic"]:
        request.state.tenant = x_tenant
    elif clean_host in [TenantDomain.PROFESSIONAL.value, TenantDomain.LOCAL_PROFESSIONAL.value] or port == "5173":
        request.state.tenant = "professional"
    elif clean_host in [TenantDomain.ACADEMIC.value, TenantDomain.LOCAL_ACADEMIC.value] or port == "5174":
        request.state.tenant = "academic"
    else:
        request.state.tenant = "system"
        
    response = await call_next(request)
    return response


# ==========================================
# PROFESSIONAL DOMAIN ROUTES (Mailing List)
# ==========================================

@app.post("/api/v1/book/signup", status_code=status.HTTP_201_CREATED)
async def add_to_mailing_list(
    entry: BookMailingList, 
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Saves a reader email to the mailing list, explicitly binding 
    it to the active tenant domain context.
    """
    if request.state.tenant != "professional":
        raise HTTPException(
            status_code=403, 
            detail="Mailing list registration is only permitted via the professional domain."
        )
        
    # Inject the tenant identifier before saving
    entry.tenant = request.state.tenant
    
    try:
        db.add(entry)
        await db.commit()
        await db.refresh(entry)
        return {"status": "success", "email": entry.email}
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="This email is already registered.")


# ==========================================
# ACADEMIC DOMAIN ROUTES (Research Index)
# ==========================================

@app.get("/api/v1/research/papers", response_model=list[ResearchPaper])
async def get_research_papers(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Fetches papers linked ONLY to the active tenant environment.
    """
    if request.state.tenant != "academic":
        raise HTTPException(
            status_code=403, 
            detail="Academic assets are restricted outside of the academic domain context."
        )
        
    # Enforce row-level multi-tenancy inside the query select statement
    statement = select(ResearchPaper).where(ResearchPaper.tenant == request.state.tenant)
    results = await db.execute(statement)
    return results.scalars().all()


@app.post("/api/v1/research/papers", status_code=status.HTTP_201_CREATED)
async def add_research_paper(
    paper: ResearchPaper,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Indexes a new academic reference, explicitly embedding the tenant key.
    """
    if request.state.tenant != "academic":
        raise HTTPException(
            status_code=403, 
            detail="Modifying academic records requires an active academic domain context."
        )
        
    paper.tenant = request.state.tenant
    db.add(paper)
    await db.commit()
    await db.refresh(paper)
    return paper