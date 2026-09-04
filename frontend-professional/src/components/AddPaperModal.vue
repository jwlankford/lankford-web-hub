<script setup lang="ts">
import { ref } from 'vue';
import type { NewResearchPaperInput } from '../types';

import RichTextEditor from './RichTextEditor.vue';

defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'submit', input: NewResearchPaperInput): void;
  (e: 'bibtexSubmit', bibtex: string): void;
}>();

const title = ref('');
const authors = ref('Lankford, J. W.');
const publication_year = ref(new Date().getFullYear());
const journal_or_conf = ref('');
const abstract = ref('');
const key_findings = ref('');
const methodology = ref('');
const zotero_key = ref('');
const url = ref('');

const isSubmitting = ref(false);
const tagsString = ref('');

const bibtexInput = ref('');
const isImporting = ref(false);
const importMessage = ref('');
const importError = ref(false);

function handleBibtexImport() {
  if (!bibtexInput.value.trim()) {
    importError.value = true;
    importMessage.value = 'Please paste BibTeX first.';
    return;
  }
  isImporting.value = true;
  importError.value = false;
  importMessage.value = '';
  emit('bibtexSubmit', bibtexInput.value);
  
  // Fake a small delay to simulate processing so UI feels responsive
  setTimeout(() => {
    isImporting.value = false;
  }, 500);
}

function handleSubmit() {
  if (!title.value.trim() || !authors.value.trim()) return;

  const parsedTags = tagsString.value
    .split('#')
    .map(t => t.trim())
    .filter(Boolean);

  isSubmitting.value = true;
  emit('submit', {
    title: title.value.trim(),
    authors: authors.value.trim(),
    publication_year: Number(publication_year.value),
    journal_or_conf: journal_or_conf.value.trim() || undefined,
    abstract: abstract.value.trim() || undefined,
    key_findings: key_findings.value.trim() || undefined,
    methodology: methodology.value.trim() || undefined,
    zotero_key: zotero_key.value.trim() || undefined,
    url: url.value.trim() || undefined,
    tags: parsedTags.length ? parsedTags : undefined
  });

  // Reset form
  title.value = '';
  abstract.value = '';
  key_findings.value = '';
  methodology.value = '';
  journal_or_conf.value = '';
  zotero_key.value = '';
  url.value = '';
  tagsString.value = '';
  isSubmitting.value = false;
}
</script>

