<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import type { ResearchPaper, NewResearchPaperInput } from './types';
import { 
  fetchResearchPapers, 
  createResearchPaper, 
  checkAcademicBackendHealth
} from './services/api';
import { useTheme } from './composables/useTheme';

// Components
import AuthorSection from './components/AuthorSection.vue';
import UdemyCourses from './components/UdemyCourses.vue';
import ContactForm from './components/ContactForm.vue';

// Ported Academic Components
import ResearchPaperCard from './components/ResearchPaperCard.vue';
import TaxonomyView from './components/TaxonomyView.vue';
import PaperDetailModal from './components/PaperDetailModal.vue';
import AddPaperModal from './components/AddPaperModal.vue';
import AdminLoginModal from './components/AdminLoginModal.vue';

// Navigation State
const activeTab = ref<'research' | 'taxonomy' | 'matrix' | 'courses' | 'about'>('courses');

// Academic Research State
const papers = ref<ResearchPaper[]>([]);
const isLiveBackend = ref(false);
const isLoadingResearch = ref(true);
const searchQuery = ref('');
const selectedTagSlug = ref<string | null>(null);
const selectedPaper = ref<ResearchPaper | null>(null);
const isAddModalOpen = ref(false);

// Admin Auth State
const isAdmin = ref(sessionStorage.getItem('academic_admin') === 'true');
const isAdminModalOpen = ref(false);
const isUserMenuOpen = ref(false);
const userMenuContainer = ref<HTMLElement | null>(null);

const { theme, toggleTheme } = useTheme();



function handleAdminLogin(passkey: string) {
  if (passkey) {
    isAdmin.value = true;
    sessionStorage.setItem('academic_admin', 'true');
    isAdminModalOpen.value = false;
  }
}

function handleAdminLogout() {
  isAdmin.value = false;
  sessionStorage.removeItem('academic_admin');
}

const allTags = computed(() => {
  const tagMap = new Map<string, { name: string; slug: string }>();
  for (const paper of papers.value) {
    if (paper.tags) {
      for (const tag of paper.tags) {
        const slug = tag.slug || tag.name.toLowerCase().replace(/\s+/g, '-');
        tagMap.set(slug, { name: tag.name, slug });
      }
    }
  }
  return Array.from(tagMap.values());
});

const filteredPapers = computed(() => {
  return papers.value.filter(paper => {
    if (selectedTagSlug.value) {
      const hasTag = paper.tags?.some(t => (t.slug || t.name.toLowerCase().replace(/\s+/g, '-')) === selectedTagSlug.value);
      if (!hasTag) return false;
    }
    if (searchQuery.value.trim()) {
      const q = searchQuery.value.toLowerCase().trim();
      const titleMatch = paper.title.toLowerCase().includes(q);
      const authorsMatch = paper.authors.toLowerCase().includes(q);
      const abstractMatch = paper.abstract?.toLowerCase().includes(q) ?? false;
      const methodologyMatch = paper.methodology?.toLowerCase().includes(q) ?? false;
      return titleMatch || authorsMatch || abstractMatch || methodologyMatch;
    }
    return true;
  });
});

async function loadData() {
  isLoadingResearch.value = true;
  isLiveBackend.value = await checkAcademicBackendHealth();
  const res = await fetchResearchPapers();
  papers.value = res.papers;
  isLiveBackend.value = res.isLiveBackend;
  isLoadingResearch.value = false;
}

async function handleAddPaper(input: NewResearchPaperInput) {
  const result = await createResearchPaper(input);
  papers.value.unshift(result.paper);
  isAddModalOpen.value = false;
  selectedPaper.value = result.paper;
}

function handleFilterTag(slug: string) {
  if (selectedTagSlug.value === slug) {
    selectedTagSlug.value = null;
  } else {
    selectedTagSlug.value = slug;
    activeTab.value = 'research';
  }
}

