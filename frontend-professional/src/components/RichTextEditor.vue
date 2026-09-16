<script setup lang="ts">
import { ref, onBeforeUnmount, watch } from 'vue';
import { useEditor, EditorContent } from '@tiptap/vue-3';
import StarterKit from '@tiptap/starter-kit';
import Placeholder from '@tiptap/extension-placeholder';
import Underline from '@tiptap/extension-underline';

const props = defineProps<{
  modelValue: string;
  placeholder?: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();

const isFullscreen = ref(false);

const editor = useEditor({
  content: props.modelValue,
  extensions: [
    StarterKit,
    Underline,
    Placeholder.configure({
      placeholder: props.placeholder || 'Write something...',
    }),
  ],
  onUpdate: () => {
    // Emit HTML changes to v-model parent
    if (editor.value) {
      emit('update:modelValue', editor.value.getHTML());
    }
  },
});

// Watch for external modelValue changes
watch(() => props.modelValue, (newVal) => {
  if (!editor.value) return;
  const isSame = editor.value.getHTML() === newVal;
  if (!isSame) {
    editor.value.commands.setContent(newVal || '', false);
  }
});

function handleHeadingChange(event: Event) {
  const target = event.target as HTMLSelectElement;
  const val = target.value;
  if (!editor.value) return;
  if (val === 'p') {
    editor.value.chain().focus().setParagraph().run();
  } else {
    const level = parseInt(val) as 1 | 2 | 3 | 4 | 5 | 6;
    editor.value.chain().focus().toggleHeading({ level }).run();
  }
}

function toggleFullscreen() {
  isFullscreen.value = !isFullscreen.value;
}

onBeforeUnmount(() => {
  editor.value?.destroy();
});
</script>

<template>
  <Teleport to="body" :disabled="!isFullscreen">
    <div v-if="isFullscreen" class="fixed inset-0 z-[60] bg-slate-950/70 backdrop-blur-sm animate-fadeIn" @click="toggleFullscreen"></div>
    <div 
      :class="[
        'border border-slate-300 dark:border-slate-700 rounded-lg overflow-hidden bg-slate-50 dark:bg-slate-950 focus-within:border-blue-500 transition-all flex flex-col',
        isFullscreen ? 'fixed inset-4 sm:inset-10 z-[70] shadow-2xl bg-white dark:bg-slate-900 animate-fadeIn' : 'relative'
      ]"
    >
      <!-- Toolbar -->
      <div v-if="editor" class="flex items-center justify-between p-1.5 bg-slate-100 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 text-xs select-none flex-wrap gap-1">
        <div class="flex items-center space-x-2.5">
          <select 
            class="p-1 rounded bg-transparent hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 border border-transparent hover:border-slate-300 dark:hover:border-slate-700 outline-none text-xs font-medium cursor-pointer transition-colors"
            @change="handleHeadingChange"
            :value="
              editor.isActive('heading', { level: 1 }) ? '1' : 
              editor.isActive('heading', { level: 2 }) ? '2' : 
              editor.isActive('heading', { level: 3 }) ? '3' : 'p'
            "
          >
            <option value="p">Normal Text</option>
            <option value="1">Heading 1</option>
            <option value="2">Heading 2</option>
            <option value="3">Heading 3</option>
          </select>
          <div class="w-px h-4 bg-slate-300 dark:bg-slate-700"></div>
          <button 
            type="button" 
            @click="editor.chain().focus().toggleBold().run()"
            :class="[
              'p-1 rounded cursor-pointer font-bold w-6 h-6 flex items-center justify-center border border-transparent hover:border-slate-300 dark:hover:border-slate-700 transition-colors',
              editor.isActive('bold') ? 'bg-slate-300 dark:bg-slate-700 text-blue-600 dark:text-cyan-400 shadow-inner' : 'hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300'
            ]"
            title="Bold"
          >
            B
          </button>
          <button 
            type="button" 
            @click="editor.chain().focus().toggleItalic().run()"
            :class="[
              'p-1 rounded cursor-pointer italic w-6 h-6 flex items-center justify-center border border-transparent hover:border-slate-300 dark:hover:border-slate-700 transition-colors',
              editor.isActive('italic') ? 'bg-slate-300 dark:bg-slate-700 text-blue-600 dark:text-cyan-400 shadow-inner' : 'hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300'
            ]"
            title="Italic"
          >
            I
          </button>
          <button 
            type="button" 
            @click="editor.chain().focus().toggleUnderline().run()"
            :class="[
              'p-1 rounded cursor-pointer underline w-6 h-6 flex items-center justify-center border border-transparent hover:border-slate-300 dark:hover:border-slate-700 transition-colors',
              editor.isActive('underline') ? 'bg-slate-300 dark:bg-slate-700 text-blue-600 dark:text-cyan-400 shadow-inner' : 'hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300'
            ]"
            title="Underline"
          >
            U
          </button>
          <button 
            type="button" 
            @click="editor.chain().focus().toggleStrike().run()"
            :class="[
              'p-1 rounded cursor-pointer line-through w-6 h-6 flex items-center justify-center border border-transparent hover:border-slate-300 dark:hover:border-slate-700 transition-colors',
              editor.isActive('strike') ? 'bg-slate-300 dark:bg-slate-700 text-blue-600 dark:text-cyan-400 shadow-inner' : 'hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300'
            ]"
            title="Strike"
          >
            S
          </button>
          <div class="w-px h-4 bg-slate-300 dark:bg-slate-700"></div>
          <button 
            type="button" 
            @click="editor.chain().focus().toggleBulletList().run()"
            :class="[
              'p-1 rounded cursor-pointer w-6 h-6 flex items-center justify-center border border-transparent hover:border-slate-300 dark:hover:border-slate-700 text-base leading-none transition-colors',
              editor.isActive('bulletList') ? 'bg-slate-300 dark:bg-slate-700 text-blue-600 dark:text-cyan-400 shadow-inner' : 'hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300'
            ]"
            title="Bullet List"
          >
            •
          </button>
          <button 
            type="button" 
            @click="editor.chain().focus().toggleOrderedList().run()"
            :class="[
              'p-1 rounded cursor-pointer w-6 h-6 flex items-center justify-center border border-transparent hover:border-slate-300 dark:hover:border-slate-700 font-mono transition-colors',
              editor.isActive('orderedList') ? 'bg-slate-300 dark:bg-slate-700 text-blue-600 dark:text-cyan-400 shadow-inner' : 'hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300'
            ]"
            title="Numbered List"
          >
            1.
          </button>
          <div class="w-px h-4 bg-slate-300 dark:bg-slate-700"></div>
          <button 
            type="button" 
            @click="editor.chain().focus().clearNodes().unsetAllMarks().run()"
            class="p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-750 dark:text-slate-300 cursor-pointer w-6 h-6 flex items-center justify-center border border-transparent hover:border-slate-300 dark:hover:border-slate-700 font-mono transition-colors"
            title="Clear Format"
          >
            Tx
          </button>
        </div>
        
        <button 
          type="button" 
          @click="toggleFullscreen" 
          class="p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 cursor-pointer w-6 h-6 flex items-center justify-center border border-transparent hover:border-slate-300 dark:hover:border-slate-700 ml-auto transition-colors"
          :title="isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'"
        >
          <svg v-if="!isFullscreen" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/></svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
      <!-- Editable Content Area -->
      <editor-content 
        :editor="editor" 
        :class="[
          'p-3 overflow-y-auto outline-none text-slate-900 dark:text-slate-100 text-sm font-sans focus:outline-none flex-grow tiptap-wrapper',
          isFullscreen ? 'h-full min-h-0 max-h-none' : 'min-h-[70px] max-h-[160px]'
        ]" 
      />
    </div>
  </Teleport>
