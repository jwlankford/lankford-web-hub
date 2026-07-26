<script setup lang="ts">
import { ref } from 'vue';
import type { NewArticleInput } from '../types';

defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'submit', input: NewArticleInput): void;
}>();

const title = ref('');
const summary = ref('');
const content = ref('');
const linkedin_url = ref('');
const image_url = ref('');

const isSubmitting = ref(false);

function handleSubmit() {
  if (!title.value.trim() || !summary.value.trim()) return;

  isSubmitting.value = true;
  emit('submit', {
    title: title.value.trim(),
    summary: summary.value.trim(),
    content: content.value.trim() || undefined,
    linkedin_url: linkedin_url.value.trim() || undefined,
    image_url: image_url.value.trim() || undefined,
    is_published: true
  });

  // Reset form
  title.value = '';
  summary.value = '';
  content.value = '';
  linkedin_url.value = '';
  image_url.value = '';
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
      <div class="relative bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl max-w-2xl w-full p-6 sm:p-8 text-slate-900 dark:text-slate-100 transition-colors">
        <!-- Header -->
        <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-4 mb-6">
          <div>
            <h2 class="text-xl font-bold font-serif text-slate-900 dark:text-white flex items-center space-x-2">
              <span class="w-3 h-3 rounded-full bg-blue-500 inline-block"></span>
              <span>Publish Weekly Article</span>
            </h2>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Publish an article to the Web and reference your LinkedIn Pulse thread</p>
          </div>
          <button 
            @click="emit('close')"
            class="text-slate-400 hover:text-slate-700 dark:hover:text-white bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 p-2 rounded-full transition-colors cursor-pointer"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4 text-sm max-h-[70vh] overflow-y-auto pr-1">
          <!-- Title -->
          <div>
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Article Title *</label>
            <input 
              v-model="title"
              type="text"
              required
              placeholder="e.g. Building the Stack Around the Copilot"
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <!-- Summary -->
          <div>
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Summary / Hook *</label>
            <textarea 
              v-model="summary"
              required
              rows="3"
              placeholder="A short summary of the article (displays on the card and LinkedIn snippet)..."
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
            ></textarea>
          </div>

          <!-- Cover Image & LinkedIn Links Row -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Cover Image Link (URL)</label>
              <input 
                v-model="image_url"
                type="url"
                placeholder="https://images.unsplash.com/..."
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700/80 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
              />
            </div>
            <div>
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">LinkedIn Pulse Link (URL)</label>
              <input 
                v-model="linkedin_url"
                type="url"
                placeholder="https://www.linkedin.com/pulse/..."
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700/80 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <!-- Full Content -->
          <div>
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Full Article Content</label>
            <textarea 
              v-model="content"
              rows="8"
              placeholder="Write the full body of the article here. You can use standard formatting..."
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500 font-sans"
            ></textarea>
          </div>

          <!-- Submit Buttons -->
          <div class="flex items-center justify-end space-x-3 pt-4 border-t border-slate-200 dark:border-slate-800">
            <button 
              type="button"
              @click="emit('close')"
              class="px-4 py-2 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800/80 transition-colors cursor-pointer"
            >
              Cancel
            </button>
            <button 
              type="submit"
              :disabled="isSubmitting"
              class="bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-500 hover:to-indigo-600 disabled:opacity-50 text-white font-semibold px-5 py-2 rounded-lg shadow-md shadow-blue-500/20 border border-blue-400/20 transition-all flex items-center space-x-1.5 cursor-pointer"
            >
              <svg v-if="isSubmitting" class="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>{{ isSubmitting ? 'Publishing...' : 'Publish Article' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>
