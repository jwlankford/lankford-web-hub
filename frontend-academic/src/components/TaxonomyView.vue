<script setup lang="ts">
import { computed } from 'vue';
import type { ResearchPaper } from '../types';

const props = defineProps<{
  papers: ResearchPaper[];
}>();

const emit = defineEmits<{
  (e: 'selectTag', tagSlug: string): void;
}>();

const tagCounts = computed(() => {
  const map: Record<string, { name: string; count: number; slug: string }> = {};
  for (const paper of props.papers) {
    if (paper.tags) {
      for (const tag of paper.tags) {
        const slug = tag.slug || tag.name.toLowerCase().replace(/\s+/g, '-');
        if (!map[slug]) {
          map[slug] = { name: tag.name, count: 0, slug };
        }
        map[slug].count++;
      }
    }
  }
  return Object.values(map).sort((a, b) => b.count - a.count);
});
</script>

<template>
  <div class="space-y-8 animate-fadeIn">
    <!-- Section Header -->
    <div class="bg-white dark:bg-slate-900 p-8 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-xl transition-colors">
      <div class="max-w-3xl">
        <span class="text-xs font-mono text-emerald-800 dark:text-emerald-400 uppercase tracking-widest bg-emerald-100 dark:bg-emerald-950/80 px-3 py-1 rounded-full border border-emerald-300 dark:border-emerald-500/30">
          Taxonomy & Research Clusters
        </span>
        <h2 class="text-2xl font-bold font-serif text-slate-900 dark:text-white mt-3 mb-2">
          Academic Tag Taxonomy Index
        </h2>
        <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">
          Structured research domains governing deterministic LLM verification, multi-tenant cloud isolation, static analysis, and software metaprogramming.
        </p>
      </div>
    </div>

    <!-- Taxonomy Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="item in tagCounts"
        :key="item.slug"
        @click="emit('selectTag', item.slug)"
        class="group cursor-pointer bg-white dark:bg-slate-900/60 hover:bg-slate-50 dark:hover:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-emerald-500/40 p-6 rounded-xl transition-all duration-300 shadow-md flex items-center justify-between"
      >
        <div class="space-y-1">
          <div class="flex items-center space-x-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500 dark:bg-emerald-400 group-hover:scale-125 transition-transform"></span>
            <h3 class="font-bold text-slate-900 dark:text-slate-100 group-hover:text-emerald-600 dark:group-hover:text-emerald-300 text-base transition-colors">
              {{ item.name }}
            </h3>
          </div>
          <p class="text-xs font-mono text-slate-500 dark:text-slate-400">
            slug: <span class="text-emerald-700 dark:text-emerald-400/90">{{ item.slug }}</span>
          </p>
        </div>
        <div class="flex flex-col items-end">
          <span class="text-xl font-black font-mono text-emerald-800 dark:text-emerald-400 bg-emerald-100 dark:bg-emerald-950 px-3 py-1 rounded-lg border border-emerald-300 dark:border-emerald-500/30">
            {{ item.count }}
          </span>
          <span class="text-[10px] text-slate-400 dark:text-slate-500 uppercase font-mono mt-1">
            {{ item.count === 1 ? 'Study' : 'Studies' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
