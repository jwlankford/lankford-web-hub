<script setup lang="ts">
import { ref, watch } from 'vue';
import type { ResearchPaper, NewResearchPaperInput } from '../types';
import { useAuth } from '../composables/useAuth';
import { updateResearchPaper } from '../services/api';
import RichTextEditor from './RichTextEditor.vue';

const props = defineProps<{
  paper: ResearchPaper | null;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'filterTag', tagSlug: string): void;
  (e: 'updated', paper: ResearchPaper): void;
}>();

const { isAdmin } = useAuth();

const isCopied = ref(false);
const isEditing = ref(false);
const isSaving = ref(false);

const draft = ref({
  title: '',
  authors: '',
  publication_year: new Date().getFullYear(),
  journal_or_conf: '',
  zotero_key: '',
  url: '',
  image_url: '',
  abstract: '',
  key_findings: '',
  methodology: '',
  used_for: '',
  tagsString: ''
});

function resetDraft(paper: ResearchPaper | null) {
  if (!paper) return;
  draft.value = {
    title: paper.title || '',
    authors: paper.authors || '',
    publication_year: paper.publication_year || new Date().getFullYear(),
    journal_or_conf: paper.journal_or_conf || '',
    zotero_key: paper.zotero_key || '',
    url: paper.url || '',
    image_url: paper.image_url || '',
    abstract: paper.abstract || '',
    key_findings: paper.key_findings || '',
    methodology: paper.methodology || '',
    used_for: paper.used_for || '',
    tagsString: (paper.tags || []).map(t => t.name).join(', ')
  };
}

// Keep the draft in sync whenever a new paper is opened, and exit edit mode.
watch(() => props.paper, (paper) => {
  isEditing.value = false;
  resetDraft(paper);
}, { immediate: true });

function startEditing() {
  resetDraft(props.paper);
  isEditing.value = true;
}

function cancelEditing() {
  resetDraft(props.paper);
  isEditing.value = false;
}

async function saveEditing() {
  if (!props.paper?.id) return;
  if (!draft.value.title.trim() || !draft.value.authors.trim()) return;

  const parsedTags = draft.value.tagsString
    .split(',')
    .map(t => t.trim())
    .filter(Boolean);

  try {
    isSaving.value = true;
    const payload: Partial<NewResearchPaperInput> = {
      title: draft.value.title.trim(),
      authors: draft.value.authors.trim(),
      publication_year: Number(draft.value.publication_year),
      journal_or_conf: draft.value.journal_or_conf.trim() || undefined,
      zotero_key: draft.value.zotero_key.trim() || undefined,
      url: draft.value.url.trim() || undefined,
      image_url: draft.value.image_url.trim() || undefined,
      abstract: draft.value.abstract.trim() || undefined,
      key_findings: draft.value.key_findings.trim() || undefined,
      methodology: draft.value.methodology.trim() || undefined,
      used_for: draft.value.used_for.trim() || undefined,
      tags: parsedTags.length ? parsedTags : undefined
    };
    const { paper } = await updateResearchPaper(props.paper.id, payload);
    emit('updated', paper);
    isEditing.value = false;
  } catch (e: any) {
    alert('Error saving paper: ' + e.message);
  } finally {
    isSaving.value = false;
  }
}

function handleClose() {
  isEditing.value = false;
  emit('close');
}

function copyToClipboard(text: string) {
  navigator.clipboard.writeText(text).then(() => {
    isCopied.value = true;
    setTimeout(() => {
      isCopied.value = false;
    }, 2000);
  });
}
</script>

