<script setup lang="ts">
import { ref, onBeforeUnmount } from 'vue';
import type { GoogleNotebook } from '../types';

const props = defineProps<{
  notebook: GoogleNotebook;
}>();

// Custom Audio Player State
const audioPlayer = ref<HTMLAudioElement | null>(null);
const isPlaying = ref(false);
const currentTime = ref(0);
const duration = ref(0);
const volume = ref(0.8);
const isMuted = ref(false);

function togglePlay() {
  if (!audioPlayer.value) return;
  if (isPlaying.value) {
    audioPlayer.value.pause();
  } else {
    audioPlayer.value.play().catch(err => console.error("Audio playback error:", err));
  }
}

function onPlayPause() {
  if (!audioPlayer.value) return;
  isPlaying.value = !audioPlayer.value.paused;
}

function onTimeUpdate() {
  if (!audioPlayer.value) return;
  currentTime.value = audioPlayer.value.currentTime;
}

function onLoadedMetadata() {
  if (!audioPlayer.value) return;
  duration.value = audioPlayer.value.duration;
}

function seekAudio(event: Event) {
  if (!audioPlayer.value) return;
  const input = event.target as HTMLInputElement;
  const targetTime = parseFloat(input.value);
  audioPlayer.value.currentTime = targetTime;
  currentTime.value = targetTime;
}

function toggleMute() {
  if (!audioPlayer.value) return;
  isMuted.value = !isMuted.value;
  audioPlayer.value.muted = isMuted.value;
}

function changeVolume(event: Event) {
  if (!audioPlayer.value) return;
  const input = event.target as HTMLInputElement;
  const targetVolume = parseFloat(input.value);
  volume.value = targetVolume;
  audioPlayer.value.volume = targetVolume;
  isMuted.value = targetVolume === 0;
  audioPlayer.value.muted = isMuted.value;
}

function formatTime(seconds: number): string {
  if (isNaN(seconds) || seconds === Infinity) return "0:00";
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
}

onBeforeUnmount(() => {
  if (audioPlayer.value) {
    audioPlayer.value.pause();
  }
});
</script>

