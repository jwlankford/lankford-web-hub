<script setup lang="ts">
import { ref } from 'vue';
import logoUrl from '../assets/logo.png';
import logoDarkUrl from '../assets/logo-dark.png';
import { useAuth } from '../composables/useAuth';

defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'login', passkey: string): void;
}>();

const { loginWithGoogle, isAuthLoading } = useAuth();
const passkey = ref('');
const error = ref('');

async function handleGoogleLogin() {
  error.value = '';
  const result = await loginWithGoogle();
  if (result.success) {
    emit('close');
  } else {
    error.value = result.message || 'Google Sign-In failed.';
  }
}

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
          <div class="flex items-center space-x-2.5">
            <img 
              :src="logoUrl" 
              alt="Jeremy Lankford Logo" 
              class="h-10 sm:h-12 w-auto object-contain dark:hidden filter drop-shadow-sm"
            />
            <img 
              :src="logoDarkUrl" 
              alt="Jeremy Lankford Logo" 
              class="h-10 sm:h-12 w-auto object-contain hidden dark:block filter drop-shadow-[0_0_12px_rgba(56,189,248,0.4)]"
            />
            <div>
              <h3 class="text-sm font-bold text-slate-900 dark:text-white font-serif">Author Authentication</h3>
              <p class="text-[10px] text-slate-500 dark:text-slate-400 font-mono">Unlock study indexing & admin controls</p>
            </div>
          </div>
          <button 
            @click="emit('close')"
            class="text-slate-400 hover:text-slate-700 dark:hover:text-white p-1 rounded-full"
          >
            ✕
          </button>
        </div>

        <div class="space-y-4">
          <!-- Google Sign-In Primary Button -->
          <button
            @click="handleGoogleLogin"
            :disabled="isAuthLoading"
            type="button"
            class="w-full py-2.5 px-4 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-950 text-slate-800 dark:text-slate-100 hover:bg-slate-50 dark:hover:bg-slate-800/80 hover:border-blue-500/50 transition-all duration-200 flex items-center justify-center space-x-3 text-xs font-semibold shadow-sm cursor-pointer disabled:opacity-50"
          >
            <!-- Google Multicolor Logo SVG -->
            <svg class="w-4 h-4" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
            </svg>
            <span>{{ isAuthLoading ? 'Signing in...' : 'Sign in with Google' }}</span>
          </button>

          <!-- Divider -->
          <div class="relative flex items-center justify-center my-3">
            <div class="border-t border-slate-200 dark:border-slate-800 w-full"></div>
            <span class="bg-white dark:bg-slate-900 px-2 text-[10px] font-mono text-slate-400 dark:text-slate-500 uppercase tracking-widest absolute">or passkey</span>
          </div>

          <!-- Passkey Form -->
          <form @submit.prevent="handleSubmit" class="space-y-3">
            <div>
              <label class="block text-xs font-mono text-slate-700 dark:text-slate-300 font-semibold mb-1">Passkey / Access Key</label>
              <input 
                v-model="passkey"
                type="password"
                placeholder="Enter passkey"
                class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500 font-mono"
              />
            </div>

            <p v-if="error" class="text-xs text-rose-500 font-mono leading-tight">{{ error }}</p>

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
    </div>
  </Teleport>
</template>
