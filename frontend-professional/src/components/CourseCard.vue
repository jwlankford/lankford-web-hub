<script setup lang="ts">
import type { Course } from '../data/courses';

const props = defineProps<{
  course: Course;
  featured?: boolean;
}>();

const emit = defineEmits<{
  (e: 'select', course: Course): void;
}>();

function handleCardClick() {
  emit('select', props.course);
}
</script>

<template>
  <div 
    @click="handleCardClick"
    class="group cursor-pointer bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-lg hover:shadow-2xl hover:border-blue-500/50 dark:hover:border-blue-500/50 transition-all duration-300 flex flex-col justify-between overflow-hidden relative transform hover:-translate-y-1"
    :class="[
      featured 
        ? 'sm:col-span-2 ring-1 ring-blue-500/30 dark:ring-blue-500/20 bg-gradient-to-br from-white via-blue-50/20 to-white dark:from-slate-900 dark:via-blue-950/20 dark:to-slate-900' 
        : ''
    ]"
  >
    <!-- Top Visual / Thumbnail -->
    <div class="relative overflow-hidden border-b border-slate-200 dark:border-slate-800" :class="featured ? 'h-52 sm:h-64' : 'h-48'">
      <img 
        :src="course.image" 
        :alt="course.title"
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
      />
      <!-- Gradient overlay -->
      <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-slate-950/20 to-transparent"></div>

      <!-- Badges overlay -->
      <div class="absolute top-3 left-3 flex flex-wrap gap-2">
        <span 
          v-if="course.badge" 
          class="px-2.5 py-1 rounded-full text-[10px] font-mono font-bold uppercase tracking-wider shadow"
          :class="course.status === 'published' ? 'bg-blue-600 text-white border border-blue-400/40' : 'bg-amber-500/90 text-white border border-amber-400/30'"
        >
          {{ course.badge }}
        </span>
        <span 
          v-if="course.id === 1" 
          class="px-2.5 py-1 rounded-full bg-indigo-900/90 text-cyan-200 text-[10px] font-mono font-bold uppercase tracking-wider border border-cyan-400/30 shadow"
        >
          Intro Course
        </span>
      </div>

      <!-- Price or timeline chip in corner -->
      <div class="absolute bottom-3 right-3 px-3 py-1 rounded-xl bg-slate-900/90 text-white text-xs font-mono font-bold border border-slate-700/80 backdrop-blur-md shadow-md">
        <span v-if="course.status === 'published'">{{ course.price }}</span>
        <span v-else class="text-amber-400">{{ course.launchTimeline || 'Coming Soon' }}</span>
      </div>

      <!-- Category chip -->
      <div class="absolute bottom-3 left-3 text-[11px] font-mono font-semibold text-cyan-300 drop-shadow">
        {{ course.category }}
      </div>
    </div>

    <!-- Card Content Body -->
    <div class="p-6 sm:p-7 flex-1 flex flex-col justify-between space-y-4">
      <div class="space-y-3">
        <div class="flex items-center justify-between text-[11px] font-mono text-slate-500 dark:text-slate-400">
          <span class="flex items-center space-x-1.5">
            <span class="w-2 h-2 rounded-full" :class="course.status === 'published' ? 'bg-emerald-500' : 'bg-amber-500'"></span>
            <span>{{ course.level }}</span>
          </span>
          <span>{{ course.duration }} • {{ course.lectures }} lectures</span>
        </div>

        <h4 
          class="font-bold text-slate-900 dark:text-white font-serif tracking-tight group-hover:text-blue-600 dark:group-hover:text-cyan-400 transition-colors leading-snug"
          :class="featured ? 'text-xl sm:text-2xl' : 'text-lg'"
        >
          {{ course.title }}
        </h4>

        <p class="text-slate-600 dark:text-slate-350 text-xs sm:text-sm leading-relaxed line-clamp-3">
          {{ course.tagline }}
        </p>

        <!-- Key Skills Badges -->
        <div class="flex flex-wrap gap-1.5 pt-1">
          <span 
            v-for="skill in course.skills.slice(0, featured ? 5 : 3)" 
            :key="skill"
            class="px-2.5 py-0.5 rounded-full text-[10px] font-mono bg-blue-50 dark:bg-blue-950/50 text-blue-800 dark:text-cyan-300 border border-blue-200 dark:border-blue-500/30"
          >
            {{ skill }}
          </span>
          <span 
            v-if="course.skills.length > (featured ? 5 : 3)" 
            class="px-2 py-0.5 rounded-full text-[10px] font-mono bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400"
          >
            +{{ course.skills.length - (featured ? 5 : 3) }} more
          </span>
        </div>
      </div>

      <!-- Action Footer with Course Overview Button -->
      <div class="pt-4 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between gap-3">
        <button 
          type="button"
          @click.stop="handleCardClick"
          class="flex-1 py-2.5 px-4 rounded-xl text-xs font-bold font-mono transition-all duration-200 flex items-center justify-center space-x-2 shadow-sm"
          :class="[
            featured
              ? 'bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-500 hover:to-indigo-600 text-white shadow-blue-500/20'
              : 'bg-slate-900 dark:bg-blue-950/80 hover:bg-blue-600 dark:hover:bg-blue-700 text-white border border-slate-800 dark:border-blue-500/30'
          ]"
        >
          <span>Course Overview</span>
          <svg class="w-3.5 h-3.5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
          </svg>
        </button>

        <a 
          :href="course.udemyUrl"
          target="_blank"
          rel="noopener noreferrer"
          @click.stop
          class="p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-slate-50 dark:bg-slate-950 text-slate-600 dark:text-slate-300 hover:text-blue-600 dark:hover:text-cyan-400 transition-colors flex items-center justify-center"
          title="View on Udemy"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 15c-2.76 0-5-2.24-5-5V7h2v5c0 1.66 1.34 3 3 3s3-1.34 3-3V7h2v5c0 2.76-2.24 5-5 5z"/>
          </svg>
        </a>
      </div>
    </div>
  </div>
</template>
