import type { SignupInput, ResearchPaper, NewResearchPaperInput, Article, NewArticleInput, GoogleNotebook, NewGoogleNotebookInput, JupyterNotebook, NewJupyterNotebookInput } from '../types';

const API_BOOK_BASE = 'http://localhost:8000/api/v1/book';
const API_RESEARCH_BASE = 'http://localhost:8000/api/v1/research';
const API_ARTICLE_BASE = 'http://localhost:8000/api/v1/articles';
const API_NOTEBOOKS_BASE = 'http://localhost:8000/api/v1/notebooks';


export const INITIAL_PAPERS: ResearchPaper[] = [
  {
    id: 1,
    title: 'Deterministic Guardrails for Large Language Model Governance in Automated Workflows',
    authors: 'Lankford, J. W.; Smith, A. R.',
    publication_year: 2026,
    journal_or_conf: 'IEEE Transactions on Software Engineering',
    abstract: 'This paper establishes formal verification patterns and runtime constraint boundaries for LLM agents operating within critical corporate software infrastructure. We analyze latency metrics, safety enforcement, and deterministic state transitions under dynamic user prompts.',
    key_findings: 'Implementing dual-layered schema validation reduces unhandled execution branching by 98.4% without incurring prohibitive model invocation overhead.',
    methodology: 'Empirical Benchmark & Automated Safety Verification Framework',
    zotero_key: 'LANKFORD_2026_GUARDRAILS',
    image_url: '/paper_guardrails.jpg',
    created_at: new Date('2026-02-15').toISOString(),
    tenant: 'academic',
    tags: [
      { id: 101, name: 'Deterministic Guardrails', slug: 'deterministic-guardrails' },
      { id: 102, name: 'LLM Governance', slug: 'llm-governance' },
      { id: 103, name: 'Agent Safety', slug: 'agent-safety' }
    ]
  },
  {
    id: 2,
    title: 'Multi-Tenant Microservice State Isolation in High-Concurrency Environments',
    authors: 'Lankford, J. W.; Chen, M.',
    publication_year: 2025,
    journal_or_conf: 'ACM Conference on Computer and Communications Security',
    abstract: 'An architectural investigation into row-level tenant enforcement versus isolated connection pooling across cloud-native relational databases. We present empirical throughput models for tenant middleware verification.',
    key_findings: 'Middleware-driven header assertion combined with SQLModel row security ensures zero cross-tenant data leaks at 50k RPS.',
    methodology: 'Quantitative Load Testing & Threat Vector Simulation',
    zotero_key: 'LANKFORD_2025_STATE_ISOLATION',
    image_url: '/paper_isolation.jpg',
    created_at: new Date('2025-11-04').toISOString(),
    tenant: 'academic',
    tags: [
      { id: 104, name: 'Multi-Tenancy', slug: 'multi-tenancy' },
      { id: 105, name: 'Cloud Architecture', slug: 'cloud-architecture' },
      { id: 106, name: 'Data Isolation', slug: 'data-isolation' }
    ]
  },
  {
    id: 3,
    title: 'Metaprogramming Abstractions for Adaptive Software Maintenance in Python & Rust',
    authors: 'Lankford, J. W.',
    publication_year: 2025,
    journal_or_conf: 'Journal of Systems and Software',
    abstract: 'We explore modern compile-time and runtime introspection techniques to automate refactoring of enterprise legacy codebases. The paper presents a unified macro taxonomy for structural invariant enforcement.',
    key_findings: 'Introspection-guided AST rewrites lower technical debt resolution cycles by 42% in production Python environments.',
    methodology: 'Static Analysis & Dynamic AST Metaprogramming',
    zotero_key: 'LANKFORD_2025_METAPROGRAMMING',
    image_url: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=1200&auto=format&fit=crop',
    created_at: new Date('2025-06-20').toISOString(),
    tenant: 'academic',
    tags: [
      { id: 107, name: 'Metaprogramming', slug: 'metaprogramming' },
      { id: 108, name: 'Static Analysis', slug: 'static-analysis' },
      { id: 102, name: 'LLM Governance', slug: 'llm-governance' }
    ]
  },
  {
    id: 4,
    title: 'Building the Stack Around the Copilot: The Agentic Development Life Cycle',
    authors: 'Lankford, J. W.',
    publication_year: 2026,
    journal_or_conf: 'LinkedIn Pulse / Industry Analysis',
    abstract: 'AI was a debate until recently. Software engineering teams spent 2 years arguing whether inline coding assistants made engineers 20% faster or 40% faster. This article examines the architectural evolution from inline autocomplete to agentic development workflows, analyzing ecosystem tooling, isolated execution sandboxes, and deterministic verification guardrails.',
    key_findings: 'Transitioning from inline completion to an agentic SDLC requires restructuring software engineering stacks around sandboxed execution environments, deterministic schema verification, and continuous context delivery.',
    methodology: 'Industry Synthesis & Agentic System Architecture Review',
    zotero_key: 'LANKFORD_2026_AGENTIC_SDLC',
    url: 'https://www.linkedin.com/pulse/building-stack-around-copilot-agentic-development-lankford-mba-nmd3e/',
    image_url: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1200&auto=format&fit=crop',
    created_at: new Date('2026-07-20').toISOString(),
    tenant: 'academic',
    tags: [
      { id: 109, name: 'Agentic Development', slug: 'agentic-development' },
      { id: 102, name: 'LLM Governance', slug: 'llm-governance' },
      { id: 110, name: 'Software Lifecycle', slug: 'software-lifecycle' }
    ]
  }
];

