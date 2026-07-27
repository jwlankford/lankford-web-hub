<script setup lang="ts">
import { ref } from 'vue';

defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'login', passkey: string): void;
}>();

const passkey = ref('');
const error = ref('');

function handleSubmit() {
  if (!passkey.value.trim()) return;
  emit('login', passkey.value.trim());
  passkey.value = '';
}
</script>

<template>
  <Teleport to="body">
    <div 
      v-if="isOpen"
      class="fixed inset-0 z-50 overflow-y-auto bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4"
      @click.self="emit('close')"
    >
      <div class="relative bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700/80 rounded-2xl shadow-2xl max-w-sm w-full p-6 text-slate-900 dark:text-slate-100 transition-colors">
        <!-- Header -->
        <div class="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3 mb-4">
          <div class="flex items-center space-x-2">
            <div class="w-8 h-8 rounded-lg bg-blue-100 dark:bg-blue-950 border border-blue-300 dark:border-blue-500/40 flex items-center justify-center text-blue-700 dark:text-cyan-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
            </div>
            <div>
              <h3 class="text-sm font-bold text-slate-900 dark:text-white font-serif">Author Authentication</h3>
              <p class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">Unlock study indexing & administrative controls</p>
            </div>
          </div>
          <button 
            @click="emit('close')"
            class="text-slate-400 hover:text-slate-700 dark:hover:text-white p-1 rounded-full"
          >
            ✕
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <div class="flex items-center justify-between mb-1">
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold">Passkey / Access Key</label>
            </div>
            <input 
              v-model="passkey"
              type="password"
              placeholder="Enter passkey"
              required
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500 font-mono"
            />
          </div>

          <p v-if="error" class="text-xs text-rose-500 font-mono">{{ error }}</p>

          <div class="flex items-center justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-slate-800">
            <button 
              type="button"
              @click="emit('close')"
              class="px-3 py-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg text-xs font-semibold"
            >
              Cancel
            </button>
            <button 
              type="submit"
              class="px-4 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-bold shadow-md shadow-blue-600/30"
            >
              Authenticate
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>
