// Thin API layer over the Flask backend. Kept separate from components so the
// network contract lives in one place.

const API_BASE = import.meta.env?.VITE_API_BASE ?? ''

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

/** Normalise the backend payload into the shape the store expects. */
export function normalisePrediction(payload) {
  if (!payload || typeof payload !== 'object') {
    throw new ApiError('The server returned an unreadable response.', 0)
  }
  if (payload.error) throw new ApiError(payload.error, 0)
  if (!payload.prediction) {
    throw new ApiError('The server response contained no prediction.', 0)
  }
  return {
    prediction: payload.prediction,
    confidence: typeof payload.confidence === 'number' ? payload.confidence : null,
    probabilities: payload.probabilities ?? null,
    model: payload.model ?? 'unknown',
    elapsedMs: typeof payload.elapsed_ms === 'number' ? payload.elapsed_ms : null,
  }
}

/** POST an image to the classifier and return a normalised prediction. */
export async function predictImage(file, { signal } = {}) {
  const body = new FormData()
  body.append('image', file)

  let response
  try {
    response = await fetch(`${API_BASE}/api/predict`, { method: 'POST', body, signal })
  } catch (cause) {
    throw new ApiError('Could not reach the server. Check your connection.', 0, {
      cause,
    })
  }

  if (!response.ok) {
    let detail = `Server responded with ${response.status}.`
    try {
      const payload = await response.json()
      if (payload?.error) detail = payload.error
    } catch {
      // Non-JSON error body: keep the status based message.
    }
    throw new ApiError(detail, response.status)
  }

  return normalisePrediction(await response.json())
}

/** Ask the backend whether it is up and whether the model is loaded. */
export async function fetchHealth({ signal } = {}) {
  try {
    const response = await fetch(`${API_BASE}/api/health`, { signal })
    if (!response.ok) return { ok: false, modelLoaded: false }
    const payload = await response.json()
    return { ok: true, modelLoaded: Boolean(payload?.model_loaded) }
  } catch {
    return { ok: false, modelLoaded: false }
  }
}
