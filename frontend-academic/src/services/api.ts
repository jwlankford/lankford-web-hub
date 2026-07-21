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
    created_at: new Date('2025-06-20').toISOString(),
    tenant: 'academic',
    tags: [
      { id: 107, name: 'Metaprogramming', slug: 'metaprogramming' },
      { id: 108, name: 'Static Analysis', slug: 'static-analysis' },
      { id: 102, name: 'LLM Governance', slug: 'llm-governance' }
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
      const data: ResearchPaper[] = await res.json();
      return { papers: data.length > 0 ? data : INITIAL_PAPERS, isLiveBackend: true };
    }
  } catch (err) {
    console.warn('[Academic Service] Backend unavailable, using local research index cache.', err);
  }
  return { papers: INITIAL_PAPERS, isLiveBackend: false };
}

export async function createResearchPaper(input: NewResearchPaperInput): Promise<{ paper: ResearchPaper; isLiveBackend: boolean }> {
  const payload: Partial<ResearchPaper> = {
    ...input,
    tenant: 'academic'
  };

  try {
    const res = await fetch(`${API_BASE}/papers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'academic.localhost',
        'X-Tenant': 'academic'
      },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      const data: ResearchPaper = await res.json();
      return { paper: data, isLiveBackend: true };
    }
  } catch (err) {
    console.warn('[Academic Service] API write failed, falling back to local session store.', err);
  }

  // Fallback local paper creation
  const fallbackPaper: ResearchPaper = {
    id: Date.now(),
    ...input,
    created_at: new Date().toISOString(),
    tenant: 'academic',
    tags: [
      { id: 999, name: 'New Research', slug: 'new-research' }
    ]
  };
  return { paper: fallbackPaper, isLiveBackend: false };
}