// ==========================================
// PROFESSIONAL DOMAIN API CALLS
// ==========================================

export async function checkProfessionalBackendHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BOOK_BASE}/signup`, {
      method: 'OPTIONS'
    });
    return res.ok || res.status === 405;
  } catch {
    return false;
  }
}

export async function submitBookMailingList(input: SignupInput): Promise<{ success: boolean; message: string; isLiveBackend: boolean }> {
  try {
    const res = await fetch(`${API_BOOK_BASE}/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'professional.localhost',
        'X-Tenant': 'professional'
      },
      body: JSON.stringify({
        email: input.email.trim(),
        first_name: input.first_name?.trim() || null,
        tenant: 'professional'
      })
    });

    if (res.ok) {
      return {
        success: true,
        message: `Welcome aboard! ${input.email} has been subscribed to launch updates.`,
        isLiveBackend: true
      };
    } else {
      const data = await res.json().catch(() => ({}));
      return {
        success: false,
        message: data.detail || 'This email address may already be registered.',
        isLiveBackend: true
      };
    }
  } catch (err) {
    console.warn('[Professional Service] Backend offline, simulating subscriber confirmation.', err);
    return {
      success: true,
      message: `[Simulated] Thank you for joining! ${input.email} registered successfully.`,
      isLiveBackend: false
    };
  }
}

// ==========================================
// ACADEMIC DOMAIN API CALLS (Shared Backend)
// ==========================================

export async function checkAcademicBackendHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_RESEARCH_BASE}/papers`, {
      method: 'GET',
      headers: {
        'Host': 'academic.localhost',
        'X-Tenant': 'academic'
      }
    });
    return res.ok;
  } catch {
    return false;
  }
}

export async function fetchResearchPapers(): Promise<{ papers: ResearchPaper[]; isLiveBackend: boolean }> {
  try {
    const res = await fetch(`${API_RESEARCH_BASE}/papers`, {
      headers: {
        'Host': 'academic.localhost',
        'X-Tenant': 'academic'
      }
    });
    if (res.ok) {
      const data = await res.json();
      return { papers: data, isLiveBackend: true };
    }
    return { papers: INITIAL_PAPERS, isLiveBackend: false };
  } catch {
    return { papers: INITIAL_PAPERS, isLiveBackend: false };
  }
}

export async function createResearchPaper(input: NewResearchPaperInput): Promise<{ paper: ResearchPaper; isLiveBackend: boolean }> {
  try {
    const res = await fetch(`${API_RESEARCH_BASE}/papers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'academic.localhost',
        'X-Tenant': 'academic'
      },
      body: JSON.stringify(input)
    });
    if (res.ok) {
      const data = await res.json();
      return { paper: data, isLiveBackend: true };
    }
    const mockPaper: ResearchPaper = {
      ...input,
      id: Date.now(),
      created_at: new Date().toISOString(),
      tenant: 'academic'
    };
    return { paper: mockPaper, isLiveBackend: false };
  } catch {
    const mockPaper: ResearchPaper = {
      ...input,
      id: Date.now(),
      created_at: new Date().toISOString(),
      tenant: 'academic'
    };
    return { paper: mockPaper, isLiveBackend: false };
  }
}