<template>
  <div 
    class="group relative bg-white dark:bg-slate-900/60 rounded-2xl p-6 border border-slate-200 dark:border-slate-800/80 hover:border-blue-500/40 transition-all duration-350 shadow-md hover:shadow-xl dark:hover:shadow-blue-950/20 flex flex-col justify-between overflow-hidden"
  >
    <!-- Top glow element -->
    <div class="absolute -top-12 -right-12 w-24 h-24 bg-blue-600/10 dark:bg-blue-500/5 rounded-full blur-2xl group-hover:scale-150 transition-transform duration-500"></div>

    <div>
      <!-- Header Row -->
      <div class="flex items-center justify-between mb-4">
        <span class="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full bg-blue-50 dark:bg-blue-950/80 border border-blue-200 dark:border-blue-500/20 text-blue-800 dark:text-cyan-300 font-mono text-[10px] font-bold">
          <span>Google NotebookLM</span>
        </span>
        <span 
          v-if="notebook.sources_count"
          class="text-[10px] font-mono text-slate-500 dark:text-slate-400 font-semibold"
        >
          {{ notebook.sources_count }} source documents
        </span>
      </div>

      <!-- Title -->
      <h4 class="text-lg font-serif font-bold text-slate-900 dark:text-white leading-snug mb-2 group-hover:text-blue-600 dark:group-hover:text-cyan-300 transition-colors">
        {{ notebook.title }}
      </h4>

      <!-- Description -->
      <p class="text-xs text-slate-650 dark:text-slate-400 mb-6 leading-relaxed">
        {{ notebook.description }}
      </p>

      <!-- Sleek Custom Audio Player Component (If Audio URL is Present) -->
      <div 
        v-if="notebook.audio_url" 
        class="mb-6 p-4 rounded-xl bg-slate-50 dark:bg-slate-950/80 border border-slate-200 dark:border-slate-850/80 backdrop-blur-md flex flex-col space-y-3"
      >
        <audio 
          ref="audioPlayer" 
          :src="notebook.audio_url" 
          @play="onPlayPause" 
          @pause="onPlayPause" 
          @timeupdate="onTimeUpdate"
          @loadedmetadata="onLoadedMetadata"
          class="hidden"
        ></audio>

        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <!-- Play/Pause Button -->
            <button 
              @click="togglePlay"
              class="w-10 h-10 flex items-center justify-center rounded-full bg-blue-600 hover:bg-blue-500 dark:bg-blue-500/90 dark:hover:bg-blue-400 text-white shadow-md transition-all active:scale-95 cursor-pointer"
              :aria-label="isPlaying ? 'Pause Audio Overview' : 'Play Audio Overview'"
            >
              <svg v-if="!isPlaying" class="w-5 h-5 fill-current ml-0.5" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z"/>
              </svg>
              <svg v-else class="w-5 h-5 fill-current" viewBox="0 0 24 24">
                <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
              </svg>
            </button>
            
            <div class="leading-tight">
              <div class="text-[10px] font-bold text-slate-900 dark:text-white uppercase tracking-wider">Audio Overview</div>
              <div class="text-[9px] font-mono text-slate-400 dark:text-slate-500">AI Podcast Summary</div>
            </div>
          </div>

          <!-- Timer display -->
          <div class="text-[10px] font-mono text-slate-500 dark:text-slate-400">
            {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
          </div>
        </div>

        <!-- Custom Seeking Track Bar -->
        <div class="flex items-center space-x-2">
          <input 
            type="range" 
            min="0" 
            :max="duration || 100" 
            :value="currentTime" 
            @input="seekAudio"
            class="w-full h-1.5 rounded-lg bg-slate-200 dark:bg-slate-800 accent-blue-600 dark:accent-blue-500 cursor-pointer outline-none transition-colors"
          />
        </div>

        <!-- Volume controller row -->
        <div class="flex items-center justify-end space-x-2 pt-1 border-t border-slate-250/20 dark:border-slate-805/40">
          <button 
            @click="toggleMute"
            class="text-slate-400 dark:text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 transition-colors"
            title="Mute/Unmute"
          >
            <!-- Mute Icon -->
            <svg v-if="isMuted || volume === 0" class="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.21.05-.42.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.03c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>
            </svg>
            <!-- Volume Low -->
            <svg v-else-if="volume < 0.5" class="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M7 9v6h4l5 5V5l-5 5H7zm11.5 2c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02z"/>
            </svg>
            <!-- Volume High -->
            <svg v-else class="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M3 9v6h4l5 5V5l-5 5H7zm11.5 2c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
            </svg>
          </button>
          
          <input 
            type="range" 
            min="0" 
            max="1" 
            step="0.05"
            :value="isMuted ? 0 : volume" 
            @input="changeVolume"
            class="w-16 h-1 rounded bg-slate-200 dark:bg-slate-800 accent-blue-600 dark:accent-blue-500 cursor-pointer outline-none"
          />
        </div>
      </div>
    </div>

    <!-- Actions Footer -->
    <div class="pt-4 border-t border-slate-200 dark:border-slate-800/80 flex items-center justify-between text-xs mt-auto">
      <a 
        :href="notebook.notebook_url" 
        target="_blank" 
        rel="noopener noreferrer"
        class="font-mono text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-205 transition-colors flex items-center space-x-1"
      >
        <span>notebooklm.google.com</span>
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
        </svg>
      </a>

      <a 
        :href="notebook.notebook_url" 
        target="_blank" 
        rel="noopener noreferrer"
        class="px-3.5 py-1.5 font-semibold text-xs rounded-xl bg-blue-50 dark:bg-blue-950 text-blue-700 dark:text-cyan-400 hover:bg-blue-100 dark:hover:bg-blue-900 border border-blue-200 dark:border-blue-500/40 transition-colors flex items-center space-x-1.5 group/btn cursor-pointer"
      >
        <span>Open Notebook</span>
        <svg class="w-3.5 h-3.5 transform group-hover/btn:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"/>
        </svg>
      </a>
    </div>
  </div>
</template>

<style scoped>
/* Custom styling for inputs */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
}
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  height: 10px;
  width: 10px;
  border-radius: 50%;
  background: currentColor;
  cursor: pointer;
}
input[type="range"]::-moz-range-thumb {
  height: 10px;
  width: 10px;
  border-radius: 50%;
  background: currentColor;
  cursor: pointer;
  border: none;
}
</style>
