import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'

// The SPA is served by Flask under /app/ in production, so asset URLs must be
// prefixed. In dev, Vite serves from the root and proxies /api to Flask.
const BASE = '/app/'

export default defineConfig({
  base: BASE,
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icon-192.png', 'icon-512.png', 'apple-touch-icon.png'],
      manifest: {
        name: 'Breast Cancer Detection',
        short_name: 'BC Detect',
        description:
          'Offline-first ultrasound image analysis for breast cancer screening support.',
        theme_color: '#be185d',
        background_color: '#0f172a',
        display: 'standalone',
        orientation: 'portrait',
        start_url: BASE,
        scope: BASE,
        icons: [
          { src: 'icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'icon-512.png', sizes: '512x512', type: 'image/png' },
          {
            src: 'icon-512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable',
          },
        ],
      },
      workbox: {
        // Pre-cache the whole app shell so the UI opens with no network at all.
        globPatterns: ['**/*.{js,css,html,png,svg,webmanifest}'],
        navigateFallback: `${BASE}index.html`,
        runtimeCaching: [
          {
            // Predictions need the model, so never serve a stale one from cache;
            // fall through to the offline queue instead.
            urlPattern: /\/api\/predict$/,
            handler: 'NetworkOnly',
          },
          {
            urlPattern: /\/api\/health$/,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-health',
              networkTimeoutSeconds: 3,
              expiration: { maxEntries: 4, maxAgeSeconds: 300 },
            },
          },
        ],
      },
      devOptions: { enabled: false },
    }),
  ],
  server: {
    port: 5173,
    // Talk to the Flask app in dev without any CORS configuration.
    proxy: {
      '/api': { target: 'http://127.0.0.1:5000', changeOrigin: true },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
  test: {
    environment: 'jsdom',
    globals: true,
    include: ['tests/**/*.test.js'],
  },
})
