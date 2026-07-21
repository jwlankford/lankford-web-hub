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
          <div class="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-blue-950/80 border border-blue-500/30 text-blue-400 text-xs font-mono font-semibold">
            <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
            <span>Upcoming Release • 2026 Edition</span>
          </div>

          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-white tracking-tight leading-tight">
            Today's Software <br class="hidden sm:inline" />
            <span class="bg-gradient-to-r from-blue-400 via-indigo-300 to-cyan-400 bg-clip-text text-transparent">
              Developer
            </span>
          </h1>

          <p class="text-slate-300 text-base sm:text-lg max-w-2xl leading-relaxed">
            Navigating modern software architecture, AI-assisted engineering workflows, deterministic guardrails, and production resilience in complex distributed systems.
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
              class="w-full sm:w-auto px-6 py-3.5 bg-slate-800/80 hover:bg-slate-800 text-slate-300 hover:text-white font-semibold rounded-xl border border-slate-700/80 transition-colors text-center"
            >
              Explore Table of Contents
            </a>
          </div>

          <!-- Quick Metrics -->
          <div class="grid grid-cols-3 gap-4 pt-6 border-t border-slate-800/80 max-w-md mx-auto lg:mx-0">
            <div>
              <div class="text-2xl font-bold font-mono text-white">12+</div>
              <div class="text-xs text-slate-400 font-mono">Core Modules</div>
            </div>
            <div>
              <div class="text-2xl font-bold font-mono text-blue-400">100%</div>
              <div class="text-xs text-slate-400 font-mono">Production Focus</div>
            </div>
            <div>
              <div class="text-2xl font-bold font-mono text-cyan-400">Free</div>
              <div class="text-xs text-slate-400 font-mono">Beta Excerpts</div>
            </div>
          </div>
        </div>

        <!-- Right Graphic Column: Book Mockup -->
        <div class="lg:col-span-5 flex justify-center">
          <div class="relative group max-w-sm w-full">
            <div class="absolute -inset-1 bg-gradient-to-r from-blue-600 to-cyan-500 rounded-3xl blur-xl opacity-40 group-hover:opacity-75 transition duration-500"></div>
            
            <div class="relative bg-slate-900 border border-slate-700/80 rounded-2xl p-8 shadow-2xl flex flex-col justify-between space-y-8 aspect-[3/4]">
              <!-- Book Spine/Header -->
              <div class="space-y-4">
                <div class="flex items-center justify-between text-xs font-mono text-blue-400">
                  <span>JEREMY LANKFORD</span>
                  <span class="px-2 py-0.5 bg-blue-950 rounded border border-blue-500/30">HARDCOVER</span>
                </div>
                <div class="h-1 bg-gradient-to-r from-blue-500 to-cyan-400 rounded-full"></div>
                <h2 class="text-3xl font-black text-white leading-tight font-sans tracking-tight">
                  TODAY'S <br />
                  SOFTWARE <br />
                  <span class="text-blue-400">DEVELOPER</span>
                </h2>
                <p class="text-xs text-slate-400 font-mono">
                  Mastering Systems Architecture, AI Integration & Metaprogramming
                </p>
              </div>

              <!-- Book Footer Code Visual -->
              <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-[11px] text-slate-400 space-y-1">
                <div class="text-blue-400">// Production Verification</div>
                <div><span class="text-purple-400">async def</span> <span class="text-emerald-400">deploy_resilience</span>():</div>
                <div class="pl-4 text-cyan-300">await system.enforce_guardrails()</div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>
