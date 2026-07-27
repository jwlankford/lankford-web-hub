<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';

const props = defineProps<{
  modelValue: string;
  placeholder?: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();

const editorRef = ref<HTMLDivElement | null>(null);

// Watch for external value changes
watch(() => props.modelValue, (newVal) => {
  if (editorRef.value && editorRef.value.innerHTML !== newVal) {
    editorRef.value.innerHTML = newVal || '';
  }
});

function handleInput() {
  if (editorRef.value) {
    emit('update:modelValue', editorRef.value.innerHTML);
  }
}

function format(command: string, value: string = '') {
  document.execCommand(command, false, value);
  handleInput();
}

onMounted(() => {
  if (editorRef.value) {
    editorRef.value.innerHTML = props.modelValue || '';
  }
});
</script>

<template>
  <div class="border border-slate-300 dark:border-slate-700 rounded-lg overflow-hidden bg-slate-50 dark:bg-slate-950 focus-within:border-blue-500 transition-colors">
    <!-- Toolbar -->
    <div class="flex items-center space-x-2.5 p-1.5 bg-slate-100 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 text-xs select-none">
      <button 
        type="button" 
        @click="format('bold')" 
        class="p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 cursor-pointer font-bold w-6 h-6 flex items-center justify-center border border-transparent hover:border-slate-300 dark:hover:border-slate-700"
        title="Bold"
      >
        B
      </button>
      <button 
        type="button" 
        @click="format('italic')" 
        class="p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 cursor-pointer italic w-6 h-6 flex items-center justify-center border border-transparent hover:border-slate-300 dark:hover:border-slate-700"
        title="Italic"
      >
        I
      </button>
      <button 
        type="button" 
        @click="format('underline')" 
        class="p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 cursor-pointer underline w-6 h-6 flex items-center justify-center border border-transparent hover:border-slate-300 dark:hover:border-slate-700"
        title="Underline"
      >
        U
      </button>
      <div class="w-px h-4 bg-slate-300 dark:bg-slate-700"></div>
      <button 
        type="button" 
        @click="format('insertUnorderedList')" 
        class="p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 cursor-pointer w-6 h-6 flex items-center justify-center border border-transparent hover:border-slate-300 dark:hover:border-slate-700 text-base leading-none"
        title="Bullet List"
      >
        •
      </button>
      <button 
        type="button" 
        @click="format('insertOrderedList')" 
        class="p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 cursor-pointer w-6 h-6 flex items-center justify-center border border-transparent hover:border-slate-300 dark:hover:border-slate-700 font-mono"
        title="Numbered List"
      >
        1.
      </button>
      <div class="w-px h-4 bg-slate-300 dark:bg-slate-700"></div>
      <button 
        type="button" 
        @click="format('removeFormat')" 
        class="p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-750 dark:text-slate-300 cursor-pointer w-6 h-6 flex items-center justify-center border border-transparent hover:border-slate-300 dark:hover:border-slate-700 font-mono"
        title="Clear Format"
      >
        Tx
      </button>
    </div>
    <!-- Editable Content Area -->
    <div 
      ref="editorRef"
      contenteditable="true"
      @input="handleInput"
      class="p-3 min-h-[70px] max-h-[160px] overflow-y-auto outline-none text-slate-900 dark:text-slate-100 text-sm font-sans focus:outline-none"
      :placeholder="placeholder"
    ></div>
  </div>
</template>

<style scoped>
[contenteditable="true"]:empty:before {
  content: attr(placeholder);
  color: #94a3b8; /* slate-400 */
  font-style: italic;
  pointer-events: none;
}
</style>
