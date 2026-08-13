<template>
  <div class="space-y-6 animate-fadeIn max-w-5xl mx-auto w-full">
    <!-- Header -->
    <div class="text-center md:text-left">
      <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-rose-100 dark:bg-rose-950 text-rose-800 dark:text-rose-300 text-xs font-mono border border-rose-300 dark:border-rose-500/30">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
        <span>SUPPORT JEREMY</span>
      </span>
      <h3 class="text-3xl font-bold font-serif text-slate-900 dark:text-white mt-4">Support & Contributions</h3>
      <p class="text-slate-600 dark:text-slate-400 mt-2 text-lg">
        Thank you for your generosity. Choose how you'd like to allocate your support below.
      </p>
    </div>

    <!-- Main Content: Two Columns -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
      
      <!-- Academic Studies Fund -->
      <div class="bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800/80 p-8 rounded-3xl border border-slate-200 dark:border-slate-700/50 shadow-sm flex flex-col h-full">
        <div class="mb-6">
          <div class="w-12 h-12 rounded-2xl bg-indigo-100 dark:bg-indigo-900/50 flex items-center justify-center mb-4 text-indigo-600 dark:text-indigo-400">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
            </svg>
          </div>
          <h4 class="text-2xl font-bold text-slate-900 dark:text-white">Academic Studies</h4>
          <p class="text-slate-600 dark:text-slate-400 mt-2 text-sm leading-relaxed">
            Jeremy is unable to work and can use your support in academics. Help cover the costs of tuition, research materials, compute resources, and ongoing academic projects.
          </p>
        </div>

        <div class="space-y-4 flex-grow">
          <div class="grid grid-cols-2 gap-3">
            <button 
              v-for="amount in [5, 10, 25, 50]" 
              :key="amount"
              @click="selectedAcademic = amount"
              class="py-3 px-4 rounded-xl border-2 transition-all flex flex-col items-center justify-center space-y-1"
              :class="selectedAcademic === amount ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20 text-indigo-700 dark:text-indigo-300 shadow-md scale-[1.02]' : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:border-indigo-300 hover:bg-slate-50 dark:hover:bg-slate-700 hover:scale-[1.02]'"
            >
              <span class="text-xl font-bold">${{ amount }}</span>
            </button>
          </div>

          <div class="pt-2">
            <label class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Custom Amount</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span class="text-slate-400 sm:text-sm">$</span>
              </div>
              <input 
                type="number" 
                min="1"
                step="any"
                v-model="customAcademic"
                @focus="selectedAcademic = null"
                class="w-full pl-7 pr-4 py-2.5 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none text-slate-900 dark:text-white transition-all shadow-sm"
                placeholder="0.00"
              />
            </div>
          </div>
        </div>

        <a 
          href="https://paypal.me/jwlankford"
          target="_blank"
          rel="noopener noreferrer"
          class="w-full mt-8 bg-gradient-to-r from-indigo-500 to-blue-600 hover:from-indigo-600 hover:to-blue-700 text-white font-bold py-3.5 px-6 rounded-xl shadow-lg shadow-indigo-500/30 transform hover:-translate-y-0.5 active:translate-y-0 transition-all flex items-center justify-center space-x-2 cursor-pointer"
        >
          <span>Support Academics {{ displayAcademic }}</span>
        </a>
      </div>

      <!-- CKD Fund -->
      <div class="bg-gradient-to-br from-rose-50 to-pink-50 dark:from-rose-950/30 dark:to-pink-900/20 p-8 rounded-3xl border border-rose-200/60 dark:border-rose-800/40 shadow-sm flex flex-col h-full">
        <div class="mb-6">
          <div class="w-12 h-12 rounded-2xl bg-rose-100 dark:bg-rose-900/50 flex items-center justify-center mb-4 text-rose-600 dark:text-rose-400">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </div>
          <h4 class="text-2xl font-bold text-slate-900 dark:text-white">Chronic Kidney Disease</h4>
          <p class="text-slate-600 dark:text-slate-400 mt-2 text-sm leading-relaxed">
            Provide support for medical expenses, specialized diets, medications, and ongoing treatments for managing CKD.
          </p>
        </div>

        <div class="space-y-4 flex-grow">
          <div class="grid grid-cols-2 gap-3">
            <button 
              v-for="amount in [5, 10, 25, 50]" 
              :key="amount"
              @click="selectedCKD = amount"
              class="py-3 px-4 rounded-xl border-2 transition-all flex flex-col items-center justify-center space-y-1"
              :class="selectedCKD === amount ? 'border-rose-500 bg-rose-50 dark:bg-rose-900/30 text-rose-700 dark:text-rose-300 shadow-md scale-[1.02]' : 'border-rose-100 dark:border-rose-800/30 bg-white dark:bg-slate-800/50 hover:border-rose-300 hover:bg-rose-50 dark:hover:bg-slate-700 hover:scale-[1.02]'"
            >
              <span class="text-xl font-bold">${{ amount }}</span>
            </button>
          </div>

          <div class="pt-2">
            <label class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Custom Amount</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span class="text-slate-400 sm:text-sm">$</span>
              </div>
              <input 
                type="number" 
                min="1"
                step="any"
                v-model="customCKD"
                @focus="selectedCKD = null"
                class="w-full pl-7 pr-4 py-2.5 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-rose-500 focus:border-rose-500 outline-none text-slate-900 dark:text-white transition-all shadow-sm"
                placeholder="0.00"
              />
            </div>
          </div>
        </div>

        <a 
          href="https://paypal.me/jwlankford"
          target="_blank"
          rel="noopener noreferrer"
          class="w-full mt-8 bg-gradient-to-r from-rose-500 via-pink-600 to-rose-600 hover:from-rose-600 hover:to-pink-700 text-white font-bold py-3.5 px-6 rounded-xl shadow-lg shadow-rose-500/30 transform hover:-translate-y-0.5 active:translate-y-0 transition-all flex items-center justify-center space-x-2 cursor-pointer"
        >
          <span>Support Health {{ displayCKD }}</span>
        </a>

      </div>

    </div>

    <!-- Kidney Donation Section -->
    <div class="max-w-3xl mx-auto mb-16 text-center bg-rose-50/50 dark:bg-rose-900/10 border border-rose-200/50 dark:border-rose-800/30 rounded-2xl p-8">
      <h5 class="text-lg font-bold text-rose-700 dark:text-rose-400 mb-2">Interested in becoming a living kidney donor?</h5>
      <p class="text-sm text-slate-600 dark:text-slate-400 mb-6">
        Living donation is a powerful way to help. If you're interested in learning more or exploring this incredible gift, please reach out directly.
      </p>
      <a 
        href="mailto:jwlankford@gmail.com?subject=Interested%20in%20Kidney%20Donation" 
        class="inline-flex items-center justify-center space-x-2 bg-white dark:bg-slate-800 hover:bg-rose-50 dark:hover:bg-slate-700 border-2 border-rose-300 dark:border-rose-700 text-rose-700 dark:text-rose-400 font-bold py-3 px-8 rounded-xl transition-all cursor-pointer shadow-sm"
      >
        <svg class="w-5 h-5 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <span>Inquire About Kidney Donation</span>
      </a>
    </div>

    <!-- Security Footer -->
    <div class="mt-8 text-center border-t border-slate-200 dark:border-slate-800 pt-6">
      <p class="text-sm text-slate-500 dark:text-slate-400 italic">
        Payments are securely processed. We do not store your payment information on our servers.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// State for Academic Support
