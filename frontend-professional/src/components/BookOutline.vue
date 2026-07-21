<script setup lang="ts">
import { ref } from 'vue';

interface Chapter {
  id: number;
  number: string;
  title: string;
  description: string;
  topics: string[];
}

interface Part {
  id: number;
  partNumber: string;
  title: string;
  subtitle: string;
  chapters: Chapter[];
}

const parts: Part[] = [
  {
    id: 1,
    partNumber: "Part 1",
    title: "The Great Transition",
    subtitle: "The \"Why\"",
    chapters: [
      {
        id: 1,
        number: "Chapter 1",
        title: "The Great Syntax Commoditization",
        description: "This chapter addresses the hard truth that the era of \"just coding\" is over. We break down the technical shift, proving how AI has turned functional Python, React, and SQL into a $20/month utility. It establishes the central thesis that your value must move from raw output to strategic judgment.",
        topics: ["AI Syntax Automation", "$20/mo Utility Shift", "Raw Output vs. Strategic Judgment"]
      },
      {
        id: 2,
        number: "Chapter 2",
        title: "The Architect Mindset",
        description: "How to stop thinking in Jira tickets and start thinking in systems. I explain systems thinking, architectural trade-offs, and why \"good enough\" for production is often better than \"perfect\" code that never ships.",
        topics: ["Systems Thinking", "Architectural Trade-offs", "Shipping vs. Perfect Code"]
      }
    ]
  },
  {
    id: 2,
    partNumber: "Part 2",
    title: "The Technical-Business Bridge",
    subtitle: "The \"MBA\" Skills",
    chapters: [
      {
        id: 3,
        number: "Chapter 3",
        title: "Speaking Executive: P&L, Not Python",
        description: "To advance your career, you must stop translating technical reality into developer whining and start translating it into financial risk. This chapter teaches you how to map technical debt, legacy CMS issues, or architectural bottlenecks directly to revenue opportunity and compliance cost, ensuring the C-suite listens to you.",
        topics: ["Financial Risk Mapping", "C-Suite Communication", "Technical Debt to P&L"]
      },
      {
        id: 4,
        number: "Chapter 4",
        title: "Engineering FinOps: Cloud Economics & Unit Costs",
        description: "As compute demands explode with AI, engineering is cost management. We explore the economics of compute power, database optimization, and why poorly architected systems become financial liabilities, applying MBA-level cost-accounting to software engineering.",
        topics: ["Cloud Economics", "Compute & Database Unit Costs", "Engineering FinOps"]
      }
    ]
  },
  {
    id: 3,
    partNumber: "Part 3",
    title: "The New Leadership & Governance",
    subtitle: "Scaling Teams & Securing the Stack",
    chapters: [
      {
        id: 5,
        number: "Chapter 5",
        title: "Team Resiliency: The True \"10x\" Engineer",
        description: "A breakdown of why the \"lone wolf\" rockstar coder is a company liability. I argue that true seniority is defined by mentorship, building robust CI/CD pipelines, and writing documentation that makes ten other developers 20% more efficient—focusing on scaling the team, not just output.",
        topics: ["Team Mentorship", "CI/CD & Documentation", "10x Team Efficiency"]
      },
      {
        id: 6,
        number: "Chapter 6",
        title: "Trust, but Validate: Securing the AI Stack",
        description: "The enterprise cannot \"move fast and break things.\" This chapter covers the critical governance, security guardrails, and compliance standards required when integrating AI tools into proprietary systems, explaining how to use these tools without compromising company intellectual property.",
        topics: ["Enterprise Governance", "Security Guardrails", "IP Protection & AI Compliance"]
      }
    ]
  },
  {
    id: 4,
    partNumber: "Part 4",
    title: "Continual Deployment",
    subtitle: "Conclusion",
    chapters: [
      {
        id: 7,
        number: "Chapter 7",
        title: "The Polyglot Pragmatist",
        description: "A final strategic summary on maintaining your relevance over a multi-decade career. I synthesize how my path through diverse languages (C++, databases) and an MBA created a resilient skill set, and I layout the frameworks for how you can build your own continuous learning pipeline to adapt to whatever paradigm shift comes after generative AI.",
        topics: ["Polyglot Skillset", "Continuous Learning Pipeline", "Post-GenAI Career Framework"]
      }
    ]
  }
];

