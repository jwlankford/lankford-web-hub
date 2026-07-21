<script setup lang="ts">
import { ref } from 'vue';
import type { NewResearchPaperInput } from '../types';

defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'submit', input: NewResearchPaperInput): void;
}>();

const title = ref('');
const authors = ref('Lankford, J. W.');
const publication_year = ref(new Date().getFullYear());
const journal_or_conf = ref('');
const abstract = ref('');
const key_findings = ref('');
const methodology = ref('');
const zotero_key = ref('');

const isSubmitting = ref(false);

function handleSubmit() {
  if (!title.value.trim() || !authors.value.trim()) return;

  isSubmitting.value = true;
  emit('submit', {
    title: title.value.trim(),
    authors: authors.value.trim(),
    publication_year: Number(publication_year.value),
    journal_or_conf: journal_or_conf.value.trim() || undefined,
    abstract: abstract.value.trim() || undefined,
    key_findings: key_findings.value.trim() || undefined,
    methodology: methodology.value.trim() || undefined,
    zotero_key: zotero_key.value.trim() || undefined
  });

  // Reset form
  title.value = '';
  abstract.value = '';
  key_findings.value = '';
  methodology.value = '';
  journal_or_conf.value = '';
  zotero_key.value = '';
  isSubmitting.value = false;
}
</script>

<template>
  <Teleport to="body">
    <div 
      v-if="isOpen"
      class="fixed inset-0 z-50 overflow-y-auto bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 sm:p-6"
      @click.self="emit('close')"
    >
      <div class="relative bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl max-w-2xl w-full p-6 sm:p-8 text-slate-100">
        <!-- Header -->
        <div class="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
          <div>
            <h2 class="text-xl font-bold font-serif text-white flex items-center space-x-2">
              <span class="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span>
              <span>Index New Research Study</span>
            </h2>
            <p class="text-xs text-slate-400 mt-0.5">Submit paper metadata to the Lankford Academic Domain Index</p>
          </div>
          <button 
            @click="emit('close')"
            class="text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700 p-2 rounded-full transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4 text-sm max-h-[70vh] overflow-y-auto pr-1">
          <!-- Title -->
          <div>
            <label class="block text-xs font-mono text-slate-300 font-semibold mb-1">Paper Title *</label>
            <input 
              v-model="title"
              type="text"
              required
              placeholder="e.g. Deterministic Verification in Autonomous LLM Workflows"
              class="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-emerald-500"
            />
          </div>

          <!-- Authors & Year Row -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="sm:col-span-2">
              <label class="block text-xs font-mono text-slate-300 font-semibold mb-1">Authors *</label>
              <input 
                v-model="authors"
                type="text"
                required
                placeholder="Lankford, J. W.; Smith, A."
                class="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-emerald-500"
              />
            </div>
            <div>
              <label class="block text-xs font-mono text-slate-300 font-semibold mb-1">Publication Year *</label>
              <input 
                v-model.number="publication_year"
                type="number"
                min="1990"
                max="2030"
                required
                class="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:border-emerald-500"
              />
            </div>
          </div>

          <!-- Journal / Conf & Zotero -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-mono text-slate-300 font-semibold mb-1">Journal / Conference</label>
              <input 
                v-model="journal_or_conf"
                type="text"
                placeholder="IEEE TSE / ACM CCS"
                class="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-emerald-500"
              />
            </div>
            <div>
              <label class="block text-xs font-mono text-slate-300 font-semibold mb-1">Zotero Reference Key</label>
              <input 
                v-model="zotero_key"
                type="text"
                placeholder="LANKFORD_2026_GOVERNANCE"
                class="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-emerald-500 font-mono text-xs"
              />
            </div>
          </div>

          <!-- Abstract -->
          <div>
            <label class="block text-xs font-mono text-slate-300 font-semibold mb-1">Abstract Summary</label>
            <textarea 
              v-model="abstract"
              rows="3"
              placeholder="Summary of research problem, methodology, and primary conclusions..."
              class="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-emerald-500 resize-none"
            ></textarea>
          </div>

          <!-- Key Findings & Methodology -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-mono text-slate-300 font-semibold mb-1">Key Empirical Findings</label>
              <textarea 
                v-model="key_findings"
                rows="2"
                placeholder="e.g. Reduced execution branching error by 98.4%"
                class="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-emerald-500 resize-none"
              ></textarea>
            </div>
            <div>
              <label class="block text-xs font-mono text-slate-300 font-semibold mb-1">Methodology</label>
              <textarea 
                v-model="methodology"
                rows="2"
                placeholder="e.g. Empirical Benchmark & Load Simulation"
                class="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-emerald-500 resize-none"
              ></textarea>
            </div>
          </div>

          <!-- Submit Controls -->
          <div class="pt-4 border-t border-slate-800 flex justify-end space-x-3">
            <button 
              type="button"
              @click="emit('close')"
              class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg font-semibold transition-colors text-xs"
            >
              Cancel
            </button>
            <button 
              type="submit"
              :disabled="isSubmitting"
              class="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-semibold shadow-md shadow-emerald-600/30 transition-all text-xs flex items-center space-x-1.5"
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
