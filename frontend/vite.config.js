import { defineConfig } from 'vite';
import vue2 from '@vitejs/plugin-vue2';

export default defineConfig({
  plugins: [
    vue2(),
  ],
  resolve: {
    alias: {
      // Wajib: Menetapkan alias untuk Vue saat menggunakan Vue 2
      'vue': 'vue/dist/vue.esm.js', 
    },
  },
});