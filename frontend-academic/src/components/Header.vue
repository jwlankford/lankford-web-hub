<script setup lang="ts">
defineProps<{
  activeTab: 'papers' | 'taxonomy' | 'matrix' | 'bio';
  isLiveBackend: boolean;
  totalPapers: number;
  totalTags: number;
}>();

const emit = defineEmits<{
  (e: 'update:activeTab', tab: 'papers' | 'taxonomy' | 'matrix' | 'bio'): void;
  (e: 'openAddModal'): void;
}>();
</script>

<template>
  <header class="sticky top-0 z-40 backdrop-blur-xl bg-slate-950/85 border-b border-emerald-500/20 shadow-2xl text-slate-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-20">
        
        <!-- Premium Academic Brand & Emblem Logo -->
        <div class="flex items-center space-x-3.5 group cursor-pointer" @click="emit('update:activeTab', 'papers')">
          <!-- Animated SVG Emblem -->
          <div class="relative flex items-center justify-center">
            <div class="absolute -inset-1 bg-gradient-to-r from-emerald-500 to-teal-400 rounded-xl blur opacity-30 group-hover:opacity-75 transition duration-300"></div>
            <div class="relative w-11 h-11 rounded-xl bg-slate-900 border border-emerald-400/40 flex items-center justify-center shadow-lg shadow-emerald-950/50 group-hover:scale-105 transition-transform duration-300">
              <!-- Geometric Academic / Neural SVG Icon -->
              <svg class="w-6 h-6 text-emerald-400 group-hover:text-teal-300 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 14l9-5-9-5-9 5 9 5z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0112 20.055a11.952 11.952 0 01-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 14l9-5-9-5-9 5 9 5zm0 0v6" />
              </svg>
            </div>
          </div>

          <!-- Brand Typography -->
          <div>
            <div class="flex items-center space-x-2">
              <span class="font-serif font-bold text-xl tracking-tight text-white group-hover:text-emerald-300 transition-colors">
                LANKFORD <span class="text-emerald-400 font-sans font-extrabold text-lg">ACADEMIA</span>
              </span>
              <span class="text-[10px] px-2 py-0.5 rounded-full font-mono bg-emerald-950/90 text-emerald-300 border border-emerald-500/40 uppercase tracking-widest hidden sm:inline-block">
                PhD Candidate
              </span>
            </div>
            <div class="flex items-center space-x-2 text-xs text-slate-400">
              <span class="font-mono text-[11px] text-emerald-400/90">jwlankford.com</span>
              <span class="text-slate-600">•</span>
              <span>Deterministic AI Governance & Systems</span>
            </div>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <nav class="hidden md:flex items-center space-x-1.5 bg-slate-900/90 p-1.5 rounded-2xl border border-slate-800 shadow-inner">
          <button
            @click="emit('update:activeTab', 'papers')"
            :class="[
              'px-4 py-2 rounded-xl text-xs font-semibold tracking-wide transition-all duration-200 flex items-center space-x-1.5',
              activeTab === 'papers'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-lg shadow-emerald-600/30 border border-emerald-400/30'
                : 'text-slate-300 hover:text-white hover:bg-slate-800/80'
            ]"
          >
            <span>Research Index</span>
            <span class="px-1.5 py-0.5 text-[10px] font-mono rounded bg-slate-950/60 text-emerald-300 border border-emerald-500/30">{{ totalPapers }}</span>
          </button>
          <button
            @click="emit('update:activeTab', 'taxonomy')"
            :class="[
              'px-4 py-2 rounded-xl text-xs font-semibold tracking-wide transition-all duration-200 flex items-center space-x-1.5',
              activeTab === 'taxonomy'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-lg shadow-emerald-600/30 border border-emerald-400/30'
                : 'text-slate-300 hover:text-white hover:bg-slate-800/80'
            ]"
          >
            <span>Taxonomy</span>
            <span class="px-1.5 py-0.5 text-[10px] font-mono rounded bg-slate-950/60 text-emerald-300 border border-emerald-500/30">{{ totalTags }}</span>
          </button>
          <button
            @click="emit('update:activeTab', 'matrix')"
            :class="[
              'px-4 py-2 rounded-xl text-xs font-semibold tracking-wide transition-all duration-200',
              activeTab === 'matrix'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-lg shadow-emerald-600/30 border border-emerald-400/30'
                : 'text-slate-300 hover:text-white hover:bg-slate-800/80'
            ]"
          >
            Synthesis Matrix
          </button>
          <button
            @click="emit('update:activeTab', 'bio')"
            :class="[
              'px-4 py-2 rounded-xl text-xs font-semibold tracking-wide transition-all duration-200',
              activeTab === 'bio'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-lg shadow-emerald-600/30 border border-emerald-400/30'
                : 'text-slate-300 hover:text-white hover:bg-slate-800/80'
            ]"
          >
            About & Bio
          </button>
        </nav>

        <!-- Right Side Actions & Status -->
        <div class="flex items-center space-x-3">
          <!-- Backend Connection Badge -->
          <div 
            class="flex items-center space-x-2 px-3 py-1.5 rounded-xl text-xs font-mono border backdrop-blur-md"
            :class="isLiveBackend 
              ? 'bg-emerald-950/70 border-emerald-500/40 text-emerald-300 shadow-md shadow-emerald-950/40' 
              : 'bg-amber-950/70 border-amber-500/40 text-amber-300 shadow-md shadow-amber-950/40'"
            :title="isLiveBackend ? 'FastAPI Academic Engine Connected' : 'Local Cache Active (Backend Offline)'"
          >
            <span class="relative flex h-2.5 w-2.5">
              <span 
                class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75"
                :class="isLiveBackend ? 'bg-emerald-400' : 'bg-amber-400'"
              ></span>
              <span 
                class="relative inline-flex rounded-full h-2.5 w-2.5"
                :class="isLiveBackend ? 'bg-emerald-500' : 'bg-amber-500'"
              ></span>
            </span>
            <span class="hidden lg:inline">{{ isLiveBackend ? 'FastAPI Connected' : 'Local Cache' }}</span>
          </div>

          <!-- Add Paper CTA Button -->
          <button
            @click="emit('openAddModal')"
            class="bg-gradient-to-r from-emerald-500 via-teal-600 to-emerald-600 hover:from-emerald-400 hover:to-teal-500 text-white text-xs font-bold px-4 py-2.5 rounded-xl shadow-lg shadow-emerald-600/30 border border-emerald-400/40 transition-all transform hover:-translate-y-0.5 active:translate-y-0 flex items-center space-x-1.5"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/>
            </svg>
            <span class="hidden sm:inline">Index Study</span>
          </button>
        </div>

      </div>

      <!-- Mobile Sub-Navigation -->
      <div class="flex md:hidden overflow-x-auto py-2.5 border-t border-slate-800/80 space-x-2">
        <button
          @click="emit('update:activeTab', 'papers')"
          :class="[
            'px-3.5 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all',
            activeTab === 'papers' ? 'bg-emerald-600 text-white font-semibold' : 'text-slate-400 bg-slate-900 border border-slate-800'
          ]"
        >
          Index ({{ totalPapers }})
        </button>
        <button
          @click="emit('update:activeTab', 'taxonomy')"
          :class="[
            'px-3.5 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all',
            activeTab === 'taxonomy' ? 'bg-emerald-600 text-white font-semibold' : 'text-slate-400 bg-slate-900 border border-slate-800'
          ]"
        >
          Taxonomy ({{ totalTags }})
        </button>
        <button
          @click="emit('update:activeTab', 'matrix')"
          :class="[
            'px-3.5 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all',
            activeTab === 'matrix' ? 'bg-emerald-600 text-white font-semibold' : 'text-slate-400 bg-slate-900 border border-slate-800'
          ]"
        >
          Matrix
        </button>
        <button
          @click="emit('update:activeTab', 'bio')"
          :class="[
            'px-3.5 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all',
            activeTab === 'bio' ? 'bg-emerald-600 text-white font-semibold' : 'text-slate-400 bg-slate-900 border border-slate-800'
          ]"
        >
          Bio
        </button>
      </div>
    </div>
  </header>
</template>
