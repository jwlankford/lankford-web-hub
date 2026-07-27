<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import type { ResearchPaper, NewResearchPaperInput, Article, NewArticleInput, GoogleNotebook, JupyterNotebook, NewGoogleNotebookInput, NewJupyterNotebookInput } from './types';
import { 
  fetchResearchPapers, 
  createResearchPaper, 
  checkAcademicBackendHealth,
  fetchArticles,
  createArticle,
  fetchGoogleNotebooks,
  createGoogleNotebook,
  fetchJupyterNotebooks,
  createJupyterNotebook
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

// Article Components
import ArticleCard from './components/ArticleCard.vue';
import ArticleDetailModal from './components/ArticleDetailModal.vue';
import AddArticleModal from './components/AddArticleModal.vue';

// Notebook Components
import GoogleNotebookCard from './components/GoogleNotebookCard.vue';
import JupyterNotebookCard from './components/JupyterNotebookCard.vue';
import AddNotebookModal from './components/AddNotebookModal.vue';


// Navigation State
const activeTab = ref<'research' | 'taxonomy' | 'matrix' | 'courses' | 'about' | 'articles'>('courses');

// Technologies Known
const technologies = [
  { name: 'Python', icon: 'https://cdn.simpleicons.org/python/3776AB' },
  { name: 'TypeScript', icon: 'https://cdn.simpleicons.org/typescript/3178C6' },
  { name: 'Vue.js', icon: 'https://cdn.simpleicons.org/vuedotjs/4FC08D' },
  { name: 'React', icon: 'https://cdn.simpleicons.org/react/61DAFB' },
  { name: 'Node.js', icon: 'https://cdn.simpleicons.org/nodedotjs/339933' },
  { name: 'PostgreSQL', icon: 'https://cdn.simpleicons.org/postgresql/4169E1' },
  { name: 'Docker', icon: 'https://cdn.simpleicons.org/docker/2496ED' },
  { name: 'Kubernetes', icon: 'https://cdn.simpleicons.org/kubernetes/326CE5' },
  { name: 'Tailwind CSS', icon: 'https://cdn.simpleicons.org/tailwindcss/06B6D4' },
  { name: 'Git', icon: 'https://cdn.simpleicons.org/git/F05032' }
];

// GitHub Repositories
const githubRepos = [
  {
    name: 'agentic-sdlc-framework',
    description: 'Multi-agent orchestration framework for automating the Software Development Life Cycle processes with LLMs.',
    url: 'https://github.com/jwlankford/agentic-sdlc-framework',
    language: 'Python',
    languageColor: 'bg-blue-500',
    stars: 124
  },
  {
    name: 'lankford-web-hub',
    description: 'Frontend professional portfolio showcasing academic research, courses, and interactive experiences.',
    url: 'https://github.com/jwlankford/lankford-web-hub',
    language: 'Vue',
    languageColor: 'bg-emerald-500',
    stars: 42
  },
  {
    name: 'crown-clothing',
    description: 'Enterprise-grade e-commerce clothing application featuring React, Redux state management, Firebase authentication, and Stripe payment integration.',
    url: 'https://github.com/jwlankford/crown-clothing',
    language: 'React',
    languageColor: 'bg-cyan-500',
    stars: 34
  },
  {
    name: 'typescript-ast-metaprogramming',
    description: 'Introspection-guided AST refactoring techniques for automated enterprise legacy scaling.',
    url: 'https://github.com/jwlankford/typescript-ast-metaprogramming',
    language: 'TypeScript',
    languageColor: 'bg-blue-600',
    stars: 56
  }
];


// Article State
const articles = ref<Article[]>([]);
const isLoadingArticles = ref(true);
const selectedArticle = ref<Article | null>(null);
const isAddArticleModalOpen = ref(false);

// Academic Research State
const papers = ref<ResearchPaper[]>([]);
const isLiveBackend = ref(false);
const isLoadingResearch = ref(true);
const searchQuery = ref('');
const selectedTagSlug = ref<string | null>(null);
const showTaxonomyFilters = ref(false);
const selectedPaper = ref<ResearchPaper | null>(null);
const isAddModalOpen = ref(false);

// Notebooks State
const googleNotebooks = ref<GoogleNotebook[]>([]);
const jupyterNotebooks = ref<JupyterNotebook[]>([]);
const isGoogleNotebooksExpanded = ref(false);
const isJupyterNotebooksExpanded = ref(false);
const isAddNotebookModalOpen = ref(false);
const isLoadingNotebooks = ref(true);
const jupyterViewMode = ref<'grid' | 'feed'>('grid');
const activeFeedNotebook = ref<JupyterNotebook | null>(null);



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

const filteredArticles = computed(() => {
  if (!searchQuery.value.trim()) return articles.value;
  const q = searchQuery.value.toLowerCase().trim();
  return articles.value.filter(article => {
    return article.title.toLowerCase().includes(q) || 
           article.summary.toLowerCase().includes(q) || 
           (article.content?.toLowerCase().includes(q) ?? false);
  });
});

async function loadData() {
  isLoadingResearch.value = true;
  isLoadingArticles.value = true;
  isLoadingNotebooks.value = true;
  isLiveBackend.value = await checkAcademicBackendHealth();
  
  // Papers
  const res = await fetchResearchPapers();
  papers.value = res.papers;
  isLiveBackend.value = res.isLiveBackend;
  isLoadingResearch.value = false;

  // Articles
  const artRes = await fetchArticles();
  articles.value = artRes.articles;
  isLoadingArticles.value = false;

  // Notebooks
  const gbookRes = await fetchGoogleNotebooks();
  googleNotebooks.value = gbookRes.notebooks;
  const jbookRes = await fetchJupyterNotebooks();
  jupyterNotebooks.value = jbookRes.notebooks;
  if (jupyterNotebooks.value.length > 0) {
    activeFeedNotebook.value = jupyterNotebooks.value[0];
  }
  isLoadingNotebooks.value = false;
}

async function handleAddNotebook(type: 'google' | 'jupyter', payload: NewGoogleNotebookInput | NewJupyterNotebookInput) {
  if (type === 'google') {
    const res = await createGoogleNotebook(payload as NewGoogleNotebookInput);
    googleNotebooks.value.unshift(res.notebook);
  } else {
    const res = await createJupyterNotebook(payload as NewJupyterNotebookInput);
    jupyterNotebooks.value.unshift(res.notebook);
    activeFeedNotebook.value = res.notebook;
  }
  isAddNotebookModalOpen.value = false;
}



async function handleAddPaper(input: NewResearchPaperInput) {
  const result = await createResearchPaper(input);
  papers.value.unshift(result.paper);
  isAddModalOpen.value = false;
  selectedPaper.value = result.paper;
}

async function handleAddArticle(input: NewArticleInput) {
  const result = await createArticle(input);
  articles.value.unshift(result.article);
  isAddArticleModalOpen.value = false;
  selectedArticle.value = result.article;
}


function handleFilterTag(slug: string) {
  if (selectedTagSlug.value === slug) {
    selectedTagSlug.value = null;
  } else {
    selectedTagSlug.value = slug;
    activeTab.value = 'research';
    showTaxonomyFilters.value = true;
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
            @click="activeTab = 'articles'"
            :class="[
              'px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all duration-200 flex items-center space-x-1.5',
              activeTab === 'articles'
                ? 'bg-gradient-to-r from-blue-600 to-indigo-700 text-white shadow-md shadow-blue-600/30 border border-blue-400/30'
                : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200/80 dark:hover:bg-slate-800/80'
            ]"
          >
            <span>Articles</span>
            <span class="px-1.5 py-0.2 text-[9px] font-mono rounded bg-blue-50 dark:bg-slate-950/60 text-blue-800 dark:text-cyan-300 border border-blue-300 dark:border-blue-500/30">{{ articles.length }}</span>
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
            class="bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-700 hover:from-blue-500 hover:to-indigo-500 text-white text-[11px] font-bold px-2.5 py-1 rounded-lg shadow-sm shadow-blue-600/20 border border-blue-400/40 transition-all transform hover:-translate-y-0.5 active:translate-y-0 flex items-center space-x-1 leading-tight cursor-pointer"
            title="Index a new study to your database"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/>
            </svg>
            <span class="hidden sm:inline">Index Study</span>
          </button>

          <!-- Index Notebook CTA Button -->
          <button
            v-if="isAdmin && activeTab === 'research'"
            @click="isAddNotebookModalOpen = true"
            class="bg-gradient-to-r from-amber-500 via-orange-650 to-amber-600 hover:from-amber-450 hover:to-orange-550 text-white text-[11px] font-bold px-2.5 py-1 rounded-lg shadow-sm shadow-amber-600/20 border border-amber-400/40 transition-all transform hover:-translate-y-0.5 active:translate-y-0 flex items-center space-x-1 leading-tight cursor-pointer"
            title="Index a new Google NotebookLM or Jupyter Notebook"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/>
            </svg>
            <span class="hidden sm:inline">Index Notebook</span>
          </button>


          <!-- Publish Article CTA Button -->
          <button
            v-if="isAdmin && activeTab === 'articles'"
            @click="isAddArticleModalOpen = true"
            class="bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-700 hover:from-blue-500 hover:to-indigo-500 text-white text-[11px] font-bold px-2.5 py-1 rounded-lg shadow-sm shadow-blue-600/20 border border-blue-400/40 transition-all transform hover:-translate-y-0.5 active:translate-y-0 flex items-center space-x-1 leading-tight cursor-pointer"
            title="Publish a new article"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"/>
            </svg>
            <span class="hidden sm:inline">Publish Article</span>
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
                  src="/jeremy-lankford.png"
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
                    <a href="https://github.com/jwlankford" target="_blank" class="px-4 py-1.5 hover:bg-slate-100 dark:hover:bg-slate-800/80 flex items-center space-x-2.5 text-slate-700 dark:text-slate-300 transition-colors">
                      <svg class="w-3.5 h-3.5 text-slate-900 dark:text-slate-100" fill="currentColor" viewBox="0 0 24 24">
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
                      </svg>
                      <span>GitHub</span>
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
          @click="activeTab = 'articles'"
          :class="[
            'px-3 py-1 rounded-lg text-xs font-medium whitespace-nowrap transition-all',
            activeTab === 'articles' ? 'bg-blue-600 text-white font-semibold' : 'text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800'
          ]"
        >
          Articles ({{ articles.length }})
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
        <!-- Dashboard Widgets Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Google NotebookLM Card Widget -->
          <button 
            @click="isGoogleNotebooksExpanded = !isGoogleNotebooksExpanded; if(isGoogleNotebooksExpanded) isJupyterNotebooksExpanded = false;"
            :class="[
              'text-left p-5 rounded-2xl border transition-all duration-300 relative overflow-hidden group cursor-pointer shadow-md hover:shadow-lg',
              isGoogleNotebooksExpanded 
                ? 'bg-gradient-to-br from-blue-50 to-indigo-50/50 dark:from-blue-950/40 dark:to-indigo-950/20 border-blue-550 dark:border-blue-400 ring-2 ring-blue-500/20 shadow-blue-500/10' 
                : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800/80 hover:border-blue-500/40'
            ]"
          >
            <div class="absolute -bottom-6 -right-6 w-16 h-16 bg-blue-600/5 rounded-full blur-xl group-hover:scale-150 transition-transform"></div>
            <div class="flex items-start justify-between">
              <div class="space-y-1">
                <div class="text-[10px] font-mono font-bold text-blue-600 dark:text-cyan-300 uppercase tracking-widest">NotebookLM Deep-Dives</div>
                <h4 class="text-base font-serif font-bold text-slate-905 dark:text-white">Google Notebooks</h4>
                <p class="text-xs text-slate-500 dark:text-slate-400 leading-tight">AI summary overviews & podcast discussions.</p>
              </div>
              <span class="px-2.5 py-1 rounded bg-blue-100 dark:bg-blue-950 border border-blue-200 dark:border-blue-500/30 text-blue-800 dark:text-cyan-300 text-[10px] font-mono font-black shadow-inner">
                {{ googleNotebooks.length }} Links
              </span>
            </div>
            <div class="flex items-center justify-between pt-4 mt-3 border-t border-slate-105/50 dark:border-slate-800 text-[10px] font-mono text-slate-405 dark:text-slate-500">
              <span>{{ isGoogleNotebooksExpanded ? 'Click to collapse grid' : 'Click to expand grid' }}</span>
              <svg class="w-3.5 h-3.5 transform transition-transform" :class="isGoogleNotebooksExpanded ? 'rotate-180 text-blue-600' : 'rotate-0'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </div>
          </button>

          <!-- Jupyter Notebooks Card Widget -->
          <button 
            @click="isJupyterNotebooksExpanded = !isJupyterNotebooksExpanded; if(isJupyterNotebooksExpanded) isGoogleNotebooksExpanded = false;"
            :class="[
              'text-left p-5 rounded-2xl border transition-all duration-300 relative overflow-hidden group cursor-pointer shadow-md hover:shadow-lg',
              isJupyterNotebooksExpanded 
                ? 'bg-gradient-to-br from-amber-50 to-orange-50/50 dark:from-amber-950/40 dark:to-orange-950/20 border-amber-550 dark:border-amber-400 ring-2 ring-amber-500/20 shadow-amber-500/10' 
                : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800/80 hover:border-amber-500/40'
            ]"
          >
            <div class="absolute -bottom-6 -right-6 w-16 h-16 bg-amber-500/5 rounded-full blur-xl group-hover:scale-150 transition-transform"></div>
            <div class="flex items-start justify-between">
              <div class="space-y-1">
                <div class="text-[10px] font-mono font-bold text-amber-600 dark:text-amber-350 uppercase tracking-widest">Interactive Code</div>
                <h4 class="text-base font-serif font-bold text-slate-905 dark:text-white">Jupyter Notebooks</h4>
                <p class="text-xs text-slate-500 dark:text-slate-400 leading-tight">Python simulations, calculations & tests.</p>
              </div>
              <span class="px-2.5 py-1 rounded bg-amber-100 dark:bg-amber-950 border border-amber-200 dark:border-amber-500/30 text-amber-800 dark:text-amber-350 text-[10px] font-mono font-black shadow-inner">
                {{ jupyterNotebooks.length }} Files
              </span>
            </div>
            <div class="flex items-center justify-between pt-4 mt-3 border-t border-slate-105/50 dark:border-slate-800 text-[10px] font-mono text-slate-405 dark:text-slate-500">
              <span>{{ isJupyterNotebooksExpanded ? 'Click to collapse grid' : 'Click to expand grid' }}</span>
              <svg class="w-3.5 h-3.5 transform transition-transform" :class="isJupyterNotebooksExpanded ? 'rotate-180 text-amber-600' : 'rotate-0'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </div>
          </button>

          <!-- Synthesis Matrix Card Widget -->
          <button 
            @click="activeTab = 'matrix'"
            class="text-left p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800/80 hover:border-cyan-500/40 transition-all duration-300 relative overflow-hidden group cursor-pointer shadow-md hover:shadow-lg"
          >
            <div class="absolute -bottom-6 -right-6 w-16 h-16 bg-cyan-600/5 rounded-full blur-xl group-hover:scale-150 transition-transform"></div>
            <div class="flex items-start justify-between">
              <div class="space-y-1">
                <div class="text-[10px] font-mono font-bold text-cyan-600 dark:text-cyan-300 uppercase tracking-widest">Cross-Reference Literature</div>
                <h4 class="text-base font-serif font-bold text-slate-905 dark:text-white">Synthesis Matrix</h4>
                <p class="text-xs text-slate-500 dark:text-slate-400 leading-tight">Comparative analysis grid of findings & metrics.</p>
              </div>
              <span class="px-2.5 py-1 rounded bg-cyan-50 dark:bg-slate-950 border border-cyan-200 dark:border-cyan-500/30 text-cyan-800 dark:text-cyan-300 text-[10px] font-mono font-black shadow-inner">
                View Matrix
              </span>
            </div>
            <div class="flex items-center justify-between pt-4 mt-3 border-t border-slate-105/50 dark:border-slate-800 text-[10px] font-mono text-slate-405 dark:text-slate-500">
              <span>Go to Matrix page</span>
              <svg class="w-3.5 h-3.5 transform group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"/>
              </svg>
            </div>
          </button>
        </div>

        <!-- Expansion 1: Google Notebooks Grid -->
        <div 
          v-if="isGoogleNotebooksExpanded" 
          class="p-6 bg-slate-100/40 dark:bg-slate-900/30 border border-slate-200 dark:border-slate-800/80 rounded-3xl space-y-4 animate-fadeIn"
        >
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-serif font-bold text-slate-900 dark:text-white">Public Google Notebooks</h3>
            <button @click="isGoogleNotebooksExpanded = false" class="text-xs text-blue-600 dark:text-cyan-400 hover:underline">Collapse Section</button>
          </div>
          <div v-if="isLoadingNotebooks" class="py-8 text-center text-slate-400 text-xs font-mono">
            Loading Google Notebooks...
          </div>
          <div v-else-if="googleNotebooks.length === 0" class="py-8 text-center text-slate-400 text-xs font-mono">
            No public Google Notebooks found.
          </div>
          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <GoogleNotebookCard 
              v-for="notebook in googleNotebooks" 
              :key="notebook.id" 
              :notebook="notebook" 
            />
          </div>
        </div>

        <!-- Expansion 2: Jupyter Notebooks Grid & Direct Feed -->
        <div 
          v-if="isJupyterNotebooksExpanded" 
          class="p-6 bg-slate-100/40 dark:bg-slate-900/30 border border-slate-200 dark:border-slate-800/80 rounded-3xl space-y-6 animate-fadeIn"
        >
          <!-- Header and Toggle Controls -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200/60 dark:border-slate-800 pb-4">
            <div class="space-y-1">
              <h3 class="text-lg font-serif font-bold text-slate-900 dark:text-white">Interactive Google Colab Notebooks</h3>
              <p class="text-xs text-slate-500 dark:text-slate-400">Run code, evaluate models, and verify orchestration loop logic.</p>
            </div>
            
            <div class="flex items-center space-x-3 self-end sm:self-auto">
              <!-- View Mode Toggle -->
              <div class="flex items-center bg-slate-200/80 dark:bg-slate-800 p-0.5 rounded-xl text-xs font-mono border border-slate-300/40 dark:border-slate-700/30">
                <button 
                  @click="jupyterViewMode = 'grid'"
                  type="button"
                  :class="[
                    'px-3 py-1.5 rounded-lg transition-all flex items-center space-x-1.5 cursor-pointer',
                    jupyterViewMode === 'grid' 
                      ? 'bg-white dark:bg-slate-900 shadow-sm text-amber-755 dark:text-amber-400 font-bold' 
                      : 'text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-205'
                  ]"
                >
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
                  </svg>
                  <span>Grid View</span>
                </button>
                <button 
                  @click="jupyterViewMode = 'feed'"
                  type="button"
                  :class="[
                    'px-3 py-1.5 rounded-lg transition-all flex items-center space-x-1.5 cursor-pointer',
                    jupyterViewMode === 'feed' 
                      ? 'bg-white dark:bg-slate-900 shadow-sm text-amber-755 dark:text-amber-400 font-bold' 
                      : 'text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-205'
                  ]"
                >
                  <!-- Google Colab Infinity Logo -->
                  <svg class="w-3.5 h-3.5" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M13.8 12.6C12.9 9.6 10.2 7.5 7.1 7.5 3.1 7.5 0 10.6 0 14.5s3.1 7 7.1 7c3.1 0 5.8-2.1 6.7-5.1L13.8 12.6z" fill="#F9AB00" />
                    <path d="M20.5 7.5c-3.1 0-5.8 2.1-6.7 5.1l0.1 3.8c0.9 3 3.6 5.1 6.7 5.1 4 0 7.1-3.1 7.1-7s-3.1-7-7.1-7z" fill="#E8710A" />
                  </svg>
                  <span>Direct Feed</span>
                </button>
              </div>
              <button @click="isJupyterNotebooksExpanded = false" class="text-xs text-amber-600 dark:text-amber-400 hover:underline">Collapse</button>
            </div>
          </div>

          <!-- Loading & Empty States -->
          <div v-if="isLoadingNotebooks" class="py-12 text-center text-slate-400 text-xs font-mono">
            Loading Google Colab Notebooks...
          </div>
          <div v-else-if="jupyterNotebooks.length === 0" class="py-12 text-center text-slate-400 text-xs font-mono">
            No interactive Google Colab Notebooks found.
          </div>

          <!-- Grid View Render -->
          <div v-else-if="jupyterViewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 gap-6 animate-fadeIn">
            <JupyterNotebookCard 
              v-for="notebook in jupyterNotebooks" 
              :key="notebook.id" 
              :notebook="notebook" 
            />
          </div>

          <!-- Direct Feed Render (Split Panel Layout) -->
          <div v-else class="flex flex-col lg:flex-row gap-6 animate-fadeIn">
            <!-- Left Sidebar: Feed List Selector -->
            <div class="w-full lg:w-1/4 flex flex-col space-y-2 lg:max-h-[690px] lg:overflow-y-auto pr-1">
              <div class="text-[10px] font-mono font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest mb-1.5 pl-1">Available Feeds</div>
              <button 
                v-for="notebook in jupyterNotebooks"
                :key="notebook.id"
                @click="activeFeedNotebook = notebook"
                type="button"
                :class="[
                  'w-full text-left p-4 rounded-xl border transition-all duration-300 flex flex-col space-y-2 cursor-pointer relative overflow-hidden group',
                  activeFeedNotebook?.id === notebook.id 
                    ? 'bg-gradient-to-r from-amber-50 to-orange-55/50 dark:from-amber-950/30 dark:to-orange-950/10 border-amber-500 dark:border-amber-400 shadow-md ring-1 ring-amber-500/20' 
                    : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800/80 hover:border-amber-500/40 hover:bg-slate-50/50 dark:hover:bg-slate-850/50'
                ]"
              >
                <!-- Active Indicator Border -->
                <div v-if="activeFeedNotebook?.id === notebook.id" class="absolute left-0 top-0 bottom-0 w-1 bg-amber-600 dark:bg-amber-500"></div>

                <div class="flex items-center justify-between">
                  <span class="inline-flex items-center space-x-1.5 px-2 py-0.5 rounded bg-slate-105 dark:bg-slate-800/80 text-[9px] font-mono font-bold text-slate-500 dark:text-slate-400">
                    <svg class="w-2.5 h-2.5" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M13.8 12.6C12.9 9.6 10.2 7.5 7.1 7.5 3.1 7.5 0 10.6 0 14.5s3.1 7 7.1 7c3.1 0 5.8-2.1 6.7-5.1L13.8 12.6z" fill="#F9AB00" />
                      <path d="M20.5 7.5c-3.1 0-5.8 2.1-6.7 5.1l0.1 3.8c0.9 3 3.6 5.1 6.7 5.1 4 0 7.1-3.1 7.1-7s-3.1-7-7.1-7z" fill="#E8710A" />
                    </svg>
                    <span>Colab Link</span>
                  </span>
                </div>
                
                <h5 class="text-sm font-bold text-slate-900 dark:text-white leading-snug group-hover:text-amber-600 dark:group-hover:text-amber-400 transition-colors line-clamp-1">
                  {{ notebook.title }}
                </h5>
                <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed line-clamp-2">
                  {{ notebook.description }}
                </p>
              </button>
            </div>

            <!-- Right Area: Embedded Iframe & Detail Info -->
            <div class="w-full lg:w-3/4 flex flex-col space-y-4">
              <div v-if="activeFeedNotebook" class="flex flex-col bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800/80 rounded-2xl overflow-hidden shadow-lg">
                <!-- Viewport Top Header -->
                <div class="p-4 bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                  <div class="space-y-1">
                    <h4 class="text-base font-serif font-black text-slate-900 dark:text-white leading-tight">
                      {{ activeFeedNotebook.title }}
                    </h4>
                    <p class="text-xs text-slate-500 dark:text-slate-400 leading-normal">
                      {{ activeFeedNotebook.description }}
                    </p>
                  </div>

                  <a 
                    :href="activeFeedNotebook.notebook_url" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    class="px-4 py-2 font-bold text-xs rounded-xl bg-amber-600 hover:bg-amber-500 dark:bg-amber-550 dark:hover:bg-amber-450 text-white shadow-md active:scale-95 transition-all flex items-center justify-center space-x-1.5 flex-shrink-0 self-end sm:self-auto cursor-pointer"
                  >
                    <span>Open in New Tab</span>
                    <svg class="w-3.5 h-3.5 stroke-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                    </svg>
                  </a>
                </div>

                <!-- Iframe Viewport Container -->
                <div class="relative bg-slate-50 dark:bg-slate-950 p-4 flex flex-col space-y-4">
                  <!-- Fallback Alert Box -->
                  <div class="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/25 text-amber-800 dark:text-amber-300 flex items-start space-x-3 text-xs leading-relaxed">
                    <svg class="w-5 h-5 text-amber-650 dark:text-amber-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                    </svg>
                    <div>
                      <span class="font-bold">Colab Iframe Notice:</span> Due to Google's strict browser security headers (`X-Frame-Options: deny`), this direct feed represents a live container reference. If the content below displays a connection error or remains blank, click <a :href="activeFeedNotebook.notebook_url" target="_blank" rel="noopener noreferrer" class="font-bold underline hover:text-amber-900 dark:hover:text-amber-250">Open in New Tab</a> to launch it directly in Google Colab.
                    </div>
                  </div>

                  <!-- Actual Frame -->
                  <div class="w-full h-[650px] rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 overflow-hidden shadow-inner relative">
                    <iframe 
                      :src="activeFeedNotebook.notebook_url"
                      class="w-full h-full border-none"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
                    ></iframe>
                  </div>
                </div>
              </div>
              <div v-else class="h-[400px] flex items-center justify-center border border-dashed border-slate-300 dark:border-slate-800 rounded-2xl text-slate-400 text-sm font-mono">
                Select a notebook from the sidebar to load the feed.
              </div>
            </div>
          </div>
        </div>

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
                type="button"
                @click="showTaxonomyFilters = !showTaxonomyFilters"
                class="px-2 py-1 rounded text-[11px] border transition-colors flex items-center gap-1 font-mono"
                :class="[
                  showTaxonomyFilters || selectedTagSlug
                    ? 'bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-cyan-400 border-blue-200 dark:border-blue-800/60 font-semibold'
                    : 'bg-slate-50 dark:bg-slate-950 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-900'
                ]"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
                </svg>
                <span>{{ showTaxonomyFilters ? 'Hide Topics' : 'Filter by Topic' }}</span>
                <span v-if="selectedTagSlug" class="ml-0.5 px-1.5 py-0.25 bg-blue-600 dark:bg-cyan-500 text-white dark:text-slate-950 rounded-full text-[9px] font-bold">1</span>
              </button>

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
          <div v-if="allTags.length && showTaxonomyFilters" class="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-200 dark:border-slate-800/80">
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
              {{ tag.name }}
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
                  <th class="p-3 w-1/3">Paper Title & Year</th>
                  <th class="p-3 w-1/6">Authors</th>
                  <th class="p-3">Methodology</th>
                  <th class="p-3">Key Empirical Findings</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 dark:divide-slate-800">
                <tr v-for="paper in papers" :key="paper.id" class="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors align-top">
                  <td class="p-3 font-semibold text-slate-900 dark:text-white font-serif">{{ paper.title }} ({{ paper.publication_year }})</td>
                  <td class="p-3 font-mono text-blue-700 dark:text-cyan-400/90">{{ paper.authors }}</td>
                  <td class="p-3 text-slate-600 dark:text-slate-400">{{ paper.methodology || 'Empirical Study' }}</td>
                  <td class="p-3 text-slate-700 dark:text-slate-300">{{ paper.key_findings || 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- TAB 5: ARTICLES VIEW -->
      <div v-else-if="activeTab === 'articles'" class="space-y-6 animate-fadeIn">
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
                placeholder="Search articles by title or body..."
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
            
            <div class="flex items-center space-x-3 text-xs font-mono text-slate-500 dark:text-slate-400">
              <span>Showing <strong class="text-blue-600 dark:text-cyan-400">{{ filteredArticles.length }}</strong> of {{ articles.length }} Articles</span>
            </div>
          </div>
        </div>

        <div v-if="isLoadingArticles" class="py-16 text-center text-slate-500 dark:text-slate-400 font-mono">
          <div class="animate-spin w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          Synchronizing Articles Database...
        </div>

        <div v-else-if="filteredArticles.length === 0" class="py-16 text-center bg-white dark:bg-slate-900/40 rounded-2xl border border-slate-200 dark:border-slate-800">
          <p class="text-slate-600 dark:text-slate-400 font-medium mb-3">No articles match your search criteria.</p>
          <button 
            @click="searchQuery = ''"
            class="text-xs font-mono px-4 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-blue-600 dark:text-cyan-400 rounded-lg border border-slate-300 dark:border-slate-700"
          >
            Reset Filters
          </button>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ArticleCard
            v-for="article in filteredArticles"
            :key="article.id || article.title"
            :article="article"
            @select="selectedArticle = $event"
          />
        </div>
      </div>

      <!-- TAB 6: UDEMY COURSES VIEW -->
      <UdemyCourses
        v-else-if="activeTab === 'courses'"
      />

      <!-- TAB 6: ABOUT & BIO VIEW (Unified biography section with contact) -->
      <div v-else-if="activeTab === 'about'" class="space-y-6 animate-fadeIn">
        <AuthorSection />

        <!-- Technologies Moving Icons Marquee -->
        <div class="max-w-4xl mx-auto w-full space-y-4">
          <div class="text-center md:text-left">
            <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-cyan-300 text-xs font-mono border border-blue-300 dark:border-blue-500/30">
              <span>TECHNICAL STACK</span>
            </span>
            <h3 class="text-xl font-bold font-serif text-slate-900 dark:text-white mt-2">Core Competencies & Technologies</h3>
          </div>
          
          <div class="relative w-full overflow-hidden bg-slate-100/50 dark:bg-slate-900/30 py-6 border border-slate-200 dark:border-slate-800 rounded-3xl transition-colors">
            <!-- Fade gradients -->
            <div class="absolute inset-y-0 left-0 w-16 bg-gradient-to-r from-white dark:from-slate-950 to-transparent z-10 pointer-events-none"></div>
            <div class="absolute inset-y-0 right-0 w-16 bg-gradient-to-l from-white dark:from-slate-950 to-transparent z-10 pointer-events-none"></div>

            <div class="animate-marquee space-x-6">
              <!-- Double the array to allow continuous looping -->
              <div 
                v-for="(tech, idx) in [...technologies, ...technologies]" 
                :key="tech.name + '-' + idx"
                class="inline-flex items-center space-x-2.5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 px-4 py-2.5 rounded-2xl shadow-sm hover:border-blue-500/30 dark:hover:border-blue-500/30 hover:shadow transition-all transform hover:-translate-y-0.5 select-none"
              >
                <img :src="tech.icon" class="w-5 h-5 shrink-0" :alt="tech.name" />
                <span class="text-xs font-mono font-bold text-slate-800 dark:text-slate-200">{{ tech.name }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- GitHub Projects Section -->
        <div class="max-w-4xl mx-auto w-full space-y-4 pt-4">
          <div class="text-center md:text-left">
            <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-cyan-300 text-xs font-mono border border-slate-300 dark:border-slate-700">
              <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
              </svg>
              <span>OPEN SOURCE</span>
            </span>
            <h3 class="text-xl font-bold font-serif text-slate-900 dark:text-white mt-2">App Development & Projects</h3>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <a 
              v-for="repo in githubRepos" 
              :key="repo.name"
              :href="repo.url"
              target="_blank"
              rel="noopener noreferrer"
              class="group block bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-5 rounded-2xl shadow-sm hover:shadow-md hover:border-blue-300 dark:hover:border-slate-700 transition-all text-left"
            >
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center space-x-2">
                  <svg class="w-5 h-5 text-slate-700 dark:text-slate-300 group-hover:text-blue-600 dark:group-hover:text-cyan-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                  <h4 class="font-bold text-slate-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-cyan-400 transition-colors">{{ repo.name }}</h4>
                </div>
                <div class="flex items-center space-x-1 text-slate-500 font-mono text-xs">
                  <svg class="w-3.5 h-3.5" viewBox="0 0 16 16" fill="currentColor">
                    <path fill-rule="evenodd" d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"></path>
                  </svg>
                  <span>{{ repo.stars }}</span>
                </div>
              </div>
              <p class="text-sm text-slate-600 dark:text-slate-400 mb-4 line-clamp-2">{{ repo.description }}</p>
              <div class="flex items-center space-x-3 text-xs font-mono">
                <span class="flex items-center space-x-1">
                  <span class="w-2.5 h-2.5 rounded-full" :class="repo.languageColor"></span>
                  <span class="text-slate-600 dark:text-slate-400">{{ repo.language }}</span>
                </span>
              </div>
            </a>
          </div>
        </div>

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
          href="https://github.com/jwlankford" 
          target="_blank" 
          rel="noopener noreferrer"
          class="hover:text-slate-900 dark:hover:text-slate-100 flex items-center space-x-1.5 transition-colors text-slate-650 dark:text-slate-305"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
          </svg>
          <span>GitHub</span>
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

    <ArticleDetailModal
      :article="selectedArticle"
      @close="selectedArticle = null"
    />

    <AddArticleModal
      :isOpen="isAddArticleModalOpen"
      @close="isAddArticleModalOpen = false"
      @submit="handleAddArticle"
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

    <AddNotebookModal
      :isOpen="isAddNotebookModalOpen"
      @close="isAddNotebookModalOpen = false"
      @submit="handleAddNotebook"
    />
  </div>
</template>