function handleClickOutside(event: MouseEvent) {
  if (userMenuContainer.value && !userMenuContainer.value.contains(event.target as Node)) {
    isUserMenuOpen.value = false;
  }
}

onMounted(() => {
  loadData();
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 font-sans selection:bg-blue-600 selection:text-white pb-16 transition-colors duration-300">
    <!-- Premium Refined Navbar -->
    <header class="sticky top-0 z-40 backdrop-blur-xl bg-white/85 dark:bg-slate-950/85 border-b border-slate-200 dark:border-blue-500/20 shadow-2xl transition-colors duration-300">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        
        <!-- High-Tech Brand & Header Title -->
        <div class="flex items-center space-x-3 group cursor-pointer" @click="activeTab = 'courses'">
          <!-- Brand Typography -->
          <div>
            <div class="flex items-center space-x-2">
              <span class="font-extrabold text-lg sm:text-xl tracking-tight text-slate-900 dark:text-white group-hover:text-cyan-600 dark:group-hover:text-cyan-300 transition-colors">
                JEREMY <span class="bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-600 dark:from-blue-400 dark:via-indigo-300 dark:to-cyan-400 bg-clip-text text-transparent">LANKFORD</span>
              </span>
            </div>
            <div class="flex items-center space-x-2 text-xs text-slate-500 dark:text-slate-400 leading-none pt-1">
              <span>Software Architect & PhD Student</span>
            </div>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <nav class="hidden lg:flex items-center space-x-1 bg-slate-100 dark:bg-slate-900/90 p-1 rounded-xl border border-slate-200 dark:border-slate-800 shadow-inner">

          <button
            @click="activeTab = 'research'"
            :class="[
              'px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all duration-200 flex items-center space-x-1.5',
              activeTab === 'research'
                ? 'bg-gradient-to-r from-blue-600 to-indigo-700 text-white shadow-md shadow-blue-600/30 border border-blue-400/30'
                : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200/80 dark:hover:bg-slate-800/80'
            ]"
          >
            <span>Research Index</span>
            <span class="px-1.5 py-0.2 text-[9px] font-mono rounded bg-blue-50 dark:bg-slate-950/60 text-blue-800 dark:text-cyan-300 border border-blue-300 dark:border-blue-500/30">{{ papers.length }}</span>
          </button>
          <button
            @click="activeTab = 'matrix'"
            :class="[
              'px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all duration-200',
              activeTab === 'matrix'
                ? 'bg-gradient-to-r from-blue-600 to-indigo-700 text-white shadow-md shadow-blue-600/30 border border-blue-400/30'
                : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200/80 dark:hover:bg-slate-800/80'
            ]"
          >
            Synthesis Matrix
          </button>
          <button
            @click="activeTab = 'courses'"
            :class="[
              'px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all duration-200',
              activeTab === 'courses'
                ? 'bg-gradient-to-r from-blue-600 to-indigo-700 text-white shadow-md shadow-blue-600/30 border border-blue-400/30'
                : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200/80 dark:hover:bg-slate-800/80'
            ]"
          >
            Udemy Courses
          </button>
          <button
            @click="activeTab = 'taxonomy'"
            :class="[
              'px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all duration-200 flex items-center space-x-1.5',
              activeTab === 'taxonomy'
                ? 'bg-gradient-to-r from-blue-600 to-indigo-700 text-white shadow-md shadow-blue-600/30 border border-blue-400/30'
                : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200/80 dark:hover:bg-slate-800/80'
            ]"
          >
            <span>Taxonomy</span>
            <span class="px-1.5 py-0.2 text-[9px] font-mono rounded bg-blue-50 dark:bg-slate-950/60 text-blue-800 dark:text-cyan-300 border border-blue-300 dark:border-blue-500/30">{{ allTags.length }}</span>
          </button>
          <button
            @click="activeTab = 'about'"
            :class="[
              'px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all duration-200',
              activeTab === 'about'
                ? 'bg-gradient-to-r from-blue-600 to-indigo-700 text-white shadow-md shadow-blue-600/30 border border-blue-400/30'
                : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200/80 dark:hover:bg-slate-800/80'
            ]"
          >
            About & Bio
          </button>
        </nav>

        <!-- Right Side Nav Actions -->
        <div class="flex items-center space-x-3">
          <!-- Add Paper CTA Button (ADMIN / AUTHENTICATED ONLY) -->
          <button
            v-if="isAdmin && activeTab === 'research'"
            @click="isAddModalOpen = true"
            class="bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-700 hover:from-blue-500 hover:to-indigo-500 text-white text-[11px] font-bold px-2.5 py-1 rounded-lg shadow-sm shadow-blue-600/20 border border-blue-400/40 transition-all transform hover:-translate-y-0.5 active:translate-y-0 flex items-center space-x-1 leading-tight"
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
              class="relative flex items-center justify-center w-8 h-8 rounded-full border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-900 text-amber-500 dark:text-amber-400 hover:scale-105 hover:border-cyan-500/50 transition-all shadow-sm cursor-pointer"
              :title="theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
              aria-label="Toggle Dark / Light Theme"
            >
              <svg v-if="theme === 'dark'" class="w-4 h-4 transform rotate-0 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
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
                  isUserMenuOpen || activeTab === 'about'
                    ? 'border-blue-500 ring-2 ring-blue-500/30 bg-blue-50 dark:bg-blue-950/40'
                    : 'border-slate-300 dark:border-slate-800 hover:border-blue-500/50 hover:bg-slate-200/80 dark:hover:bg-slate-800/80'
                ]"
                title="User Menu & Profile Options"
                aria-label="Open User Menu"
              >
                <img
                  src="/jeremy-lankford.jpg"
                  alt="Jeremy Lankford"
                  class="w-7 h-7 rounded-full object-cover ring-1.5 ring-blue-400/50 transition-transform"
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
                  <div class="text-[9px] font-mono text-blue-600 dark:text-cyan-400">PhD in IT (AI Focus) Student</div>
                </div>

                <!-- Menu Options -->
                <div class="py-1.5 text-xs font-medium">
                  <!-- Account & Profile -->
                  <button 
                    @click="activeTab = 'about'; isUserMenuOpen = false;"
                    class="w-full px-4 py-2 text-left hover:bg-slate-100 dark:hover:bg-slate-800/80 flex items-center space-x-2.5 text-slate-700 dark:text-slate-200 transition-colors"
                  >
                    <svg class="w-4 h-4 text-blue-600 dark:text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
                    <span class="text-[10px] font-mono capitalize text-blue-700 dark:text-cyan-400 bg-blue-50 dark:bg-blue-950 px-2 py-0.5 rounded border border-blue-300 dark:border-blue-500/30">
                      {{ theme }} mode
                    </span>
                  </button>

                  <!-- Direct Hub Social Link shortcuts -->
                  <div class="border-t border-slate-100 dark:border-slate-800 pt-1.5 mt-1 pb-1">
                    <div class="px-4 py-1 text-[9px] font-mono text-slate-400 uppercase tracking-wider">Social Contacts</div>
                    <a href="http://www.linkedin.com/in/jwlankford" target="_blank" class="px-4 py-1.5 hover:bg-slate-100 dark:hover:bg-slate-800/80 flex items-center space-x-2.5 text-slate-700 dark:text-slate-300 transition-colors">
                      <svg class="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
                      <span>LinkedIn</span>
                    </a>
                    <a href="https://x.com/jwlankford" target="_blank" class="px-4 py-1.5 hover:bg-slate-100 dark:hover:bg-slate-800/80 flex items-center space-x-2.5 text-slate-700 dark:text-slate-300 transition-colors">
                      <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                      <span>X (Twitter)</span>
                    </a>
                    <a href="https://www.udemy.com/user/jeremy-lankford-22/" target="_blank" class="px-4 py-1.5 hover:bg-slate-100 dark:hover:bg-slate-800/80 flex items-center space-x-2.5 text-slate-700 dark:text-slate-300 transition-colors">
                      <svg class="w-3.5 h-3.5 text-indigo-500" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 15c-2.76 0-5-2.24-5-5V7h2v5c0 1.66 1.34 3 3 3s3-1.34 3-3V7h2v5c0 2.76-2.24 5-5 5z"/>
                      </svg>
                      <span>Udemy Profile</span>
                    </a>
                  </div>
                </div>

                <div class="border-t border-slate-100 dark:border-slate-800 pt-1.5">
                  <!-- Admin Auth / Logout Button -->
                  <button 
                    v-if="isAdmin"
                    @click="handleAdminLogout(); isUserMenuOpen = false;"
                    class="w-full px-4 py-2 text-left hover:bg-rose-50 dark:hover:bg-rose-950/50 flex items-center space-x-2.5 text-rose-600 dark:text-rose-400 transition-colors"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                    </svg>
                    <span>Log Out (Lock Admin)</span>
                  </button>

                  <button 
                    v-else
                    @click="isAdminModalOpen = true; isUserMenuOpen = false;"
                    class="w-full px-4 py-2 text-left hover:bg-slate-100 dark:hover:bg-slate-800/80 flex items-center space-x-2.5 text-slate-700 dark:text-slate-300 transition-colors"
                  >
                    <svg class="w-4 h-4 text-blue-600 dark:text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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

      <!-- Mobile Tabs Sub-Navigation -->
      <div class="flex lg:hidden overflow-x-auto py-2 px-4 border-t border-slate-200 dark:border-slate-800/80 space-x-2">

        <button
          @click="activeTab = 'research'"
          :class="[
            'px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition-all',
            activeTab === 'research' ? 'bg-blue-600 text-white font-semibold' : 'text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800'
          ]"
        >
          Research Index ({{ papers.length }})
        </button>
        <button
          @click="activeTab = 'matrix'"
          :class="[
            'px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition-all',
            activeTab === 'matrix' ? 'bg-blue-600 text-white font-semibold' : 'text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800'
          ]"
        >
          Matrix
        </button>
        <button
          @click="activeTab = 'courses'"
          :class="[
            'px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition-all',
            activeTab === 'courses' ? 'bg-blue-600 text-white font-semibold' : 'text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800'
          ]"
        >
          Udemy Courses
        </button>
        <button
          @click="activeTab = 'taxonomy'"
          :class="[
            'px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition-all',
            activeTab === 'taxonomy' ? 'bg-blue-600 text-white font-semibold' : 'text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800'
          ]"
        >
          Taxonomy ({{ allTags.length }})
        </button>
        <button
          @click="activeTab = 'about'"
          :class="[
            'px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition-all',
            activeTab === 'about' ? 'bg-blue-600 text-white font-semibold' : 'text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800'
          ]"
        >
          Bio
        </button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
      
      <!-- TAB 2: RESEARCH INDEX VIEW -->
      <div v-if="activeTab === 'research'" class="space-y-6 animate-fadeIn">
        <!-- Search & Tag Chips Bar -->
        <div class="bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 p-4 sm:p-6 rounded-2xl shadow-xl space-y-4 transition-colors">
          <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
            <!-- Search Bar -->
            <div class="relative w-full sm:max-w-md">
              <svg class="w-5 h-5 text-slate-400 absolute left-3.5 top-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
              <input 
                v-model="searchQuery"
                type="text"
                placeholder="Search by title, author, findings, or methodology..."
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700/80 rounded-xl pl-10 pr-4 py-2.5 text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors shadow-inner"
              />
              <button 
                v-if="searchQuery"
                @click="searchQuery = ''"
                class="absolute right-3 top-3 text-slate-400 hover:text-slate-700 dark:hover:text-white"
              >
                ✕
              </button>
            </div>

            <!-- Active Tag Filter Badge / Counter -->
            <div class="flex items-center space-x-3 text-xs font-mono text-slate-500 dark:text-slate-400">
              <span>Showing <strong class="text-blue-600 dark:text-cyan-400">{{ filteredPapers.length }}</strong> of {{ papers.length }} Studies</span>
              <button 
                v-if="selectedTagSlug || searchQuery"
                @click="selectedTagSlug = null; searchQuery = '';"
                class="text-amber-700 dark:text-amber-400 hover:underline px-2 py-1 bg-amber-50 dark:bg-amber-950/50 border border-amber-300 dark:border-amber-500/30 rounded"
              >
                Clear Filters
              </button>
            </div>
          </div>

          <!-- Tag Chips -->
          <div v-if="allTags.length" class="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-200 dark:border-slate-800/80">
            <span class="text-xs font-mono text-slate-500 dark:text-slate-400 mr-1">Taxonomy Filter:</span>
            <button
              @click="selectedTagSlug = null"
              :class="[
                'text-xs px-3 py-1 rounded-full font-mono transition-all',
                !selectedTagSlug ? 'bg-blue-600 text-white font-semibold' : 'bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-400 hover:bg-slate-300 dark:hover:bg-slate-700'
              ]"
            >
              All Topics
            </button>
            <button
              v-for="tag in allTags"
              :key="tag.slug"
              @click="handleFilterTag(tag.slug)"
              :class="[
                'text-xs px-3 py-1 rounded-full font-mono transition-all',
                selectedTagSlug === tag.slug
                  ? 'bg-blue-600 text-white font-semibold shadow-md shadow-blue-600/30'
                  : 'bg-slate-100 dark:bg-slate-800/80 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-700/60'
              ]"
            >
              #{{ tag.name }}
            </button>
          </div>
        </div>

        <!-- Papers Grid -->
        <div v-if="isLoadingResearch" class="py-16 text-center text-slate-500 dark:text-slate-400 font-mono">
          <div class="animate-spin w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          Synchronizing Research Database...
        </div>

        <div v-else-if="filteredPapers.length === 0" class="py-16 text-center bg-white dark:bg-slate-900/40 rounded-2xl border border-slate-200 dark:border-slate-800">
          <p class="text-slate-600 dark:text-slate-400 font-medium mb-3">No research studies match your current search criteria.</p>
          <button 
            @click="selectedTagSlug = null; searchQuery = '';"
            class="text-xs font-mono px-4 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-blue-600 dark:text-cyan-400 rounded-lg border border-slate-300 dark:border-slate-700"
          >
            Reset Filters
          </button>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ResearchPaperCard
            v-for="paper in filteredPapers"
            :key="paper.id || paper.title"
            :paper="paper"
            @select="selectedPaper = $event"
            @filterTag="handleFilterTag"
          />
        </div>
      </div>

      <!-- TAB 3: TAXONOMY VIEW -->
      <TaxonomyView
        v-else-if="activeTab === 'taxonomy'"
        :papers="papers"
        @selectTag="handleFilterTag"
      />

      <!-- TAB 4: SYNTHESIS MATRIX VIEW -->
      <div v-else-if="activeTab === 'matrix'" class="space-y-6 animate-fadeIn">
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 rounded-2xl shadow-xl transition-colors">
          <h2 class="text-2xl font-bold font-serif text-slate-900 dark:text-white mb-2">Literature Synthesis Matrix</h2>
          <p class="text-slate-600 dark:text-slate-400 text-sm mb-6">Cross-paper methodology comparison and empirical findings breakdown.</p>
          
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs text-slate-700 dark:text-slate-300">
              <thead class="bg-slate-100 dark:bg-slate-950 font-mono text-blue-700 dark:text-cyan-400 uppercase border-b border-slate-200 dark:border-slate-800">
                <tr>
                  <th class="p-3">Paper Title & Year</th>
                  <th class="p-3">Authors</th>
                  <th class="p-3">Methodology</th>
                  <th class="p-3">Key Empirical Findings</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 dark:divide-slate-800">
                <tr v-for="paper in papers" :key="paper.id" class="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors">
                  <td class="p-3 font-semibold text-slate-900 dark:text-white font-serif max-w-xs">{{ paper.title }} ({{ paper.publication_year }})</td>
                  <td class="p-3 font-mono text-blue-700 dark:text-cyan-400/90 whitespace-nowrap">{{ paper.authors }}</td>
                  <td class="p-3 text-slate-600 dark:text-slate-400">{{ paper.methodology || 'Empirical Study' }}</td>
                  <td class="p-3 text-slate-700 dark:text-slate-300">{{ paper.key_findings || 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- TAB 5: UDEMY COURSES VIEW -->
      <UdemyCourses
        v-else-if="activeTab === 'courses'"
      />

      <!-- TAB 6: ABOUT & BIO VIEW (Unified biography section with contact) -->
      <div v-else-if="activeTab === 'about'" class="space-y-12 animate-fadeIn">
        <AuthorSection />
        <ContactForm />
      </div>

    </main>

    <!-- Footer -->
    <footer class="mt-20 border-t border-slate-200 dark:border-slate-900 pt-8 pb-4 text-center text-xs font-mono text-slate-500 dark:text-slate-500 space-y-4">
      <div class="flex items-center justify-center space-x-6">
        <a 
          href="http://www.linkedin.com/in/jwlankford" 
          target="_blank" 
          rel="noopener noreferrer"
          class="hover:text-blue-600 dark:hover:text-blue-400 flex items-center space-x-1.5 transition-colors"
        >
          <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 24 24">
            <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
          </svg>
          <span>LinkedIn</span>
        </a>

        <a 
          href="https://x.com/jwlankford" 
          target="_blank" 
          rel="noopener noreferrer"
          class="hover:text-cyan-600 dark:hover:text-cyan-400 flex items-center space-x-1.5 transition-colors text-slate-600 dark:text-slate-300"
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
          class="hover:text-blue-600 dark:hover:text-blue-400 flex items-center space-x-1.5 transition-colors"
        >
          <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 24 24">
            <path d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H7.5v-3H10V9.69c0-2.47 1.47-3.83 3.72-3.83 1.08 0 2.2.19 2.2.19v2.42h-1.24c-1.23 0-1.61.76-1.61 1.54V12h2.73l-.44 3h-2.29v6.8c4.56-.93 8-4.96 8-9.8z"/>
          </svg>
          <span>Facebook</span>
        </a>

        <a 
          href="https://www.udemy.com/user/jeremy-lankford-22/" 
          target="_blank" 
          rel="noopener noreferrer"
          class="hover:text-indigo-600 dark:hover:text-indigo-400 flex items-center space-x-1.5 transition-colors"
        >
          <svg class="w-4 h-4 text-indigo-500" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 15c-2.76 0-5-2.24-5-5V7h2v5c0 1.66 1.34 3 3 3s3-1.34 3-3V7h2v5c0 2.76-2.24 5-5 5z"/>
          </svg>
          <span>Udemy</span>
        </a>
      </div>
      <p>© 2026 Jeremy Lankford. Consolidated Domain Workspace (jeremylankford.com)</p>
    </footer>

    <!-- Modals -->
    <PaperDetailModal
      :paper="selectedPaper"
      @close="selectedPaper = null"
      @filterTag="handleFilterTag"
    />

    <AddPaperModal
      :isOpen="isAddModalOpen"
      @close="isAddModalOpen = false"
      @submit="handleAddPaper"
    />

    <AdminLoginModal
      :isOpen="isAdminModalOpen"
      @close="isAdminModalOpen = false"
      @login="handleAdminLogin"
    />
  </div>
</template>