<template>
  <div 
    v-if="paper"
    class="relative w-full max-w-5xl mx-auto text-slate-900 dark:text-slate-100 transition-colors flex flex-col animate-fadeIn"
  >
    <!-- Background Decorative Gradient -->
    <div class="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -z-0 pointer-events-none"></div>

    <!-- Back button -->
    <button
      @click="handleClose"
      class="flex items-center space-x-2 text-sm font-mono text-slate-500 dark:text-slate-400 hover:text-blue-700 dark:hover:text-cyan-300 mb-4 cursor-pointer relative z-10 w-fit"
      title="Back to research papers"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
      </svg>
      <span>Back to Research Papers</span>
    </button>

        <!-- Paper Cover Image (Above Title) -->
        <div v-if="!isEditing">
          <div v-if="paper.image_url" class="relative overflow-hidden rounded-xl mb-4 border border-slate-200 dark:border-slate-800 shadow-md">
            <img 
              :src="paper.image_url" 
              :alt="paper.title"
              class="w-full h-52 sm:h-72 object-cover"
            />
          </div>
        </div>
        <div v-else class="mb-4">
          <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Cover Image URL</label>
          <input 
            v-model="draft.image_url"
            type="url"
            placeholder="https://images.unsplash.com/..."
            class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
        </div>

        <!-- Header Controls -->
        <div class="flex items-start justify-between border-b border-slate-200 dark:border-slate-800 pb-4 mb-6 relative z-10">
          <div class="flex-1 min-w-0 pr-4">
            <div v-if="!isEditing" class="flex items-center space-x-2 text-xs font-mono text-blue-700 dark:text-cyan-400 mb-1">
              <span class="px-2 py-0.5 rounded bg-blue-100 dark:bg-blue-950 border border-blue-300 dark:border-blue-500/30">
                Year: {{ paper.publication_year }}
              </span>
              <span v-if="paper.journal_or_conf" class="text-slate-500 dark:text-slate-400">• {{ paper.journal_or_conf }}</span>
            </div>
            <div v-else class="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-2">
              <input 
                v-model.number="draft.publication_year"
                type="number"
                min="1990"
                max="2030"
                class="sm:col-span-1 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-900 dark:text-slate-100 focus:outline-none focus:border-blue-500"
                placeholder="Year"
              />
              <input 
                v-model="draft.journal_or_conf"
                type="text"
                class="sm:col-span-2 bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
                placeholder="Journal / Conference"
              />
            </div>
            <h2 v-if="!isEditing" class="text-xl sm:text-3xl font-bold font-serif text-slate-900 dark:text-white leading-tight">
              {{ paper.title }}
            </h2>
            <input
              v-else
              v-model="draft.title"
              type="text"
              placeholder="Paper Title"
              class="w-full text-xl sm:text-2xl font-bold font-serif bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-white focus:outline-none focus:border-blue-500"
            />
          </div>
          <div class="flex items-center space-x-2 ml-4 flex-shrink-0 mt-1 sm:mt-0">
            <button 
              v-if="isAdmin && !isEditing"
              @click="startEditing"
              class="text-slate-500 dark:text-slate-300 hover:text-blue-700 dark:hover:text-cyan-300 bg-slate-100 dark:bg-slate-800 hover:bg-blue-100 dark:hover:bg-blue-900/50 p-2 rounded-full transition-colors cursor-pointer"
              title="Edit paper"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </button>
            <button 
              @click="handleClose"
              class="text-slate-400 hover:text-slate-700 dark:hover:text-white bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 p-2 rounded-full transition-colors cursor-pointer"
              title="Close modal"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="space-y-6 text-sm relative z-10 flex-1">
          <!-- Authors & Metadata -->
          <div v-if="!isEditing" class="bg-slate-50 dark:bg-slate-800/50 p-4 rounded-xl border border-slate-200 dark:border-slate-700/50 space-y-2">
            <div>
              <span class="text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 font-mono">Authors</span>
              <p class="text-blue-800 dark:text-cyan-300 font-mono font-medium">{{ paper.authors }}</p>
            </div>
            <div v-if="paper.zotero_key" class="pt-2 border-t border-slate-200 dark:border-slate-700/40 flex items-center justify-between">
              <span class="text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 font-mono">Zotero Reference Key</span>
              <div class="flex items-center space-x-1.5 bg-slate-100/50 dark:bg-slate-900/60 px-2.5 py-1 rounded border border-slate-200/60 dark:border-slate-800/60 font-mono text-xs text-blue-800 dark:text-cyan-400">
                <span>{{ paper.zotero_key }}</span>
                <button 
                  type="button"
                  @click.stop="copyToClipboard(paper.zotero_key)"
                  class="text-slate-400 hover:text-blue-600 dark:hover:text-cyan-400 p-0.5 rounded transition-colors flex items-center justify-center cursor-pointer ml-1.5"
                  title="Copy Zotero Key"
                >
                  <svg v-if="!isCopied" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/>
                  </svg>
                  <svg v-else class="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                  </svg>
                </button>
              </div>
            </div>
            <div v-if="paper.url" class="pt-2 border-t border-slate-200 dark:border-slate-700/40 flex items-center justify-between">
              <span class="text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 font-mono">Article Link</span>
              <a 
                :href="paper.url"
                target="_blank"
                rel="noopener noreferrer"
                class="text-xs font-mono text-blue-700 dark:text-cyan-400 hover:underline flex items-center space-x-1 truncate max-w-sm"
              >
                <span class="truncate">{{ paper.url }}</span>
                <svg class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
              </a>
            </div>
          </div>
          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Authors</label>
              <input 
                v-model="draft.authors"
                type="text"
                placeholder="Lankford, J. W.; Smith, A."
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
              />
            </div>
            <div>
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Zotero Reference Key</label>
              <input 
                v-model="draft.zotero_key"
                type="text"
                placeholder="LANKFORD_2026_GOVERNANCE"
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500 font-mono text-xs"
              />
            </div>
            <div class="sm:col-span-2">
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Article / Publication Link (URL)</label>
              <input 
                v-model="draft.url"
                type="url"
                placeholder="https://www.linkedin.com/pulse/..."
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500 font-mono text-xs"
              />
            </div>
          </div>

          <!-- Abstract Section -->
          <div v-if="!isEditing && paper.abstract">
            <h3 class="text-xs font-mono uppercase tracking-wider text-blue-700 dark:text-cyan-400 mb-2 font-semibold">
              Abstract & Context
            </h3>
            <div class="text-slate-700 dark:text-slate-300 leading-relaxed text-base font-sans bg-slate-50 dark:bg-slate-950/40 p-4 rounded-xl border border-slate-200 dark:border-slate-800/80 prose dark:prose-invert max-w-none" v-html="paper.abstract">
            </div>
          </div>
          <div v-else-if="isEditing">
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Abstract Summary</label>
            <RichTextEditor 
              v-model="draft.abstract"
              placeholder="Summary of research problem, methodology, and primary conclusions..."
            />
          </div>

          <!-- Key Findings -->
          <div v-if="!isEditing && paper.key_findings" class="bg-blue-50 dark:bg-blue-950/30 border border-blue-300 dark:border-blue-500/30 p-4 rounded-xl">
            <h3 class="text-xs font-mono uppercase tracking-wider text-blue-800 dark:text-cyan-400 mb-2 font-semibold flex items-center space-x-1.5">
              <svg class="w-4 h-4 text-blue-600 dark:text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
              <span>Key Analytical Findings</span>
            </h3>
            <div class="text-slate-800 dark:text-slate-200 leading-relaxed font-medium prose dark:prose-invert prose-sm max-w-none" v-html="paper.key_findings">
            </div>
          </div>
          <div v-else-if="isEditing">
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Key Empirical Findings</label>
            <RichTextEditor 
              v-model="draft.key_findings"
              placeholder="e.g. Reduced execution branching error by 98.4%"
            />
          </div>

          <!-- Methodology -->
          <div v-if="!isEditing && paper.methodology">
            <h3 class="text-xs font-mono uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2 font-semibold">
              Methodology & Design Framework
            </h3>
            <div class="text-slate-700 dark:text-slate-300 bg-slate-50 dark:bg-slate-800/40 p-3 rounded-lg border border-slate-200 dark:border-slate-700/40 prose dark:prose-invert prose-sm max-w-none" v-html="paper.methodology">
            </div>
          </div>
          <div v-else-if="isEditing">
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Methodology</label>
            <RichTextEditor 
              v-model="draft.methodology"
              placeholder="e.g. Empirical Benchmark & Load Simulation"
            />
          </div>

          <!-- Used For -->
          <div v-if="!isEditing && paper.used_for">
            <h3 class="text-xs font-mono uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2 font-semibold">
              Used For
            </h3>
            <p class="text-slate-700 dark:text-slate-300 bg-slate-50 dark:bg-slate-800/40 p-3 rounded-lg border border-slate-200 dark:border-slate-700/40">
              {{ paper.used_for }}
            </p>
          </div>
          <div v-else-if="isEditing">
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Used For</label>
            <input 
              type="text"
              v-model="draft.used_for"
              placeholder="e.g. Chapter 3, App feature"
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <!-- Associated Tags -->
          <div v-if="!isEditing && paper.tags && paper.tags.length">
            <h3 class="text-xs font-mono uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2 font-semibold">
              Indexed Taxonomy Tags
            </h3>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="tag in paper.tags"
                :key="tag.slug || tag.name"
                @click="emit('filterTag', tag.slug); emit('close');"
                class="px-3 py-1 rounded-full text-xs font-mono bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-cyan-300 border border-blue-300 dark:border-blue-500/40 hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors"
              >
                {{ tag.name }}
              </button>
            </div>
          </div>
          <div v-else-if="isEditing">
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Tags (comma separated)</label>
            <input 
              v-model="draft.tagsString"
              type="text"
              placeholder="e.g. AI, Software Engineering, Automation"
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500 font-mono text-xs"
            />
          </div>
        </div>

        <!-- Footer -->
        <div class="mt-6 pt-4 border-t border-slate-200 dark:border-slate-800 flex justify-end space-x-3 relative z-10">
          <template v-if="isEditing">
            <button 
              @click="cancelEditing"
              class="px-4 py-2 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800/80 transition-colors cursor-pointer"
            >
              Cancel
            </button>
            <button 
              @click="saveEditing"
              :disabled="isSaving"
              class="px-5 py-2 bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-500 hover:to-indigo-600 disabled:opacity-50 text-white rounded-lg text-sm font-semibold shadow-md shadow-blue-600/30 transition-all flex items-center space-x-1.5 cursor-pointer"
            >
              <span v-if="isSaving" class="animate-spin h-3.5 w-3.5 border-2 border-white border-t-transparent rounded-full"></span>
              <span>{{ isSaving ? 'Saving...' : 'Save Changes' }}</span>
            </button>
          </template>
          <template v-else>
            <a
              v-if="paper.url"
              :href="paper.url"
              target="_blank"
              rel="noopener noreferrer"
              class="px-5 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-semibold shadow-md shadow-blue-600/30 transition-all flex items-center space-x-1.5"
            >
              <span>Read Article</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
              </svg>
            </a>
            <button 
              @click="handleClose"
              class="px-5 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 rounded-lg text-sm font-semibold transition-colors cursor-pointer"
            >
              Close
            </button>
          </template>
        </div>
  </div>
</template>
