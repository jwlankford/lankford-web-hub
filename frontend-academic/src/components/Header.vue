<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useTheme } from '../composables/useTheme';

defineProps<{
  activeTab: 'papers' | 'taxonomy' | 'matrix' | 'bio';
  isLiveBackend: boolean;
  totalPapers: number;
  totalTags: number;
  isAdmin: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:activeTab', tab: 'papers' | 'taxonomy' | 'matrix' | 'bio'): void;
  (e: 'openAddModal'): void;
  (e: 'openAdminModal'): void;
  (e: 'logoutAdmin'): void;
}>();

const { theme, toggleTheme } = useTheme();
const isUserMenuOpen = ref(false);
const userMenuContainer = ref<HTMLElement | null>(null);

function handleClickOutside(event: MouseEvent) {
  if (userMenuContainer.value && !userMenuContainer.value.contains(event.target as Node)) {
    isUserMenuOpen.value = false;
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<template>
  <header class="sticky top-0 z-40 backdrop-blur-xl bg-white/90 dark:bg-slate-950/90 border-b border-slate-200 dark:border-emerald-500/20 shadow-xl text-slate-900 dark:text-slate-100 transition-colors duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-14 sm:h-16">
        
        <!-- Premium Academic Brand Typography -->
        <div class="flex items-center space-x-2.5 group cursor-pointer" @click="emit('update:activeTab', 'papers')">
          <!-- Brand Typography -->
          <div>
            <div class="flex items-center space-x-1.5">
              <span class="font-serif font-bold text-base tracking-tight text-slate-900 dark:text-white group-hover:text-emerald-600 dark:group-hover:text-emerald-300 transition-colors leading-none">
                LANKFORD <span class="text-emerald-600 dark:text-emerald-400 font-sans font-extrabold text-sm">ACADEMIA</span>
              </span>
              <span class="text-[9px] px-1.5 py-0.2 rounded-full font-mono bg-emerald-100 dark:bg-emerald-950/90 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-500/40 uppercase tracking-widest hidden sm:inline-block">
                PhD Candidate
              </span>
            </div>
            <div class="flex items-center space-x-1.5 text-[10px] text-slate-500 dark:text-slate-400 leading-none pt-0.5">
              <span class="font-mono text-emerald-700 dark:text-emerald-400/90">jwlankford.com</span>
              <span class="text-slate-400 dark:text-slate-600">•</span>
              <span class="hidden md:inline">Deterministic AI Governance & Systems</span>
            </div>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <nav class="hidden md:flex items-center space-x-1 bg-slate-100 dark:bg-slate-900/90 p-1 rounded-xl border border-slate-200 dark:border-slate-800 shadow-inner">
          <button
            @click="emit('update:activeTab', 'papers')"
            :class="[
              'px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all duration-200 flex items-center space-x-1.5',
              activeTab === 'papers'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-md shadow-emerald-600/30 border border-emerald-400/30'
                : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200/80 dark:hover:bg-slate-800/80'
            ]"
          >
            <span>Research Index</span>
            <span class="px-1.5 py-0.2 text-[9px] font-mono rounded bg-emerald-100 dark:bg-slate-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-500/30">{{ totalPapers }}</span>
          </button>
          <button
            @click="emit('update:activeTab', 'taxonomy')"
            :class="[
              'px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all duration-200 flex items-center space-x-1.5',
              activeTab === 'taxonomy'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-md shadow-emerald-600/30 border border-emerald-400/30'
                : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200/80 dark:hover:bg-slate-800/80'
            ]"
          >
            <span>Taxonomy</span>
            <span class="px-1.5 py-0.2 text-[9px] font-mono rounded bg-emerald-100 dark:bg-slate-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-500/30">{{ totalTags }}</span>
          </button>
          <button
            @click="emit('update:activeTab', 'matrix')"
            :class="[
              'px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all duration-200',
              activeTab === 'matrix'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-md shadow-emerald-600/30 border border-emerald-400/30'
                : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200/80 dark:hover:bg-slate-800/80'
            ]"
          >
            Synthesis Matrix
          </button>
          <button
            @click="emit('update:activeTab', 'bio')"
            :class="[
              'px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all duration-200',
              activeTab === 'bio'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-md shadow-emerald-600/30 border border-emerald-400/30'
                : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200/80 dark:hover:bg-slate-800/80'
            ]"
          >
            About & Bio
          </button>
        </nav>

        <!-- Right Side Actions & Status -->
        <div class="flex items-center space-x-2">
          
          <!-- Add Paper CTA Button (ADMIN / AUTHENTICATED ONLY) -->
          <button
            v-if="isAdmin"
            @click="emit('openAddModal')"
            class="bg-gradient-to-r from-emerald-500 via-teal-600 to-emerald-600 hover:from-emerald-400 hover:to-teal-500 text-white text-[11px] font-bold px-2.5 py-1 rounded-lg shadow-sm shadow-emerald-600/20 border border-emerald-400/40 transition-all transform hover:-translate-y-0.5 active:translate-y-0 flex items-center space-x-1 leading-tight"
            title="Index a new study to your database"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/>
            </svg>
            <span class="hidden sm:inline">Index Study</span>
          </button>

          <!-- Grouped Icons: Dark/Light Toggle, Backend Status Icon, Avatar Icon with Dropdown Menu -->
          <div class="flex items-center space-x-1.5 pl-1 border-l border-slate-200 dark:border-slate-800">
            <!-- Dark / Light Theme Toggle Button -->
            <button
              @click="toggleTheme"
              class="relative flex items-center justify-center w-8 h-8 rounded-full border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-900 text-amber-500 dark:text-amber-400 hover:scale-105 hover:border-emerald-500/50 transition-all shadow-sm cursor-pointer"
              :title="theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
              aria-label="Toggle Dark / Light Theme"
            >
              <!-- Sun Icon (for Dark Mode) -->
              <svg v-if="theme === 'dark'" class="w-4 h-4 transform rotate-0 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              <!-- Moon Icon (for Light Mode) -->
              <svg v-else class="w-4 h-4 text-indigo-600 transform rotate-0 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
            </button>

            <!-- Backend Connection Status Icon -->
            <div 
              class="relative flex items-center justify-center w-8 h-8 rounded-full border backdrop-blur-md cursor-help transition-all shadow-sm"
              :class="isLiveBackend 
                ? 'bg-emerald-50 dark:bg-emerald-950/70 border-emerald-300 dark:border-emerald-500/40 text-emerald-700 dark:text-emerald-300' 
                : 'bg-amber-50 dark:bg-amber-950/70 border-amber-300 dark:border-amber-500/40 text-amber-700 dark:text-amber-300'"
              :title="isLiveBackend ? 'FastAPI Engine Connected (Database Live)' : 'Local Cache Active (Backend Offline)'"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s-8-1.79-8-4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"/>
              </svg>
              <span class="absolute -top-0.5 -right-0.5 flex h-2 w-2">
                <span 
                  class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75"
                  :class="isLiveBackend ? 'bg-emerald-400' : 'bg-amber-400'"
                ></span>
                <span 
                  class="relative inline-flex rounded-full h-2 w-2"
                  :class="isLiveBackend ? 'bg-emerald-500' : 'bg-amber-500'"
                ></span>
              </span>
            </div>

            <!-- Profile Avatar Chip Icon & User Dropdown Menu -->
            <div ref="userMenuContainer" class="relative">
              <button
                @click="isUserMenuOpen = !isUserMenuOpen"
                class="flex items-center justify-center p-0.5 rounded-full bg-slate-100 dark:bg-slate-900/90 border transition-all duration-200 group shadow-sm hover:scale-105 cursor-pointer"
                :class="[
                  isUserMenuOpen || activeTab === 'bio'
                    ? 'border-emerald-500 ring-2 ring-emerald-500/30 bg-emerald-50 dark:bg-emerald-950/40'
                    : 'border-slate-300 dark:border-slate-800 hover:border-emerald-500/50 hover:bg-slate-200/80 dark:hover:bg-slate-800/80'
                ]"
                title="User Menu & Profile Options"
                aria-label="Open User Menu"
              >
                <img
                  src="/jeremy-lankford.jpg"
                  alt="JW Lankford"
                  class="w-7 h-7 rounded-full object-cover ring-1.5 ring-emerald-400/50 transition-transform"
                />
              </button>

              <!-- Dropdown Menu -->
              <div 
                v-if="isUserMenuOpen"
                class="absolute right-0 mt-2 w-60 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl py-2 z-50 animate-fadeIn text-slate-900 dark:text-slate-100"
              >
                <!-- User Header Info -->
                <div class="px-4 py-2.5 border-b border-slate-100 dark:border-slate-800">
                  <div class="text-xs font-bold font-serif text-slate-900 dark:text-white">Jeremy W. Lankford</div>
                  <div class="text-[10px] font-mono text-emerald-700 dark:text-emerald-400">PhD Candidate & Researcher</div>
                </div>

                <!-- Menu Options -->
                <div class="py-1.5 text-xs font-medium">
                  <!-- Account & Profile -->
                  <button 
                    @click="emit('update:activeTab', 'bio'); isUserMenuOpen = false;"
                    class="w-full px-4 py-2 text-left hover:bg-slate-100 dark:hover:bg-slate-800/80 flex items-center space-x-2.5 text-slate-700 dark:text-slate-200 transition-colors"
                  >
                    <svg class="w-4 h-4 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                    </svg>
                    <span>Account & Bio</span>
                  </button>

                  <!-- Preferences / Theme -->
                  <button 
                    @click="toggleTheme();"
                    class="w-full px-4 py-2 text-left hover:bg-slate-100 dark:hover:bg-slate-800/80 flex items-center justify-between text-slate-700 dark:text-slate-200 transition-colors"
                  >
                    <div class="flex items-center space-x-2.5">
                      <svg class="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      </svg>
                      <span>Preferences</span>
                    </div>
                    <span class="text-[10px] font-mono capitalize text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950 px-2 py-0.5 rounded border border-emerald-300 dark:border-emerald-500/30">
                      {{ theme }} mode
                    </span>
                  </button>
                </div>

                <!-- Social Contacts Section -->
                <div class="border-t border-slate-100 dark:border-slate-800 pt-1.5 pb-1">
                  <div class="px-4 py-1 text-[10px] font-mono text-slate-400 dark:text-slate-500 uppercase tracking-wider">
                    Social Contacts
                  </div>
                  <a 
                    href="http://www.linkedin.com/in/jwlankford" 
                    target="_blank"
                    rel="noopener noreferrer"
                    class="px-4 py-1.5 hover:bg-slate-100 dark:hover:bg-slate-800/80 flex items-center space-x-2.5 text-slate-700 dark:text-slate-200 transition-colors"
                  >
                    <svg class="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
                    </svg>
                    <span>LinkedIn</span>
                  </a>
                  <a 
                    href="https://x.com/jwlankford" 
                    target="_blank"
                    rel="noopener noreferrer"
                    class="px-4 py-1.5 hover:bg-slate-100 dark:hover:bg-slate-800/80 flex items-center space-x-2.5 text-slate-700 dark:text-slate-200 transition-colors"
                  >
                    <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                    </svg>
                    <span>X (Twitter)</span>
                  </a>
                  <a 
                    href="https://www.facebook.com/profile.php?id=61591720403485" 
                    target="_blank"
                    rel="noopener noreferrer"
                    class="px-4 py-1.5 hover:bg-slate-100 dark:hover:bg-slate-800/80 flex items-center space-x-2.5 text-slate-700 dark:text-slate-200 transition-colors"
                  >
                    <svg class="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H7.5v-3H10V9.69c0-2.47 1.47-3.83 3.72-3.83 1.08 0 2.2.19 2.2.19v2.42h-1.24c-1.23 0-1.61.76-1.61 1.54V12h2.73l-.44 3h-2.29v6.8c4.56-.93 8-4.96 8-9.8z"/>
                    </svg>
                    <span>Facebook</span>
                  </a>
                </div>

                <div class="border-t border-slate-100 dark:border-slate-800 pt-1.5">
                  <!-- Admin Auth / Logout Button -->
                  <button 
                    v-if="isAdmin"
                    @click="emit('logoutAdmin'); isUserMenuOpen = false;"
                    class="w-full px-4 py-2 text-left hover:bg-rose-50 dark:hover:bg-rose-950/50 flex items-center space-x-2.5 text-rose-600 dark:text-rose-400 transition-colors"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                    </svg>
                    <span>Log Out (Lock Admin)</span>
                  </button>

                  <button 
                    v-else
                    @click="emit('openAdminModal'); isUserMenuOpen = false;"
                    class="w-full px-4 py-2 text-left hover:bg-slate-100 dark:hover:bg-slate-800/80 flex items-center space-x-2.5 text-slate-700 dark:text-slate-300 transition-colors"
                  >
                    <svg class="w-4 h-4 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                    </svg>
                    <span>Author Login</span>
                  </button>
                </div>
              </div>
            </div>

          </div>

        </div>

      </div>

      <!-- Mobile Sub-Navigation -->
      <div class="flex md:hidden overflow-x-auto py-2 border-t border-slate-200 dark:border-slate-800/80 space-x-2">
        <button
          @click="emit('update:activeTab', 'papers')"
          :class="[
            'px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition-all',
            activeTab === 'papers' ? 'bg-emerald-600 text-white font-semibold' : 'text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800'
          ]"
        >
          Index ({{ totalPapers }})
        </button>
        <button
          @click="emit('update:activeTab', 'taxonomy')"
          :class="[
            'px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition-all',
            activeTab === 'taxonomy' ? 'bg-emerald-600 text-white font-semibold' : 'text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800'
          ]"
        >
          Taxonomy ({{ totalTags }})
        </button>
        <button
          @click="emit('update:activeTab', 'matrix')"
          :class="[
            'px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition-all',
            activeTab === 'matrix' ? 'bg-emerald-600 text-white font-semibold' : 'text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800'
          ]"
        >
          Matrix
        </button>
        <button
          @click="emit('update:activeTab', 'bio')"
          :class="[
            'px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition-all',
            activeTab === 'bio' ? 'bg-emerald-600 text-white font-semibold' : 'text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800'
          ]"
        >
          Bio
        </button>
      </div>
    </div>
  </header>
</template>