// ==========================================
// ARTICLES API CALLS (Dual-Domain Context)
// ==========================================

export const INITIAL_ARTICLES: Article[] = [
  {
    id: 1,
    title: 'Building the Stack Around the Copilot: The Agentic Development Life Cycle',
    summary: 'AI was a debate until recently. Software engineering teams spent 2 years arguing whether inline coding assistants made engineers 20% faster or 40% faster. This article examines the architectural evolution from inline autocomplete to agentic development workflows.',
    content: '### The Shift from Auto-Complete to Autonomous Agents\n\nAI was a debate until recently. Software engineering teams spent 2 years arguing whether inline coding assistants made engineers 20% faster or 40% faster. But those days of IDE autocomplete are long gone. Between college baseball and struggling to ship software in an AI-first world, we’ve passed a Rubicon. We’ve moved past human-centric, AI-assisted tooling into what is being called the **Agentic Development Life Cycle (ADLC)**.\n\nImagine a future where autonomous agents don’t sit inside your IDE waiting for you to type. Agents take context from the system, clone repos, pull real-time enterprise context from a protocol like MCP into ephemeral sandboxes, and autonomously create multi-file changesets & open sophisticated PRs themselves. This idea that there’s always a human engineer between every line of code and the pipeline? Dead.\n\n#### Machine Velocity and the Bottleneck Shift\n\nADLC agents operate at unprecedented machine velocity. But that also creates a massive architectural dilemma. If a team of specialized micro-agents working concurrently can grab tickets from a backlog and simultaneously execute dozens of multi-file changesets—the bottleneck suddenly moves downstream FAST.\n\nEnter **validation bottleneck syndrome**. Engineering teams are suddenly slammed with overwhelming queues of AI-generated PRs. Humans can only process so much information at machine speed. Soon enough you’ll notice your reviewers start getting lazy. A high-level architectural review gives way to a blind review of syntax in an effort to keep the funnel moving. Left unchecked, unlimited agent throughput doesn’t prevent technical debt—it amplifies latent architectural debt, code duplication, and yes, even security vulnerabilities at scale. Autonomy forces us to take our eyes off the code. Recent industry data from Forrester shows autonomous workflows are driving an unprecedented surge in repository volume. What we need is a way to build continuous trust at machine velocity.\n\nIt is paramount that enterprises begin migrating from reactive PR scanning to **Continuous Agentic / Continuous Deployment (CA/CD)** practices. There is a critical control plane that needs to be built beneath the probabilistic whims of LLM decision-making.\n\n---\n\n### Best Practices for Building Trust at Machine Velocity\n\nStandardization becomes our friend again. Engineering policy around agents requires a new obsession with deterministic systems. Building the guardrails for agent autonomy starts with three best practices:\n\n#### 1. Context Engineering & Routing\nAgents cannot be fed the entire repo. End of story. Every code engineer knows repository sprawl creates siloed context and hidden logical errors. Engineering cognition and routing determine how well your agents and your teams perform. According to Anthropic\'s latest engineering benchmarks, using graph-backed repository indexing & automated context routing to knowledgeably serve system state, schemata, and temporal traces to your agents at runtime is the only way to prevent severe context degradation and silent execution failures.\n\n#### 2. Risk-Based Autonomy Tiers\nEnterprise teams need to begin mapping an agent’s autonomy to the risk profile of their actions. All autonomous work should be split into 3 tiers:\n- **Tier 1**: Changes are verified internally by the agent (e.g. linting, documentation, or granular refactors).\n- **Tier 2**: Actions should always auto-generate alerts while executing autonomously.\n- **Tier 3**: Anything that can mutate core system schemas or merge into stable branches must be blocked behind explicit human-in-the-loop approval gates.\n\nSound familiar? It should. This is practically the same runtime model we’ve enforced with auto-scaling/cloud tiering for years. If the failure domain is isolated, let it run at machine speed.\n\n#### 3. Define the Invariants\nThere is no silver bullet for non-deterministic AI. However, nothing stops you from writing a bulletproof validation suite. Stop reviewing your AI’s code. Let your engineers write the invariants. Define explicit interfaces and auto-generate behavioral test baselines to prove any agent implementation mathematically and logically "passes the test" before a human reviewer even sees the PR.\n\n---\n\n### The Future of Engineering Leadership\n\nAs we shift into ADLC, engineering organizations no longer need individuals who can churn out 10x more raw syntax than a human can. Instead, tomorrow’s architects are investing every ounce of political capital defining ambiguous problems. There is a massive opportunity for senior engineers who can optimize their stack around autonomous agents by thinking through context boundaries and assembling veteran software engineers into multi-agent guilds.',
    linkedin_url: 'https://www.linkedin.com/pulse/building-stack-around-copilot-agentic-development-lankford-mba-nmd3e/',
    image_url: 'https://media.licdn.com/dms/image/v2/D4E12AQFSem-lCgGdhg/article-cover_image-shrink_720_1280/B4EZ.dSz4hKYAQ-/0/1785050386855?e=2147483647&v=beta&t=4r2ATXRbVeVsXNS75B09Sdlim8fQxQMjBnjSiZQSpH4',
    published_at: new Date('2026-07-20').toISOString(),
    is_published: true,
    tenant: 'professional'
  }
];

