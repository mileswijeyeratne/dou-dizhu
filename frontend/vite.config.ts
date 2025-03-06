import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  base: "/",
  plugins: [react()],
  preview: {
    port: 8080,
    strictPort: true,
  },
  server: {
    watch: {
      usePolling: true,
    },
    port: 8080,
    strictPort: true,
    host: true,
    origin: "localhost:8080",
 },
})
