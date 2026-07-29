<script setup lang="ts">
import { ref } from 'vue';
import { submitContactMessage } from '../services/api';
import logoUrl from '../assets/logo.png';
import logoDarkUrl from '../assets/logo-dark.png';

const name = ref('');
const email = ref('');
const subject = ref('General Inquiry');
const message = ref('');

const isSubmitting = ref(false);
const isSuccess = ref(false);
const errorMessage = ref('');

async function handleSubmit() {
  if (!name.value || !email.value || !message.value) {
    errorMessage.value = 'Please fill out all required fields.';
    return;
  }
  
  isSubmitting.value = true;
  errorMessage.value = '';
  
  try {
    const res = await submitContactMessage({
      name: name.value,
      email: email.value,
      subject: subject.value,
      message: message.value
    });
    
    if (res.success) {
      isSuccess.value = true;
      // Reset form fields
      name.value = '';
      email.value = '';
      subject.value = 'General Inquiry';
      message.value = '';
      
      // Auto clear success banner after 6 seconds
      setTimeout(() => {
        isSuccess.value = false;
      }, 6000);
    } else {
      errorMessage.value = res.message;
    }
  } catch (err: any) {
    errorMessage.value = err.message || 'An error occurred while sending your message.';
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-8 sm:p-10 rounded-3xl shadow-xl max-w-4xl mx-auto relative overflow-hidden transition-colors">
    <div class="absolute top-0 left-0 w-32 h-32 bg-blue-600/10 rounded-full blur-2xl pointer-events-none"></div>

    <div class="relative z-10 space-y-6">
      <div class="space-y-2 text-center sm:text-left">
        <div class="flex items-center justify-center sm:justify-start space-x-3 mb-1">
          <img 
            :src="logoUrl" 
            alt="Jeremy Lankford Logo" 
            class="h-11 sm:h-13 w-auto object-contain dark:hidden filter drop-shadow-sm"
          />
          <img 
            :src="logoDarkUrl" 
            alt="Jeremy Lankford Logo" 
            class="h-11 sm:h-13 w-auto object-contain hidden dark:block filter drop-shadow-[0_0_12px_rgba(56,189,248,0.4)]"
          />
          <span class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-cyan-300 text-xs font-mono border border-blue-300 dark:border-blue-500/30">
            <span>CONTACT FORM</span>
          </span>
        </div>
        <h3 class="text-2xl font-bold font-serif text-slate-900 dark:text-white">Get in Touch</h3>
        <p class="text-slate-655 dark:text-slate-400 text-xs font-mono">
          Have questions regarding the ADLC curriculum, enterprise consulting opportunities, or academic collaborations? Drop a message below.
        </p>
      </div>

      <!-- Success Notification banner -->
      <div 
        v-if="isSuccess"
        class="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/65 border border-emerald-300 dark:border-emerald-500/40 text-emerald-800 dark:text-emerald-300 text-xs font-mono flex items-center space-x-2.5 animate-fadeIn"
      >
        <svg class="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>Thank you! Your message was sent successfully. I will get back to you shortly.</span>
      </div>

      <!-- Error banner -->
      <div 
        v-if="errorMessage"
        class="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/65 border border-rose-300 dark:border-rose-500/40 text-rose-800 dark:text-rose-300 text-xs font-mono flex items-center space-x-2.5 animate-fadeIn"
      >
        <svg class="w-5 h-5 text-rose-600 dark:text-rose-450 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ errorMessage }}</span>
      </div>

      <!-- Contact input form -->
      <form @submit.prevent="handleSubmit" class="space-y-4 font-mono text-xs">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <!-- Name Field -->
          <div class="space-y-1.5">
            <label for="name" class="block text-slate-700 dark:text-slate-350 font-semibold uppercase tracking-wider">Your Name <span class="text-rose-500">*</span></label>
            <input 
              v-model="name"
              id="name"
              type="text" 
              placeholder="e.g. John Doe"
              required
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30 transition-all shadow-inner"
            />
          </div>

          <!-- Email Field -->
          <div class="space-y-1.5">
            <label for="email" class="block text-slate-700 dark:text-slate-350 font-semibold uppercase tracking-wider">Your Email <span class="text-rose-500">*</span></label>
            <input 
              v-model="email"
              id="email"
              type="email" 
              placeholder="e.g. john@example.com"
              required
              class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30 transition-all shadow-inner"
            />
          </div>
        </div>

        <!-- Subject Select -->
        <div class="space-y-1.5">
          <label for="subject" class="block text-slate-700 dark:text-slate-350 font-semibold uppercase tracking-wider">Subject</label>
          <select 
            v-model="subject"
            id="subject"
            class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-slate-900 dark:text-slate-100 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30 transition-all shadow-inner"
          >
            <option value="General Inquiry">General Inquiry</option>
            <option value="Udemy Course Support">Udemy Course Support / ADLC Questions</option>
            <option value="Enterprise Consulting">Enterprise Architectural Consulting</option>
            <option value="Academic Collaboration">Academic Research Collaborations</option>
          </select>
        </div>

        <!-- Message Body -->
        <div class="space-y-1.5">
          <label for="message" class="block text-slate-700 dark:text-slate-350 font-semibold uppercase tracking-wider">Message <span class="text-rose-500">*</span></label>
          <textarea 
            v-model="message"
            id="message"
            rows="5"
            placeholder="Type your message details here..."
            required
            class="w-full bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-800 rounded-xl px-4 py-3 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30 transition-all shadow-inner"
          ></textarea>
        </div>

        <!-- Submit Button -->
        <div class="pt-2 flex justify-end">
          <button 
            type="submit"
            :disabled="isSubmitting"
            class="px-6 py-3.5 bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-500 hover:to-indigo-650 text-white font-bold rounded-xl shadow-lg shadow-blue-600/20 border border-blue-400/20 transition-all transform hover:-translate-y-0.5 active:translate-y-0 flex items-center space-x-2 text-xs uppercase tracking-wider"
          >
            <span v-if="isSubmitting">Sending Message...</span>
            <span v-else>Send Message</span>
            <svg 
              v-if="!isSubmitting" 
              class="w-3.5 h-3.5" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
            </svg>
            <div 
              v-else 
              class="animate-spin w-3 h-3 border-2 border-white border-t-transparent rounded-full"
            ></div>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