export async function fetchArticles(): Promise<{ articles: Article[]; isLiveBackend: boolean }> {
  try {
    const res = await fetch(API_ARTICLE_BASE, {
      headers: {
        'Host': 'professional.localhost',
        'X-Tenant': 'professional'
      }
    });
    if (res.ok) {
      const data = await res.json();
      return { articles: data, isLiveBackend: true };
    }
    return { articles: INITIAL_ARTICLES, isLiveBackend: false };
  } catch {
    return { articles: INITIAL_ARTICLES, isLiveBackend: false };
  }
}

export async function createArticle(input: NewArticleInput): Promise<{ article: Article; isLiveBackend: boolean }> {
  try {
    const res = await fetch(API_ARTICLE_BASE, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'professional.localhost',
        'X-Tenant': 'professional'
      },
      body: JSON.stringify(input)
    });
    if (res.ok) {
      const data = await res.json();
      return { article: data, isLiveBackend: true };
    }
    const mockArticle: Article = {
      ...input,
      id: Date.now(),
      published_at: new Date().toISOString(),
      tenant: 'professional'
    };
    return { article: mockArticle, isLiveBackend: false };
  } catch {
    const mockArticle: Article = {
      ...input,
      id: Date.now(),
      published_at: new Date().toISOString(),
      tenant: 'professional'
    };
    return { article: mockArticle, isLiveBackend: false };
  }
}


export const INITIAL_GOOGLE_NOTEBOOKS: GoogleNotebook[] = [
  {
    id: 1,
    title: "Agentic Software Engineering & ADLC Handbook",
    description: "Study companion synthesizing LLM agent loops, non-human IAM access management, self-correcting code analysis, and LLM-as-a-Judge frameworks.",
    notebook_url: "https://notebooklm.google.com/notebook/professional-adlc-handbook",
    sources_count: 8,
    audio_url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    tenant: "professional"
  },
  {
    id: 2,
    title: "LLMOps & Generative AI Testing",
    description: "A comprehensive notebook covering non-deterministic testing methodologies, statistical evaluation rubrics, and cosine similarity checking.",
    notebook_url: "https://notebooklm.google.com/notebook/professional-llmops-quality-assurance",
    sources_count: 5,
    audio_url: undefined,
    tenant: "professional"
  }
];

