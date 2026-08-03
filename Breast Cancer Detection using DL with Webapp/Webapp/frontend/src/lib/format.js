// Pure helpers shared by the components. Kept free of React and of the store so
// they can be unit tested directly.

export const CLASS_NAMES = ['Benign', 'Malignant', 'Normal']

export const ACCEPTED_TYPES = ['image/png', 'image/jpeg', 'image/webp', 'image/bmp']

export const MAX_FILE_BYTES = 8 * 1024 * 1024 // 8 MB

/** Format a 0..1 probability as a percentage string. */
export function formatConfidence(value) {
  if (typeof value !== 'number' || Number.isNaN(value)) return '—'
  const clamped = Math.min(Math.max(value, 0), 1)
  return `${(clamped * 100).toFixed(1)}%`
}

/** Human readable file size. */
export function formatBytes(bytes) {
  if (typeof bytes !== 'number' || bytes < 0 || Number.isNaN(bytes)) return '—'
  if (bytes < 1024) return `${bytes} B`
  const units = ['KB', 'MB', 'GB']
  let value = bytes / 1024
  let unit = 0
  while (value >= 1024 && unit < units.length - 1) {
    value /= 1024
    unit += 1
  }
  return `${value.toFixed(1)} ${units[unit]}`
}

/** Short relative time such as "just now" or "12 min ago". */
export function formatRelativeTime(timestamp, now = Date.now()) {
  if (!timestamp) return '—'
  const seconds = Math.max(0, Math.round((now - timestamp) / 1000))
  if (seconds < 45) return 'just now'
  const minutes = Math.round(seconds / 60)
  if (minutes < 60) return `${minutes} min ago`
  const hours = Math.round(minutes / 60)
  if (hours < 24) return `${hours} h ago`
  const days = Math.round(hours / 24)
  return `${days} d ago`
}

/**
 * Map a predicted class to presentation tokens.
 * Malignant is deliberately the only "danger" tone so it stands out at a glance.
 */
export function toneForPrediction(prediction) {
  switch (prediction) {
    case 'Malignant':
      return {
        label: 'Malignant',
        severity: 'high',
        badge: 'bg-rose-100 text-rose-700 dark:bg-rose-500/15 dark:text-rose-300',
        bar: 'bg-rose-500',
        ring: 'ring-rose-500/40',
      }
    case 'Benign':
      return {
        label: 'Benign',
        severity: 'medium',
        badge: 'bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300',
        bar: 'bg-amber-500',
        ring: 'ring-amber-500/40',
      }
    case 'Normal':
      return {
        label: 'Normal',
        severity: 'low',
        badge:
          'bg-emerald-100 text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-300',
        bar: 'bg-emerald-500',
        ring: 'ring-emerald-500/40',
      }
    default:
      return {
        label: prediction || 'Unknown',
        severity: 'unknown',
        badge: 'bg-slate-100 text-slate-600 dark:bg-slate-500/15 dark:text-slate-300',
        bar: 'bg-slate-400',
        ring: 'ring-slate-400/40',
      }
  }
}

/** Validate a user supplied file before any upload is attempted. */
export function validateImageFile(file) {
  if (!file) return { ok: false, error: 'Choose an ultrasound image first.' }
  if (!ACCEPTED_TYPES.includes(file.type)) {
    return { ok: false, error: 'Unsupported format. Use PNG, JPEG, WebP or BMP.' }
  }
  if (file.size > MAX_FILE_BYTES) {
    return {
      ok: false,
      error: `Image is ${formatBytes(file.size)}. The limit is ${formatBytes(MAX_FILE_BYTES)}.`,
    }
  }
  return { ok: true, error: null }
}

/** Sort a probability map into descending [name, value] pairs. */
export function rankProbabilities(probabilities) {
  if (!probabilities || typeof probabilities !== 'object') return []
  return Object.entries(probabilities)
    .filter(([, value]) => typeof value === 'number' && !Number.isNaN(value))
    .sort((a, b) => b[1] - a[1])
}
