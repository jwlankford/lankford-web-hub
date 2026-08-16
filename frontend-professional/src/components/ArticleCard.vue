<script setup lang="ts">
import type { Article } from '../types';

defineProps<{
  article: Article;
}>();

const emit = defineEmits<{
  (e: 'select', article: Article): void;
}>();

function formatDate(dateStr?: string) {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}
</script>

<template>
  <div 
    class="group relative bg-white dark:bg-slate-900/60 hover:bg-slate-50 dark:hover:bg-slate-900/90 rounded-xl p-6 border border-slate-200 dark:border-slate-800 hover:border-blue-500/40 transition-all duration-300 shadow-md hover:shadow-xl dark:hover:shadow-blue-950/40 overflow-hidden"
  >
    <div class="flex flex-col md:flex-row gap-6 h-full">
      <!-- Left side: Image -->
      <div class="md:w-1/3 shrink-0">
        <div 
          v-if="article.image_url" 
          @click="emit('select', article)"
          class="relative overflow-hidden rounded-lg cursor-pointer border border-slate-200 dark:border-slate-800 group/img h-full min-h-[12rem] max-h-48 md:max-h-none"
        >
          <img 
            :src="article.image_url" 
            :alt="article.title"
            class="w-full h-full object-cover absolute inset-0 group-hover/img:scale-105 transition-transform duration-500"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950/60 via-transparent to-transparent opacity-0 group-hover/img:opacity-100 transition-opacity"></div>
        </div>
        
        <div 
          v-else 
          @click="emit('select', article)"
          class="relative overflow-hidden rounded-lg cursor-pointer bg-gradient-to-br from-blue-600/10 via-indigo-600/5 to-cyan-600/10 dark:from-blue-950/30 dark:via-indigo-950/20 dark:to-cyan-950/30 border border-slate-200 dark:border-slate-800 flex items-center justify-center group/img h-full min-h-[12rem] max-h-48 md:max-h-none"
        >
          <svg class="w-10 h-10 text-slate-300 dark:text-slate-700 group-hover/img:scale-110 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 20H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v1m2 4a2 2 0 0 0-2-2v3m2-3V9m0 0a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-2m-4-7a1 1 0 1 1-2 0 1 1 0 0 1 2 0ZM9 9h.01M9 13h.01"/>
          </svg>
        </div>
      </div>

      <!-- Right side: Content -->
      <div class="flex-1 flex flex-col justify-between">
        <div>
          <!-- Card Top: Published Date -->
          <div class="flex items-center justify-between text-xs mb-3 text-slate-500 dark:text-slate-400 font-mono">
            <span class="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-md bg-blue-50 dark:bg-blue-950/80 border border-blue-300 dark:border-blue-500/30 text-blue-800 dark:text-cyan-300 font-semibold">
              <span>{{ formatDate(article.published_at) }}</span>
            </span>
            <span class="text-xs uppercase tracking-wider text-slate-400 dark:text-slate-500 font-semibold">
              Weekly Article
            </span>
          </div>

          <!-- Title -->
          <h3 
            @click="emit('select', article)"
            class="text-xl font-bold text-slate-900 dark:text-slate-100 group-hover:text-blue-600 dark:group-hover:text-cyan-300 cursor-pointer transition-colors leading-snug mb-3 font-serif"
          >
            {{ article.title }}
          </h3>

          <!-- Summary -->
          <p 
            class="text-sm text-slate-600 dark:text-slate-400 line-clamp-3 mb-6 leading-relaxed"
          >
            {{ article.summary }}
          </p>
        </div>

        <!-- Actions -->
        <div class="pt-4 border-t border-slate-200 dark:border-slate-800/80 flex items-center justify-between text-xs mt-auto">
          <div>
            <a 
              v-if="article.linkedin_url"
              :href="article.linkedin_url"
              target="_blank"
              rel="noopener noreferrer"
              class="text-xs text-blue-600 dark:text-blue-400 hover:underline flex items-center space-x-1.5 font-medium"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h-2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
              </svg>
              <span>LinkedIn Pulse</span>
            </a>
          </div>

          <div class="flex items-center space-x-3">
            <button 
              @click="emit('select', article)"
              class="text-xs font-semibold text-blue-600 dark:text-cyan-400 hover:text-blue-700 dark:hover:text-cyan-300 bg-blue-50 dark:bg-blue-950/80 hover:bg-blue-100 dark:hover:bg-blue-900 border border-blue-300 dark:border-blue-500/40 px-3 py-1.5 rounded-lg flex items-center space-x-1.5 transition-colors cursor-pointer"
            >
              <span>Read Article</span>
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
