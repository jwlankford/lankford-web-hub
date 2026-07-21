<script setup lang="ts">
</script>

<template>
  <section class="py-12 border-t border-slate-800">
    <div class="max-w-4xl mx-auto bg-gradient-to-br from-slate-900 via-slate-900 to-slate-950 p-8 sm:p-10 rounded-3xl border border-slate-800 shadow-2xl relative overflow-hidden">
      <div class="absolute bottom-0 right-0 w-64 h-64 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="grid grid-cols-1 md:grid-cols-12 gap-8 items-center relative z-10">
        <!-- Author Avatar / Initials -->
        <div class="md:col-span-4 flex justify-center">
          <div class="w-32 h-32 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-500 flex items-center justify-center text-white font-black text-5xl shadow-2xl ring-4 ring-blue-500/30">
            JL
          </div>
        </div>

        <!-- Author Bio Details -->
        <div class="md:col-span-8 space-y-4 text-center md:text-left">
          <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-blue-950 text-blue-400 text-xs font-mono border border-blue-500/30">
            <span>ABOUT THE AUTHOR</span>
          </div>

          <h2 class="text-2xl font-bold text-white">Jeremy Lankford</h2>
          <p class="text-sm font-mono text-cyan-400">Senior Software Architect & PhD Researcher</p>

          <p class="text-slate-300 text-sm leading-relaxed">
            Jeremy Lankford leads engineering teams building mission-critical distributed systems and multi-tenant cloud platforms. His work bridges high-concurrency production engineering with cutting-edge academic research in deterministic LLM governance.
          </p>

          <div class="pt-2 flex flex-wrap items-center justify-center md:justify-start gap-4 text-xs font-mono">
            <span class="text-slate-400">Domain: <strong class="text-white">jeremylankford.com</strong></span>
            <a 
              href="http://academic.localhost:5174" 
              target="_blank" 
              class="text-blue-400 hover:text-cyan-300 hover:underline flex items-center space-x-1"
            >
              <span>Explore PhD Research Index (jwlankford.com)</span>
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
