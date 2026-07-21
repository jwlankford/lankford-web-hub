<script setup lang="ts">
import { ref, onMounted } from 'vue';
import HeroSection from './components/HeroSection.vue';
import MailingListForm from './components/MailingListForm.vue';
import BookOutline from './components/BookOutline.vue';
import AuthorSection from './components/AuthorSection.vue';
import { checkProfessionalBackendHealth } from './services/api';
import { useTheme } from './composables/useTheme';

const isBackendConnected = ref(false);
const { theme, toggleTheme } = useTheme();

function scrollToSignup() {
  const el = document.getElementById('signup-form');
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' });
  }
}

onMounted(async () => {
  isBackendConnected.value = await checkProfessionalBackendHealth();
});
</script>

<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 font-sans selection:bg-blue-600 selection:text-white pb-16 transition-colors duration-300">
    <!-- Premium Professional Navbar -->
    <header class="sticky top-0 z-40 backdrop-blur-xl bg-white/85 dark:bg-slate-950/85 border-b border-slate-200 dark:border-blue-500/20 shadow-2xl transition-colors duration-300">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        
        <!-- High-Tech Brand & Header Title -->
        <div class="flex items-center space-x-3 group cursor-pointer" @click="scrollToSignup">
          <!-- Brand Typography -->
          <div>
            <div class="flex items-center space-x-2">
              <span class="font-extrabold text-lg sm:text-xl tracking-tight text-slate-900 dark:text-white group-hover:text-cyan-600 dark:group-hover:text-cyan-300 transition-colors">
                TODAY'S <span class="bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-600 dark:from-blue-400 dark:via-indigo-300 dark:to-cyan-400 bg-clip-text text-transparent">SOFTWARE DEVELOPER</span>
              </span>
              <span class="text-[10px] px-2 py-0.5 rounded-full font-mono bg-blue-100 dark:bg-blue-950/90 text-blue-800 dark:text-cyan-300 border border-blue-300 dark:border-blue-500/40 uppercase tracking-widest hidden sm:inline-block">
                2026 Edition
              </span>
            </div>
            <div class="flex items-center space-x-2 text-xs text-slate-500 dark:text-slate-400">
              <span class="font-mono text-[11px] text-blue-600 dark:text-blue-400/90">jeremylankford.com</span>
              <span class="text-slate-400 dark:text-slate-600">•</span>
              <span>By Jeremy Lankford</span>
            </div>
          </div>
        </div>

        <!-- Right Side Nav & Actions -->
        <div class="flex items-center space-x-6">
          <!-- Navigation Links -->
          <nav class="hidden md:flex items-center space-x-6 text-xs font-mono font-semibold tracking-wider text-slate-600 dark:text-slate-300">
            <a href="#outline" class="hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors flex items-center space-x-1">
              <span>CURRICULUM</span>
            </a>
            <a href="#signup-form" class="hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors flex items-center space-x-1">
              <span>MAILING LIST</span>
            </a>
            <a 
              href="http://academic.localhost:5174" 
              target="_blank" 
              class="hover:text-cyan-600 dark:hover:text-cyan-400 transition-colors flex items-center space-x-1.5 text-slate-600 dark:text-slate-400 bg-slate-100 dark:bg-slate-900 px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-800"
            >
              <span>ACADEMIC HUB</span>
              <svg class="w-3.5 h-3.5 text-blue-500 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
              </svg>
            </a>
          </nav>

          <div class="flex items-center space-x-3">
            <!-- Theme Toggle Button -->
            <button
              @click="toggleTheme"
              class="relative flex items-center justify-center p-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-900 text-amber-500 dark:text-amber-400 hover:scale-105 hover:border-cyan-500/50 transition-all shadow-sm cursor-pointer"
              :title="theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
              aria-label="Toggle Dark / Light Theme"
            >
              <svg v-if="theme === 'dark'" class="w-4 h-4 transform rotate-0 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              <svg v-else class="w-4 h-4 text-indigo-600 transform rotate-0 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
            </button>

            <!-- Action CTA Button -->
            <button
              @click="scrollToSignup"
              class="bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white text-xs font-bold px-4 sm:px-5 py-2.5 rounded-xl shadow-lg shadow-blue-600/30 border border-blue-400/30 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
            >
              Join Readers
            </button>
          </div>
        </div>

      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16">
      <HeroSection @scrollToForm="scrollToSignup" />
      <MailingListForm />
      <BookOutline />
      <AuthorSection />
    </main>

    <!-- Footer -->
    <footer class="mt-20 border-t border-slate-200 dark:border-slate-900 pt-8 pb-4 text-center text-xs font-mono text-slate-500 dark:text-slate-500 space-y-4">
      <div class="flex items-center justify-center space-x-6">
        <a 
          href="http://www.linkedin.com/in/jwlankford" 
          target="_blank" 
          rel="noopener noreferrer"
          class="hover:text-blue-600 dark:hover:text-blue-400 flex items-center space-x-1.5 transition-colors"
        >
          <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 24 24">
            <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
          </svg>
          <span>LinkedIn</span>
        </a>

        <a 
          href="https://x.com/jwlankford" 
          target="_blank" 
          rel="noopener noreferrer"
          class="hover:text-cyan-600 dark:hover:text-cyan-400 flex items-center space-x-1.5 transition-colors text-slate-600 dark:text-slate-300"
        >
          <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
          </svg>
          <span>X / Twitter</span>
        </a>

        <a 
          href="https://www.facebook.com/profile.php?id=61591720403485" 
          target="_blank" 
          rel="noopener noreferrer"
          class="hover:text-blue-600 dark:hover:text-blue-400 flex items-center space-x-1.5 transition-colors"
        >
          <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 24 24">
            <path d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H7.5v-3H10V9.69c0-2.47 1.47-3.83 3.72-3.83 1.08 0 2.2.19 2.2.19v2.42h-1.24c-1.23 0-1.61.76-1.61 1.54V12h2.73l-.44 3h-2.29v6.8c4.56-.93 8-4.96 8-9.8z"/>
          </svg>
          <span>Facebook</span>
        </a>
      </div>
      <p>© 2026 Jeremy Lankford. Professional Domain Workspace (jeremylankford.com)</p>
    </footer>
  </div>
</template>