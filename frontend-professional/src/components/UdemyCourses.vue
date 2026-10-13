<script setup lang="ts">
import { ref, computed } from 'vue';
import { courses as coursesData, type Course } from '../data/courses';

const emit = defineEmits<{
  (e: 'select', course: Course): void;
}>();

const activeCourseId = ref<number | null>(null);
const courses = ref<Course[]>(coursesData);

const featuredCourse = computed(() => courses.value[0]);
const upcomingCourses = computed(() => courses.value.slice(1));

function toggleSyllabus(courseId: number) {
  if (activeCourseId.value === courseId) {
    activeCourseId.value = null;
  } else {
    activeCourseId.value = courseId;
  }
}
</script>

<template>
  <div class="space-y-8 animate-fadeIn">
    <!-- Udemy Page Summary Header -->
    <div class="bg-white dark:bg-slate-900 p-8 sm:p-10 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-xl relative overflow-hidden transition-colors">
      <div class="absolute bottom-0 right-0 w-64 h-64 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="flex flex-col md:flex-row md:items-center justify-between gap-8 relative z-10">
        <div class="max-w-2xl space-y-4">
          <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-cyan-300 text-xs font-mono border border-blue-300 dark:border-blue-500/30">
            <span>UDEMY COURSES</span>
          </span>
          <h2 class="text-3xl font-extrabold font-serif text-slate-900 dark:text-white leading-tight">
            Advance Your Engineering Career
          </h2>
          <p class="text-slate-600 dark:text-slate-350 text-sm leading-relaxed">
            Premium curriculum courses focused on advanced backend architecture, software metaprogramming, and LLM agentic safety structures. Designed for developers transitioning into staff engineering and systems design roles.
          </p>
        </div>

        <!-- Instructor Stats -->
        <div class="grid grid-cols-3 gap-4 bg-slate-50 dark:bg-slate-950/60 p-4 rounded-2xl border border-slate-200 dark:border-slate-800/80 font-mono text-center shadow-inner">
          <div class="space-y-1">
            <div class="text-[9px] text-slate-400 dark:text-slate-500 uppercase tracking-widest whitespace-nowrap">Total Students</div>
            <div class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white">0</div>
          </div>
          <div class="space-y-1 border-l border-slate-200 dark:border-slate-800 pl-2 sm:pl-4">
            <div class="text-[9px] text-slate-400 dark:text-slate-500 uppercase tracking-widest whitespace-nowrap">Reviews</div>
            <div class="text-xl sm:text-2xl font-black text-slate-900 dark:text-white">0</div>
          </div>
          <div class="space-y-1 border-l border-slate-200 dark:border-slate-800 pl-2 sm:pl-4">
            <div class="text-[9px] text-slate-400 dark:text-slate-500 uppercase tracking-widest whitespace-nowrap">Rating</div>
            <div class="text-xl sm:text-2xl font-black text-blue-600 dark:text-cyan-400">★ 0.0</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Under Development Pill -->
    <div class="w-full bg-yellow-400/20 dark:bg-yellow-900/40 text-yellow-800 dark:text-yellow-400 font-mono text-xs sm:text-sm font-bold tracking-[0.2em] uppercase py-3 rounded-full border border-yellow-400/50 dark:border-yellow-600/50 flex text-center justify-center items-center shadow-sm">
      Under Development
    </div>

    <!-- FEATURED COURSE SPOTLIGHT -->
    <div 
      class="bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 border border-blue-500/30 p-6 sm:p-10 rounded-3xl shadow-2xl relative overflow-hidden text-white transition-all duration-300"
    >
      <div class="absolute top-0 right-0 w-[400px] h-[400px] bg-gradient-to-tr from-blue-600/15 via-indigo-650/15 to-transparent blur-3xl rounded-full pointer-events-none"></div>
      
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
        <!-- Featured Left Column Details -->
        <div class="lg:col-span-8 space-y-6">
          <div class="flex items-center space-x-2">
            <span class="px-3 py-1 rounded-full bg-gradient-to-r from-blue-600 to-indigo-650 text-white text-[10px] font-mono font-bold uppercase tracking-wider shadow border border-blue-450/40">
              Instructor Spotlight
            </span>
            <span class="px-2.5 py-1 rounded bg-amber-500/90 text-white text-[10px] font-mono font-bold uppercase tracking-wider shadow border border-amber-400/30">
              Under Development
            </span>
            <span class="px-2.5 py-1 rounded bg-slate-800 text-cyan-300 text-[10px] font-mono border border-slate-700">
              Target: 2026
            </span>
          </div>

          <h3 
            @click="emit('select', featuredCourse)"
            class="text-3xl sm:text-4xl font-black font-serif tracking-tight leading-tight text-white cursor-pointer hover:text-cyan-300 transition-colors"
          >
            {{ featuredCourse.title }}
          </h3>

          <p class="text-slate-300 text-sm font-mono leading-relaxed max-w-3xl">
            {{ featuredCourse.tagline }}
          </p>

          <p class="text-slate-400 text-xs leading-relaxed max-w-3xl">
            {{ featuredCourse.description }}
          </p>

          <!-- Core Skills Badges -->
          <div class="flex flex-wrap gap-2 pt-1">
            <span 
              v-for="skill in featuredCourse.skills" 
              :key="skill"
              class="px-2.5 py-1 rounded-full bg-blue-950/60 text-[10px] font-mono text-cyan-350 border border-blue-500/30"
            >
              {{ skill }}
            </span>
          </div>

          <!-- Stats list row -->
          <div class="pt-4 border-t border-slate-800 flex flex-wrap items-center gap-6 text-xs font-mono text-slate-400">
            <span>{{ featuredCourse.duration }} • {{ featuredCourse.lectures }} lectures</span>
          </div>
        </div>

        <!-- Featured Right Column: Visual and Buy Now -->
        <div class="lg:col-span-4 flex flex-col justify-between space-y-6 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 shadow-inner">
          <div class="relative rounded-xl overflow-hidden border border-slate-800 aspect-video lg:aspect-auto h-40 cursor-pointer" @click="emit('select', featuredCourse)">
            <img 
              :src="featuredCourse.image" 
              :alt="featuredCourse.title"
              class="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
            />
            <span class="absolute top-2.5 left-2.5 px-2.5 py-1 rounded bg-amber-600/90 text-white text-[10px] font-mono font-bold uppercase tracking-wider shadow border border-amber-500/30">
              Under Development
            </span>
          </div>

          <div class="space-y-4">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3 text-xs font-mono">
              <div class="flex items-center space-x-1.5 text-amber-400">
                <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>
                <span>Under Development</span>
              </div>
              <span class="text-cyan-300 font-mono">{{ featuredCourse.launchTimeline || 'Target: 2026' }}</span>
            </div>

            <div class="flex flex-col gap-2">
              <button 
                type="button"
                @click="emit('select', featuredCourse)"
                class="w-full py-3 bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-700 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-center text-sm rounded-xl shadow-lg shadow-blue-500/25 flex items-center justify-center space-x-2 transition-all cursor-pointer"
              >
                <span>View Full Course Overview</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
                </svg>
              </button>

              <button 
                @click="toggleSyllabus(featuredCourse.id)"
                class="w-full py-2 border border-slate-800 hover:border-slate-700 bg-slate-950 text-slate-300 hover:text-white font-semibold text-center text-xs rounded-xl transition-colors flex items-center justify-center space-x-1.5"
              >
                <span>{{ activeCourseId === featuredCourse.id ? 'Hide Quick Syllabus' : 'Quick Syllabus Preview' }}</span>
                <svg 
                  class="w-3.5 h-3.5 transform transition-transform duration-250"
                  :class="activeCourseId === featuredCourse.id ? 'rotate-180' : 'rotate-0'"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Animated Accordion Syllabus Outline (Featured Course) -->
      <div 
        v-if="activeCourseId === featuredCourse.id"
        class="bg-slate-950/75 border-t border-slate-850 p-6 sm:p-8 rounded-2xl mt-8 animate-fadeIn space-y-4 shadow-inner"
      >
        <h4 class="text-xs font-mono uppercase tracking-widest text-blue-400 font-bold mb-3">AI Development Life Cycle (ADLC) Course Curriculum Syllabus</h4>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="section in featuredCourse.syllabus" 
            :key="section.chapter"
            class="bg-slate-900 border border-slate-800 p-4 rounded-xl space-y-2.5 shadow-sm"
          >
            <h5 class="text-xs font-bold text-white font-serif">{{ section.chapter }}</h5>
            <ul class="space-y-1.5 text-xs text-slate-400 list-disc pl-4 font-mono leading-relaxed">
              <li v-for="topic in section.topics" :key="topic">{{ topic }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- UPCOMING COURSES GRID (LAUNCHING 2027) -->
    <div v-if="true" class="space-y-6 pt-4 border-t border-slate-200 dark:border-slate-800/80">
      <div class="max-w-2xl">
        <h3 class="text-xl font-bold font-serif text-slate-900 dark:text-white mb-1">Upcoming Courses (Planned for 2027)</h3>
        <p class="text-xs font-mono text-slate-500 dark:text-slate-400">Curriculums currently under development. Follow the instructor for launch notifications.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div 
          v-for="course in upcomingCourses" 
          :key="course.id"
          class="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-xl overflow-hidden hover:border-blue-500/40 transition-all duration-350 flex flex-col justify-between"
        >
          <div>
            <!-- Image visual -->
            <div class="relative h-44 overflow-hidden border-b border-slate-200 dark:border-slate-800 shadow-sm cursor-pointer" @click="emit('select', course)">
              <img 
                :src="course.image" 
                :alt="course.title" 
                class="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
              />
              <span class="absolute top-3 left-3 px-2.5 py-1 rounded bg-amber-600/90 text-white text-[10px] font-mono font-bold uppercase tracking-wider shadow border border-amber-500/30">
                Under Development
              </span>
            </div>

            <!-- Content details -->
            <div class="p-6 space-y-3.5">
              <div class="flex items-center justify-between text-[10px] font-mono">
                <span class="text-blue-600 dark:text-cyan-400 font-bold uppercase tracking-wider">{{ course.category }}</span>
                <span class="text-slate-400 dark:text-slate-500">{{ course.level }}</span>
              </div>

              <h4 
                @click="emit('select', course)"
                class="text-lg font-bold text-slate-900 dark:text-white font-serif leading-snug cursor-pointer hover:text-blue-600 dark:hover:text-cyan-400 transition-colors"
              >
                {{ course.title }}
              </h4>

              <p class="text-slate-500 dark:text-slate-400 text-xs font-mono leading-snug">
                {{ course.tagline }}
              </p>

              <p class="text-slate-600 dark:text-slate-350 text-xs leading-relaxed">
                {{ course.description }}
              </p>

              <!-- Skills badges -->
              <div class="flex flex-wrap gap-1.5 pt-1">
                <span 
                  v-for="skill in course.skills" 
                  :key="skill"
                  class="px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800/80 text-[9px] font-mono text-slate-700 dark:text-slate-350 border border-slate-200 dark:border-slate-750"
                >
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>

          <!-- Bottom Action panel -->
          <div class="p-6 border-t border-slate-200 dark:border-slate-850/80 space-y-4">
            <div class="flex items-center justify-between text-xs font-mono">
              <div class="flex items-center space-x-1.5 text-amber-700 dark:text-amber-400">
                <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>
                <span>Target: Q{{ course.id === 2 ? '1' : course.id === 3 ? '2' : course.id === 4 ? '3' : '4' }} 2027</span>
              </div>
              <span class="text-slate-400 dark:text-slate-500 font-mono">Coming Soon</span>
            </div>

            <div class="grid grid-cols-2 gap-2.5">
              <button 
                type="button"
                @click="emit('select', course)"
                class="py-2 bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-500 hover:to-indigo-600 text-white text-xs font-bold rounded-xl transition-all flex items-center justify-center space-x-1 shadow-sm cursor-pointer"
              >
                <span>Course Overview</span>
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
                </svg>
              </button>

              <button 
                @click="toggleSyllabus(course.id)"
                class="py-2 border border-slate-200 dark:border-slate-850 hover:border-blue-500/50 bg-slate-50 dark:bg-slate-950 text-slate-700 dark:text-slate-200 text-xs font-bold rounded-xl transition-all flex items-center justify-center space-x-1 shadow-sm cursor-pointer"
              >
                <span>Quick Syllabus</span>
                <svg 
                  class="w-3 h-3 transform transition-transform duration-250"
                  :class="activeCourseId === course.id ? 'rotate-180' : 'rotate-0'"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
            </div>

            <!-- Syllabus Accordion (Upcoming Courses) -->
            <div 
              v-if="activeCourseId === course.id"
              class="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800 animate-fadeIn space-y-2 mt-2"
            >
              <h5 class="text-[10px] font-mono uppercase tracking-wider text-blue-600 dark:text-cyan-400 font-bold">Planned Core Curriculum Topics</h5>
              <ul class="space-y-1 text-xs text-slate-600 dark:text-slate-400 list-disc pl-4 font-mono leading-relaxed">
                <li v-for="topic in course.syllabus[0].topics" :key="topic">{{ topic }}</li>
              </ul>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>
