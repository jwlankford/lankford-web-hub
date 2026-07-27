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
import urllib.request
import json
from typing import Optional, List
from pydantic import BaseModel
from bs4 import BeautifulSoup
import google.generativeai as genai

from database import init_db, get_async_session
from sqlalchemy.orm import selectinload
# Import our new data models alongside the tenant helpers
from models import TenantDomain, BookMailingList, ResearchPaper, ResearchTag, ResearchPaperRead, Article, GoogleNotebook, JupyterNotebook, ContactMessage

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
        
    # Enforce row-level multi-tenancy inside the query select statement
    statement = (
        select(ResearchPaper)
        .where(ResearchPaper.tenant == request.state.tenant)
        .options(selectinload(ResearchPaper.tags))
    )
    results = await db.execute(statement)
    return results.scalars().all()


class AutoExtractRequest(BaseModel):
    url: str

class ResearchPaperCreateSchema(BaseModel):
    title: str
    authors: str
    publication_year: int
    journal_or_conf: Optional[str] = None
    abstract: Optional[str] = None
    key_findings: Optional[str] = None
    methodology: Optional[str] = None
    zotero_key: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[List[str]] = None

@app.post("/api/v1/research/auto-extract")
async def auto_extract_paper_metadata(
    payload: AutoExtractRequest,
    request: Request
):
    """
    Downloads article content from URL, uses Gemini to extract structured metadata,
    and returns it to pre-fill the index paper form.
    """
    if request.state.tenant not in ["professional", "academic"]:
        raise HTTPException(
            status_code=403, 
            detail="Metadata extraction requires an active domain context."
        )

    url = payload.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")
        
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch content from URL: {str(e)}")
        
    try:
        soup = BeautifulSoup(html, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        clean_text = soup.get_text(separator=' ')
        clean_text = " ".join(clean_text.split())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse article content: {str(e)}")
        
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured on the server.")
        
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        You are an expert academic research assistant.
        Analyze the following text scraped from a research article URL. Extract:
        1. Title of the article.
        2. Authors (formatted as a semicolon-separated list of author names, e.g. "Lankford, J. W.; Chen, M.").
        3. Publication Year (as an integer).
        4. Journal or Conference name (e.g., "arXiv Preprint", "ACM", "LinkedIn Pulse", or fallback to 'Web Publication' if not specified).
        5. Abstract/Summary of the article (comprehensive summary).
        6. Key empirical findings of the article (1-2 sentences).
        7. Methodology used in the article (1-2 sentences).
        8. A list of exactly 8 to 12 highly relevant taxonomy tags/keywords.

        URL: {url}
        Content Snippet:
        {clean_text[:10000]}

        Provide the output strictly in the following JSON format:
        {{
          "title": "...",
          "authors": "...",
          "publication_year": 2026,
          "journal_or_conf": "...",
          "abstract": "...",
          "key_findings": "...",
          "methodology": "...",
          "tags": ["tag1", "tag2", ...]
        }}
        Do not include any other markdown formatting, wrap code blocks, or write conversational text besides the JSON object.
        """
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        extracted = json.loads(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI extraction failed: {str(e)}")
        
    # Calculate Zotero Key: LASTNAME_YEAR_FIRST_TWO_WORDS
    try:
        authors_str = extracted.get("authors", "Unknown")
        authors = [a.strip() for a in authors_str.split(';') if a.strip()]
        last_name = "Unknown"
        if authors:
            first_author = authors[0]
            if ',' in first_author:
                last_name = first_author.split(',')[0].strip()
            else:
                last_name = first_author.split(' ')[-1].strip()
        last_name = "".join(c for c in last_name if c.isalnum())
        
        title_val = extracted.get("title", "")
        clean_title = "".join(c if (c.isalnum() or c.isspace()) else "" for c in title_val)
        words = [w.strip() for w in clean_title.split() if w.strip()]
        first_two_words = words[:2]
        first_two_words_str = "_".join(first_two_words)
        
        year_val = extracted.get("publication_year", 2026)
        zotero_key = f"{last_name.upper()}_{year_val}_{first_two_words_str.upper()}"
        extracted["zotero_key"] = zotero_key
    except Exception:
        extracted["zotero_key"] = "UNKNOWN_KEY"
        
    return extracted

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
        zotero_key=payload.zotero_key,
        url=payload.url,
        image_url=payload.image_url,
        tenant=request.state.tenant
    )
    db.add(paper)
    await db.flush() # Populate paper.id
    
    # 2. Add and link tags
    if payload.tags:
        for t_name in payload.tags:
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
                
            # Add link to join table directly to avoid async lazy loading problems
            from models import ResearchPaperTagLink
            link = ResearchPaperTagLink(paper_id=paper.id, tag_id=db_tag.id)
            db.add(link)
            
    await db.commit()
    await db.refresh(paper)
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
    statement = select(Article).where(
        Article.tenant == request.state.tenant,
        Article.is_published == True
    ).order_by(Article.published_at.desc())
    results = await db.execute(statement)
    return results.scalars().all()


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
    statement = select(GoogleNotebook).where(
        GoogleNotebook.tenant == request.state.tenant,
        GoogleNotebook.is_public == True
    ).order_by(GoogleNotebook.created_at.desc())
    results = await db.execute(statement)
    return results.scalars().all()


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
    statement = select(JupyterNotebook).where(
        JupyterNotebook.tenant == request.state.tenant
    ).order_by(JupyterNotebook.created_at.desc())
    results = await db.execute(statement)
    return results.scalars().all()


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
    return notebook