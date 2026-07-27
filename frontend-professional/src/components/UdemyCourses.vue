<script setup lang="ts">
import { ref, computed } from 'vue';

interface Course {
  id: number;
  title: string;
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
  syllabus: { chapter: string; topics: string[] }[];
}

const activeCourseId = ref<number | null>(null);

const courses = ref<Course[]>([
  {
    id: 1,
    title: 'AI Development Life Cycle (ADLC) - (2026 Edition)',
    category: 'AI Software Engineering',
    tagline: 'Master the transition from traditional SDLC to autonomous agentic pipelines. Focus on loop engineering, machine-speed quality gates, evaluation, and least-privilege IAM.',
    rating: 4.9,
    reviewsCount: 3840,
    studentsCount: 24800,
    duration: '32 hours',
    lectures: 158,
    level: 'Advanced',
    price: '$74.99',
    originalPrice: '$149.99',
    badge: 'Featured Course',
    image: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=600&auto=format&fit=crop',
    skills: ['ADLC Paradigm', 'Loop Engineering', 'Quality Gates', 'LLM-as-a-Judge'],
    description: 'Deconstruct traditional SDLC limits to launch self-correcting autonomous multi-agent pipelines with robust inter-agent state preservation, least-privilege non-human IAM access, and automated LLM judge rubrics.',
    syllabus: [
      {
        chapter: 'Section 0: Course Onboarding & Setup',
        topics: ['Welcome & Course Overview', 'Prerequisites & Target Audience', 'How to Succeed in This Course']
      },
      {
        chapter: 'Section 1: The Evolution of Development Life Cycles',
        topics: ['Structural limitations of traditional SDLC', 'Defining the ADLC paradigm', 'Visualizing the autonomous pipeline', 'Lab: Mapping legacy workflows to ADLC structures']
      },
      {
        chapter: 'Section 2: Aligning Agents with Enterprise Strategy',
        topics: ['Identifying high-value use cases', 'ROI and token-cost projections', 'Formulating integration roadmaps', 'Coding Exercise: Token cost estimator script']
      },
      {
        chapter: 'Section 3: Governance and Risk Management',
        topics: ['Data privacy & tenant isolation', 'Regulatory frameworks (GDPR, HIPAA)', 'Human-in-the-loop safeguards', 'Coding Exercise: Programmatic PII scrubber']
      },
      {
        chapter: 'Section 4: ADLC Infrastructure and Tooling',
        topics: ['Vector DBs & RAG structures', 'Orchestration selection (LangChain, AutoGen)', 'Compute scaling & API routing keys']
      },
      {
        chapter: 'Section 5: Anatomy of an Autonomous Agent',
        topics: ['Reasoning engines and prompting limits', 'Tool calling and internal APIs', 'Execution planning & sequential logic']
      },
      {
        chapter: 'Section 6: Transitioning from Prompts to Systems',
        topics: ['Systemic instructions vs single prompts', 'Dynamic context windows', 'Lab: Building a single-purpose agent from scratch']
      },
      {
        chapter: 'Section 7: State Management and Memory',
        topics: ['Short-term vs long-term agent memory', 'State persistence across sessions', 'Managing token degradation limits']
      },
      {
        chapter: 'Section 8: Fundamentals of Multi-Agent Systems (MAS)',
        topics: ['Agent specialization & domain experts', 'Collaborative vs competitive pattern logic', 'Inter-agent communication contracts']
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
    title: 'LLMOps & Evaluation: Testing Non-Deterministic AI Systems',
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
    image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=600&auto=format&fit=crop',
    skills: ['Statistical QA', 'Factual Drift', 'Golden Datasets', 'LLM-as-a-Judge'],
    description: 'A complete deep dive into testing AI systems where binary pass/fail assertions fail. Learn to structure LLM-as-a-judge scoring rubrics, benchmark accuracy, and deploy continuous pre-production evaluation loops.',
    syllabus: [
      {
        chapter: 'Course Status: Under Development (Launching Q1 2027)',
        topics: [
          'Why traditional binary QA fails generative models',
          'Building custom Golden Datasets for continuous baseline testing',
          'Deploying evaluator agents using model-on-model evaluation loops',
          'Factual drift and context grounding constraints'
        ]
      }
    ]
  },
  {
    id: 3,
    title: 'Agentic Design Patterns & Architecture',
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
    image: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=600&auto=format&fit=crop',
    skills: ['Orchestration Patterns', 'Multi-Agent Topologies', 'State Invariance', 'ReAct'],
    description: 'Master true agentic architectures. Move beyond single-agent prompt engineering to complex decentralized agent networks with robust inter-agent communication, state persistence, and ReAct routing patterns.',
    syllabus: [
      {
        chapter: 'Course Status: Under Development (Launching Q2 2027)',
        topics: [
          'The philosophy of agent specialization and domain separation',
          'Designing Manager/Worker hierarchical control structures',
          'Decentralized and asynchronous agent interaction networks',
          'Structuring robust inter-agent JSON schemas & communication contracts'
        ]
      }
    ]
  },
  {
    id: 4,
    title: 'Enterprise Data Pipelines for AI: RAG & Fine-Tuning',
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
    image: 'https://images.unsplash.com/photo-1544383835-bda2bc66a55d?q=80&w=600&auto=format&fit=crop',
    skills: ['Enterprise RAG', 'Vector DB Orchestration', 'Model Fine-Tuning', 'Embeddings'],
    description: 'Build production-ready retrieval systems and fine-tuning pipelines. Ground model context windows in secure corporate databases, structure semantic vector namespace routing, and optimize embedding models.',
    syllabus: [
      {
        chapter: 'Course Status: Under Development (Launching Q3 2027)',
        topics: [
          'RAG scaling with metadata filtering namespaces',
          'Orchestrating production vector databases (Pinecone, pgvector)',
          'Preparing high-quality datasets for domain-specific fine-tuning',
          'Measuring retrieval accuracy and token density degradation'
        ]
      }
    ]
  },
  {
    id: 5,
    title: 'Advanced AI Orchestration: Multi-Agent Systems',
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
    image: 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=600&auto=format&fit=crop',
    skills: ['Multi-Agent Orchestration', 'Asynchronous Networks', 'Non-Human IAM', 'Timeout Circuit Breakers'],
    description: 'Build and scale complex multi-agent setups. Secure non-human agent identities and permissions (least privilege), monitor infinite routing loops, and implement automated timeout circuit breakers.',
    syllabus: [
      {
        chapter: 'Course Status: Under Development (Launching Q4 2027)',
        topics: [
          'Least-privilege security permissions for non-human agent actors',
          'Auditing, logging, and tracing inter-agent routing flows',
          'Implementing loop circuit breakers and execution timeouts',
          'Human-in-the-loop escalation protocols'
        ]
      }
    ]
  }
]);

const featuredCourse = computed(() => courses.value[0]);
const upcomingCourses = computed(() => courses.value.slice(1));



function toggleSyllabus(courseId: number) {
  if (activeCourseId.value === courseId) {
    activeCourseId.value = null;
  } else {
    activeCourseId.value = courseId;
  }
}
</script>

<template>
  <div class="space-y-8 animate-fadeIn">
    <!-- Udemy Page Summary Header -->
    <div class="bg-white dark:bg-slate-900 p-8 sm:p-10 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-xl relative overflow-hidden transition-colors">
      <div class="absolute bottom-0 right-0 w-64 h-64 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="flex flex-col md:flex-row md:items-center justify-between gap-8 relative z-10">
        <div class="max-w-2xl space-y-4">
          <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-cyan-300 text-xs font-mono border border-blue-300 dark:border-blue-500/30">
            <span>UDEMY COURSES</span>
          </span>
          <h2 class="text-3xl font-extrabold font-serif text-slate-900 dark:text-white leading-tight">
            Advance Your Engineering Career
          </h2>
          <p class="text-slate-600 dark:text-slate-350 text-sm leading-relaxed">
            Premium curriculum courses focused on advanced backend architecture, software metaprogramming, and LLM agentic safety structures. Designed for developers transitioning into staff engineering and systems design roles.
          </p>
        </div>

        <!-- Instructor Stats -->
        <div class="grid grid-cols-3 gap-4 bg-slate-50 dark:bg-slate-950/60 p-4 rounded-2xl border border-slate-200 dark:border-slate-800/80 font-mono text-center shadow-inner">
          <div class="space-y-1">
            <div class="text-[9px] text-slate-400 dark:text-slate-500 uppercase tracking-widest whitespace-nowrap">Total Students</div>
            <div class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white">0</div>
          </div>
          <div class="space-y-1 border-l border-slate-200 dark:border-slate-800 pl-2 sm:pl-4">
            <div class="text-[9px] text-slate-400 dark:text-slate-500 uppercase tracking-widest whitespace-nowrap">Reviews</div>
            <div class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white">0</div>
          </div>
          <div class="space-y-1 border-l border-slate-200 dark:border-slate-800 pl-2 sm:pl-4">
            <div class="text-[9px] text-slate-400 dark:text-slate-500 uppercase tracking-widest whitespace-nowrap">Rating</div>
            <div class="text-xl sm:text-2xl font-black text-blue-600 dark:text-cyan-400">★ 0.0</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Under Development Pill -->
    <div class="w-full bg-yellow-400/20 dark:bg-yellow-900/40 text-yellow-800 dark:text-yellow-400 font-mono text-xs sm:text-sm font-bold tracking-[0.2em] uppercase py-3 rounded-full border border-yellow-400/50 dark:border-yellow-600/50 flex text-center justify-center items-center shadow-sm">
      Under Development
    </div>

    <!-- FEATURED COURSE SPOTLIGHT -->
    <div 
      class="bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 border border-blue-500/30 p-6 sm:p-10 rounded-3xl shadow-2xl relative overflow-hidden text-white transition-all duration-300"
    >
      <div class="absolute top-0 right-0 w-[400px] h-[400px] bg-gradient-to-tr from-blue-600/15 via-indigo-650/15 to-transparent blur-3xl rounded-full pointer-events-none"></div>
      
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
        <!-- Featured Left Column Details -->
        <div class="lg:col-span-8 space-y-6">
          <div class="flex items-center space-x-2">
            <span class="px-3 py-1 rounded-full bg-gradient-to-r from-blue-600 to-indigo-650 text-white text-[10px] font-mono font-bold uppercase tracking-wider shadow border border-blue-450/40">
              Instructor Spotlight
            </span>
            <span class="px-2.5 py-1 rounded bg-slate-800 text-cyan-300 text-[10px] font-mono border border-slate-700">
              2026 Edition
            </span>
          </div>

          <h3 class="text-3xl sm:text-4xl font-black font-serif tracking-tight leading-tight text-white">
            {{ featuredCourse.title }}
          </h3>

          <p class="text-slate-300 text-sm font-mono leading-relaxed max-w-3xl">
            {{ featuredCourse.tagline }}
          </p>

          <p class="text-slate-400 text-xs leading-relaxed max-w-3xl">
            {{ featuredCourse.description }}
          </p>

          <!-- Core Skills Badges -->
          <div class="flex flex-wrap gap-2 pt-1">
            <span 
              v-for="skill in featuredCourse.skills" 
              :key="skill"
              class="px-2.5 py-1 rounded-full bg-blue-950/60 text-[10px] font-mono text-cyan-350 border border-blue-500/30"
            >
              {{ skill }}
            </span>
          </div>

          <!-- Stats list row -->
          <div class="pt-4 border-t border-slate-800 flex flex-wrap items-center gap-6 text-xs font-mono text-slate-400">
            <span>{{ featuredCourse.duration }} • {{ featuredCourse.lectures }} lectures</span>
          </div>
        </div>

        <!-- Featured Right Column: Visual and Buy Now -->
        <div class="lg:col-span-4 flex flex-col justify-between space-y-6 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 shadow-inner">
          <div class="relative rounded-xl overflow-hidden border border-slate-800 aspect-video lg:aspect-auto h-40">
            <img 
              :src="featuredCourse.image" 
              :alt="featuredCourse.title"
              class="w-full h-full object-cover"
            />
          </div>

          <div class="space-y-4">
            <div class="flex items-baseline justify-between border-b border-slate-800 pb-3">
              <span class="text-xs font-mono text-slate-400">Course Price:</span>
              <div class="text-right">
                <span class="text-xs line-through text-slate-500 font-mono mr-1.5">{{ featuredCourse.originalPrice }}</span>
                <span class="text-2xl font-black text-white font-mono">{{ featuredCourse.price }}</span>
              </div>
            </div>

            <div class="flex flex-col gap-2">
              <span 
                class="w-full py-3 bg-slate-800 text-slate-400 font-bold text-center text-sm rounded-xl border border-slate-700 cursor-not-allowed flex items-center justify-center space-x-2"
                title="Coming soon"
              >
                <span>Buy Now (Coming Soon)</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
                </svg>
              </span>

              <button 
                @click="toggleSyllabus(featuredCourse.id)"
                class="w-full py-2 border border-slate-800 hover:border-slate-700 bg-slate-950 text-slate-300 hover:text-white font-semibold text-center text-xs rounded-xl transition-colors flex items-center justify-center space-x-1.5"
              >
                <span>{{ activeCourseId === featuredCourse.id ? 'Hide Syllabus' : 'View Course Curriculum' }}</span>
                <svg 
                  class="w-3.5 h-3.5 transform transition-transform duration-250"
                  :class="activeCourseId === featuredCourse.id ? 'rotate-180' : 'rotate-0'"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Animated Accordion Syllabus Outline (Featured Course) -->
      <div 
        v-if="activeCourseId === featuredCourse.id"
        class="bg-slate-950/75 border-t border-slate-850 p-6 sm:p-8 rounded-2xl mt-8 animate-fadeIn space-y-4 shadow-inner"
      >
        <h4 class="text-xs font-mono uppercase tracking-widest text-blue-400 font-bold mb-3">AI Development Life Cycle (ADLC) Course Curriculum Syllabus</h4>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="section in featuredCourse.syllabus" 
            :key="section.chapter"
            class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-2.5 shadow-sm"
          >
            <h5 class="text-xs font-bold text-white font-serif">{{ section.chapter }}</h5>
            <ul class="space-y-1.5 text-xs text-slate-400 list-disc pl-4 font-mono leading-relaxed">
              <li v-for="topic in section.topics" :key="topic">{{ topic }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- UPCOMING COURSES GRID (LAUNCHING 2027) (HIDDEN UNTIL PUBLISHED) -->
    <div v-if="false" class="space-y-6 pt-4 border-t border-slate-200 dark:border-slate-800/80">
      <div class="max-w-2xl">
        <h3 class="text-xl font-bold font-serif text-slate-900 dark:text-white mb-1">Upcoming Courses (Planned for 2027)</h3>
        <p class="text-xs font-mono text-slate-500 dark:text-slate-400">Curriculums currently under development. Follow the instructor for launch notifications.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div 
          v-for="course in upcomingCourses" 
          :key="course.id"
          class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-xl overflow-hidden hover:border-blue-500/40 transition-all duration-350 flex flex-col justify-between"
        >
          <div>
            <!-- Image visual -->
            <div class="relative h-44 overflow-hidden border-b border-slate-200 dark:border-slate-800 shadow-sm">
              <img 
                :src="course.image" 
                :alt="course.title" 
                class="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
              />
              <span class="absolute top-3 left-3 px-2.5 py-1 rounded bg-amber-600/90 text-white text-[10px] font-mono font-bold uppercase tracking-wider shadow border border-amber-500/30">
                Under Development
              </span>
            </div>

            <!-- Content details -->
            <div class="p-6 space-y-3.5">
              <div class="flex items-center justify-between text-[10px] font-mono">
                <span class="text-blue-600 dark:text-cyan-400 font-bold uppercase tracking-wider">{{ course.category }}</span>
                <span class="text-slate-400 dark:text-slate-500">{{ course.level }}</span>
              </div>

              <h4 class="text-lg font-bold text-slate-900 dark:text-white font-serif leading-snug">
                {{ course.title }}
              </h4>

              <p class="text-slate-500 dark:text-slate-400 text-xs font-mono leading-snug">
                {{ course.tagline }}
              </p>

              <p class="text-slate-600 dark:text-slate-350 text-xs leading-relaxed">
                {{ course.description }}
              </p>

              <!-- Skills badges -->
              <div class="flex flex-wrap gap-1.5 pt-1">
                <span 
                  v-for="skill in course.skills" 
                  :key="skill"
                  class="px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800/80 text-[9px] font-mono text-slate-700 dark:text-slate-350 border border-slate-200 dark:border-slate-750"
                >
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>

          <!-- Bottom Action panel -->
          <div class="p-6 border-t border-slate-200 dark:border-slate-850/80 space-y-4">
            <div class="flex items-center justify-between text-xs font-mono">
              <div class="flex items-center space-x-1.5 text-amber-700 dark:text-amber-400">
                <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>
                <span>Target: Q{{ course.id === 2 ? '1' : course.id === 3 ? '2' : course.id === 4 ? '3' : '4' }} 2027</span>
              </div>
              <span class="text-slate-400 dark:text-slate-500 font-mono">Coming Soon</span>
            </div>

            <div class="grid grid-cols-2 gap-2.5">
              <button 
                @click="toggleSyllabus(course.id)"
                class="py-2 border border-slate-200 dark:border-slate-850 hover:border-blue-500/50 bg-slate-50 dark:bg-slate-950 text-slate-700 dark:text-slate-200 text-xs font-bold rounded-xl transition-all flex items-center justify-center space-x-1 shadow-sm"
              >
                <span>Syllabus Highlights</span>
                <svg 
                  class="w-3 h-3 transform transition-transform duration-250"
                  :class="activeCourseId === course.id ? 'rotate-180' : 'rotate-0'"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>

              <a 
                href="https://www.udemy.com/user/jeremy-lankford-22/" 
                target="_blank" 
                rel="noopener noreferrer"
                class="py-2 bg-gradient-to-r from-slate-100 to-slate-200 dark:from-slate-800 dark:to-slate-800/80 hover:from-blue-600 hover:to-indigo-700 text-slate-700 dark:text-slate-200 hover:text-white text-xs font-bold rounded-xl text-center border border-slate-300 dark:border-slate-750 transition-all flex items-center justify-center space-x-1 shadow-sm"
              >
                <span>Follow Instructor</span>
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
              </a>
            </div>

            <!-- Syllabus Accordion (Upcoming Courses) -->
            <div 
              v-if="activeCourseId === course.id"
              class="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800 animate-fadeIn space-y-2 mt-2"
            >
              <h5 class="text-[10px] font-mono uppercase tracking-wider text-blue-600 dark:text-cyan-400 font-bold">Planned Core Curriculum Topics</h5>
              <ul class="space-y-1 text-xs text-slate-600 dark:text-slate-400 list-disc pl-4 font-mono leading-relaxed">
                <li v-for="topic in course.syllabus[0].topics" :key="topic">{{ topic }}</li>
              </ul>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>
