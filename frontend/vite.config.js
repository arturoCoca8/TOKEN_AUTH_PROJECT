import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: [
      '5173-i3gclw5szkpzqwsq228x3-941dbb97.manusvm.computer',
      'localhost'
    ]
  }
})

