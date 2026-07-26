<script setup lang="ts">
import { ref, reactive } from 'vue';

const props = defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'submit', type: 'google' | 'jupyter', payload: any): void;
}>();

const notebookType = ref<'google' | 'jupyter'>('google');

const googleForm = reactive({
  title: '',
  description: '',
  notebook_url: '',
  audio_url: '',
  sources_count: 0
});

const jupyterForm = reactive({
  title: '',
  description: '',
  notebook_url: '',
  tags: ''
});

function handleSubmit() {
  if (notebookType.value === 'google') {
    if (!googleForm.title || !googleForm.description || !googleForm.notebook_url) return;
    emit('submit', 'google', {
      title: googleForm.title.trim(),
      description: googleForm.description.trim(),
      notebook_url: googleForm.notebook_url.trim(),
      audio_url: googleForm.audio_url.trim() || undefined,
      sources_count: googleForm.sources_count || 0
    });
    // Reset
    googleForm.title = '';
    googleForm.description = '';
    googleForm.notebook_url = '';
    googleForm.audio_url = '';
    googleForm.sources_count = 0;
  } else {
    if (!jupyterForm.title || !jupyterForm.description || !jupyterForm.notebook_url) return;
    emit('submit', 'jupyter', {
      title: jupyterForm.title.trim(),
      description: jupyterForm.description.trim(),
      notebook_url: jupyterForm.notebook_url.trim(),
      tags: jupyterForm.tags.trim() || undefined
    });
    // Reset
    jupyterForm.title = '';
    jupyterForm.description = '';
    jupyterForm.notebook_url = '';
    jupyterForm.tags = '';
  }
}
</script>

<template>
  <div 
    v-if="isOpen"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-md animate-fadeIn"
  >
    <div 
      class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl w-full max-w-lg shadow-2xl p-6 sm:p-8 space-y-6 text-slate-900 dark:text-slate-100 max-h-[90vh] overflow-y-auto"
    >
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
        <h3 class="text-xl font-bold font-serif">Index New Research Notebook</h3>
        <button 
          @click="emit('close')"
          class="text-slate-400 hover:text-slate-700 dark:hover:text-white text-lg transition-colors cursor-pointer"
        >
          ✕
        </button>
      </div>

      <!-- Type Selector Tabs -->
      <div class="grid grid-cols-2 p-1 bg-slate-100 dark:bg-slate-950 rounded-xl border border-slate-200 dark:border-slate-800">
        <button 
          type="button"
          @click="notebookType = 'google'"
          :class="[
            'py-2 text-xs font-semibold rounded-lg transition-all cursor-pointer',
            notebookType === 'google' 
              ? 'bg-blue-600 text-white shadow' 
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-white'
          ]"
        >
          Google NotebookLM
        </button>
        <button 
          type="button"
          @click="notebookType = 'jupyter'"
          :class="[
            'py-2 text-xs font-semibold rounded-lg transition-all cursor-pointer',
            notebookType === 'jupyter' 
              ? 'bg-blue-600 text-white shadow' 
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-white'
          ]"
        >
          Jupyter Notebook
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Form for Google NotebookLM -->
        <div v-if="notebookType === 'google'" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Notebook Title *</label>
            <input 
              v-model="googleForm.title"
              type="text"
              required
              placeholder="e.g. Guardrails & Safety in LLMs"
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-350 dark:border-slate-800 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-blue-500 transition-colors"
            />
          </div>

          <div>
            <label class="block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Description *</label>
            <textarea 
              v-model="googleForm.description"
              required
              rows="3"
              placeholder="Provide a summary of notes, research directions, and sources indexed..."
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-350 dark:border-slate-800 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-blue-500 transition-colors"
            ></textarea>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Sources Count</label>
              <input 
                v-model.number="googleForm.sources_count"
                type="number"
                min="0"
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-350 dark:border-slate-800 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-blue-500 transition-colors"
              />
            </div>
            <div>
              <label class="block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Audio Podcast URL</label>
              <input 
                v-model="googleForm.audio_url"
                type="url"
                placeholder="https://example.com/audio.mp3"
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-350 dark:border-slate-800 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-blue-500 transition-colors"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">NotebookLM Link *</label>
            <input 
              v-model="googleForm.notebook_url"
              type="url"
              required
              placeholder="https://notebooklm.google.com/notebook/..."
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-350 dark:border-slate-800 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-blue-500 transition-colors"
            />
          </div>
        </div>

        <!-- Form for Jupyter Notebook -->
        <div v-else class="space-y-4">
          <div>
            <label class="block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Notebook Title *</label>
            <input 
              v-model="jupyterForm.title"
              type="text"
              required
              placeholder="e.g. Guardrail Verification Simulation"
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-350 dark:border-slate-800 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-blue-500 transition-colors"
            />
          </div>

          <div>
            <label class="block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Description *</label>
            <textarea 
              v-model="jupyterForm.description"
              required
              rows="3"
              placeholder="Briefly describe the interactive code blocks, imports, and visualizations included..."
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-350 dark:border-slate-800 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-blue-500 transition-colors"
            ></textarea>
          </div>

          <div>
            <label class="block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Tags (Comma-Separated)</label>
            <input 
              v-model="jupyterForm.tags"
              type="text"
              placeholder="Pydantic,Simulation,LLM-Safety"
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-350 dark:border-slate-800 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-blue-500 transition-colors"
            />
          </div>

          <div>
            <label class="block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Jupyter Notebook Link *</label>
            <input 
              v-model="jupyterForm.notebook_url"
              type="url"
              required
              placeholder="e.g. GitHub URL or Google Colab Link"
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-350 dark:border-slate-800 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-blue-500 transition-colors"
            />
          </div>
        </div>

        <div class="flex items-center justify-end space-x-3 pt-4 border-t border-slate-100 dark:border-slate-800 mt-6">
          <button 
            type="button" 
            @click="emit('close')"
            class="px-4 py-2 text-xs font-semibold rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-205 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition-colors cursor-pointer"
          >
            Cancel
          </button>
          <button 
            type="submit"
            class="px-5 py-2 text-xs font-bold rounded-xl bg-blue-600 hover:bg-blue-500 text-white shadow-md transition-all active:scale-98 cursor-pointer"
          >
            Index Notebook
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
