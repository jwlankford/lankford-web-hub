<script setup lang="ts">
import type { ResearchPaper } from '../types';

defineProps<{
  paper: ResearchPaper;
}>();

const emit = defineEmits<{
  (e: 'select', paper: ResearchPaper): void;
  (e: 'filterTag', tagSlug: string): void;
}>();
</script>

<template>
  <div 
    class="group relative bg-white dark:bg-slate-900/60 hover:bg-slate-50 dark:hover:bg-slate-900/90 rounded-xl p-6 border border-slate-200 dark:border-slate-800 hover:border-blue-500/40 transition-all duration-300 shadow-md hover:shadow-xl dark:hover:shadow-blue-950/40 flex flex-col justify-between overflow-hidden"
  >
    <!-- Card Top: Publication Year & Journal -->
    <div>
      <div class="flex items-center justify-between text-xs mb-3 text-slate-500 dark:text-slate-400 font-mono">
        <span class="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-md bg-blue-50 dark:bg-blue-950/80 border border-blue-300 dark:border-blue-500/30 text-blue-800 dark:text-cyan-300 font-semibold">
          <span>{{ paper.publication_year }}</span>
        </span>
        <span class="truncate max-w-[200px] text-right font-sans text-slate-500 dark:text-slate-400" :title="paper.journal_or_conf">
          {{ paper.journal_or_conf || 'Peer-Reviewed Study' }}
        </span>
      </div>

      <!-- Article Cover Image (Above Title) -->
      <div 
        v-if="paper.image_url" 
        @click="emit('select', paper)"
        class="relative overflow-hidden rounded-lg mb-3 cursor-pointer border border-slate-200 dark:border-slate-800 group/img"
      >
        <img 
          :src="paper.image_url" 
          :alt="paper.title"
          class="w-full h-44 object-cover group-hover/img:scale-105 transition-transform duration-500"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/60 via-transparent to-transparent opacity-0 group-hover/img:opacity-100 transition-opacity"></div>
      </div>

      <!-- Title -->
      <h3 
        @click="emit('select', paper)"
        class="text-lg font-bold text-slate-900 dark:text-slate-100 group-hover:text-blue-600 dark:group-hover:text-cyan-300 cursor-pointer transition-colors leading-snug mb-2 font-serif"
      >
        {{ paper.title }}
      </h3>

      <!-- Authors -->
      <p class="text-xs font-mono text-blue-700 dark:text-cyan-400/90 mb-4">
        {{ paper.authors }}
      </p>

      <!-- Abstract Snippet -->
      <p 
        v-if="paper.abstract" 
        class="text-sm text-slate-600 dark:text-slate-400 line-clamp-3 mb-4 leading-relaxed"
      >
        {{ paper.abstract }}
      </p>
    </div>

    <!-- Card Bottom: Tags & Action Button -->
    <div>
      <!-- Tags list -->
      <div v-if="paper.tags && paper.tags.length" class="flex flex-wrap gap-1.5 mb-4">
        <button
          v-for="tag in paper.tags"
          :key="tag.slug || tag.name"
          @click.stop="emit('filterTag', tag.slug)"
          class="text-xs px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-blue-100 dark:hover:bg-blue-900/60 text-slate-700 dark:text-slate-300 hover:text-blue-900 dark:hover:text-cyan-200 border border-slate-200 dark:border-slate-700/60 hover:border-blue-500/30 transition-all"
        >
          #{{ tag.name }}
        </button>
      </div>

      <!-- Action Row -->
      <div class="pt-3 border-t border-slate-200 dark:border-slate-800/80 flex items-center justify-between text-xs">
        <span v-if="paper.zotero_key" class="font-mono text-slate-500 flex items-center space-x-1">
          <svg class="w-3.5 h-3.5 text-blue-600 dark:text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
          </svg>
          <span class="truncate max-w-[120px]">{{ paper.zotero_key }}</span>
        </span>
        <span v-else-if="paper.url" class="font-mono text-blue-700 dark:text-cyan-400/80 flex items-center space-x-1">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
          </svg>
          <span>External Reference</span>
        </span>
        <span v-else class="text-slate-400 dark:text-slate-600">Reference Ready</span>

        <div class="flex items-center space-x-3">
          <a
            v-if="paper.url"
            :href="paper.url"
            target="_blank"
            rel="noopener noreferrer"
            @click.stop
            class="text-xs font-semibold text-blue-700 dark:text-cyan-400 hover:text-blue-800 dark:hover:text-cyan-300 bg-blue-50 dark:bg-blue-950/80 hover:bg-blue-100 dark:hover:bg-blue-900 border border-blue-300 dark:border-blue-500/40 px-2.5 py-1 rounded-md flex items-center space-x-1 transition-colors"
          >
            <span>Read Article</span>
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
            </svg>
          </a>
          <button 
            @click="emit('select', paper)"
            class="text-xs font-semibold text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white flex items-center space-x-1 group-hover:translate-x-0.5 transition-all"
          >
            <span>Examine Study</span>
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
