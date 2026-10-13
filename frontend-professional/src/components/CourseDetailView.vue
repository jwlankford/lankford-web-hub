<script setup lang="ts">
import { ref } from 'vue';
import type { Course } from '../data/courses';

const props = withDefaults(
  defineProps<{
    course: Course;
    backLabel?: string;
  }>(),
  {
    backLabel: 'Back to About & Bio'
  }
);

const emit = defineEmits<{
  (e: 'close'): void;
}>();

// Expanded chapters tracking (default first 3 open)
const openChapters = ref<Record<number, boolean>>({
  0: true,
  1: true,
  2: true
});

const isAllExpanded = ref(false);
const copySuccess = ref(false);

function toggleChapter(index: number) {
  openChapters.value[index] = !openChapters.value[index];
}

function toggleExpandAll() {
  isAllExpanded.value = !isAllExpanded.value;
  props.course.syllabus.forEach((_, idx) => {
    openChapters.value[idx] = isAllExpanded.value;
  });
}

function handleCopyLink() {
  navigator.clipboard.writeText(window.location.href);
  copySuccess.value = true;
  setTimeout(() => {
    copySuccess.value = false;
  }, 2500);
}
</script>

<template>
  <div class="relative w-full max-w-6xl mx-auto text-slate-900 dark:text-slate-100 transition-colors flex flex-col animate-fadeIn pb-16">
    <!-- Top Decorative Glow -->
    <div class="absolute top-0 right-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl -z-0 pointer-events-none"></div>

    <!-- Back Navigation Bar -->
    <div class="flex items-center justify-between mb-6 relative z-10">
      <button
        @click="emit('close')"
        class="inline-flex items-center space-x-2 text-xs sm:text-sm font-mono text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-cyan-300 transition-colors cursor-pointer py-1.5 px-3 rounded-xl bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm hover:border-blue-400/50"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
        <span>{{ backLabel }}</span>
      </button>

      <div class="flex items-center space-x-2 text-xs font-mono text-slate-500 dark:text-slate-400">
        <span class="hidden sm:inline">Udemy Course ID:</span>
        <span class="px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-cyan-300 border border-blue-200 dark:border-blue-500/30">#{{ course.id }}</span>
      </div>
    </div>

    <!-- Hero Header Banner -->
    <div class="bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 text-white rounded-3xl p-6 sm:p-10 border border-slate-800 shadow-2xl relative overflow-hidden mb-8">
      <div class="absolute -top-12 -right-12 w-80 h-80 bg-blue-600/15 rounded-full blur-3xl pointer-events-none"></div>

      <div class="relative z-10 max-w-4xl space-y-4">
        <!-- Badges -->
        <div class="flex flex-wrap items-center gap-2">
          <span 
            v-if="course.badge"
            class="px-3 py-1 rounded-full text-[10px] font-mono font-bold uppercase tracking-wider"
            :class="course.status === 'published' ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white border border-blue-400/40' : 'bg-amber-500/90 text-white border border-amber-400/30'"
          >
            {{ course.badge }}
          </span>
          <span 
            v-if="course.id === 1"
            class="px-3 py-1 rounded-full bg-cyan-950/80 text-cyan-300 text-[10px] font-mono font-bold uppercase tracking-wider border border-cyan-500/40"
          >
            Intro Course
          </span>
          <span class="px-3 py-1 rounded-full bg-slate-800/80 text-slate-300 text-[10px] font-mono border border-slate-700">
            {{ course.category }}
          </span>
          <span class="px-3 py-1 rounded-full bg-slate-800/80 text-slate-300 text-[10px] font-mono border border-slate-700">
            Level: {{ course.level }}
          </span>
        </div>

        <!-- Course Title -->
        <h1 class="text-3xl sm:text-4xl md:text-5xl font-black font-serif text-white tracking-tight leading-tight">
          {{ course.title }}
        </h1>

        <!-- Tagline -->
        <p class="text-slate-300 text-base sm:text-lg font-mono leading-relaxed max-w-3xl">
          {{ course.tagline }}
        </p>

        <!-- Instructor Row & Key Meta Info -->
        <div class="pt-4 border-t border-slate-800/80 flex flex-wrap items-center gap-y-3 gap-x-6 text-xs font-mono text-slate-300">
          <div class="flex items-center space-x-2">
            <img 
              src="/jeremy-lankford.png" 
              alt="Jeremy Lankford" 
              class="w-7 h-7 rounded-full object-cover ring-1 ring-blue-400"
            />
            <span>Created by <strong class="text-white">Jeremy Lankford</strong></span>
          </div>

          <div v-if="course.status === 'published'" class="flex items-center space-x-1 text-amber-400 font-bold">
            <span>★ {{ course.rating.toFixed(1) }}</span>
            <span class="text-slate-400 font-normal">({{ course.reviewsCount.toLocaleString() }} ratings)</span>
          </div>

          <div v-if="course.status === 'published'" class="text-slate-300">
            <span>{{ course.studentsCount.toLocaleString() }} students</span>
          </div>

          <div class="flex items-center space-x-1.5 text-slate-300">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ course.duration }} • {{ course.lectures }} lectures</span>
          </div>

          <div class="flex items-center space-x-1.5 text-cyan-300">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
            </svg>
            <span>English (CC)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Grid: Left Detailed Content vs Right Sticky Enrollment Box -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 relative z-10">
      
      <!-- LEFT COLUMN: Comprehensive Course Details -->
      <div class="lg:col-span-8 space-y-8">
        
        <!-- Course Overview / Synopsis -->
        <section class="bg-white dark:bg-slate-900 rounded-3xl p-6 sm:p-8 border border-slate-200 dark:border-slate-800 shadow-md space-y-4">
          <div class="flex items-center space-x-2">
            <span class="w-2.5 h-2.5 rounded-full bg-blue-600"></span>
            <h2 class="text-xl font-bold font-serif text-slate-900 dark:text-white">Course Overview & Vision</h2>
          </div>
          
          <div class="text-slate-600 dark:text-slate-300 text-sm leading-relaxed space-y-3 font-sans">
            <p v-for="(paragraph, idx) in (course.longDescription || [course.description])" :key="idx">
              {{ paragraph }}
            </p>
          </div>

          <!-- Skills Focus Tags -->
          <div class="pt-4 border-t border-slate-100 dark:border-slate-800 space-y-2">
            <h3 class="text-xs font-mono font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
              Core Technical Competencies Mastered
            </h3>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="skill in course.skills" 
                :key="skill"
                class="px-3 py-1 rounded-full text-xs font-mono bg-blue-50 dark:bg-blue-950/60 text-blue-800 dark:text-cyan-300 border border-blue-200 dark:border-blue-500/30"
              >
                {{ skill }}
              </span>
            </div>
          </div>
        </section>

        <!-- What You'll Learn Grid -->
        <section class="bg-white dark:bg-slate-900 rounded-3xl p-6 sm:p-8 border border-slate-200 dark:border-slate-800 shadow-md space-y-4">
          <div class="flex items-center space-x-2">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
            <h2 class="text-xl font-bold font-serif text-slate-900 dark:text-white">What You'll Learn</h2>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-2">
            <div 
              v-for="(item, idx) in course.whatYouWillLearn" 
              :key="idx"
              class="flex items-start space-x-2.5 bg-slate-50 dark:bg-slate-950/60 p-3.5 rounded-2xl border border-slate-200 dark:border-slate-800 text-xs sm:text-sm text-slate-700 dark:text-slate-300 leading-snug"
            >
              <svg class="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
              </svg>
              <span>{{ item }}</span>
            </div>
          </div>
        </section>

        <!-- Complete Course Curriculum Syllabus -->
        <section class="bg-white dark:bg-slate-900 rounded-3xl p-6 sm:p-8 border border-slate-200 dark:border-slate-800 shadow-md space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
            <div>
              <div class="flex items-center space-x-2">
                <span class="w-2.5 h-2.5 rounded-full bg-indigo-600"></span>
                <h2 class="text-xl font-bold font-serif text-slate-900 dark:text-white">Course Curriculum & Syllabus</h2>
              </div>
              <p class="text-xs font-mono text-slate-500 dark:text-slate-400 mt-1">
                {{ course.syllabus.length }} Sections • {{ course.lectures }} Lectures • {{ course.duration }} total length
              </p>
            </div>

            <button 
              type="button"
              @click="toggleExpandAll"
              class="text-xs font-mono font-bold text-blue-600 dark:text-cyan-400 hover:underline cursor-pointer"
            >
              {{ isAllExpanded ? 'Collapse All Sections' : 'Expand All Sections' }}
            </button>
          </div>

          <!-- Section List -->
          <div class="space-y-3 pt-2">
            <div 
              v-for="(section, idx) in course.syllabus" 
              :key="section.chapter"
              class="border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden bg-slate-50/50 dark:bg-slate-950/40 transition-colors"
            >
              <button 
                type="button"
                @click="toggleChapter(idx)"
                class="w-full p-4 text-left flex items-center justify-between gap-4 hover:bg-slate-100/70 dark:hover:bg-slate-900 transition-colors cursor-pointer"
              >
                <div class="flex items-center space-x-3">
                  <span class="text-xs font-mono text-blue-600 dark:text-cyan-400 font-bold">#{{ idx + 1 }}</span>
                  <span class="text-sm font-bold text-slate-900 dark:text-white font-serif">{{ section.chapter }}</span>
                </div>

                <div class="flex items-center space-x-3 shrink-0">
                  <span class="text-xs font-mono text-slate-500 dark:text-slate-400">
                    {{ section.topics.length }} {{ section.topics.length === 1 ? 'topic' : 'topics' }}
                  </span>
                  <svg 
                    class="w-4 h-4 text-slate-400 transform transition-transform duration-200"
                    :class="openChapters[idx] ? 'rotate-180' : 'rotate-0'"
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                  </svg>
                </div>
              </button>

              <!-- Topic List Accordion -->
              <div 
                v-if="openChapters[idx]" 
                class="p-4 pt-1 bg-white dark:bg-slate-900 border-t border-slate-100 dark:border-slate-800/80 space-y-2"
              >
                <ul class="space-y-2 text-xs font-mono text-slate-600 dark:text-slate-350">
                  <li 
                    v-for="(topic, topicIdx) in section.topics" 
                    :key="topicIdx"
                    class="flex items-start space-x-2.5"
                  >
                    <span class="text-slate-400 mt-0.5">•</span>
                    <span class="leading-relaxed">{{ topic }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <!-- Requirements & Prerequisites -->
        <section class="bg-white dark:bg-slate-900 rounded-3xl p-6 sm:p-8 border border-slate-200 dark:border-slate-800 shadow-md space-y-4">
          <div class="flex items-center space-x-2">
            <span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
            <h2 class="text-xl font-bold font-serif text-slate-900 dark:text-white">Requirements & Prerequisites</h2>
          </div>

          <ul class="space-y-2 text-xs sm:text-sm text-slate-600 dark:text-slate-350 list-disc pl-5 font-sans leading-relaxed">
            <li v-for="(req, idx) in course.requirements" :key="idx">{{ req }}</li>
          </ul>
        </section>

        <!-- Target Audience -->
        <section class="bg-white dark:bg-slate-900 rounded-3xl p-6 sm:p-8 border border-slate-200 dark:border-slate-800 shadow-md space-y-4">
          <div class="flex items-center space-x-2">
            <span class="w-2.5 h-2.5 rounded-full bg-cyan-500"></span>
            <h2 class="text-xl font-bold font-serif text-slate-900 dark:text-white">Who This Course Is For</h2>
          </div>

          <ul class="space-y-2 text-xs sm:text-sm text-slate-600 dark:text-slate-350 list-disc pl-5 font-sans leading-relaxed">
            <li v-for="(aud, idx) in course.targetAudience" :key="idx">{{ aud }}</li>
          </ul>
        </section>

        <!-- Instructor Bio in Course Context -->
        <section class="bg-white dark:bg-slate-900 rounded-3xl p-6 sm:p-8 border border-slate-200 dark:border-slate-800 shadow-md space-y-4">
          <div class="flex items-center space-x-2">
            <span class="w-2.5 h-2.5 rounded-full bg-blue-600"></span>
            <h2 class="text-xl font-bold font-serif text-slate-900 dark:text-white">Instructor</h2>
          </div>

          <div class="flex flex-col sm:flex-row items-center sm:items-start gap-5 pt-2">
            <img 
              src="/jeremy-lankford.png" 
              alt="Jeremy Lankford" 
              class="w-20 h-20 rounded-2xl object-cover ring-2 ring-blue-500/40 shadow-md shrink-0"
            />
            <div class="space-y-2 text-center sm:text-left">
              <h3 class="text-lg font-bold text-slate-900 dark:text-white font-serif">Jeremy Lankford</h3>
              <p class="text-xs font-mono text-cyan-600 dark:text-cyan-400">
                Senior Software Architect, Premier Instructor & PhD in IT (AI Focus) student at University of the Cumberlands
              </p>
              <p class="text-xs text-slate-600 dark:text-slate-350 leading-relaxed font-sans">
                Jeremy leads engineering teams building mission-critical distributed systems and multi-tenant cloud platforms. As a premier Udemy instructor, he teaches advanced system design, database isolation patterns, metaprogramming abstractions, and AI guardrails to thousands of software engineers worldwide.
              </p>
              
              <div class="flex flex-wrap items-center justify-center sm:justify-start gap-3 pt-2 text-xs font-mono">
                <a 
                  :href="course.udemyUrl" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  class="inline-flex items-center space-x-1.5 text-blue-600 dark:text-cyan-400 hover:underline"
                >
                  <span>Udemy Instructor Profile</span>
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </section>

      </div>

      <!-- RIGHT COLUMN: Sticky Sidebar Action Card -->
      <div class="lg:col-span-4">
        <div class="sticky top-24 space-y-6">
          <div class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-xl overflow-hidden p-6 space-y-6">
            
            <!-- Video / Image Preview -->
            <div class="relative rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800 aspect-video shadow-inner">
              <img 
                :src="course.image" 
                :alt="course.title"
                class="w-full h-full object-cover"
              />
              <div class="absolute inset-0 bg-slate-950/30 flex items-center justify-center">
                <a 
                  :href="course.udemyUrl"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="w-12 h-12 rounded-full bg-blue-600/90 text-white flex items-center justify-center hover:scale-110 hover:bg-blue-500 transition-all shadow-lg backdrop-blur-sm"
                  title="Watch Preview on Udemy"
                >
                  <svg class="w-5 h-5 ml-0.5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M8 5v14l11-7z"/>
                  </svg>
                </a>
              </div>
            </div>

            <!-- Pricing / Status Block -->
            <div class="space-y-2">
              <div class="flex items-baseline justify-between">
                <span class="text-xs font-mono text-slate-500 dark:text-slate-400">Course Status:</span>
                <span 
                  class="px-2.5 py-0.5 rounded-full text-xs font-mono font-bold"
                  :class="course.status === 'published' ? 'bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300' : 'bg-amber-100 dark:bg-amber-950/80 text-amber-800 dark:text-amber-300'"
                >
                  {{ course.status === 'published' ? 'Active Enrollment' : 'Under Development' }}
                </span>
              </div>

              <div class="flex items-baseline justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
                <span class="text-xs font-mono text-slate-500 dark:text-slate-400">Tuition Price:</span>
                <div class="text-right">
                  <span v-if="course.status === 'published'" class="text-xs line-through text-slate-400 font-mono mr-2">{{ course.originalPrice }}</span>
                  <span class="text-2xl font-black font-mono text-slate-900 dark:text-white">{{ course.price }}</span>
                </div>
              </div>
            </div>

            <!-- Primary CTAs -->
            <div class="space-y-3">
              <a 
                :href="course.udemyUrl"
                target="_blank"
                rel="noopener noreferrer"
                class="w-full py-3.5 px-4 rounded-xl text-center font-bold text-sm text-white font-mono transition-all duration-200 flex items-center justify-center space-x-2 shadow-lg"
                :class="[
                  course.status === 'published'
                    ? 'bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-700 hover:from-blue-500 hover:to-indigo-500 shadow-blue-500/25'
                    : 'bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 shadow-amber-500/25'
                ]"
              >
                <span>{{ course.status === 'published' ? 'Enroll on Udemy' : 'Follow for Launch Alerts' }}</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
              </a>

              <button 
                type="button"
                @click="handleCopyLink"
                class="w-full py-2.5 px-4 rounded-xl text-xs font-mono font-semibold border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 transition-colors flex items-center justify-center space-x-2 cursor-pointer"
              >
                <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                </svg>
                <span>{{ copySuccess ? 'Link Copied to Clipboard!' : 'Share Course Link' }}</span>
              </button>
            </div>

            <!-- Includes Checklist -->
            <div class="space-y-3 pt-3 border-t border-slate-100 dark:border-slate-800">
              <h4 class="text-xs font-mono font-bold uppercase tracking-wider text-slate-900 dark:text-white">
                This course includes:
              </h4>
              <ul class="space-y-2.5 text-xs font-mono text-slate-600 dark:text-slate-350">
                <li class="flex items-center space-x-2.5">
                  <svg class="w-4 h-4 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  <span>{{ course.duration }} on-demand video</span>
                </li>
                <li class="flex items-center space-x-2.5">
                  <svg class="w-4 h-4 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                  <span>{{ course.lectures }} comprehensive lectures</span>
                </li>
                <li class="flex items-center space-x-2.5">
                  <svg class="w-4 h-4 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
                  </svg>
                  <span>Interactive lab code exercises</span>
                </li>
                <li class="flex items-center space-x-2.5">
                  <svg class="w-4 h-4 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                  </svg>
                  <span>Access on mobile, tablet, and TV</span>
                </li>
                <li class="flex items-center space-x-2.5">
                  <svg class="w-4 h-4 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"/>
                  </svg>
                  <span>Certificate of completion</span>
                </li>
              </ul>
            </div>

          </div>
        </div>
      </div>

    </div>
  </div>
</template>
