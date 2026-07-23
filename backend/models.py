from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# ==========================================
# WEEK 1: FOUNDATIONAL MULTI-TENANT ROUTING
# ==========================================

class TenantDomain(str, Enum):
    PROFESSIONAL = "jeremylankford.com"
    ACADEMIC = "jwlankford.com"
    LOCAL_PROFESSIONAL = "professional.localhost"
    LOCAL_ACADEMIC = "academic.localhost"

class TenantBase(SQLModel):
    """
    All multi-tenant database tables inherit from this base class 
    to guarantee strict row-level isolation.
    """
    tenant: str = Field(index=True)


# ==========================================
# WEEK 2: THE DATA SCHEMAS
# ==========================================

class BookMailingList(TenantBase, table=True):
    """
    Captures audience leads for 'Today's Software Developer'.
    Sits under the 'professional' tenant context.
    """
    __tablename__ = "book_mailing_list"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    first_name: Optional[str] = None
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)


# --- STEP 1: DEFINE THE LINK TABLE FIRST SO IT IS FULLY EVALUATED ---
class ResearchPaperTagLink(SQLModel, table=True):
    """Many-to-Many link table between Papers and Tags."""
    __tablename__ = "research_paper_tag_link"

    paper_id: Optional[int] = Field(
        default=None, foreign_key="research_papers.id", primary_key=True
    )
    tag_id: Optional[int] = Field(
        default=None, foreign_key="research_tags.id", primary_key=True
    )


# --- STEP 2: DEFINE THE MAIN SCHEMAS USING THE CLASS REFERENCES ---
class ResearchPaper(TenantBase, table=True):
    """
    Indexes academic lit reviews, paper structures, and statistical tracking.
    Sits under the 'academic' tenant context.
    """
    __tablename__ = "research_papers"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    authors: str = Field(nullable=False)  # Semicolon separated list of authors
    publication_year: int = Field(index=True)
    journal_or_conf: Optional[str] = None
    
    # Research Metaprogramming
    abstract: Optional[str] = None
    key_findings: Optional[str] = None
    methodology: Optional[str] = None
    
    # Internal Organization
    zotero_key: Optional[str] = Field(default=None, index=True)
    url: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Pass the actual class object directly now:
    tags: List["ResearchTag"] = Relationship(
        back_populates="papers", 
        link_model=ResearchPaperTagLink
    )


class ResearchTag(TenantBase, table=True):
    """
    Dynamic taxonomy for indexing studies (e.g., 'Deterministic Guardrails', 'LLM Governance').
    """
    __tablename__ = "research_tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    slug: str = Field(unique=True, nullable=False)
    
    # Pass the actual class object directly now:
    papers: List[ResearchPaper] = Relationship(
        back_populates="tags", 
        link_model=ResearchPaperTagLink
    )