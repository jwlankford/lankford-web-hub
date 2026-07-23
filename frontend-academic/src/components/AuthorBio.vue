<script setup lang="ts">
</script>

<template>
  <div class="space-y-8 animate-fadeIn max-w-4xl mx-auto">
    <!-- Main Bio Header Card -->
    <div class="relative bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-8 sm:p-10 shadow-2xl overflow-hidden transition-colors">
      <div class="absolute top-0 right-0 w-80 h-80 bg-emerald-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="flex flex-col sm:flex-row items-start sm:items-center space-y-6 sm:space-y-0 sm:space-x-8 relative z-10">
        <img
          src="/jeremy-lankford.jpg" 
          alt="Jeremy W. Lankford" 
          class="w-24 h-24 sm:w-28 sm:h-28 rounded-2xl object-cover shadow-xl ring-2 ring-emerald-500/40 flex-shrink-0" 
        />
        <div class="space-y-2">
          <div class="flex items-center space-x-3">
            <h2 class="text-3xl font-bold font-serif text-slate-900 dark:text-white">Jeremy W. Lankford</h2>
            <span class="px-3 py-1 rounded-full text-xs font-mono bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-500/40">
              PhD Researcher
            </span>
          </div>
          <p class="text-emerald-700 dark:text-emerald-400 font-mono text-sm">
            Focus: Deterministic Systems, LLM Governance, & High-Concurrency Multi-Tenancy
          </p>
          <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed pt-1">
            Investigating robust guardrails, dynamic constraint enforcement, and metaprogramming paradigms for mission-critical software automation.
          </p>

          <!-- Social Media Links -->
          <div class="flex items-center space-x-3 pt-3">
            <a 
              href="http://www.linkedin.com/in/jwlankford" 
              target="_blank" 
              rel="noopener noreferrer"
              class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-mono bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-500/30 hover:bg-blue-100 dark:hover:bg-blue-900 transition-colors"
              title="LinkedIn Profile"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
              </svg>
              <span>LinkedIn</span>
            </a>

            <a 
              href="https://x.com/jwlankford" 
              target="_blank" 
              rel="noopener noreferrer"
              class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-mono bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-slate-300 dark:border-slate-700 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
              title="X (Twitter) Profile"
            >
              <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
              </svg>
              <span>X / Twitter</span>
            </a>

            <a 
              href="https://www.facebook.com/profile.php?id=61591720403485" 
              target="_blank" 
              rel="noopener noreferrer"
              class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-mono bg-blue-50 dark:bg-blue-950/60 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-500/30 hover:bg-blue-100 dark:hover:bg-indigo-900 transition-colors"
              title="Facebook Profile"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H7.5v-3H10V9.69c0-2.47 1.47-3.83 3.72-3.83 1.08 0 2.2.19 2.2.19v2.42h-1.24c-1.23 0-1.61.76-1.61 1.54V12h2.73l-.44 3h-2.29v6.8c4.56-.93 8-4.96 8-9.8z"/>
              </svg>
              <span>Facebook</span>
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Core Research Pillars -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white dark:bg-slate-900/60 p-6 rounded-xl border border-slate-200 dark:border-slate-800 space-y-3 transition-colors shadow-sm">
        <div class="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-950 border border-emerald-300 dark:border-emerald-500/30 flex items-center justify-center text-emerald-800 dark:text-emerald-400 font-bold">
          01
        </div>
        <h3 class="font-bold text-slate-900 dark:text-white text-base font-serif">LLM Governance</h3>
        <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
          Enforcing mathematical and deterministic boundaries around non-deterministic model inference pipelines.
        </p>
      </div>

      <div class="bg-white dark:bg-slate-900/60 p-6 rounded-xl border border-slate-200 dark:border-slate-800 space-y-3 transition-colors shadow-sm">
        <div class="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-950 border border-emerald-300 dark:border-emerald-500/30 flex items-center justify-center text-emerald-800 dark:text-emerald-400 font-bold">
          02
        </div>
        <h3 class="font-bold text-slate-900 dark:text-white text-base font-serif">Multi-Tenant Isolation</h3>
        <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
          Row-level security architectures and connection pool isolation for multi-tenant data storage.
        </p>
      </div>

      <div class="bg-white dark:bg-slate-900/60 p-6 rounded-xl border border-slate-200 dark:border-slate-800 space-y-3 transition-colors shadow-sm">
        <div class="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-950 border border-emerald-300 dark:border-emerald-500/30 flex items-center justify-center text-emerald-800 dark:text-emerald-400 font-bold">
          03
        </div>
        <h3 class="font-bold text-slate-900 dark:text-white text-base font-serif">Metaprogramming</h3>
        <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
          Static code analysis, dynamic AST transformations, and macro systems for structural code enforcement.
        </p>
      </div>
    </div>

    <!-- Contact & Hub Reference -->
    <div class="bg-white dark:bg-slate-900/40 p-6 rounded-xl border border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono transition-colors shadow-sm">
      <div class="text-slate-600 dark:text-slate-400">
        Academic Domain: <span class="text-emerald-700 dark:text-emerald-400">jwlankford.com</span>
      </div>
      <div class="flex items-center space-x-4">
        <a href="http://professional.localhost:5173" target="_blank" class="text-emerald-700 dark:text-emerald-400 hover:underline flex items-center space-x-1">
          <span>Visit Professional Hub (jeremylankford.com)</span>
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
          </svg>
        </a>
      </div>
    </div>
  </div>
</template>
