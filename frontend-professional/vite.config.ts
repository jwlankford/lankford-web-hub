import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite' // <--- Add this import

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss() // <--- Activate the native compiler
  ],
  server: {
    port: 5173
  }
})