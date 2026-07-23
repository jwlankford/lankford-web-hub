<script setup lang="ts">
</script>

<template>
  <section class="py-12 border-t border-slate-200 dark:border-slate-800">
    <div class="max-w-4xl mx-auto bg-white dark:bg-slate-900 p-8 sm:p-10 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-2xl relative overflow-hidden transition-colors">
      <div class="absolute bottom-0 right-0 w-64 h-64 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="grid grid-cols-1 md:grid-cols-12 gap-8 items-center relative z-10">
        <!-- Author Avatar Image -->
        <div class="md:col-span-4 flex justify-center">
          <img
            src="/jeremy-lankford.jpg"
            alt="Jeremy Lankford"
            class="w-32 h-32 rounded-2xl object-cover shadow-2xl ring-4 ring-blue-500/30"
          />
        </div>

        <!-- Author Bio Details -->
        <div class="md:col-span-8 space-y-4 text-center md:text-left">
          <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-blue-400 text-xs font-mono border border-blue-300 dark:border-blue-500/30">
            <span>ABOUT THE INSTRUCTOR</span>
          </div>

          <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Jeremy Lankford</h2>
          <p class="text-sm font-mono text-cyan-700 dark:text-cyan-400">Senior Software Architect, Premier Instructor & PhD in IT (AI Focus) student at University of the Cumberlands</p>

          <p class="text-slate-600 dark:text-slate-300 text-sm leading-relaxed">
            Jeremy Lankford leads engineering teams building mission-critical distributed systems and multi-tenant cloud platforms. As a premier Udemy instructor, he teaches advanced system design, database isolation patterns, metaprogramming abstractions, and AI guardrails to thousands of software engineers worldwide.
          </p>

          <!-- Social Media Contact Links -->
          <div class="flex flex-wrap items-center justify-center md:justify-start gap-3 pt-1">
            <a 
              href="http://www.linkedin.com/in/jwlankford" 
              target="_blank" 
              rel="noopener noreferrer"
              class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-mono bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-500/30 hover:bg-blue-100 dark:hover:bg-blue-900 transition-colors"
              title="LinkedIn Profile"
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
              class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-mono bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-slate-300 dark:border-slate-700 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
              title="X (Twitter) Profile"
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
              class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-mono bg-blue-50 dark:bg-blue-950/60 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-500/30 hover:bg-blue-100 dark:hover:bg-indigo-900 transition-colors"
              title="Facebook Profile"
            >
              <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 24 24">
                <path d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H7.5v-3H10V9.69c0-2.47 1.47-3.83 3.72-3.83 1.08 0 2.2.19 2.2.19v2.42h-1.24c-1.23 0-1.61.76-1.61 1.54V12h2.73l-.44 3h-2.29v6.8c4.56-.93 8-4.96 8-9.8z"/>
              </svg>
              <span>Facebook</span>
            </a>

            <a 
              href="https://www.udemy.com/user/jeremy-lankford-22/" 
              target="_blank" 
              rel="noopener noreferrer"
              class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-mono bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-500/30 hover:bg-indigo-100 dark:hover:bg-indigo-900 transition-colors"
              title="Udemy Instructor Profile"
            >
              <svg class="w-4 h-4 text-indigo-650 dark:text-indigo-405" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 15c-2.76 0-5-2.24-5-5V7h2v5c0 1.66 1.34 3 3 3s3-1.34 3-3V7h2v5c0 2.76-2.24 5-5 5z"/>
              </svg>
              <span>Udemy</span>
            </a>
          </div>

          <div class="pt-2 flex flex-wrap items-center justify-center md:justify-start gap-4 text-xs font-mono">
            <span class="text-slate-500 dark:text-slate-400">Domain: <strong class="text-slate-900 dark:text-white">jeremylankford.com</strong></span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
