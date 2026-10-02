<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Article, NewArticleInput } from '../types';
import { useAuth } from '../composables/useAuth';

const props = defineProps<{
  article: Article | null;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'update', id: number, input: Partial<NewArticleInput>): void;
}>();

const { isAdmin } = useAuth();

const isEditing = ref(false);
const isSaving = ref(false);

const draft = ref({
  title: '',
  summary: '',
  content: '',
  image_url: '',
  linkedin_url: '',
  substack_url: ''
});

function resetDraft(article: Article | null) {
  if (!article) return;
  draft.value = {
    title: article.title || '',
    summary: article.summary || '',
    content: article.content || '',
    image_url: article.image_url || '',
    linkedin_url: article.linkedin_url || '',
    substack_url: article.substack_url || ''
  };
}

// Keep the draft in sync whenever a new article is opened, and exit edit mode.
watch(() => props.article, (article) => {
  isEditing.value = false;
  resetDraft(article);
}, { immediate: true });

function startEditing() {
  resetDraft(props.article);
  isEditing.value = true;
}

function cancelEditing() {
  resetDraft(props.article);
  isEditing.value = false;
}

function saveEditing() {
  if (!props.article?.id) return;
  if (!draft.value.title.trim() || !draft.value.summary.trim()) return;

  isSaving.value = true;
  emit('update', props.article.id, {
    title: draft.value.title.trim(),
    summary: draft.value.summary.trim(),
    content: draft.value.content.trim() || undefined,
    image_url: draft.value.image_url.trim() || undefined,
    linkedin_url: draft.value.linkedin_url.trim() || undefined,
    substack_url: draft.value.substack_url.trim() || undefined
  });
  isSaving.value = false;
  isEditing.value = false;
}

function handleClose() {
  isEditing.value = false;
  emit('close');
}

function formatDate(dateStr?: string) {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}
</script>

