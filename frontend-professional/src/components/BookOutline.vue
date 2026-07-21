<script setup lang="ts">
import { ref } from 'vue';

interface Chapter {
  id: number;
  number: string;
  title: string;
  subtitle: string;
  description: string;
  topics: string[];
}

const chapters: Chapter[] = [
  {
    id: 1,
    number: '01',
    title: 'The Modern Software Paradigm',
    subtitle: 'Architectural Evolution from Monoliths to Agentic Workflows',
    description: 'Deconstructing contemporary engineering requirements: distributed systems resilience, asynchronous message passing, and integrating agentic automation.',
    topics: ['System Isolation', 'Asynchronous Message Loops', 'API Gateway Boundaries']
  },
  {
    id: 2,
    number: '02',
    title: 'Deterministic LLM Guardrails',
    subtitle: 'Runtime Constraint Verification in Non-Deterministic AI Pipelines',
    description: 'How to build mathematically sound safety barriers and schema assertion wrappers around large language model outputs in production.',
    topics: ['JSON Schema Enforcers', 'State Machine Routing', 'Fallback & Self-Correction']
  },
  {
    id: 3,
    number: '03',
    title: 'Multi-Tenant Microservices',
    subtitle: 'Row-Level Isolation & Tenant Context Propagation',
    description: 'Deep dive into database isolation techniques, context middleware in FastAPI/Node, and preventing cross-tenant data leaks.',
    topics: ['FastAPI Middleware', 'SQLModel Isolation', 'Multi-Tenant Security Auditing']
  },
  {
    id: 4,
    number: '04',
    title: 'Metaprogramming & Introspection',
    subtitle: 'Dynamic Code Analysis, AST Rewriting & Macros',
    description: 'Leveraging AST analysis in Python and Rust macros to eliminate structural debt and automate repetitive refactoring patterns.',
    topics: ['AST Introspection', 'Custom Linter Rules', 'Production Code Automation']
  }
];

const openChapterId = ref<number | null>(1);

function toggleChapter(id: number) {
  openChapterId.value = openChapterId.value === id ? null : id;
}
</script>

<template>
  <section id="outline" class="py-12 space-y-8">
    <div class="text-center max-w-3xl mx-auto space-y-3">
      <span class="text-xs font-mono text-blue-400 uppercase tracking-widest bg-blue-950/80 px-3 py-1 rounded-full border border-blue-500/30">
        Curriculum Breakdown
      </span>
      <h2 class="text-3xl font-extrabold text-white tracking-tight">
        Table of Contents & Core Topics
      </h2>
      <p class="text-slate-400 text-sm leading-relaxed">
        Curated chapters addressing real-world challenges faced by senior developers, engineering leads, and technical architects.
      </p>
    </div>

    <!-- Accordion / Grid -->
    <div class="max-w-4xl mx-auto space-y-4">
      <div 
        v-for="ch in chapters"
        :key="ch.id"
        class="bg-slate-900/80 border border-slate-800 hover:border-slate-700 rounded-2xl overflow-hidden transition-all duration-300 shadow-md"
      >
        <!-- Header Button -->
        <button 
          @click="toggleChapter(ch.id)"
          class="w-full p-6 text-left flex items-center justify-between space-x-4 focus:outline-none"
        >
          <div class="flex items-center space-x-4">
            <span class="text-xl font-bold font-mono text-blue-400 bg-blue-950 px-3 py-1.5 rounded-xl border border-blue-500/30">
              {{ ch.number }}
            </span>
            <div>
              <h3 class="text-lg font-bold text-white group-hover:text-blue-400 transition-colors">
                {{ ch.title }}
              </h3>
              <p class="text-xs text-slate-400 font-mono mt-0.5">{{ ch.subtitle }}</p>
            </div>
          </div>
          <svg 
            class="w-5 h-5 text-slate-400 transform transition-transform duration-300"
            :class="openChapterId === ch.id ? 'rotate-180 text-blue-400' : ''"
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
          class="px-6 pb-6 pt-2 border-t border-slate-800/60 space-y-4 text-sm animate-fadeIn"
        >
          <p class="text-slate-300 leading-relaxed bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
            {{ ch.description }}
          </p>

          <div class="space-y-1.5">
            <span class="text-xs font-mono uppercase tracking-wider text-blue-400 font-semibold">Key Takeaways:</span>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="topic in ch.topics"
                :key="topic"
                class="px-3 py-1 bg-slate-800 text-slate-300 rounded-lg text-xs font-mono border border-slate-700/60"
              >
                ✓ {{ topic }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