<template>
  <Teleport to="body">
    <div 
      v-if="isOpen"
      class="fixed inset-0 z-50 overflow-y-auto bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4 sm:p-6"
      @click.self="emit('close')"
    >
      <div class="relative bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700/80 rounded-2xl shadow-2xl max-w-2xl w-full p-6 sm:p-8 text-slate-900 dark:text-slate-100 transition-colors">
        <!-- Header -->
        <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-4 mb-6">
          <div>
            <h2 class="text-xl font-bold font-serif text-slate-900 dark:text-white flex items-center space-x-2">
              <span class="w-3 h-3 rounded-full bg-blue-500 inline-block"></span>
              <span>Index New Research Study</span>
            </h2>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Submit paper metadata to the Lankford Academic Domain Index</p>
          </div>
          <button 
            @click="emit('close')"
            class="text-slate-400 hover:text-slate-700 dark:hover:text-white bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 p-2 rounded-full transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4 text-sm max-h-[70vh] overflow-y-auto pr-1">
          <!-- Bulk Import BibTeX -->
          <div class="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800/80 space-y-3 mb-4">
            <div class="flex items-center justify-between">
              <span class="text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 font-mono font-bold">Bulk Import (BibTeX)</span>
              <span class="text-[10px] text-blue-650 dark:text-cyan-400 font-mono font-semibold">Zotero Support</span>
            </div>
            <div class="flex flex-col space-y-2">
              <textarea 
                v-model="bibtexInput"
                rows="4"
                placeholder="Paste BibTeX entries here to import multiple papers..."
                class="w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500 text-xs font-mono"
              ></textarea>
              <button
                type="button"
                @click="handleBibtexImport"
                :disabled="isImporting"
                class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-semibold shadow-sm transition-colors text-xs flex items-center justify-center min-w-[120px] disabled:bg-emerald-600/60 self-end"
              >
                <span v-if="isImporting">Importing...</span>
                <span v-else>Parse & Import</span>
              </button>
              <p v-if="importMessage" :class="importError ? 'text-red-500 dark:text-red-400' : 'text-emerald-500 dark:text-emerald-400'" class="text-xs font-medium font-sans">
                {{ importMessage }}
              </p>
            </div>
          </div>
          
          <div class="relative flex py-2 items-center">
             <div class="flex-grow border-t border-slate-200 dark:border-slate-700"></div>
             <span class="flex-shrink-0 mx-4 text-slate-400 text-xs font-mono">OR MANUAL ENTRY</span>
             <div class="flex-grow border-t border-slate-200 dark:border-slate-700"></div>
          </div>
          <div>
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Paper Title *</label>
            <input 
              v-model="title"
              type="text"
              required
              placeholder="e.g. Deterministic Verification in Autonomous LLM Workflows"
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <!-- Authors & Year Row -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="sm:col-span-2">
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Authors *</label>
              <input 
                v-model="authors"
                type="text"
                required
                placeholder="Lankford, J. W.; Smith, A."
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
              />
            </div>
            <div>
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Publication Year *</label>
              <input 
                v-model.number="publication_year"
                type="number"
                min="1990"
                max="2030"
                required
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <!-- Journal / Conf & Zotero -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Journal / Conference</label>
              <input 
                v-model="journal_or_conf"
                type="text"
                placeholder="IEEE TSE / ACM CCS"
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
              />
            </div>
            <div>
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Zotero Reference Key</label>
              <input 
                v-model="zotero_key"
                type="text"
                placeholder="LANKFORD_2026_GOVERNANCE"
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500 font-mono text-xs"
              />
            </div>
          </div>

          <!-- URL Link -->
          <div>
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Article / Publication Link (URL)</label>
            <input 
              v-model="url"
              type="url"
              placeholder="https://www.linkedin.com/pulse/..."
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500 font-mono text-xs"
            />
          </div>

          <!-- Abstract Summary (Rich Text) -->
          <div>
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Abstract Summary</label>
            <RichTextEditor 
              v-model="abstract"
              placeholder="Summary of research problem, methodology, and primary conclusions..."
            />
          </div>

          <!-- Key Findings & Methodology (Rich Text) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Key Empirical Findings</label>
              <RichTextEditor 
                v-model="key_findings"
                placeholder="e.g. Reduced execution branching error by 98.4%"
              />
            </div>
            <div>
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Methodology</label>
              <RichTextEditor 
                v-model="methodology"
                placeholder="e.g. Empirical Benchmark & Load Simulation"
              />
            </div>
          </div>

          <!-- TAGS Input (Hashtag formatted string) -->
          <div>
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">TAGS (Hashtag format)</label>
            <input 
              v-model="tagsString"
              type="text"
              placeholder="e.g. #AI #SoftwareEngineering #Automation"
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500 font-mono text-xs"
            />
          </div>

          <!-- Submit Controls -->
          <div class="pt-4 border-t border-slate-200 dark:border-slate-800 flex justify-end space-x-3">
            <button 
              type="button"
              @click="emit('close')"
              class="px-4 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg font-semibold transition-colors text-xs"
            >
              Cancel
            </button>
            <button 
              type="submit"
              :disabled="isSubmitting"
              class="px-5 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-semibold shadow-md shadow-blue-600/30 transition-all text-xs flex items-center space-x-1.5"
            >
              <span v-if="isSubmitting">Indexing...</span>
              <span v-else>Commit to Index</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>