const selectedAcademic = ref<number | null>(10);
const customAcademic = ref<string>('');

const displayAcademic = computed(() => {
  if (selectedAcademic.value !== null) {
    return `($${selectedAcademic.value})`;
  }
  const parsed = parseFloat(customAcademic.value);
  if (!isNaN(parsed) && parsed > 0) {
    return `($${parsed.toFixed(2)})`;
  }
  return '';
});

// State for CKD Support
const selectedCKD = ref<number | null>(10);
const customCKD = ref<string>('');

const displayCKD = computed(() => {
  if (selectedCKD.value !== null) {
    return `($${selectedCKD.value})`;
  }
  const parsed = parseFloat(customCKD.value);
  if (!isNaN(parsed) && parsed > 0) {
    return `($${parsed.toFixed(2)})`;
  }
  return '';
});

const paypalLinkAcademic = computed(() => {
  let amount = 0;
  if (selectedAcademic.value !== null) {
    amount = selectedAcademic.value;
  } else {
    const parsed = parseFloat(customAcademic.value);
    if (!isNaN(parsed) && parsed > 0) {
      amount = parsed;
    }
  }
  return amount > 0 ? `https://paypal.me/jwlankford/${amount}` : 'https://paypal.me/jwlankford';
});

const paypalLinkCKD = computed(() => {
  let amount = 0;
  if (selectedCKD.value !== null) {
    amount = selectedCKD.value;
  } else {
    const parsed = parseFloat(customCKD.value);
    if (!isNaN(parsed) && parsed > 0) {
      amount = parsed;
    }
  }
  return amount > 0 ? `https://paypal.me/jwlankford/${amount}` : 'https://paypal.me/jwlankford';
});
</script>
