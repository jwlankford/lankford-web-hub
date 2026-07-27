import os
import ssl
from dotenv import load_dotenv
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from config import settings

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Apply ssl args conditionally if using Neon or specific remote databases
connect_args = {}
if settings.ASYNC_DATABASE_URL and "neon.tech" in settings.ASYNC_DATABASE_URL:
    connect_args["ssl"] = "require"

# 1. Create the asynchronous database engine
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=False, # Set to False for clean console output
    future=True,
    connect_args=connect_args
)

# 2. Create a session factory to generate isolated request sessions
async_session_maker = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Dependency for FastAPI endpoints
async def get_db():
    async with async_session_maker() as session:
        yield session

# 3. Dynamic initialization & automatic seed helper
async def init_db() -> None:
    import models  
    
    os_url = os.environ.get("DATABASE_URL")
    safe_os_host = os_url.split("@")[1].split("/")[0] if os_url and "@" in os_url else os_url
    safe_settings_host = settings.DATABASE_URL.split("@")[1].split("/")[0] if settings.DATABASE_URL and "@" in settings.DATABASE_URL else settings.DATABASE_URL
    print(f"[SYSTEM] Debug OS Env DATABASE_URL Host: {safe_os_host}")
    print(f"[SYSTEM] Debug Settings DATABASE_URL Host: {safe_settings_host}")
    
    db_url = settings.ASYNC_DATABASE_URL
    if "@" in db_url:
        host = db_url.split("@")[1].split("/")[0]
        print(f"[SYSTEM] Database connection target host: {host}")
    else:
        print(f"[SYSTEM] Database connection target: {db_url}")

    async with engine.begin() as conn:
        # Automatically generate missing tables safely
        await conn.run_sync(SQLModel.metadata.create_all)
        
        # Migrate existing academic tenant rows to professional tenant context
        from sqlalchemy import text
        for table in ["book_mailing_list", "research_papers", "research_tags", "articles", "google_notebooks", "jupyter_notebooks", "contact_messages"]:
            await conn.execute(text(f"UPDATE {table} SET tenant = 'professional' WHERE tenant = 'academic'"))
            try:
                await conn.execute(text(f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), coalesce(max(id), 1)) FROM {table}"))
            except Exception:
                pass

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
                    tenant="professional"
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
                    tenant="professional"
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
                    tenant="professional"
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
                    tenant="professional"
                )
            ]
            for paper in initial_papers:
                session.add(paper)
            await session.commit()
            print("[SYSTEM] Initial database seed applied successfully.")

        # Seed initial articles if table is empty
        statement_articles = select(models.Article)
        result_articles = await session.execute(statement_articles)
        existing_articles = result_articles.scalars().all()
        
        if not existing_articles:
            initial_articles = [
                models.Article(
                    title="Building the Stack Around the Copilot: The Agentic Development Life Cycle",
                    summary="AI was a debate until recently. Software engineering teams spent 2 years arguing whether inline coding assistants made engineers 20% faster or 40% faster. This article examines the architectural evolution from inline autocomplete to agentic development workflows.",
                    content="""### The Shift from Auto-Complete to Autonomous Agents

AI was a debate until recently. Software engineering teams spent 2 years arguing whether inline coding assistants made engineers 20% faster or 40% faster. But those days of IDE autocomplete are long gone. Between college baseball and struggling to ship software in an AI-first world, we’ve passed a Rubicon. We’ve moved past human-centric, AI-assisted tooling into what is being called the **Agentic Development Life Cycle (ADLC)**.

Imagine a future where autonomous agents don’t sit inside your IDE waiting for you to type. Agents take context from the system, clone repos, pull real-time enterprise context from a protocol like MCP into ephemeral sandboxes, and autonomously create multi-file changesets & open sophisticated PRs themselves. This idea that there’s always a human engineer between every line of code and the pipeline? Dead.

#### Machine Velocity and the Bottleneck Shift

ADLC agents operate at unprecedented machine velocity. But that also creates a massive architectural dilemma. If a team of specialized micro-agents working concurrently can grab tickets from a backlog and simultaneously execute dozens of multi-file changesets—the bottleneck suddenly moves downstream FAST.

Enter **validation bottleneck syndrome**. Engineering teams are suddenly slammed with overwhelming queues of AI-generated PRs. Humans can only process so much information at machine speed. Soon enough you’ll notice your reviewers start getting lazy. A high-level architectural review gives way to a blind review of syntax in an effort to keep the funnel moving. Left unchecked, unlimited agent throughput doesn’t prevent technical debt—it amplifies latent architectural debt, code duplication, and yes, even security vulnerabilities at scale. Autonomy forces us to take our eyes off the code. Recent industry data from Forrester shows autonomous workflows are driving an unprecedented surge in repository volume. What we need is a way to build continuous trust at machine velocity.

It is paramount that enterprises begin migrating from reactive PR scanning to **Continuous Agentic / Continuous Deployment (CA/CD)** practices. There is a critical control plane that needs to be built beneath the probabilistic whims of LLM decision-making.

---

### Best Practices for Building Trust at Machine Velocity

Standardization becomes our friend again. Engineering policy around agents requires a new obsession with deterministic systems. Building the guardrails for agent autonomy starts with three best practices:

#### 1. Context Engineering & Routing
Agents cannot be fed the entire repo. End of story. Every code engineer knows repository sprawl creates siloed context and hidden logical errors. Engineering cognition and routing determine how well your agents and your teams perform. According to Anthropic's latest engineering benchmarks, using graph-backed repository indexing & automated context routing to knowledgeably serve system state, schemata, and temporal traces to your agents at runtime is the only way to prevent severe context degradation and silent execution failures.

#### 2. Risk-Based Autonomy Tiers
Enterprise teams need to begin mapping an agent’s autonomy to the risk profile of their actions. All autonomous work should be split into 3 tiers:
- **Tier 1**: Changes are verified internally by the agent (e.g. linting, documentation, or granular refactors).
- **Tier 2**: Actions should always auto-generate alerts while executing autonomously.
- **Tier 3**: Anything that can mutate core system schemas or merge into stable branches must be blocked behind explicit human-in-the-loop approval gates.

Sound familiar? It should. This is practically the same runtime model we’ve enforced with auto-scaling/cloud tiering for years. If the failure domain is isolated, let it run at machine speed.

#### 3. Define the Invariants
There is no silver bullet for non-deterministic AI. However, nothing stops you from writing a bulletproof validation suite. Stop reviewing your AI’s code. Let your engineers write the invariants. Define explicit interfaces and auto-generate behavioral test baselines to prove any agent implementation mathematically and logically "passes the test" before a human reviewer even sees the PR.

---

### The Future of Engineering Leadership

As we shift into ADLC, engineering organizations no longer need individuals who can churn out 10x more raw syntax than a human can. Instead, tomorrow’s architects are investing every ounce of political capital defining ambiguous problems. There is a massive opportunity for senior engineers who can optimize their stack around autonomous agents by thinking through context boundaries and assembling veteran software engineers into multi-agent guilds.""",
                    linkedin_url="https://www.linkedin.com/pulse/building-stack-around-copilot-agentic-development-lankford-mba-nmd3e/",
                    image_url="https://media.licdn.com/dms/image/v2/D4E12AQFSem-lCgGdhg/article-cover_image-shrink_720_1280/B4EZ.dSz4hKYAQ-/0/1785050386855?e=2147483647&v=beta&t=4r2ATXRbVeVsXNS75B09Sdlim8fQxQMjBnjSiZQSpH4",
                    tenant="professional"
                ),
                models.Article(
                    title="Formal Verification Patterns for LLMs in Multi-Tenant Architectures",
                    summary="Enforcing strict tenant separation requires more than standard ORM policies when LLMs generate database filters. We present formal constraint patterns to guarantee database tenant isolation.",
                    content="""### Enforcing Row-Level Tenancy in AI-Generated Queries

Multi-tenant systems built around FastAPI, SQLModel, and PostgreSQL typically rely on middleware-level headers to inject tenant keys into active database sessions. However, when introducing LLM agents that execute dynamic SQL or write queries on the fly, this boundary can easily break.

#### The Vulnerability
An LLM designed to help a client query their data might fail to restrict the filter scope, resulting in cross-tenant leakage.

#### The Safe Verification Pattern
To solve this, we implement a **dual-layered verification pattern**:
- **Application Middleware Validation**: Asserts that every outgoing query AST contains a tenant filter matching the current request session.
- **SQLModel Enforcement**: Dynamically patching SQLModel session executes to inject `where(Model.tenant == active_tenant)` boundaries.

By treating the database session as a bounded environment, we ensure zero cross-tenant leakage even with open-ended AI agents.""",
                    linkedin_url="https://www.linkedin.com/",
                    image_url="https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=1200&auto=format&fit=crop",
                    tenant="professional"
                )
            ]
            for article in initial_articles:
                session.add(article)
            await session.commit()
            print("[SYSTEM] Initial articles seed applied successfully.")

        # Seed initial Google Notebooks if table is empty
        statement_gbooks = select(models.GoogleNotebook)
        result_gbooks = await session.execute(statement_gbooks)
        existing_gbooks = result_gbooks.scalars().all()

        if not existing_gbooks:
            initial_gbooks = [
                models.GoogleNotebook(
                    title="Deterministic Guardrails & Safety in LLMs",
                    description="AI study guide and podcast summarizing research on runtime validation, output assertions, and state machine enforcement in critical agent workflows.",
                    notebook_url="https://notebooklm.google.com/notebook/academic-guardrails-study-guide",
                    sources_count=4,
                    audio_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
                    tenant="professional"
                ),
                models.GoogleNotebook(
                    title="State Isolation in Multi-Tenant Relational Architectures",
                    description="Interactive notes on PostgreSQL row-level security, connection pool scaling limits, and middleware context paradigm under high concurrency.",
                    notebook_url="https://notebooklm.google.com/notebook/academic-isolation-database-design",
                    sources_count=3,
                    audio_url=None,
                    tenant="professional"
                ),
                models.GoogleNotebook(
                    title="Agentic Software Engineering & ADLC Handbook",
                    description="Study companion synthesizing LLM agent loops, non-human IAM access management, self-correcting code analysis, and LLM-as-a-Judge frameworks.",
                    notebook_url="https://notebooklm.google.com/notebook/professional-adlc-handbook",
                    sources_count=8,
                    audio_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
                    tenant="professional"
                ),
                models.GoogleNotebook(
                    title="LLMOps & Generative AI Testing",
                    description="A comprehensive notebook covering non-deterministic testing methodologies, statistical evaluation rubrics, and cosine similarity checking.",
                    notebook_url="https://notebooklm.google.com/notebook/professional-llmops-quality-assurance",
                    sources_count=5,
                    audio_url=None,
                    tenant="professional"
                )
            ]
            for gbook in initial_gbooks:
                session.add(gbook)
            await session.commit()
            print("[SYSTEM] Initial Google Notebooks seed applied successfully.")

        # Seed initial Jupyter Notebooks if table is empty
        statement_jbooks = select(models.JupyterNotebook)
        result_jbooks = await session.execute(statement_jbooks)
        existing_jbooks = result_jbooks.scalars().all()

        if not existing_jbooks:
            initial_jbooks = [
                models.JupyterNotebook(
                    title="Colab Notebook: Multi-Agent Evaluation & Verification",
                    description="Interactive Google Colab workspace demonstrating live feed integration, multi-agent evaluation workflows, and runtime verification constraints.",
                    notebook_url="https://colab.research.google.com/drive/1XEQT-oTF_KkmY5FHkMIcWEuAlJziBaoe?usp=sharing",
                    tags="Colab,Agentic,Integrations",
                    tenant="professional"
                )
            ]
            for jbook in initial_jbooks:
                session.add(jbook)
            await session.commit()
            print("[SYSTEM] Initial Jupyter Notebooks seed applied successfully.")



# 4. Dependency injection helper for FastAPI routes
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session