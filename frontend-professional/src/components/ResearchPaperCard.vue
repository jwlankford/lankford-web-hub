<script setup lang="ts">
import { ref } from 'vue';
import type { ResearchPaper } from '../types';
import { useAuth } from '../composables/useAuth';
import { updateResearchPaper } from '../services/api';

const props = defineProps<{
  paper: ResearchPaper;
}>();

const emit = defineEmits<{
  (e: 'select', paper: ResearchPaper): void;
  (e: 'filterTag', tagSlug: string): void;
  (e: 'updated', paper: ResearchPaper): void;
}>();

const { isAdmin } = useAuth();
const isExpanded = ref(false);
const isSaving = ref(false);
const localKeyFindings = ref(props.paper.key_findings || '');
const localUsedFor = ref(props.paper.used_for || '');

function toggleExpand() {
  isExpanded.value = !isExpanded.value;
  if (isExpanded.value) {
    localKeyFindings.value = props.paper.key_findings || '';
    localUsedFor.value = props.paper.used_for || '';
  }
}

async function saveKeyFindings() {
  try {
    isSaving.value = true;
    const { paper } = await updateResearchPaper(props.paper.id!, {
      key_findings: localKeyFindings.value,
      used_for: localUsedFor.value
    });
    emit('updated', paper);
    isExpanded.value = false;
  } catch (e: any) {
    alert('Error saving paper: ' + e.message);
  } finally {
    isSaving.value = false;
  }
}
</script>

<template>
  <div 
    class="group relative bg-white dark:bg-slate-900/60 hover:bg-slate-50 dark:hover:bg-slate-900/90 rounded-xl p-6 border border-slate-200 dark:border-slate-800 hover:border-blue-500/40 transition-all duration-300 shadow-md hover:shadow-xl dark:hover:shadow-blue-950/40 overflow-hidden flex flex-col justify-between h-full w-full"
  >
    <div class="relative">
      <div class="flex items-center justify-between text-xs mb-3 text-slate-500 dark:text-slate-400 font-mono">
        <span class="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-md bg-blue-50 dark:bg-blue-950/80 border border-blue-300 dark:border-blue-500/30 text-blue-800 dark:text-cyan-300 font-semibold">
          <span>{{ paper.publication_year }}</span>
        </span>
        <span class="truncate max-w-[200px] text-right font-sans text-slate-500 dark:text-slate-400" :title="paper.journal_or_conf">
          {{ paper.journal_or_conf || 'Peer-Reviewed Study' }}
        </span>
      </div>

      <!-- Expand Arrow -->
      <button @click.stop="toggleExpand" class="absolute top-8 right-0 p-1 text-slate-400 hover:text-blue-600 dark:hover:text-cyan-400 transition-colors z-10" title="Expand card">
        <svg :class="{'rotate-180': isExpanded}" class="w-6 h-6 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
      </button>

      <!-- Title -->
      <h3 
        @click="emit('select', paper)"
        class="text-lg font-bold text-slate-900 dark:text-slate-100 group-hover:text-blue-600 dark:group-hover:text-cyan-300 cursor-pointer transition-colors leading-snug mb-2 font-serif pr-8"
      >
        {{ paper.title }}
      </h3>

      <!-- Authors -->
      <p class="text-xs font-mono text-blue-700 dark:text-cyan-400/90 mb-4">
        {{ paper.authors }}
      </p>

      <!-- Extra info when expanded (Editable Fields) -->
      <div v-if="isExpanded" class="mb-4 space-y-4 pt-2 border-t border-slate-100 dark:border-slate-800/50">
        <div>
          <h4 class="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide mb-2">Key Findings</h4>
          <textarea 
            v-if="isAdmin"
            v-model="localKeyFindings"
            rows="4" 
            class="w-full px-3 py-2 text-sm border rounded-lg dark:bg-slate-800/50 dark:border-slate-700 outline-none focus:border-blue-500 transition-colors text-slate-800 dark:text-slate-200"
            placeholder="Add key findings here..."
          ></textarea>
          <p v-else class="text-sm text-slate-600 dark:text-slate-400 mt-1 whitespace-pre-wrap">
            {{ paper.key_findings || 'No key findings recorded yet.' }}
          </p>
        </div>

        <div v-if="isAdmin">
          <h4 class="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide mb-2">Used For</h4>
          <input 
            type="text"
            v-model="localUsedFor"
            class="w-full px-3 py-2 text-sm border rounded-lg dark:bg-slate-800/50 dark:border-slate-700 outline-none focus:border-blue-500 transition-colors text-slate-800 dark:text-slate-200"
            placeholder="Where did you use this resource? (e.g. Chapter 3, App feature)"
          />
        </div>
        <div v-else-if="paper.used_for">
          <h4 class="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide mb-2">Used For</h4>
          <p class="text-sm text-slate-600 dark:text-slate-400 mt-1 whitespace-pre-wrap">
            {{ paper.used_for }}
          </p>
        </div>
        
        <div v-if="isAdmin" class="flex justify-end pt-2">
          <button @click.stop="saveKeyFindings" :disabled="isSaving" class="text-xs bg-blue-600 text-white hover:bg-blue-500 disabled:opacity-50 px-4 py-2 rounded-lg transition-colors font-semibold flex items-center space-x-2">
            <span v-if="isSaving" class="animate-spin h-3.5 w-3.5 border-2 border-white border-t-transparent rounded-full"></span>
            <span>{{ isSaving ? 'Saving...' : 'Save Updates' }}</span>
          </button>
        </div>
      </div>
      
      <!-- Used For Display at Bottom -->
      <div v-if="!isExpanded && paper.used_for" class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800/50">
        <h4 class="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wide mb-1">Used For</h4>
        <p class="text-xs font-medium text-slate-700 dark:text-slate-300">
          {{ paper.used_for }}
        </p>
      </div>
    </div>

  </div>
</template>
