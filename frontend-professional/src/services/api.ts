import type { SignupInput, ResearchPaper, NewResearchPaperInput, Article, NewArticleInput, GoogleNotebook, NewGoogleNotebookInput, JupyterNotebook, NewJupyterNotebookInput } from '../types';

const API_BOOK_BASE = 'http://localhost:8000/api/v1/book';
const API_RESEARCH_BASE = 'http://localhost:8000/api/v1/research';
const API_ARTICLE_BASE = 'http://localhost:8000/api/v1/articles';
const API_NOTEBOOKS_BASE = 'http://localhost:8000/api/v1/notebooks';


export const INITIAL_PAPERS: ResearchPaper[] = [
  {
    id: 1,
    title: 'Towards the Integration of Large Language Models into the Software Development Life Cycle: A Systematic Literature Review',
    authors: 'Madani, M.; Neumann, K.; Nahhas, A.; Chernigovskaya, M.; Walia, D.S. and Turowski, K.',
    publication_year: 2025,
    journal_or_conf: 'IEEE Xplore',
    abstract: 'Models (LLMs) are reshaping the Software Development Life Cycle (SDLC) by introducing new levels of automation and intelligent assistance across core phases, including requirements engineering, design, testing, and maintenance. Previous works have examined the adoption of LLM in these areas, but have overlooked its influence on traditional practices in SDLC. Therefore, this paper builds upon this foundation and investigates, from a phase-level perspective, how LLMs interact with the SDLC as a whole and whether their presence necessitates rethinking of conventional methodologies. To achieve this objective, this article reviews the state of the field using a systematic literature review method. Peer-reviewed studies published between 2019 and 2025, examining the integration, benefits, and limitations of LLM within SDLC are analyzed. The findings indicate that LLMs are most commonly applied in implementation and testing, where they improve productivity through code generation, test automation, and fault localisation. However, their adoption also introduces challenges related to model hallucination, contextual misalignment, computational overhead, and ethical risks such as bias and opacity. Therefore, we synthesise several LLM integration patterns and stress various risk mitigation strategies that can be adopted to enhance the integration of LLMs into software engineering practices. The study concludes by outlining practical implications for software teams and proposing future research directions to improve LLM’s integration with agile, DevOps and CI/CD workflows.',
    key_findings: 'Implementing dual-layered schema validation reduces unhandled execution branching by 98.4% without incurring prohibitive model invocation overhead.',
    methodology: 'Empirical Benchmark & Automated Safety Verification Framework',
    zotero_key: 'LANKFORD_2026_LLM_ADLC',
    created_at: new Date('2026-07-27').toISOString(),
    tenant: 'academic',
    tags: [
        { id: 101, name: 'Automation', slug: 'automation' },
        { id: 102, name: 'Large language models', slug: 'large-language-models' },
        { id: 103, name: 'Software', slug: 'software' },
        { id: 104, name: 'Deterministic guardrails', slug: 'deterministic-guardrails' },
        { id: 105, name: 'Software reliability', slug: 'software-reliability' },
        { id: 106, name: 'Requirements engineering', slug: 'requirements-engineering' },
        { id: 107, name: 'Stress testing', slug: 'stress-testing' },
        { id: 108, name: 'Systematic literature review', slug: 'systematic-literature-review' },
        { id: 109, name: 'Testing', slug: 'testing' },
        { id: 110, name: 'Software engineering', slug: 'software-engineering' },
    ]
  },
  {id: 2,
    title: 'The Generative SDLC: A Systematic Review of Integrating Modern LLMs in Software Development Life-Cycle',
    authors: 'Mohamanlal, A.; Alaswad, F.; Aljaddouh, B.',
    publication_year: 2026,
    journal_or_conf: 'IJSRT Journal',
    abstract: 'The rapid advancement of artificial intelligence (AI), machine learning (ML), deep learning (DL), and large language models (LLMs) has created transformative opportunities across every phase of the Software Development Life Cycle (SDLC). This paper presents a comprehensive review of the current state of AI integration in software engineering, examining each SDLC stage: requirements engineering, system design, implementation, testing, deployment, and maintenance. Particular emphasis is placed on modern LLMs such as GPT-4, Codex, and their derivatives, which have emerged as powerful tools capable of automating routine engineering tasks, augmenting developer productivity, and reshaping how software effort is estimated. Drawing upon a curated corpus of recent literature, the review synthesises theoretical frameworks and empirical findings, identifies persistent challenges including hallucination, context limitations, and bias, and outlines future research directions. The paper demonstrates that while LLMs offer significant potential as qualitative decision-support tools and AI pair programmers, their integration into safety-critical and large-scale production environments requires careful architectural alignment, cost-aware evaluation, and robust human oversight.',
    key_findings: 'The review concludes that LLMs significantly enhance productivity and automation across all SDLC phases, but their adoption requires careful architectural alignment, mitigation of hallucinations, cost‑aware evaluation, and strong human oversight to be viable in real-world, safety‑critical environments.',
    methodology: 'The study uses a systematic review methodology, collecting peer‑reviewed research from major digital libraries, applying inclusion/exclusion criteria, categorizing findings by SDLC phase, and synthesizing cross‑cutting themes such as productivity gains, hallucination risks, and governance concerns',
    zotero_key: 'ALDC_2026_Generative_SDLC',
    created_at: new Date('2026-07-27').toISOString(),
    tenant: 'academic',
    tags: [
        { id: 113, name: 'Artificial Intelligence', slug: 'artificial-intelligence' },
        { id: 114, name: 'Large Language Models', slug: 'large-language-models' },
        { id: 115, name: 'Software Development Life Cycle', slug: 'software-development-life-cycle' },
        { id: 116, name: 'Machine Learning', slug: 'machine-learning' },
        { id: 117, name: 'Deep Learning', slug: 'deep-learning' },
        { id: 118, name: 'GPT', slug: 'gpt' },
        { id: 119, name: 'GitHub Copilot', slug: 'github-copilot' },
        { id: 120, name: 'Software Testing', slug: 'software-testing' },
        { id: 121, name: 'Requirements Engineering', slug: 'requirements-engineering' }
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


