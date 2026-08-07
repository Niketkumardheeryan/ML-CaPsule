import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const MAX_HISTORY = 20

/**
 * Status machine
 *
 *   idle ──selectFile──> ready ──startPrediction──> loading ──> success | error
 *                                     │
 *                                     └──(offline)──> queued ──(reconnect)──> loading
 *
 * `history` and `theme` survive reloads (and work offline); the selected file
 * and its object URL deliberately do not.
 */
export const initialState = {
  theme: 'light',
  status: 'idle',
  file: null,
  previewUrl: null,
  result: null,
  error: null,
  history: [],
  queuedAt: null,
}

export const createStore = (set, get) => ({
  ...initialState,

  toggleTheme: () =>
    set((state) => ({ theme: state.theme === 'dark' ? 'light' : 'dark' })),

  setTheme: (theme) => set({ theme: theme === 'dark' ? 'dark' : 'light' }),

  selectFile: (file, previewUrl = null) =>
    set({
      file: file ? { name: file.name, size: file.size, type: file.type } : null,
      previewUrl,
      status: file ? 'ready' : 'idle',
      result: null,
      error: null,
      queuedAt: null,
    }),

  clearSelection: () =>
    set({
      file: null,
      previewUrl: null,
      status: 'idle',
      result: null,
      error: null,
      queuedAt: null,
    }),

  startPrediction: () => set({ status: 'loading', error: null }),

  queueOffline: (now = Date.now()) => set({ status: 'queued', queuedAt: now }),

  predictionSucceeded: (result, now = Date.now()) => {
    const entry = {
      id: `${now}-${Math.random().toString(36).slice(2, 8)}`,
      prediction: result.prediction,
      confidence: result.confidence ?? null,
      probabilities: result.probabilities ?? null,
      model: result.model ?? 'unknown',
      elapsedMs: result.elapsedMs ?? null,
      fileName: get().file?.name ?? 'image',
      at: now,
    }
    set((state) => ({
      status: 'success',
      result: entry,
      error: null,
      queuedAt: null,
      history: [entry, ...state.history].slice(0, MAX_HISTORY),
    }))
    return entry
  },

  predictionFailed: (message) =>
    set({ status: 'error', error: message || 'Prediction failed.', queuedAt: null }),

  clearHistory: () => set({ history: [] }),

  removeFromHistory: (id) =>
    set((state) => ({ history: state.history.filter((entry) => entry.id !== id) })),
})

export const usePredictionStore = create(
  persist(createStore, {
    name: 'bc-detect-store',
    // Only durable, serialisable state is persisted: an object URL would be
    // dead on the next load and a File cannot be serialised at all.
    partialize: (state) => ({ theme: state.theme, history: state.history }),
  })
)

export default usePredictionStore
