export interface CourseSection {
  chapter: string;
  topics: string[];
}

export interface Course {
  id: number;
  slug: string;
  title: string;
  shortTitle: string;
  category: string;
  tagline: string;
  rating: number;
  reviewsCount: number;
  studentsCount: number;
  duration: string;
  lectures: number;
  level: string;
  price: string;
  originalPrice: string;
  badge?: string;
  image: string;
  skills: string[];
  description: string;
  longDescription?: string[];
  whatYouWillLearn: string[];
  requirements: string[];
  targetAudience: string[];
  syllabus: CourseSection[];
  udemyUrl: string;
  status: 'published' | 'in_development';
  launchTimeline?: string;
}

export const courses: Course[] = [
  {
    id: 1,
    slug: 'adlc-intro-course',
    title: 'AI Development Life Cycle (ADLC) - Intro Course',
    shortTitle: 'ADLC Intro Course',
    category: 'AI Software Engineering',
    tagline: 'Master the transition from traditional SDLC to autonomous agentic pipelines. Focus on loop engineering, machine-speed quality gates, evaluation, and least-privilege IAM.',
    rating: 0,
    reviewsCount: 0,
    studentsCount: 0,
    duration: 'Targeting 32 hours',
    lectures: 158,
    level: 'Introductory to Advanced',
    price: '$74.99',
    originalPrice: '$149.99',
    badge: 'Under Development',
    image: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=800&auto=format&fit=crop',
    skills: ['ADLC Paradigm', 'Loop Engineering', 'Machine-Speed Quality Gates', 'LLM-as-a-Judge', 'Non-Human IAM', 'Multi-Agent Orchestration'],
    status: 'in_development',
    launchTimeline: 'Targeting 2026',
    udemyUrl: 'https://www.udemy.com/user/jeremy-lankford-22/',
    description: 'Deconstruct traditional SDLC limits to launch self-correcting autonomous multi-agent pipelines with robust inter-agent state preservation, least-privilege non-human IAM access, and automated LLM judge rubrics.',
    longDescription: [
      'The software industry has moved past simple IDE autocompletion into the era of autonomous agentic software development. Engineering teams are no longer bottlenecked by raw code synthesis, but by validation, architectural consistency, and trust at machine speed.',
      'This foundational and comprehensive course deconstructs traditional Software Development Life Cycle (SDLC) boundaries and introduces the Agentic Development Life Cycle (ADLC). You will learn how to architect self-correcting autonomous multi-agent pipelines with robust inter-agent state preservation, least-privilege non-human IAM access, automated LLM-as-a-judge rubrics, and continuous quality gates.',
      'Through 24 comprehensive sections combining theoretical architectures, Python labs, and real-world implementation exercises, you will transform into an engineer capable of leading agentic initiatives in enterprise environments.'
    ],
    whatYouWillLearn: [
      'Understand the structural limitations of traditional SDLC and map legacy workflows to ADLC architectures',
      'Design and deploy self-correcting autonomous feedback loops with deterministic boundaries',
      'Implement circuit breakers to prevent infinite hallucination loops and token burn',
      'Construct automated LLM-as-a-Judge scoring rubrics for multi-dimensional evaluation',
      'Enforce least-privilege Non-Human IAM policies, credential segregation, and audit trails',
      'Architect Manager-Worker and decentralized asynchronous Multi-Agent System (MAS) topologies',
      'Establish Continuous Agentic / Continuous Deployment (CA/CD) machine-speed quality gates',
      'Build end-to-end production capstone pipelines with human-in-the-loop escalation protocols'
    ],
    requirements: [
      'Solid foundations in general programming (Python, TypeScript, or modern backend language)',
      'Basic familiarity with version control (Git) and CI/CD concepts',
      'No deep mathematical ML model training knowledge required; all agentic concepts are taught systematically'
    ],
    targetAudience: [
      'Senior Software Engineers & Architects transitioning to autonomous agentic architectures',
      'Engineering Managers & Technical Leads designing machine-speed delivery pipelines',
      'Platform & DevOps Engineers managing non-human IAM, API compute scaling, and AI quality gates',
      'Full-Stack Developers wanting to master the cutting edge of AI-driven software lifecycle'
    ],
    syllabus: [
      {
        chapter: 'Section 0: Course Onboarding & Setup',
        topics: ['Welcome & Course Overview', 'Prerequisites & Target Audience', 'Course Repository & Environment Setup', 'How to Succeed in This Course']
      },
      {
        chapter: 'Section 1: The Evolution of Development Life Cycles',
        topics: ['Structural limitations of traditional SDLC', 'Defining the ADLC paradigm', 'Visualizing the autonomous pipeline', 'Lab: Mapping legacy workflows to ADLC structures']
      },
      {
        chapter: 'Section 2: Aligning Agents with Enterprise Strategy',
        topics: ['Identifying high-value agentic use cases', 'ROI and token-cost projections', 'Formulating integration roadmaps', 'Coding Exercise: Token cost estimator script']
      },
      {
        chapter: 'Section 3: Governance and Risk Management',
        topics: ['Data privacy & tenant isolation in agent workflows', 'Regulatory frameworks (GDPR, HIPAA, SOC 2)', 'Human-in-the-loop safeguards', 'Coding Exercise: Programmatic PII scrubber']
      },
      {
        chapter: 'Section 4: ADLC Infrastructure and Tooling',
        topics: ['Vector DBs & RAG structures in CI/CD', 'Orchestration framework selection (LangChain, AutoGen, CrewAI)', 'Compute scaling & API routing keys']
      },
      {
        chapter: 'Section 5: Anatomy of an Autonomous Agent',
        topics: ['Reasoning engines and prompting limits', 'Tool calling and internal APIs', 'Execution planning & sequential logic']
      },
      {
        chapter: 'Section 6: Transitioning from Prompts to Systems',
        topics: ['Systemic instructions vs single prompts', 'Dynamic context windows & context engineering', 'Lab: Building a single-purpose agent from scratch']
      },
      {
        chapter: 'Section 7: State Management and Memory',
        topics: ['Short-term vs long-term agent memory', 'State persistence across sessions', 'Managing token degradation limits']
      },
      {
        chapter: 'Section 8: Fundamentals of Multi-Agent Systems (MAS)',
        topics: ['Agent specialization & domain experts', 'Collaborative vs competitive pattern logic', 'Inter-agent communication contracts & JSON schemas']
      },
      {
        chapter: 'Section 9: Orchestration and Workflow Topologies',
        topics: ['Manager/Worker hierarchical patterns', 'Decentralized asynchronous networks', 'Lab: Support system MAS diagram & schemas']
      },
      {
        chapter: 'Section 10: Principles of Loop Engineering',
        topics: ['Defining autonomous feedback loops', 'Deterministic vs non-deterministic routing', 'Establishing boundary constraints']
      },
      {
        chapter: 'Section 11: Building Self-Correcting Mechanisms',
        topics: ['Designing error detection triggers', 'Automated fallback and retry logic', 'Lab: Coding a self-correcting agent loop in Python']
      },
      {
        chapter: 'Section 12: Managing Infinite Loops and Timeouts',
        topics: ['Recognizing hallucination spirals', 'Circuit breakers in agentic workflows', 'Alerting and human escalation protocols']
      },
      {
        chapter: 'Section 13: Advanced Agentic Logic',
        topics: ['Chain-of-thought & tree-of-thought models', 'ReAct logic structures', 'Lab: Reasoning path debugging']
      },
      {
        chapter: 'Section 14: The Machine-Speed CI/CD Pipeline',
        topics: ['CI/CD for agent-generated outputs', 'VCS automated action integrations', 'Coding Exercise: Automated Python review script']
      },
      {
        chapter: 'Section 15: Non-Human IAM Policy',
        topics: ['Least-privilege permissions for agents', 'Securing API keys & environment secrets', 'Auditing non-human pipeline actions']
      },
      {
        chapter: 'Section 16: AI in Code Analysis',
        topics: ['Semantic logic reviews vs static linting', 'Specialized code reviews by agents', 'Autonomously flagging security smell vectors']
      },
      {
        chapter: 'Section 17: Automated Quality Gates',
        topics: ['Quantitative acceptance thresholds', 'Handling review hallucinations', 'Lab: Scripting automated code reviews']
      },
      {
        chapter: 'Section 18: Testing Non-Deterministic Systems',
        topics: ['Why binary QA fails AI outputs', 'Statistical evaluation methods', 'Building baseline golden datasets']
      },
      {
        chapter: 'Section 19: Core Evaluation Metrics',
        topics: ['Measuring task completion accuracy', 'Tracking token & compute efficiency', 'Evaluating execution latency profiles']
      },
      {
        chapter: 'Section 20: Hallucination & Factual Drift',
        topics: ['Quantifying drift in long-running runs', 'Data grounding constraints', 'Lab: Hallucination reporting loops']
      },
      {
        chapter: 'Section 21: The LLM-as-a-Judge Framework',
        topics: ['Evaluating models using models', 'Creating scoring rubrics for judges', 'Lab: Automated evaluation judge loop']
      },
      {
        chapter: 'Section 22: Capstone Build and Integration',
        topics: ['Capstone architecture design kickoff', 'Deploying routing APIs & agents', 'Integrating quality gates & judge loop']
      },
      {
        chapter: 'Section 23: Operational Hand-off',
        topics: ['Stress testing and token limit audits', 'Ops hand-off and runbooks', 'ADLC Certification wrap-up']
      }
    ]
  },
  {
    id: 2,
    slug: 'llmops-evaluation',
    title: 'LLMOps & Evaluation: Testing Non-Deterministic AI Systems',
    shortTitle: 'LLMOps & Evaluation',
    category: 'AI Quality & Testing',
    tagline: 'Design statistical QA pipelines, build cosine similarity evaluations, and structure golden test datasets for generative models.',
    rating: 0,
    reviewsCount: 0,
    studentsCount: 0,
    duration: 'Targeting 15 hours',
    lectures: 70,
    level: 'Advanced',
    price: '$14.99',
    originalPrice: '$99.99',
    badge: 'Under Development',
    image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=800&auto=format&fit=crop',
    skills: ['Statistical QA', 'Factual Drift', 'Golden Datasets', 'LLM-as-a-Judge', 'Cosine Similarity', 'Eval Harness'],
    status: 'in_development',
    launchTimeline: 'Launching Q1 2027',
    udemyUrl: 'https://www.udemy.com/user/jeremy-lankford-22/',
    description: 'A complete deep dive into testing AI systems where binary pass/fail assertions fail. Learn to structure LLM-as-a-judge scoring rubrics, benchmark accuracy, and deploy continuous pre-production evaluation loops.',
    longDescription: [
      'Generative AI outputs cannot be evaluated with unit assertions like `assert response == expected`. Every deployment introduces probabilistic variations, subtle factual drifts, and semantic hallucinations.',
      'This course addresses the unique QA bottleneck of modern AI engineering. You will master statistical quality assurance, vector embedding similarity checks, custom Golden Datasets, and automated evaluator LLM harnesses that score production readiness objectively.'
    ],
    whatYouWillLearn: [
      'Why traditional binary QA fails generative AI models and how statistical evaluation solves it',
      'Construct curated Golden Test Datasets for regression prevention across prompt updates',
      'Build cosine similarity and semantic distance evaluation pipelines using embedding vectors',
      'Implement multi-tiered LLM-as-a-Judge scoring rubrics with calibrated synthetic test suites',
      'Deploy continuous automated pre-commit evaluation gates in CI/CD'
    ],
    requirements: [
      'Familiarity with Python and modern testing concepts (pytest, assertions)',
      'Basic understanding of LLM APIs and prompt construction'
    ],
    targetAudience: [
      'QA Engineers and SDETs transitioning into AI evaluation',
      'Backend Engineers building mission-critical LLM applications',
      'MLOps Engineers implementing automated CI/CD model verification'
    ],
    syllabus: [
      {
        chapter: 'Section 1: Fundamentals of Non-Deterministic Testing',
        topics: ['Why binary assertions fail with generative models', 'Probabilistic variance and statistical boundaries', 'Defining acceptable error tolerances']
      },
      {
        chapter: 'Section 2: Golden Datasets & Benchmarks',
        topics: ['Designing representative golden datasets', 'Synthetic dataset augmentation', 'Versioning test corpora alongside codebase']
      },
      {
        chapter: 'Section 3: Metric Formulations & Semantic Scoring',
        topics: ['BLEU, ROUGE, and cosine similarity limitations', 'Embedding distance metrics and semantic clustering', 'Hallucination detection algorithms']
      },
      {
        chapter: 'Section 4: The LLM-as-a-Judge Production Pipeline',
        topics: ['Model-on-model evaluation design', 'Rubric calibration and bias mitigation', 'Lab: Automated continuous evaluation harness']
      }
    ]
  },
  {
    id: 3,
    slug: 'agentic-design-patterns',
    title: 'Agentic Design Patterns & Architecture',
    shortTitle: 'Agentic Patterns',
    category: 'System Architecture',
    tagline: 'Master specialized agent routing, collaborative/competitive multi-agent patterns, and manager-worker delegation topologies.',
    rating: 0,
    reviewsCount: 0,
    studentsCount: 0,
    duration: 'Targeting 18 hours',
    lectures: 85,
    level: 'Advanced',
    price: '$19.99',
    originalPrice: '$129.99',
    badge: 'Under Development',
    image: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=800&auto=format&fit=crop',
    skills: ['Orchestration Patterns', 'Multi-Agent Topologies', 'State Invariance', 'ReAct', 'Dynamic Routing'],
    status: 'in_development',
    launchTimeline: 'Launching Q2 2027',
    udemyUrl: 'https://www.udemy.com/user/jeremy-lankford-22/',
    description: 'Master true agentic architectures. Move beyond single-agent prompt engineering to complex decentralized agent networks with robust inter-agent communication, state persistence, and ReAct routing patterns.',
    longDescription: [
      'Moving beyond toy prompts requires structured architectural patterns. Multi-agent systems face deadlocks, state drift, and routing inefficiencies if not engineered with clear protocols.',
      'This course explores proven architectural topologies including Manager-Worker hierarchies, reflection and critique loops, voting ensembles, and asynchronous event-driven agent meshes.'
    ],
    whatYouWillLearn: [
      'Master the core architectural topologies of multi-agent networks',
      'Implement ReAct (Reasoning + Acting) loops with robust backpressure handling',
      'Design JSON schema-backed inter-agent communication contracts',
      'Structure distributed state persistence and memory hierarchies',
      'Deploy human-in-the-loop escalation paths for high-risk actions'
    ],
    requirements: [
      'Proficiency in Python or TypeScript',
      'Basic knowledge of distributed systems concepts (queues, events, APIs)'
    ],
    targetAudience: [
      'Software Architects designing next-generation enterprise software',
      'Senior Developers moving into multi-agent systems design',
      'Technical Founders building agent-driven software products'
    ],
    syllabus: [
      {
        chapter: 'Section 1: Multi-Agent Topology Paradigms',
        topics: ['Agent specialization vs generalist bottlenecks', 'Hierarchical manager-worker architectures', 'Decentralized peer networks']
      },
      {
        chapter: 'Section 2: Communication & Schemas',
        topics: ['Inter-agent JSON contracts', 'Strict type validation for agent outputs', 'Structured tool call protocol design']
      },
      {
        chapter: 'Section 3: Advanced Reasoning Patterns',
        topics: ['ReAct, Plan-and-Solve, and Reflexion patterns', 'Self-critique and debate loops', 'Dynamic context pruning']
      },
      {
        chapter: 'Section 4: Enterprise State & Persistence',
        topics: ['Session state vs persistent episodic memory', 'Transactional integrity across multi-agent steps', 'Lab: Resilient customer support multi-agent network']
      }
    ]
  },
  {
    id: 4,
    slug: 'enterprise-data-pipelines-rag',
    title: 'Enterprise Data Pipelines for AI: RAG & Fine-Tuning',
    shortTitle: 'Enterprise Data & RAG',
    category: 'Enterprise Data',
    tagline: 'Scale vector database orchestrations, retrieval-augmented generation architectures, and domain fine-tuning models.',
    rating: 0,
    reviewsCount: 0,
    studentsCount: 0,
    duration: 'Targeting 20 hours',
    lectures: 95,
    level: 'Advanced',
    price: '$19.99',
    originalPrice: '$149.99',
    badge: 'Under Development',
    image: 'https://images.unsplash.com/photo-1544383835-bda2bc66a55d?q=80&w=800&auto=format&fit=crop',
    skills: ['Enterprise RAG', 'Vector DB Orchestration', 'Model Fine-Tuning', 'Embeddings', 'Metadata Filtering'],
    status: 'in_development',
    launchTimeline: 'Launching Q3 2027',
    udemyUrl: 'https://www.udemy.com/user/jeremy-lankford-22/',
    description: 'Build production-ready retrieval systems and fine-tuning pipelines. Ground model context windows in secure corporate databases, structure semantic vector namespace routing, and optimize embedding models.',
    longDescription: [
      'Raw LLMs lack company domain knowledge. Naive RAG setups suffer from semantic noise, lost-in-the-middle context limits, and multitenancy data leaks.',
      'This course provides an enterprise blueprint for grounding models safely. You will learn production vector indexing, hybrid sparse/dense search, metadata filtering namespaces, and domain dataset synthesis for parameter-efficient fine-tuning (PEFT/LoRA).'
    ],
    whatYouWillLearn: [
      'Design multi-tenant secure RAG pipelines with isolated namespaces',
      'Orchestrate production vector engines (pgvector, Pinecone, Qdrant)',
      'Implement hybrid search combining BM25 keyword matching with dense vector embeddings',
      'Synthesize high-grade training datasets from enterprise documentation',
      'Fine-tune small open-weight models (LoRA/QLoRA) for specialized reasoning tasks'
    ],
    requirements: [
      'Basic knowledge of SQL and database indexing',
      'Python programming experience'
    ],
    targetAudience: [
      'Data Engineers and Backend Architects modernizing corporate search and knowledge bases',
      'AI Engineers requiring strict tenant isolation and high precision retrieval'
    ],
    syllabus: [
      {
        chapter: 'Section 1: Modern Retrieval Architectures',
        topics: ['Limitations of naive vector search', 'Chunking strategies and semantic boundary preservation', 'Hybrid search: Dense vectors + BM25']
      },
      {
        chapter: 'Section 2: Enterprise Vector Database Scaling',
        topics: ['Indexing in pgvector and cloud vector engines', 'Tenant namespace isolation and security filtering', 'Rerankers and context compression']
      },
      {
        chapter: 'Section 3: Domain Fine-Tuning & PEFT',
        topics: ['When to RAG vs when to fine-tune', 'Curating high-quality domain instruction sets', 'Parameter-efficient fine-tuning with LoRA']
      },
      {
        chapter: 'Section 4: Production Evaluation & Monitoring',
        topics: ['Measuring RAG precision, recall, and faithfulness', 'Latency and cost optimization', 'Lab: Production knowledge retrieval service']
      }
    ]
  },
  {
    id: 5,
    slug: 'advanced-ai-orchestration',
    title: 'Advanced AI Orchestration: Multi-Agent Systems',
    shortTitle: 'Multi-Agent Orchestration',
    category: 'AI Software Engineering',
    tagline: 'Architect secure, asynchronous inter-agent messaging pipelines, least-privilege non-human IAM policies, and execution timeouts.',
    rating: 0,
    reviewsCount: 0,
    studentsCount: 0,
    duration: 'Targeting 16 hours',
    lectures: 80,
    level: 'Advanced',
    price: '$19.99',
    originalPrice: '$139.99',
    badge: 'Under Development',
    image: 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=800&auto=format&fit=crop',
    skills: ['Multi-Agent Orchestration', 'Asynchronous Networks', 'Non-Human IAM', 'Timeout Circuit Breakers', 'Tracing & Telemetry'],
    status: 'in_development',
    launchTimeline: 'Launching Q4 2027',
    udemyUrl: 'https://www.udemy.com/user/jeremy-lankford-22/',
    description: 'Build and scale complex multi-agent setups. Secure non-human agent identities and permissions (least privilege), monitor infinite routing loops, and implement automated timeout circuit breakers.',
    longDescription: [
      'As agent systems expand into production, infrastructure concerns dominate: non-human access management, rate-limiting, tracing asynchronous workflows, and preventing cascading failures.',
      'This course delivers the infrastructure playbook for orchestrating enterprise agent clusters with complete observability, zero-trust security postures, and fail-safe recovery.'
    ],
    whatYouWillLearn: [
      'Design secure asynchronous messaging backbones for distributed agents',
      'Enforce least-privilege non-human identity and access management (IAM)',
      'Deploy distributed tracing and telemetry (OpenTelemetry) across multi-agent hops',
      'Implement circuit breakers, rate limiters, and exponential backoff retry systems',
      'Audit and record full deterministic reproduction logs for compliance'
    ],
    requirements: [
      'Familiarity with cloud microservices, messaging queues, or asynchronous programming',
      'Python or TypeScript background'
    ],
    targetAudience: [
      'Platform Engineers & DevOps leads managing agent runtimes',
      'Site Reliability Engineers (SREs) monitoring AI systems',
      'Security Engineers auditing automated non-human pipeline credentials'
    ],
    syllabus: [
      {
        chapter: 'Section 1: Asynchronous Agent Messaging & Queues',
        topics: ['Event-driven agent architectures', 'Message queues vs polling', 'Dead-letter queues and dropped call recovery']
      },
      {
        chapter: 'Section 2: Non-Human IAM & Zero Trust',
        topics: ['Least-privilege scoping for autonomous actors', 'Ephemeral credentials and token rotation', 'Audit log immutability']
      },
      {
        chapter: 'Section 3: Observability & Distributed Tracing',
        topics: ['Tracing multi-agent execution graphs with OpenTelemetry', 'Cost attribution per agent/step', 'Detecting latency bottlenecks']
      },
      {
        chapter: 'Section 4: Resilience & Circuit Breakers',
        topics: ['Infinite loop detectors', 'Circuit breaker implementations', 'Lab: Resilient production multi-agent cluster']
      }
    ]
  }
];

export function getCourseById(id: number): Course | undefined {
  return courses.find(c => c.id === id);
}

export function getCourseBySlug(slug: string): Course | undefined {
  return courses.find(c => c.slug === slug);
}