export const INITIAL_JUPYTER_NOTEBOOKS: JupyterNotebook[] = [
  {
    id: 1,
    title: "Orchestration Loop Simulation",
    description: "Walkthrough of ReAct orchestration flows and Manager/Worker hierarchies. Implements circuit breakers to detect agent loop spirals.",
    notebook_url: "https://github.com/jwlankford/notebook-vault/blob/main/react_orchestration_loop.ipynb",
    tags: "Orchestration,ReAct,Agentic",
    tenant: "professional"
  },
  {
    id: 2,
    title: "LLM-as-a-Judge Evaluation Playground",
    description: "An interactive workspace testing judge prompts, consensus algorithms, and agreement scores against baseline golden datasets.",
    notebook_url: "https://github.com/jwlankford/notebook-vault/blob/main/llm_as_a_judge_evaluator.ipynb",
    tags: "LLM-as-a-Judge,Evaluation,Factual-Drift",
    tenant: "professional"
  },
  {
    id: 3,
    title: "Colab Notebook: Multi-Agent Evaluation & Verification",
    description: "Interactive Google Colab workspace demonstrating live feed integration, multi-agent evaluation workflows, and runtime verification constraints.",
    notebook_url: "https://colab.research.google.com/drive/1XEQT-oTF_KkmY5FHkMIcWEuAlJziBaoe?usp=sharing",
    tags: "Colab,Agentic,Integrations",
    tenant: "professional"
  }
];

export async function fetchGoogleNotebooks(): Promise<{ notebooks: GoogleNotebook[]; isLiveBackend: boolean }> {
  try {
    const res = await fetch(`${API_NOTEBOOKS_BASE}/google`, {
      headers: {
        'Host': 'professional.localhost',
        'X-Tenant': 'professional'
      }
    });
    if (res.ok) {
      const data = await res.json();
      return { notebooks: data, isLiveBackend: true };
    }
    return { notebooks: INITIAL_GOOGLE_NOTEBOOKS, isLiveBackend: false };
  } catch {
    return { notebooks: INITIAL_GOOGLE_NOTEBOOKS, isLiveBackend: false };
  }
}

export async function createGoogleNotebook(input: NewGoogleNotebookInput): Promise<{ notebook: GoogleNotebook; isLiveBackend: boolean }> {
  try {
    const res = await fetch(`${API_NOTEBOOKS_BASE}/google`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'professional.localhost',
        'X-Tenant': 'professional'
      },
      body: JSON.stringify(input)
    });
    if (res.ok) {
      const data = await res.json();
      return { notebook: data, isLiveBackend: true };
    }
    const mockBook: GoogleNotebook = {
      ...input,
      id: Date.now(),
      created_at: new Date().toISOString(),
      tenant: 'professional'
    };
    return { notebook: mockBook, isLiveBackend: false };
  } catch {
    const mockBook: GoogleNotebook = {
      ...input,
      id: Date.now(),
      created_at: new Date().toISOString(),
      tenant: 'professional'
    };
    return { notebook: mockBook, isLiveBackend: false };
  }
}

export async function fetchJupyterNotebooks(): Promise<{ notebooks: JupyterNotebook[]; isLiveBackend: boolean }> {
  try {
    const res = await fetch(`${API_NOTEBOOKS_BASE}/jupyter`, {
      headers: {
        'Host': 'professional.localhost',
        'X-Tenant': 'professional'
      }
    });
    if (res.ok) {
      const data = await res.json();
      return { notebooks: data, isLiveBackend: true };
    }
    return { notebooks: INITIAL_JUPYTER_NOTEBOOKS, isLiveBackend: false };
  } catch {
    return { notebooks: INITIAL_JUPYTER_NOTEBOOKS, isLiveBackend: false };
  }
}

export async function createJupyterNotebook(input: NewJupyterNotebookInput): Promise<{ notebook: JupyterNotebook; isLiveBackend: boolean }> {
  try {
    const res = await fetch(`${API_NOTEBOOKS_BASE}/jupyter`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'professional.localhost',
        'X-Tenant': 'professional'
      },
      body: JSON.stringify(input)
    });
    if (res.ok) {
      const data = await res.json();
      return { notebook: data, isLiveBackend: true };
    }
    const mockBook: JupyterNotebook = {
      ...input,
      id: Date.now(),
      created_at: new Date().toISOString(),
      tenant: 'professional'
    };
    return { notebook: mockBook, isLiveBackend: false };
  } catch {
    const mockBook: JupyterNotebook = {
      ...input,
      id: Date.now(),
      created_at: new Date().toISOString(),
      tenant: 'professional'
    };
    return { notebook: mockBook, isLiveBackend: false };
  }
}