const openChapterId = ref<number | null>(1);

function toggleChapter(id: number) {
  openChapterId.value = openChapterId.value === id ? null : id;
}
</script>

<template>
  <section id="outline" class="py-12 space-y-10">
    <div class="text-center max-w-3xl mx-auto space-y-3">
      <span class="text-xs font-mono text-cyan-800 dark:text-cyan-400 uppercase tracking-widest bg-blue-100 dark:bg-blue-950/80 px-3.5 py-1 rounded-full border border-blue-300 dark:border-blue-500/30">
        Curriculum & Chapter Outline
      </span>
      <h2 class="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">
        Table of Contents & Core Modules
      </h2>
      <p class="text-slate-600 dark:text-slate-300 text-sm sm:text-base leading-relaxed">
        7 strategic chapters divided into 4 core pillars addressing real-world engineering leadership, cloud economics, and AI stack governance.
      </p>
    </div>

    <!-- Parts Container -->
    <div class="max-w-4xl mx-auto space-y-10">
      <div 
        v-for="part in parts" 
        :key="part.id"
        class="space-y-4"
      >
        <!-- Part Header Banner -->
        <div class="flex items-center space-x-3 pb-2 border-b border-slate-200 dark:border-slate-800">
          <span class="text-xs font-mono font-bold text-blue-800 dark:text-blue-400 bg-blue-100 dark:bg-blue-950 px-2.5 py-1 rounded-md border border-blue-300 dark:border-blue-500/30 uppercase tracking-wider">
            {{ part.partNumber }}
          </span>
          <h3 class="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
            {{ part.title }}
          </h3>
          <span class="text-xs font-mono text-cyan-700 dark:text-cyan-400">({{ part.subtitle }})</span>
        </div>

        <!-- Chapters in Part -->
        <div class="space-y-3">
          <div 
            v-for="ch in part.chapters"
            :key="ch.id"
            class="bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800/90 hover:border-blue-500/40 rounded-2xl overflow-hidden transition-all duration-300 shadow-lg"
          >
            <!-- Header Button -->
            <button 
              @click="toggleChapter(ch.id)"
              class="w-full p-5 sm:p-6 text-left flex items-center justify-between space-x-4 focus:outline-none group"
            >
              <div class="flex items-center space-x-4">
                <span class="text-sm font-bold font-mono text-cyan-800 dark:text-cyan-400 bg-slate-100 dark:bg-slate-950 px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-800 flex-shrink-0">
                  {{ ch.number }}
                </span>
                <div>
                  <h4 class="text-base sm:text-lg font-bold text-slate-900 dark:text-white group-hover:text-cyan-600 dark:group-hover:text-cyan-300 transition-colors">
                    {{ ch.title }}
                  </h4>
                </div>
              </div>
              <svg 
                class="w-5 h-5 text-slate-400 transform transition-transform duration-300 flex-shrink-0"
                :class="openChapterId === ch.id ? 'rotate-180 text-cyan-600 dark:text-cyan-400' : ''"
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>

            <!-- Expandable Content -->
            <div 
              v-if="openChapterId === ch.id"
              class="px-5 sm:px-6 pb-6 pt-2 border-t border-slate-200 dark:border-slate-800/80 space-y-4 text-sm animate-fadeIn"
            >
              <p class="text-slate-700 dark:text-slate-200 leading-relaxed bg-slate-50 dark:bg-slate-950/70 p-4 rounded-xl border border-slate-200 dark:border-slate-800/80 text-sm sm:text-base">
                {{ ch.description }}
              </p>

              <div class="space-y-2">
                <span class="text-xs font-mono uppercase tracking-wider text-cyan-800 dark:text-cyan-400 font-semibold">Key Topics & Takeaways:</span>
                <div class="flex flex-wrap gap-2">
                  <span 
                    v-for="topic in ch.topics"
                    :key="topic"
                    class="px-3 py-1 bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 rounded-lg text-xs font-mono border border-slate-300 dark:border-slate-700/60"
                  >
                    ✓ {{ topic }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>
