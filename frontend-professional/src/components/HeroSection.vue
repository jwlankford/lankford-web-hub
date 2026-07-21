<script setup lang="ts">
defineEmits<{
  (e: 'scrollToForm'): void;
}>();
</script>

<template>
  <section class="relative pt-12 pb-16 overflow-hidden">
    <!-- Background Glows -->
    <div class="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-gradient-to-r from-blue-600/20 via-indigo-500/20 to-cyan-400/20 blur-3xl pointer-events-none rounded-full"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        
        <!-- Left Text Column -->
        <div class="lg:col-span-7 space-y-6 text-center lg:text-left">
          <div class="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-blue-100 dark:bg-blue-950/80 border border-blue-300 dark:border-blue-500/30 text-blue-800 dark:text-blue-400 text-xs font-mono font-semibold transition-colors">
            <span class="w-2 h-2 rounded-full bg-cyan-500 dark:bg-cyan-400 animate-pulse"></span>
            <span>Upcoming Release • 2026 Edition</span>
          </div>

          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 dark:text-white tracking-tight leading-tight transition-colors">
            Today's Software <br class="hidden sm:inline" />
            <span class="bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-600 dark:from-blue-400 dark:via-indigo-300 dark:to-cyan-400 bg-clip-text text-transparent">
              Developer
            </span>
          </h1>

          <p class="text-slate-600 dark:text-slate-300 text-base sm:text-lg max-w-2xl leading-relaxed">
            <strong class="text-cyan-700 dark:text-cyan-300 font-semibold block mb-1">Developing Software in the AI Era</strong>
            Navigating modern software architecture, engineering FinOps, executive communication, and team resiliency in complex distributed systems.
          </p>

          <div class="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-2">
            <button 
              @click="$emit('scrollToForm')"
              class="w-full sm:w-auto px-8 py-3.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold rounded-xl shadow-lg shadow-blue-600/30 border border-blue-400/30 transition-all transform hover:-translate-y-0.5"
            >
              Get Early Access & Sample Chapters
            </button>
            <a 
              href="#outline"
              class="w-full sm:w-auto px-6 py-3.5 bg-slate-100 dark:bg-slate-800/80 hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white font-semibold rounded-xl border border-slate-300 dark:border-slate-700/80 transition-colors text-center"
            >
              Explore Table of Contents
            </a>
          </div>

          <!-- Quick Metrics -->
          <div class="grid grid-cols-3 gap-4 pt-6 border-t border-slate-200 dark:border-slate-800/80 max-w-md mx-auto lg:mx-0">
            <div>
              <div class="text-2xl font-bold font-mono text-slate-900 dark:text-white">7</div>
              <div class="text-xs text-slate-500 dark:text-slate-400 font-mono">Chapters in 4 Parts</div>
            </div>
            <div>
              <div class="text-2xl font-bold font-mono text-blue-600 dark:text-blue-400">100%</div>
              <div class="text-xs text-slate-500 dark:text-slate-400 font-mono">Production Focus</div>
            </div>
            <div>
              <div class="text-2xl font-bold font-mono text-cyan-600 dark:text-cyan-400">Free</div>
              <div class="text-xs text-slate-500 dark:text-slate-400 font-mono">Beta Excerpts</div>
            </div>
          </div>
        </div>

        <!-- Right Graphic Column: Book Cover -->
        <div class="lg:col-span-5 flex justify-center">
          <div class="relative group max-w-xs sm:max-w-sm w-full">
            <!-- Glow background -->
            <div class="absolute -inset-1.5 bg-gradient-to-r from-blue-600 via-indigo-500 to-cyan-400 rounded-3xl blur-2xl opacity-40 dark:opacity-50 group-hover:opacity-85 transition duration-500"></div>
            
            <!-- Book Cover Image Container -->
            <div class="relative rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-700/80 shadow-2xl bg-white dark:bg-slate-900 group-hover:scale-[1.02] transition-transform duration-500">
              <img
                src="/book-cover.jpg"
                alt="Today's Software Developer - Mastering the Business of Tech in the Era of AI by Jeremy Lankford"
                class="w-full h-auto object-cover rounded-2xl shadow-2xl"
              />
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>