</template>

<style>
/* Tiptap removes the outline on focus internally if we use ProseMirror-focused, but we should make sure */
.tiptap-wrapper .ProseMirror {
  outline: none;
  min-height: 100%;
}
.tiptap-wrapper .ProseMirror p.is-editor-empty:first-child::before {
  color: #94a3b8; /* slate-400 */
  content: attr(data-placeholder);
  float: left;
  height: 0;
  pointer-events: none;
  font-style: italic;
}
/* Basic styles for Tiptap */
.tiptap-wrapper .ProseMirror ul {
  list-style-type: disc;
  padding-left: 1.5rem;
  margin-top: 0.25rem;
  margin-bottom: 0.25rem;
}
.tiptap-wrapper .ProseMirror ol {
  list-style-type: decimal;
  padding-left: 1.5rem;
  margin-top: 0.25rem;
  margin-bottom: 0.25rem;
}
.tiptap-wrapper .ProseMirror h1 {
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1.2;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}
.tiptap-wrapper .ProseMirror h2 {
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.3;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}
.tiptap-wrapper .ProseMirror h3 {
  font-size: 1.125rem;
  font-weight: 600;
  line-height: 1.4;
  margin-top: 0.75rem;
  margin-bottom: 0.5rem;
}
.tiptap-wrapper .ProseMirror p {
  margin-bottom: 0.5rem;
}
.tiptap-wrapper .ProseMirror p:last-child {
  margin-bottom: 0;
}
</style>
