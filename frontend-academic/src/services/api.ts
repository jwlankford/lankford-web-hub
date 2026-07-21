import type { ResearchPaper, NewResearchPaperInput } from '../types';

const API_BASE = 'http://localhost:8000/api/v1/research';

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

export async function checkBackendHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/papers`, {
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
    const res = await fetch(`${API_BASE}/papers`, {
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
    const res = await fetch(`${API_BASE}/papers`, {
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
