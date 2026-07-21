<script setup lang="ts">
import { ref, onMounted } from 'vue';
import HeroSection from './components/HeroSection.vue';
import MailingListForm from './components/MailingListForm.vue';
import BookOutline from './components/BookOutline.vue';
import AuthorSection from './components/AuthorSection.vue';
import { checkProfessionalBackendHealth } from './services/api';

const isBackendConnected = ref(false);

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
  <div class="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-blue-600 selection:text-white pb-16">
    <!-- Premium Professional Navbar -->
    <header class="sticky top-0 z-40 backdrop-blur-xl bg-slate-950/85 border-b border-blue-500/20 shadow-2xl">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        
        <!-- High-Tech Developer Logo & Branding -->
        <div class="flex items-center space-x-3.5 group cursor-pointer" @click="scrollToSignup">
          <!-- Animated Cyber Code SVG Icon -->
          <div class="relative flex items-center justify-center">
            <div class="absolute -inset-1 bg-gradient-to-r from-blue-600 via-indigo-500 to-cyan-400 rounded-xl blur opacity-30 group-hover:opacity-80 transition duration-300"></div>
            <div class="relative w-11 h-11 rounded-xl bg-slate-900 border border-blue-400/40 flex items-center justify-center shadow-lg shadow-blue-950/50 group-hover:scale-105 transition-transform duration-300">
              <svg class="w-6 h-6 text-cyan-400 group-hover:text-blue-300 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
            </div>
          </div>

          <!-- Brand Typography -->
          <div>
            <div class="flex items-center space-x-2">
              <span class="font-extrabold text-xl tracking-tight text-white group-hover:text-cyan-300 transition-colors">
                TODAY'S <span class="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">DEVELOPER</span>
              </span>
              <span class="text-[10px] px-2 py-0.5 rounded-full font-mono bg-blue-950/90 text-cyan-300 border border-blue-500/40 uppercase tracking-widest hidden sm:inline-block">
                2026 Edition
              </span>
            </div>
            <div class="flex items-center space-x-2 text-xs text-slate-400">
              <span class="font-mono text-[11px] text-blue-400/90">jeremylankford.com</span>
              <span class="text-slate-600">•</span>
              <span>By Jeremy Lankford</span>
            </div>
          </div>
        </div>

        <!-- Navigation Links -->
        <nav class="hidden md:flex items-center space-x-8 text-xs font-mono font-semibold tracking-wider text-slate-300">
          <a href="#outline" class="hover:text-cyan-400 transition-colors flex items-center space-x-1">
            <span>CURRICULUM</span>
          </a>
          <a href="#signup-form" class="hover:text-cyan-400 transition-colors flex items-center space-x-1">
            <span>MAILING LIST</span>
          </a>
          <a 
            href="http://academic.localhost:5174" 
            target="_blank" 
            class="hover:text-cyan-400 transition-colors flex items-center space-x-1.5 text-slate-400 bg-slate-900 px-3 py-1.5 rounded-xl border border-slate-800"
          >
            <span>ACADEMIC HUB</span>
            <svg class="w-3.5 h-3.5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
            </svg>
          </a>
        </nav>

        <!-- Action CTA Button -->
        <button
          @click="scrollToSignup"
          class="bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white text-xs font-bold px-5 py-2.5 rounded-xl shadow-lg shadow-blue-600/30 border border-blue-400/30 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
        >
          Join Readers
        </button>
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
    <footer class="mt-20 border-t border-slate-900 pt-8 text-center text-xs font-mono text-slate-500">
      <p>© 2026 Jeremy Lankford. Professional Domain Workspace (jeremylankford.com)</p>
    </footer>
  </div>
</template>