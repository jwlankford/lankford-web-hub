<script setup lang="ts">
import { ref } from 'vue';
import type { ResearchPaper } from '../types';

defineProps<{
  paper: ResearchPaper | null;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'filterTag', tagSlug: string): void;
}>();

const isCopied = ref(false);

function copyToClipboard(text: string) {
  navigator.clipboard.writeText(text).then(() => {
    isCopied.value = true;
    setTimeout(() => {
      isCopied.value = false;
    }, 2000);
  });
}
</script>

<template>
  <Teleport to="body">
    <div 
      v-if="paper"
      class="fixed inset-0 z-50 overflow-y-auto bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4 sm:p-6 animate-fadeIn"
      @click.self="emit('close')"
    >
      <div 
        class="relative bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700/80 rounded-2xl shadow-2xl max-w-3xl w-full p-6 sm:p-8 text-slate-900 dark:text-slate-100 overflow-hidden transition-colors"
      >
        <!-- Background Decorative Gradient -->
        <div class="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -z-0 pointer-events-none"></div>

        <!-- Article Cover Image (Above Title) -->
        <div v-if="paper.image_url" class="relative overflow-hidden rounded-xl mb-4 border border-slate-200 dark:border-slate-800 shadow-md">
          <img 
            :src="paper.image_url" 
            :alt="paper.title"
            class="w-full h-52 sm:h-60 object-cover"
          />
        </div>

        <!-- Header Controls -->
        <div class="flex items-start justify-between border-b border-slate-200 dark:border-slate-800 pb-4 mb-6 relative z-10">
          <div>
            <div class="flex items-center space-x-2 text-xs font-mono text-blue-700 dark:text-cyan-400 mb-1">
              <span class="px-2 py-0.5 rounded bg-blue-100 dark:bg-blue-950 border border-blue-300 dark:border-blue-500/30">
                Year: {{ paper.publication_year }}
              </span>
              <span v-if="paper.journal_or_conf" class="text-slate-500 dark:text-slate-400">• {{ paper.journal_or_conf }}</span>
            </div>
            <h2 class="text-2xl font-bold font-serif text-slate-900 dark:text-white leading-tight">
              {{ paper.title }}
            </h2>
          </div>
          <div class="flex items-center space-x-2 ml-4 flex-shrink-0 mt-1 sm:mt-0">
            <button 
              @click="emit('close')"
              class="text-slate-400 hover:text-slate-700 dark:hover:text-white bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 p-2 rounded-full transition-colors"
              title="Close modal"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="space-y-6 text-sm relative z-10 max-h-[70vh] overflow-y-auto pr-1">
          <!-- Authors & Metadata -->
          <div class="bg-slate-50 dark:bg-slate-800/50 p-4 rounded-xl border border-slate-200 dark:border-slate-700/50 space-y-2">
            <div>
              <span class="text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 font-mono">Authors</span>
              <p class="text-blue-800 dark:text-cyan-300 font-mono font-medium">{{ paper.authors }}</p>
            </div>
            <div v-if="paper.zotero_key" class="pt-2 border-t border-slate-200 dark:border-slate-700/40 flex items-center justify-between">
              <span class="text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 font-mono">Zotero Reference Key</span>
              <div class="flex items-center space-x-1.5 bg-slate-100/50 dark:bg-slate-900/60 px-2.5 py-1 rounded border border-slate-200/60 dark:border-slate-800/60 font-mono text-xs text-blue-800 dark:text-cyan-400">
                <span>{{ paper.zotero_key }}</span>
                <button 
                  type="button"
                  @click.stop="copyToClipboard(paper.zotero_key)"
                  class="text-slate-400 hover:text-blue-600 dark:hover:text-cyan-400 p-0.5 rounded transition-colors flex items-center justify-center cursor-pointer ml-1.5"
                  title="Copy Zotero Key"
                >
                  <svg v-if="!isCopied" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/>
                  </svg>
                  <svg v-else class="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                  </svg>
                </button>
              </div>
            </div>
            <div v-if="paper.url" class="pt-2 border-t border-slate-200 dark:border-slate-700/40 flex items-center justify-between">
              <span class="text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 font-mono">Article Link</span>
              <a 
                :href="paper.url"
                target="_blank"
                rel="noopener noreferrer"
                class="text-xs font-mono text-blue-700 dark:text-cyan-400 hover:underline flex items-center space-x-1 truncate max-w-sm"
              >
                <span class="truncate">{{ paper.url }}</span>
                <svg class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
              </a>
            </div>
          </div>

          <!-- Abstract Section -->
          <div v-if="paper.abstract">
            <h3 class="text-xs font-mono uppercase tracking-wider text-blue-700 dark:text-cyan-400 mb-2 font-semibold">
              Abstract & Context
            </h3>
            <p class="text-slate-700 dark:text-slate-300 leading-relaxed text-base font-sans bg-slate-50 dark:bg-slate-950/40 p-4 rounded-xl border border-slate-200 dark:border-slate-800/80">
              {{ paper.abstract }}
            </p>
          </div>

          <!-- Key Findings -->
          <div v-if="paper.key_findings" class="bg-blue-50 dark:bg-blue-950/30 border border-blue-300 dark:border-blue-500/30 p-4 rounded-xl">
            <h3 class="text-xs font-mono uppercase tracking-wider text-blue-800 dark:text-cyan-400 mb-2 font-semibold flex items-center space-x-1.5">
              <svg class="w-4 h-4 text-blue-600 dark:text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
              <span>Key Analytical Findings</span>
            </h3>
            <p class="text-slate-800 dark:text-slate-200 leading-relaxed font-medium">
              {{ paper.key_findings }}
            </p>
          </div>

          <!-- Methodology -->
          <div v-if="paper.methodology">
            <h3 class="text-xs font-mono uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2 font-semibold">
              Methodology & Design Framework
            </h3>
            <p class="text-slate-700 dark:text-slate-300 bg-slate-50 dark:bg-slate-800/40 p-3 rounded-lg border border-slate-200 dark:border-slate-700/40">
              {{ paper.methodology }}
            </p>
          </div>

          <!-- Associated Tags -->
          <div v-if="paper.tags && paper.tags.length">
            <h3 class="text-xs font-mono uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2 font-semibold">
              Indexed Taxonomy Tags
            </h3>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="tag in paper.tags"
                :key="tag.slug || tag.name"
                @click="emit('filterTag', tag.slug); emit('close');"
                class="px-3 py-1 rounded-full text-xs font-mono bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-cyan-300 border border-blue-300 dark:border-blue-500/40 hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors"
              >
                {{ tag.name }}
              </button>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="mt-6 pt-4 border-t border-slate-200 dark:border-slate-800 flex justify-end space-x-3 relative z-10">
          <a
            v-if="paper.url"
            :href="paper.url"
            target="_blank"
            rel="noopener noreferrer"
            class="px-5 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-semibold shadow-md shadow-blue-600/30 transition-all flex items-center space-x-1.5"
          >
            <span>Read Article</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
            </svg>
          </a>
          <button 
            @click="emit('close')"
            class="px-5 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 rounded-lg text-sm font-semibold transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
