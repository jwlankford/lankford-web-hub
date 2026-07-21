<script setup lang="ts">
import type { ResearchPaper } from '../types';

defineProps<{
  paper: ResearchPaper | null;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'filterTag', tagSlug: string): void;
}>();
</script>

<template>
  <Teleport to="body">
    <div 
      v-if="paper"
      class="fixed inset-0 z-50 overflow-y-auto bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 sm:p-6 animate-fadeIn"
      @click.self="emit('close')"
    >
      <div 
        class="relative bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl max-w-3xl w-full p-6 sm:p-8 text-slate-100 overflow-hidden"
      >
        <!-- Background Decorative Gradient -->
        <div class="absolute top-0 right-0 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl -z-0 pointer-events-none"></div>

        <!-- Header Controls -->
        <div class="flex items-start justify-between border-b border-slate-800 pb-4 mb-6 relative z-10">
          <div>
            <div class="flex items-center space-x-2 text-xs font-mono text-emerald-400 mb-1">
              <span class="px-2 py-0.5 rounded bg-emerald-950 border border-emerald-500/30">
                Year: {{ paper.publication_year }}
              </span>
              <span v-if="paper.journal_or_conf" class="text-slate-400">• {{ paper.journal_or_conf }}</span>
            </div>
            <h2 class="text-2xl font-bold font-serif text-white leading-tight">
              {{ paper.title }}
            </h2>
          </div>
          <button 
            @click="emit('close')"
            class="text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700 p-2 rounded-full transition-colors ml-4 flex-shrink-0"
            title="Close modal"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div class="space-y-6 text-sm relative z-10 max-h-[70vh] overflow-y-auto pr-1">
          <!-- Authors & Metadata -->
          <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700/50 space-y-2">
            <div>
              <span class="text-xs uppercase tracking-wider text-slate-400 font-mono">Authors</span>
              <p class="text-emerald-300 font-mono font-medium">{{ paper.authors }}</p>
            </div>
            <div v-if="paper.zotero_key" class="pt-2 border-t border-slate-700/40 flex items-center justify-between">
              <span class="text-xs uppercase tracking-wider text-slate-400 font-mono">Zotero Reference Key</span>
              <span class="text-xs font-mono bg-slate-900 px-2.5 py-1 rounded text-emerald-400 border border-emerald-500/20">
                {{ paper.zotero_key }}
              </span>
            </div>
          </div>

          <!-- Abstract Section -->
          <div v-if="paper.abstract">
            <h3 class="text-xs font-mono uppercase tracking-wider text-emerald-400 mb-2 font-semibold">
              Abstract & Context
            </h3>
            <p class="text-slate-300 leading-relaxed text-base font-sans bg-slate-950/40 p-4 rounded-xl border border-slate-800/80">
              {{ paper.abstract }}
            </p>
          </div>

          <!-- Key Findings -->
          <div v-if="paper.key_findings" class="bg-emerald-950/30 border border-emerald-500/30 p-4 rounded-xl">
            <h3 class="text-xs font-mono uppercase tracking-wider text-emerald-400 mb-2 font-semibold flex items-center space-x-1.5">
              <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
              <span>Key Analytical Findings</span>
            </h3>
            <p class="text-slate-200 leading-relaxed font-medium">
              {{ paper.key_findings }}
            </p>
          </div>

          <!-- Methodology -->
          <div v-if="paper.methodology">
            <h3 class="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2 font-semibold">
              Methodology & Design Framework
            </h3>
            <p class="text-slate-300 bg-slate-800/40 p-3 rounded-lg border border-slate-700/40">
              {{ paper.methodology }}
            </p>
          </div>

          <!-- Associated Tags -->
          <div v-if="paper.tags && paper.tags.length">
            <h3 class="text-xs font-mono uppercase tracking-wider text-slate-400 mb-2 font-semibold">
              Indexed Taxonomy Tags
            </h3>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="tag in paper.tags"
                :key="tag.slug || tag.name"
                @click="emit('filterTag', tag.slug); emit('close');"
                class="px-3 py-1 rounded-full text-xs font-mono bg-emerald-950 text-emerald-300 border border-emerald-500/40 hover:bg-emerald-800 transition-colors"
              >
                #{{ tag.name }}
              </button>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="mt-6 pt-4 border-t border-slate-800 flex justify-end space-x-3 relative z-10">
          <button 
            @click="emit('close')"
            class="px-5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-sm font-semibold transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
