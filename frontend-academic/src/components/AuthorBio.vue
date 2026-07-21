<script setup lang="ts">
</script>

<template>
  <div class="space-y-8 animate-fadeIn max-w-4xl mx-auto">
    <!-- Main Bio Header Card -->
    <div class="relative bg-slate-900 border border-slate-800 rounded-2xl p-8 sm:p-10 shadow-2xl overflow-hidden">
      <div class="absolute top-0 right-0 w-80 h-80 bg-emerald-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="flex flex-col sm:flex-row items-start sm:items-center space-y-6 sm:space-y-0 sm:space-x-8 relative z-10">
        <div class="w-24 h-24 sm:w-28 sm:h-28 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-800 flex items-center justify-center text-white font-black text-4xl shadow-xl ring-2 ring-emerald-400/40 flex-shrink-0">
          JW
        </div>
        <div class="space-y-2">
          <div class="flex items-center space-x-3">
            <h2 class="text-3xl font-bold font-serif text-white">Jeremy W. Lankford</h2>
            <span class="px-3 py-1 rounded-full text-xs font-mono bg-emerald-950 text-emerald-300 border border-emerald-500/40">
              PhD Researcher
            </span>
          </div>
          <p class="text-emerald-400 font-mono text-sm">
            Focus: Deterministic Systems, LLM Governance, & High-Concurrency Multi-Tenancy
          </p>
          <p class="text-slate-400 text-sm leading-relaxed pt-1">
            Investigating robust guardrails, dynamic constraint enforcement, and metaprogramming paradigms for mission-critical software automation.
          </p>
        </div>
      </div>
    </div>

    <!-- Core Research Pillars -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-3">
        <div class="w-10 h-10 rounded-lg bg-emerald-950 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold">
          01
        </div>
        <h3 class="font-bold text-white text-base font-serif">LLM Governance</h3>
        <p class="text-xs text-slate-400 leading-relaxed">
          Enforcing mathematical and deterministic boundaries around non-deterministic model inference pipelines.
        </p>
      </div>

      <div class="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-3">
        <div class="w-10 h-10 rounded-lg bg-emerald-950 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold">
          02
        </div>
        <h3 class="font-bold text-white text-base font-serif">Multi-Tenant Isolation</h3>
        <p class="text-xs text-slate-400 leading-relaxed">
          Row-level security architectures and connection pool isolation for multi-tenant data storage.
        </p>
      </div>

      <div class="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-3">
        <div class="w-10 h-10 rounded-lg bg-emerald-950 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold">
          03
        </div>
        <h3 class="font-bold text-white text-base font-serif">Metaprogramming</h3>
        <p class="text-xs text-slate-400 leading-relaxed">
          Static code analysis, dynamic AST transformations, and macro systems for structural code enforcement.
        </p>
      </div>
    </div>

    <!-- Contact & Hub Reference -->
    <div class="bg-slate-900/40 p-6 rounded-xl border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono">
      <div class="text-slate-400">
        Academic Domain: <span class="text-emerald-400">jwlankford.com</span>
      </div>
      <div class="flex items-center space-x-4">
        <a href="http://professional.localhost:5173" target="_blank" class="text-emerald-400 hover:underline flex items-center space-x-1">
          <span>Visit Professional Hub (jeremylankford.com)</span>
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
          </svg>
        </a>
      </div>
    </div>
  </div>
</template>
