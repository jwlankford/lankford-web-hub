<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import type { ResearchPaper, NewResearchPaperInput } from './types';
import { fetchResearchPapers, createResearchPaper, checkBackendHealth } from './services/api';
import Header from './components/Header.vue';
import ResearchPaperCard from './components/ResearchPaperCard.vue';
import PaperDetailModal from './components/PaperDetailModal.vue';
import AddPaperModal from './components/AddPaperModal.vue';
import TaxonomyView from './components/TaxonomyView.vue';
import AuthorBio from './components/AuthorBio.vue';

const activeTab = ref<'papers' | 'taxonomy' | 'matrix' | 'bio'>('papers');
const papers = ref<ResearchPaper[]>([]);
const isLiveBackend = ref(false);
const isLoading = ref(true);

const searchQuery = ref('');
const selectedTagSlug = ref<string | null>(null);
const selectedPaper = ref<ResearchPaper | null>(null);
const isAddModalOpen = ref(false);

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
    // Tag match
    if (selectedTagSlug.value) {
      const hasTag = paper.tags?.some(t => (t.slug || t.name.toLowerCase().replace(/\s+/g, '-')) === selectedTagSlug.value);
      if (!hasTag) return false;
    }
    // Search query match
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
  isLoading.value = true;
  isLiveBackend.value = await checkBackendHealth();
  const res = await fetchResearchPapers();
  papers.value = res.papers;
  isLiveBackend.value = res.isLiveBackend;
  isLoading.value = false;
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
    activeTab.value = 'papers';
  }
}

onMounted(() => {
  loadData();
});
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-emerald-500 selection:text-white pb-16">
    <!-- Navigation & Header -->
    <Header
      :activeTab="activeTab"
      @update:activeTab="activeTab = $event"
      :isLiveBackend="isLiveBackend"
      :totalPapers="papers.length"
      :totalTags="allTags.length"
      @openAddModal="isAddModalOpen = true"
    />

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
      
      <!-- TAB 1: RESEARCH INDEX VIEW -->
      <div v-if="activeTab === 'papers'" class="space-y-6">
        <!-- Search & Tag Chips Bar -->
        <div class="bg-slate-900/80 border border-slate-800 p-4 sm:p-6 rounded-2xl shadow-xl space-y-4">
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
                class="w-full bg-slate-950 border border-slate-700/80 rounded-xl pl-10 pr-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition-colors shadow-inner"
              />
              <button 
                v-if="searchQuery"
                @click="searchQuery = ''"
                class="absolute right-3 top-3 text-slate-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            <!-- Active Tag Filter Badge / Counter -->
            <div class="flex items-center space-x-3 text-xs font-mono text-slate-400">
              <span>Showing <strong class="text-emerald-400">{{ filteredPapers.length }}</strong> of {{ papers.length }} Studies</span>
              <button 
                v-if="selectedTagSlug || searchQuery"
                @click="selectedTagSlug = null; searchQuery = '';"
                class="text-amber-400 hover:underline px-2 py-1 bg-amber-950/50 border border-amber-500/30 rounded"
              >
                Clear Filters
              </button>
            </div>
          </div>

          <!-- Tag Chips -->
          <div v-if="allTags.length" class="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-800/80">
            <span class="text-xs font-mono text-slate-400 mr-1">Taxonomy Filter:</span>
            <button
              @click="selectedTagSlug = null"
              :class="[
                'text-xs px-3 py-1 rounded-full font-mono transition-all',
                !selectedTagSlug ? 'bg-emerald-600 text-white font-semibold' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
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
                  ? 'bg-emerald-600 text-white font-semibold shadow-md shadow-emerald-600/30'
                  : 'bg-slate-800/80 text-slate-300 hover:bg-slate-700 border border-slate-700/60'
              ]"
            >
              #{{ tag.name }}
            </button>
          </div>
        </div>

        <!-- Papers Grid -->
        <div v-if="isLoading" class="py-16 text-center text-slate-400 font-mono">
          <div class="animate-spin w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          Synchronizing Research Database...
        </div>

        <div v-else-if="filteredPapers.length === 0" class="py-16 text-center bg-slate-900/40 rounded-2xl border border-slate-800">
          <p class="text-slate-400 font-medium mb-3">No research studies match your current search criteria.</p>
          <button 
            @click="selectedTagSlug = null; searchQuery = '';"
            class="text-xs font-mono px-4 py-2 bg-slate-800 hover:bg-slate-700 text-emerald-400 rounded-lg border border-slate-700"
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

      <!-- TAB 2: TAXONOMY VIEW -->
      <TaxonomyView
        v-else-if="activeTab === 'taxonomy'"
        :papers="papers"
        @selectTag="handleFilterTag"
      />

      <!-- TAB 3: SYNTHESIS MATRIX VIEW -->
      <div v-else-if="activeTab === 'matrix'" class="space-y-6 animate-fadeIn">
        <div class="bg-slate-900 border border-slate-800 p-8 rounded-2xl">
          <h2 class="text-2xl font-bold font-serif text-white mb-2">Literature Synthesis Matrix</h2>
          <p class="text-slate-400 text-sm mb-6">Cross-paper methodology comparison and empirical findings breakdown.</p>
          
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs text-slate-300">
              <thead class="bg-slate-950 font-mono text-emerald-400 uppercase border-b border-slate-800">
                <tr>
                  <th class="p-3">Paper Title & Year</th>
                  <th class="p-3">Authors</th>
                  <th class="p-3">Methodology</th>
                  <th class="p-3">Key Empirical Findings</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-800">
                <tr v-for="paper in papers" :key="paper.id" class="hover:bg-slate-800/40">
                  <td class="p-3 font-semibold text-white font-serif max-w-xs">{{ paper.title }} ({{ paper.publication_year }})</td>
                  <td class="p-3 font-mono text-emerald-400/90 whitespace-nowrap">{{ paper.authors }}</td>
                  <td class="p-3 text-slate-400">{{ paper.methodology || 'Empirical Study' }}</td>
                  <td class="p-3 text-slate-300">{{ paper.key_findings || 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- TAB 4: AUTHOR BIO & RESEARCH STATEMENT -->
      <AuthorBio v-else-if="activeTab === 'bio'" />

    </main>

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
  </div>
</template>