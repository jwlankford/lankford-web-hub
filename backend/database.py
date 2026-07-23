from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from config import settings

# 1. Create the asynchronous database engine
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=False, # Set to False for clean console output
    future=True
)

# 2. Create a session factory to generate isolated request sessions
async_session_maker = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 3. Dynamic initialization & automatic seed helper
async def init_db() -> None:
    import models  
    
    async with engine.begin() as conn:
        # Automatically generate missing tables safely
        await conn.run_sync(SQLModel.metadata.create_all)

    # Seed initial academic research papers if table is empty
    async with async_session_maker() as session:
        statement = select(models.ResearchPaper)
        result = await session.execute(statement)
        existing = result.scalars().all()
        
        if not existing:
            initial_papers = [
                models.ResearchPaper(
                    title="Deterministic Guardrails for Large Language Model Governance in Automated Workflows",
                    authors="Lankford, J. W.; Smith, A. R.",
                    publication_year=2026,
                    journal_or_conf="IEEE Transactions on Software Engineering",
                    abstract="This paper establishes formal verification patterns and runtime constraint boundaries for LLM agents operating within critical corporate software infrastructure.",
                    key_findings="Implementing dual-layered schema validation reduces unhandled execution branching by 98.4% without incurring prohibitive model invocation overhead.",
                    methodology="Empirical Benchmark & Automated Safety Verification Framework",
                    zotero_key="LANKFORD_2026_GUARDRAILS",
                    tenant="academic"
                ),
                models.ResearchPaper(
                    title="Multi-Tenant Microservice State Isolation in High-Concurrency Environments",
                    authors="Lankford, J. W.; Chen, M.",
                    publication_year=2025,
                    journal_or_conf="ACM Conference on Computer and Communications Security",
                    abstract="An architectural investigation into row-level tenant enforcement versus isolated connection pooling across cloud-native relational databases.",
                    key_findings="Middleware-driven header assertion combined with SQLModel row security ensures zero cross-tenant data leaks at 50k RPS.",
                    methodology="Quantitative Load Testing & Threat Vector Simulation",
                    zotero_key="LANKFORD_2025_STATE_ISOLATION",
                    tenant="academic"
                ),
                models.ResearchPaper(
                    title="Metaprogramming Abstractions for Adaptive Software Maintenance in Python & Rust",
                    authors="Lankford, J. W.",
                    publication_year=2025,
                    journal_or_conf="Journal of Systems and Software",
                    abstract="We explore modern compile-time and runtime introspection techniques to automate refactoring of enterprise legacy codebases.",
                    key_findings="Introspection-guided AST rewrites lower technical debt resolution cycles by 42% in production Python environments.",
                    methodology="Static Analysis & Dynamic AST Metaprogramming",
                    zotero_key="LANKFORD_2025_METAPROGRAMMING",
                    tenant="academic"
                ),
                models.ResearchPaper(
                    title="Building the Stack Around the Copilot: The Agentic Development Life Cycle",
                    authors="Lankford, J. W.",
                    publication_year=2026,
                    journal_or_conf="LinkedIn Pulse / Industry Analysis",
                    abstract="AI was a debate until recently. Software engineering teams spent 2 years arguing whether inline coding assistants made engineers 20% faster or 40% faster. This article examines the architectural evolution from inline autocomplete to agentic development workflows.",
                    key_findings="Transitioning from inline completion to an agentic SDLC requires restructuring software engineering stacks around sandboxed execution environments, deterministic schema verification, and continuous context delivery.",
                    methodology="Industry Synthesis & Agentic System Architecture Review",
                    zotero_key="LANKFORD_2026_AGENTIC_SDLC",
                    url="https://www.linkedin.com/pulse/building-stack-around-copilot-agentic-development-lankford-mba-nmd3e/",
                    tenant="academic"
                )
            ]
            for paper in initial_papers:
                session.add(paper)
            await session.commit()
            print("[SYSTEM] Initial database seed applied successfully.")

# 4. Dependency injection helper for FastAPI routes
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session