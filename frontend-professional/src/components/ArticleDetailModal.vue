<script setup lang="ts">
import type { Article } from '../types';

defineProps<{
  article: Article | null;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
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
  <Teleport to="body">
    <div 
      v-if="article"
      class="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4 sm:p-6 animate-fadeIn"
      @click.self="emit('close')"
    >
      <div 
        class="relative bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-3xl w-full p-6 sm:p-8 text-slate-900 dark:text-slate-100 overflow-hidden transition-colors flex flex-col max-h-[90vh]"
      >
        <!-- Background Decorative Gradient -->
        <div class="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -z-0 pointer-events-none"></div>

        <!-- Header Controls -->
        <div class="flex items-start justify-between border-b border-slate-200 dark:border-slate-800 pb-4 mb-4 relative z-10">
          <div>
            <div class="flex items-center space-x-2 text-xs font-mono text-blue-700 dark:text-cyan-400 mb-1">
              <span class="px-2 py-0.5 rounded bg-blue-100 dark:bg-blue-950 border border-blue-300 dark:border-blue-500/30">
                Published: {{ formatDate(article.published_at) }}
              </span>
            </div>
            <h2 class="text-xl sm:text-2xl font-bold font-serif text-slate-900 dark:text-white leading-tight">
              {{ article.title }}
            </h2>
          </div>
          <button 
            @click="emit('close')"
            class="text-slate-400 hover:text-slate-700 dark:hover:text-white bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 p-2 rounded-full transition-colors ml-4 flex-shrink-0 cursor-pointer"
            title="Close modal"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- Scrollable content -->
        <div class="space-y-6 text-sm relative z-10 overflow-y-auto pr-1 flex-1">
          <!-- Article Cover Image -->
          <div v-if="article.image_url" class="relative overflow-hidden rounded-xl border border-slate-200 dark:border-slate-800 shadow-md">
            <img 
              :src="article.image_url" 
              :alt="article.title"
              class="w-full h-52 sm:h-64 object-cover"
            />
          </div>

          <!-- Summary section -->
          <div class="bg-blue-50/50 dark:bg-blue-950/20 p-4 rounded-xl border border-blue-200/50 dark:border-blue-900/30">
            <p class="text-sm font-sans italic text-slate-700 dark:text-slate-300 leading-relaxed">
              &ldquo;{{ article.summary }}&rdquo;
            </p>
          </div>

          <!-- Full Content -->
          <div class="prose dark:prose-invert max-w-none text-slate-850 dark:text-slate-200 font-sans leading-relaxed text-sm sm:text-base space-y-4 white-space-pre-wrap">
            <div class="whitespace-pre-wrap font-sans">{{ article.content || 'No article content available.' }}</div>
          </div>
        </div>

        <!-- Footer link -->
        <div class="mt-6 pt-4 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs relative z-10">
          <div>
            <a 
              v-if="article.linkedin_url"
              :href="article.linkedin_url"
              target="_blank"
              rel="noopener noreferrer"
              class="text-xs font-semibold text-blue-600 dark:text-blue-400 hover:underline flex items-center space-x-1"
            >
              <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h-2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
              </svg>
              <span>Read original thread on LinkedIn</span>
            </a>
          </div>
          <button 
            @click="emit('close')"
            class="px-4 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-350 text-xs font-semibold rounded-lg transition-colors cursor-pointer"
          >
            Done Reading
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
