import os
import sys

from dotenv import load_dotenv

# Load environment variables before setting up app config
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

# Dynamic root patching for Python 3.14 worker threads
backend_root = os.path.dirname(os.path.abspath(__file__))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
import urllib.request
import json
from typing import Optional, List
from pydantic import BaseModel
from bs4 import BeautifulSoup


from database import init_db, get_async_session
from config import settings
from sqlalchemy.orm import selectinload
import time
# Import our new data models alongside the tenant helpers
from models import TenantDomain, BookMailingList, ResearchPaper, ResearchTag, ResearchPaperRead, Article, GoogleNotebook, JupyterNotebook, ContactMessage

# Simple in-memory TTL cache to reduce database round-trips
_api_cache = {}
def get_cached_response(key: str, ttl: int = 300):
    if key in _api_cache:
        data, ts = _api_cache[key]
        if time.time() - ts < ttl:
            return data
    return None

def set_cached_response(key: str, data):
    _api_cache[key] = (data, time.time())

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
    "https://jeremylankford.com",
    "https://www.jeremylankford.com",
    "https://jwlankford.com",
    "https://www.jwlankford.com",
    "https://jwlankford.github.io",
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


@app.post("/api/v1/contact", status_code=status.HTTP_201_CREATED)
async def submit_contact_message(
    message: ContactMessage,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Saves a contact form message submission, binding it to the active tenant context.
    """
    if request.state.tenant not in ["professional", "academic"]:
        raise HTTPException(
            status_code=403,
            detail="Contact message submission requires a valid tenant domain context."
        )
        
    message.tenant = request.state.tenant
    try:
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return {"status": "success", "id": message.id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database submission failed: {str(e)}"
        )


# ==========================================
# ACADEMIC DOMAIN ROUTES (Research Index)
# ==========================================

@app.get("/api/v1/research/papers", response_model=list[ResearchPaperRead])
async def get_research_papers(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Fetches papers linked ONLY to the active tenant environment.
    """
    if request.state.tenant not in ["professional", "academic"]:
        raise HTTPException(
            status_code=403, 
            detail="Academic assets are restricted outside of valid domain contexts."
        )
        
    cache_key = f"papers_{request.state.tenant}"
    cached = get_cached_response(cache_key)
    if cached is not None:
        return cached
        
    # Enforce row-level multi-tenancy inside the query select statement
    statement = (
        select(ResearchPaper)
        .where(ResearchPaper.tenant == request.state.tenant)
        .options(selectinload(ResearchPaper.tags))
    )
    results = await db.execute(statement)
    papers = results.scalars().all()
    set_cached_response(cache_key, papers)
    return papers

from datetime import datetime
from models import ResearchTag

class ResearchPaperCreateSchema(BaseModel):
    title: str
    authors: str
    publication_year: int
    journal_or_conf: Optional[str] = None
    abstract: Optional[str] = None
    key_findings: Optional[str] = None
    methodology: Optional[str] = None
    used_for: Optional[str] = None
    zotero_key: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[List[str]] = None



class ResearchPaperUpdateSchema(BaseModel):
    title: Optional[str] = None
    authors: Optional[str] = None
    publication_year: Optional[int] = None
    journal_or_conf: Optional[str] = None
    abstract: Optional[str] = None
    key_findings: Optional[str] = None
    methodology: Optional[str] = None
    used_for: Optional[str] = None
    zotero_key: Optional[str] = None
    url: Optional[str] = None
    tags: Optional[List[str]] = None

@app.patch("/api/v1/research/papers/{paper_id}", response_model=ResearchPaperRead)
async def update_research_paper(
    paper_id: int,
    payload: ResearchPaperUpdateSchema,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    if request.state.tenant not in ["professional", "academic"]:
        raise HTTPException(
            status_code=403, 
            detail="Modifying academic records requires an active domain context."
        )
        
    stmt = select(ResearchPaper).where(
        (ResearchPaper.id == paper_id) & (ResearchPaper.tenant == request.state.tenant)
    ).options(selectinload(ResearchPaper.tags))
    res = await db.execute(stmt)
    paper = res.scalars().first()
    
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
        
    update_data = payload.model_dump(exclude_unset=True)
    
    if "tags" in update_data:
        tags_input = update_data.pop("tags")
        if tags_input is not None:
            # clear existing tags
            paper.tags = []
            for t_name in tags_input:
                t_slug = t_name.lower().strip().replace(' ', '-')
                t_slug = "".join(c for c in t_slug if (c.isalnum() or c == '-'))
                
                tag_stmt = select(ResearchTag).where(ResearchTag.slug == t_slug)
                tag_res = await db.execute(tag_stmt)
                db_tag = tag_res.scalars().first()
                
                if not db_tag:
                    db_tag = ResearchTag(
                        name=t_name,
                        slug=t_slug,
                        tenant=request.state.tenant
                    )
                    db.add(db_tag)
                    await db.flush()
                paper.tags.append(db_tag)
        else:
            paper.tags = []
            
    for key, value in update_data.items():
        setattr(paper, key, value)
        
    db.add(paper)
    await db.commit()
    await db.refresh(paper)
    
    cache_key = f"papers_{request.state.tenant}"
    if cache_key in _api_cache:
        del _api_cache[cache_key]
        
    return paper


@app.post("/api/v1/research/papers", status_code=status.HTTP_201_CREATED)
async def add_research_paper(
    payload: ResearchPaperCreateSchema,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Indexes a new academic reference, explicitly embedding the tenant key and resolving tags.
    """
    if request.state.tenant not in ["professional", "academic"]:
        raise HTTPException(
            status_code=403, 
            detail="Modifying academic records requires an active domain context."
        )
        
    # 1. Create the base paper object
    paper = ResearchPaper(
        title=payload.title,
        authors=payload.authors,
        publication_year=payload.publication_year,
        journal_or_conf=payload.journal_or_conf,
        abstract=payload.abstract,
        key_findings=payload.key_findings,
        methodology=payload.methodology,
        used_for=payload.used_for,
        zotero_key=payload.zotero_key,
        url=payload.url,
        image_url=payload.image_url,
        tenant=request.state.tenant
    )
    db.add(paper)
    await db.flush() # Populate paper.id
    
    # 2. Add and link tags
    all_tags = payload.tags or []
    
    # Auto-generate tags from title, abstract, key_findings
    import re
    combined_text = f"{payload.title or ''} {payload.abstract or ''} {payload.key_findings or ''}"
    if combined_text.strip():
        # Strip HTML tags
        combined_text = BeautifulSoup(combined_text, "html.parser").get_text(separator=" ")
        words = re.findall(r'\b[a-zA-Z]{4,}\b', combined_text.lower())
        stopwords = {"this", "that", "with", "from", "your", "have", "more", "these", "were", "which", "also", "their", "they", "will", "would", "there", "could", "than", "been", "some", "other", "into", "only", "very", "even", "must", "such", "should", "about", "many", "what", "after", "when", "most", "through", "over", "between", "because", "using", "used", "based", "both", "each", "those", "does", "while", "where", "same", "then", "upon", "within", "without", "during", "however", "under", "well", "results", "analysis", "study", "paper", "research", "method", "approach", "model", "data"}
        
        freq = {}
        for w in words:
            if w not in stopwords:
                freq[w] = freq.get(w, 0) + 1
                
        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        # Select up to 5 top words as tags
        generated = [w[0].capitalize() for w in sorted_words[:5]]
        
        for g in generated:
            if not any(t.lower() == g.lower() for t in all_tags):
                all_tags.append(g)

    if all_tags:
        for t_name in all_tags:
            t_slug = t_name.lower().strip().replace(' ', '-')
            t_slug = "".join(c for c in t_slug if (c.isalnum() or c == '-'))
            
            # Check if tag already exists in database by slug (unique constraint)
            tag_stmt = select(ResearchTag).where(ResearchTag.slug == t_slug)
            tag_res = await db.execute(tag_stmt)
            db_tag = tag_res.scalars().first()
            
            if not db_tag:
                db_tag = ResearchTag(
                    name=t_name,
                    slug=t_slug,
                    tenant=request.state.tenant
                )
                db.add(db_tag)
                await db.flush() # Populate db_tag.id
                
            # Add link to join table directly if it doesn't already exist
            from models import ResearchPaperTagLink
            link_stmt = select(ResearchPaperTagLink).where(
                ResearchPaperTagLink.paper_id == paper.id,
                ResearchPaperTagLink.tag_id == db_tag.id
            )
            link_res = await db.execute(link_stmt)
            db_link = link_res.scalars().first()
            
            if not db_link:
                link = ResearchPaperTagLink(paper_id=paper.id, tag_id=db_tag.id)
                db.add(link)
            
    await db.commit()
    await db.refresh(paper)
    
    # Invalidate cache
    cache_key = f"papers_{request.state.tenant}"
    if cache_key in _api_cache:
        del _api_cache[cache_key]
        
    return paper


# ==========================================
# WEEKLY ARTICLES ROUTES (LinkedIn & Web)
# ==========================================

@app.get("/api/v1/articles", response_model=list[Article])
async def get_articles(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Fetches articles linked ONLY to the active tenant environment.
    """
    cache_key = f"articles_{request.state.tenant}"
    cached = get_cached_response(cache_key)
    if cached is not None:
        return cached

    statement = select(Article).where(
        Article.tenant == request.state.tenant,
        Article.is_published == True
    ).order_by(Article.published_at.desc())
    results = await db.execute(statement)
    articles = results.scalars().all()
    set_cached_response(cache_key, articles)
    return articles


@app.post("/api/v1/articles", status_code=status.HTTP_201_CREATED, response_model=Article)
async def add_article(
    article: Article,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Publishes a new article, explicitly embedding the active tenant identifier.
    """
    # Restrict modifying articles to active tenants (e.g., professional or academic)
    if request.state.tenant not in ["professional", "academic"]:
        raise HTTPException(
            status_code=403,
            detail="Modifying articles requires a valid domain context."
        )
        
    article.tenant = request.state.tenant
    db.add(article)
    await db.commit()
    await db.refresh(article)
    
    # Invalidate cache
    cache_key = f"articles_{request.state.tenant}"
    if cache_key in _api_cache:
        del _api_cache[cache_key]
        
    return article


# ==========================================
# GOOGLE NOTEBOOKLM ROUTES
# ==========================================

@app.get("/api/v1/notebooks/google", response_model=list[GoogleNotebook])
async def get_google_notebooks(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Fetches Google NotebookLM notebooks linked ONLY to the active tenant environment.
    """
    if request.state.tenant not in ["professional", "academic"]:
        raise HTTPException(
            status_code=403,
            detail="Domain context is required to query Google Notebooks."
        )
        
    cache_key = f"google_notebooks_{request.state.tenant}"
    cached = get_cached_response(cache_key)
    if cached is not None:
        return cached
        
    statement = select(GoogleNotebook).where(
        GoogleNotebook.tenant == request.state.tenant,
        GoogleNotebook.is_public == True
    ).order_by(GoogleNotebook.created_at.desc())
    results = await db.execute(statement)
    notebooks = results.scalars().all()
    set_cached_response(cache_key, notebooks)
    return notebooks


@app.post("/api/v1/notebooks/google", status_code=status.HTTP_201_CREATED, response_model=GoogleNotebook)
async def add_google_notebook(
    notebook: GoogleNotebook,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Saves a new Google NotebookLM link, explicitly embedding the active tenant context.
    """
    if request.state.tenant not in ["professional", "academic"]:
        raise HTTPException(
            status_code=403,
            detail="Modifying records requires a valid domain context."
        )
    notebook.tenant = request.state.tenant
    db.add(notebook)
    await db.commit()
    await db.refresh(notebook)
    
    # Invalidate cache
    cache_key = f"google_notebooks_{request.state.tenant}"
    if cache_key in _api_cache:
        del _api_cache[cache_key]
        
    return notebook


# ==========================================
# JUPYTER NOTEBOOK ROUTES
# ==========================================

@app.get("/api/v1/notebooks/jupyter", response_model=list[JupyterNotebook])
async def get_jupyter_notebooks(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Fetches Jupyter notebooks linked ONLY to the active tenant environment.
    """
    if request.state.tenant not in ["professional", "academic"]:
        raise HTTPException(
            status_code=403,
            detail="Domain context is required to query Jupyter Notebooks."
        )
        
    cache_key = f"jupyter_notebooks_{request.state.tenant}"
    cached = get_cached_response(cache_key)
    if cached is not None:
        return cached
        
    statement = select(JupyterNotebook).where(
        JupyterNotebook.tenant == request.state.tenant
    ).order_by(JupyterNotebook.created_at.desc())
    results = await db.execute(statement)
    notebooks = results.scalars().all()
    set_cached_response(cache_key, notebooks)
    return notebooks


@app.post("/api/v1/notebooks/jupyter", status_code=status.HTTP_201_CREATED, response_model=JupyterNotebook)
async def add_jupyter_notebook(
    notebook: JupyterNotebook,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Saves a new Jupyter notebook link, explicitly embedding the active tenant context.
    """
    if request.state.tenant not in ["professional", "academic"]:
        raise HTTPException(
            status_code=403,
            detail="Modifying records requires a valid domain context."
        )
    notebook.tenant = request.state.tenant
    db.add(notebook)
    await db.commit()
    await db.refresh(notebook)
    
    # Invalidate cache
    cache_key = f"jupyter_notebooks_{request.state.tenant}"
    if cache_key in _api_cache:
        del _api_cache[cache_key]
        
    return notebook
