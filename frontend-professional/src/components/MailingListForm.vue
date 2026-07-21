<script setup lang="ts">
import { ref } from 'vue';
import { submitBookMailingList } from '../services/api';

const email = ref('');
const firstName = ref('');
const isSubmitting = ref(false);
const statusMessage = ref<{ text: string; isError: boolean } | null>(null);

async function handleSubmit() {
  if (!email.value.trim()) return;

  isSubmitting.value = true;
  statusMessage.value = null;

  const res = await submitBookMailingList({
    email: email.value.trim(),
    first_name: firstName.value.trim() || undefined
  });

  isSubmitting.value = false;

  if (res.success) {
    statusMessage.value = { text: res.message, isError: false };
    email.value = '';
    firstName.value = '';
  } else {
    statusMessage.value = { text: res.message, isError: true };
  }
}
</script>

<template>
  <div id="signup-form" class="relative bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-8 sm:p-12 shadow-2xl overflow-hidden max-w-4xl mx-auto transition-colors">
    <!-- Accent Background Layer -->
    <div class="absolute -top-24 -right-24 w-72 h-72 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>

    <div class="max-w-2xl mx-auto text-center space-y-4 relative z-10">
      <span class="text-xs font-mono text-cyan-800 dark:text-cyan-400 uppercase tracking-widest bg-cyan-100 dark:bg-cyan-950/80 px-3 py-1 rounded-full border border-cyan-300 dark:border-cyan-500/30">
        Reader Community
      </span>

      <h2 class="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
        Join the Launch Reader List
      </h2>

      <p class="text-slate-600 dark:text-slate-300 text-sm sm:text-base leading-relaxed">
        Be the first to receive free preview chapters, technical architectural breakdowns, and release notifications for <strong class="text-blue-600 dark:text-blue-400">Today's Software Developer</strong>.
      </p>

      <form @submit.prevent="handleSubmit" class="pt-4 space-y-4 text-left">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">First Name (Optional)</label>
            <input 
              v-model="firstName"
              type="text"
              placeholder="e.g. Alex"
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700/80 rounded-xl px-4 py-3 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors text-sm"
            />
          </div>

          <div>
            <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Email Address *</label>
            <input 
              v-model="email"
              type="email"
              required
              placeholder="developer@company.com"
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700/80 rounded-xl px-4 py-3 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors text-sm"
            />
          </div>
        </div>

        <button 
          type="submit"
          :disabled="isSubmitting"
          class="w-full py-3.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold rounded-xl shadow-lg shadow-blue-600/30 border border-blue-400/30 transition-all text-sm flex items-center justify-center space-x-2"
        >
          <span v-if="isSubmitting" class="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></span>
          <span>{{ isSubmitting ? 'Registering Email...' : 'Subscribe for Free Chapter Previews' }}</span>
        </button>
      </form>

      <!-- Feedback Alert -->
      <div 
        v-if="statusMessage"
        class="mt-4 p-4 rounded-xl text-xs font-mono border transition-all text-left"
        :class="statusMessage.isError 
          ? 'bg-red-50 dark:bg-red-950/80 border-red-300 dark:border-red-500/40 text-red-800 dark:text-red-300' 
          : 'bg-emerald-50 dark:bg-emerald-950/80 border-emerald-300 dark:border-emerald-500/40 text-emerald-800 dark:text-emerald-300'"
      >
        <div class="flex items-center space-x-2">
          <span>{{ statusMessage.isError ? '⚠️' : '🎉' }}</span>
          <span>{{ statusMessage.text }}</span>
        </div>
      </div>

      <p class="text-[11px] text-slate-500 font-mono pt-2">
        Zero spam guarantee. Unsubscribe at any time with one click. Bound to the <span class="text-blue-600 dark:text-blue-400">jeremylankford.com</span> domain context.
      </p>
    </div>
  </div>
</template>
