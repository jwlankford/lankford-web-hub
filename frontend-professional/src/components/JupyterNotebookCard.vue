<script setup lang="ts">
import { computed } from 'vue';
import type { JupyterNotebook } from '../types';

const props = defineProps<{
  notebook: JupyterNotebook;
}>();

const tagList = computed(() => {
  if (!props.notebook.tags) return [];
  return props.notebook.tags.split(',').map(t => t.trim()).filter(Boolean);
});
</script>

<template>
  <div 
    class="group relative bg-white dark:bg-slate-900/60 rounded-2xl p-6 border border-slate-200 dark:border-slate-800/80 hover:border-amber-500/40 transition-all duration-350 shadow-md hover:shadow-xl dark:hover:shadow-amber-950/20 flex flex-col justify-between overflow-hidden"
  >
    <!-- Top glow element -->
    <div class="absolute -top-12 -right-12 w-24 h-24 bg-amber-500/10 dark:bg-amber-500/5 rounded-full blur-2xl group-hover:scale-150 transition-transform duration-500"></div>

    <div>
      <!-- Header Row -->
      <div class="flex items-center justify-between mb-4">
        <span class="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full bg-amber-50 dark:bg-amber-950/80 border border-amber-250 dark:border-amber-500/20 text-amber-800 dark:text-amber-350 font-mono text-[10px] font-bold">
          <!-- Google Colab Infinity Logo -->
          <svg class="w-3.5 h-3.5 mr-1" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M13.8 12.6C12.9 9.6 10.2 7.5 7.1 7.5 3.1 7.5 0 10.6 0 14.5s3.1 7 7.1 7c3.1 0 5.8-2.1 6.7-5.1L13.8 12.6z" fill="#F9AB00" />
            <path d="M20.5 7.5c-3.1 0-5.8 2.1-6.7 5.1l0.1 3.8c0.9 3 3.6 5.1 6.7 5.1 4 0 7.1-3.1 7.1-7s-3.1-7-7.1-7z" fill="#E8710A" />
          </svg>
          <span>Google Colab</span>
        </span>
        <span class="text-[9px] font-mono text-slate-400 dark:text-slate-500 uppercase tracking-widest">
          Interactive Script
        </span>
      </div>

      <!-- Title -->
      <h4 class="text-lg font-serif font-bold text-slate-900 dark:text-white leading-snug mb-2 group-hover:text-amber-600 dark:group-hover:text-amber-400 transition-colors">
        {{ notebook.title }}
      </h4>

      <!-- Description -->
      <p class="text-xs text-slate-650 dark:text-slate-400 mb-4 leading-relaxed">
        {{ notebook.description }}
      </p>

      <!-- Tags Badges -->
      <div v-if="tagList.length" class="flex flex-wrap gap-1.5 mb-6">
        <span 
          v-for="tag in tagList" 
          :key="tag"
          class="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800/80 text-[10px] font-mono text-slate-600 dark:text-slate-350 border border-slate-200 dark:border-slate-750"
        >
          #{{ tag }}
        </span>
      </div>
    </div>

    <!-- Actions Footer -->
    <div class="pt-4 border-t border-slate-200 dark:border-slate-800/80 flex items-center justify-between text-xs mt-auto">
      <div class="flex items-center space-x-1 text-slate-400 dark:text-slate-500 font-mono text-[10px]">
        <!-- Python code mark -->
        <svg class="w-3.5 h-3.5 mr-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
        </svg>
        <span>executable code</span>
      </div>

      <a 
        :href="notebook.notebook_url" 
        target="_blank" 
        rel="noopener noreferrer"
        class="px-3.5 py-1.5 font-semibold text-xs rounded-xl bg-amber-50 dark:bg-amber-950 text-amber-700 dark:text-amber-400 hover:bg-amber-100 dark:hover:bg-amber-900 border border-amber-200 dark:border-amber-500/40 transition-colors flex items-center space-x-1.5 group/btn cursor-pointer"
      >
        <span>Launch Notebook</span>
        <svg class="w-3.5 h-3.5 transform group-hover/btn:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
        </svg>
      </a>
    </div>
  </div>
</template>