<template>
  <Teleport to="body">
    <div 
      v-if="article"
      class="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center sm:p-4 animate-fadeIn"
    >
      <div 
        class="relative bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 sm:rounded-2xl shadow-2xl w-full h-full sm:max-w-5xl sm:h-[95vh] p-6 sm:p-8 text-slate-900 dark:text-slate-100 overflow-hidden transition-colors flex flex-col"
      >
        <!-- Background Decorative Gradient -->
        <div class="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -z-0 pointer-events-none"></div>

        <!-- Header Controls -->
        <div class="flex items-start justify-between border-b border-slate-200 dark:border-slate-800 pb-4 mb-4 relative z-10">
          <div class="flex-1 min-w-0 pr-4">
            <div class="flex items-center space-x-2 text-xs font-mono text-blue-700 dark:text-cyan-400 mb-1">
              <span class="px-2 py-0.5 rounded bg-blue-100 dark:bg-blue-950 border border-blue-300 dark:border-blue-500/30">
                Published: {{ formatDate(article.published_at) }}
              </span>
            </div>
            <h2 v-if="!isEditing" class="text-xl sm:text-3xl font-bold font-serif text-slate-900 dark:text-white leading-tight">
              {{ article.title }}
            </h2>
            <input
              v-else
              v-model="draft.title"
              type="text"
              placeholder="Article Title"
              class="w-full text-xl sm:text-2xl font-bold font-serif bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-white focus:outline-none focus:border-blue-500"
            />
          </div>
          <div class="flex items-center space-x-2 flex-shrink-0">
            <button 
              v-if="isAdmin && !isEditing"
              @click="startEditing"
              class="text-slate-500 dark:text-slate-300 hover:text-blue-700 dark:hover:text-cyan-300 bg-slate-100 dark:bg-slate-800 hover:bg-blue-100 dark:hover:bg-blue-900/50 p-2 rounded-full transition-colors cursor-pointer"
              title="Edit article"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </button>
            <button 
              @click="handleClose"
              class="text-slate-400 hover:text-slate-700 dark:hover:text-white bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 p-2 rounded-full transition-colors flex-shrink-0 cursor-pointer"
              title="Close modal"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Scrollable content -->
        <div class="space-y-6 text-sm relative z-10 overflow-y-auto pr-1 flex-1">
          <!-- Article Cover Image -->
          <div v-if="!isEditing">
            <div v-if="article.image_url" class="relative overflow-hidden rounded-xl border border-slate-200 dark:border-slate-800 shadow-md">
              <img 
                :src="article.image_url" 
                :alt="article.title"
                class="w-full h-52 sm:h-80 object-cover"
              />
            </div>
          </div>
          <div v-else>
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Cover Image URL</label>
            <input 
              v-model="draft.image_url"
              type="url"
              placeholder="https://images.unsplash.com/..."
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          <!-- Summary section -->
          <div v-if="!isEditing" class="bg-blue-50/50 dark:bg-blue-950/20 p-4 rounded-xl border border-blue-200/50 dark:border-blue-900/30">
            <p class="text-sm font-sans italic text-slate-700 dark:text-slate-300 leading-relaxed">
              &ldquo;{{ article.summary }}&rdquo;
            </p>
          </div>
          <div v-else>
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Summary / Hook</label>
            <textarea 
              v-model="draft.summary"
              rows="3"
              placeholder="A short summary of the article..."
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
            ></textarea>
          </div>

          <!-- Platform links (edit mode only) -->
          <div v-if="isEditing" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">LinkedIn URL</label>
              <input 
                v-model="draft.linkedin_url"
                type="url"
                placeholder="https://www.linkedin.com/pulse/..."
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700/80 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
              />
            </div>
            <div>
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Substack URL</label>
              <input 
                v-model="draft.substack_url"
                type="url"
                placeholder="https://your.substack.com/p/..."
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700/80 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <!-- Full Content -->
          <div v-if="!isEditing" class="prose dark:prose-invert max-w-none text-slate-850 dark:text-slate-200 font-sans leading-relaxed text-sm sm:text-base space-y-4 white-space-pre-wrap">
            <div class="whitespace-pre-wrap font-sans">{{ article.content || 'No article content available.' }}</div>
          </div>
          <div v-else>
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Full Article Content</label>
            <textarea 
              v-model="draft.content"
              rows="14"
              placeholder="Write the full body of the article here..."
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500 font-sans"
            ></textarea>
          </div>
        </div>

        <!-- Footer link -->
        <div class="mt-6 pt-4 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs relative z-10">
          <div v-if="!isEditing">
            <a 
              v-if="article.linkedin_url"
              :href="article.linkedin_url"
              target="_blank"
              rel="noopener noreferrer"
              class="text-xs font-semibold text-blue-600 dark:text-blue-400 hover:underline flex items-center space-x-1"
            >
              <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h-2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
              </svg>
              <span>Read original thread on LinkedIn</span>
            </a>
            <a 
              v-else-if="article.substack_url"
              :href="article.substack_url"
              target="_blank"
              rel="noopener noreferrer"
              class="text-xs font-semibold text-orange-600 dark:text-orange-400 hover:underline flex items-center space-x-1"
            >
              <svg class="w-4 h-4 text-orange-600 dark:text-orange-400" fill="currentColor" viewBox="0 0 24 24">
                <path d="M22.539 8.242H1.46V5.406h21.08v2.836zM1.46 10.812V24L12 18.11 22.54 24V10.812H1.46zM22.54 0H1.46v2.836h21.08V0z"/>
              </svg>
              <span>Read original post on Substack</span>
            </a>
          </div>
          <div v-else></div>
          <div class="flex items-center space-x-3">
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
                class="px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-500 hover:to-indigo-600 disabled:opacity-50 text-white text-xs font-semibold rounded-lg shadow-md shadow-blue-500/20 transition-all cursor-pointer"
              >
                {{ isSaving ? 'Saving...' : 'Save Changes' }}
              </button>
            </template>
            <button 
              v-else
              @click="handleClose"
              class="px-4 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-350 text-xs font-semibold rounded-lg transition-colors cursor-pointer"
            >
              Done Reading
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
