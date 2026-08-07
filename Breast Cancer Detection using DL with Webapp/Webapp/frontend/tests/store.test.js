import { beforeEach, describe, expect, it } from 'vitest'

import {
  MAX_HISTORY,
  initialState,
  usePredictionStore,
} from '../src/store/usePredictionStore.js'
import { ApiError, normalisePrediction } from '../src/lib/api.js'

// Merge rather than replace: a replacing setState would drop the actions too.
const reset = () => {
  usePredictionStore.setState({ ...initialState })
  localStorage.clear()
}
const state = () => usePredictionStore.getState()
const fakeFile = (name = 'scan.png') => ({ name, size: 2048, type: 'image/png' })

describe('theme', () => {
  beforeEach(reset)

  it('toggles between light and dark', () => {
    expect(state().theme).toBe('light')
    state().toggleTheme()
    expect(state().theme).toBe('dark')
    state().toggleTheme()
    expect(state().theme).toBe('light')
  })

  it('ignores an unknown theme name', () => {
    state().setTheme('neon')
    expect(state().theme).toBe('light')
  })
})

describe('selection', () => {
  beforeEach(reset)

  it('stores only serialisable file metadata', () => {
    state().selectFile(fakeFile(), 'blob:preview')
    expect(state().file).toEqual({ name: 'scan.png', size: 2048, type: 'image/png' })
    expect(state().previewUrl).toBe('blob:preview')
    expect(state().status).toBe('ready')
  })

  it('clears a previous error and result when a new file is chosen', () => {
    state().predictionFailed('boom')
    state().selectFile(fakeFile(), 'blob:preview')
    expect(state().error).toBeNull()
    expect(state().result).toBeNull()
  })

  it('returns to idle when the selection is cleared', () => {
    state().selectFile(fakeFile(), 'blob:preview')
    state().clearSelection()
    expect(state().status).toBe('idle')
    expect(state().file).toBeNull()
    expect(state().previewUrl).toBeNull()
  })
})

describe('prediction lifecycle', () => {
  beforeEach(reset)

  it('walks ready -> loading -> success', () => {
    state().selectFile(fakeFile(), 'blob:preview')
    state().startPrediction()
    expect(state().status).toBe('loading')

    state().predictionSucceeded({
      prediction: 'Benign',
      confidence: 0.91,
      probabilities: { Benign: 0.91, Malignant: 0.05, Normal: 0.04 },
      model: 'VGG16',
      elapsedMs: 120,
    })

    expect(state().status).toBe('success')
    expect(state().result.prediction).toBe('Benign')
    expect(state().result.fileName).toBe('scan.png')
    expect(state().history).toHaveLength(1)
  })

  it('records the failure message and leaves history untouched', () => {
    state().predictionFailed('Could not reach the server.')
    expect(state().status).toBe('error')
    expect(state().error).toBe('Could not reach the server.')
    expect(state().history).toHaveLength(0)
  })

  it('queues while offline and clears the queue on success', () => {
    state().selectFile(fakeFile(), 'blob:preview')
    state().queueOffline(1_000)
    expect(state().status).toBe('queued')
    expect(state().queuedAt).toBe(1_000)

    state().predictionSucceeded({ prediction: 'Normal' })
    expect(state().status).toBe('success')
    expect(state().queuedAt).toBeNull()
  })

  it('always supplies a fallback error message', () => {
    state().predictionFailed()
    expect(state().error).toBe('Prediction failed.')
  })
})

describe('history', () => {
  beforeEach(reset)

  it('keeps the newest entry first', () => {
    state().selectFile(fakeFile('first.png'), null)
    state().predictionSucceeded({ prediction: 'Benign' })
    state().selectFile(fakeFile('second.png'), null)
    state().predictionSucceeded({ prediction: 'Malignant' })

    expect(state().history.map((entry) => entry.fileName)).toEqual([
      'second.png',
      'first.png',
    ])
  })

  it(`caps at ${MAX_HISTORY} entries`, () => {
    for (let index = 0; index < MAX_HISTORY + 5; index += 1) {
      state().selectFile(fakeFile(`scan-${index}.png`), null)
      state().predictionSucceeded({ prediction: 'Normal' })
    }
    expect(state().history).toHaveLength(MAX_HISTORY)
    expect(state().history[0].fileName).toBe(`scan-${MAX_HISTORY + 4}.png`)
  })

  it('removes a single entry by id', () => {
    state().selectFile(fakeFile(), null)
    const entry = state().predictionSucceeded({ prediction: 'Benign' })
    state().removeFromHistory(entry.id)
    expect(state().history).toHaveLength(0)
  })

  it('clears everything', () => {
    state().selectFile(fakeFile(), null)
    state().predictionSucceeded({ prediction: 'Benign' })
    state().clearHistory()
    expect(state().history).toHaveLength(0)
  })
})

describe('normalisePrediction', () => {
  it('maps the backend payload onto the store shape', () => {
    expect(
      normalisePrediction({
        prediction: 'Malignant',
        confidence: 0.87,
        probabilities: { Malignant: 0.87 },
        model: 'VGG16',
        elapsed_ms: 143.2,
      })
    ).toEqual({
      prediction: 'Malignant',
      confidence: 0.87,
      probabilities: { Malignant: 0.87 },
      model: 'VGG16',
      elapsedMs: 143.2,
    })
  })

  it('raises when the payload carries an error or no prediction', () => {
    expect(() => normalisePrediction({ error: 'model missing' })).toThrow(ApiError)
    expect(() => normalisePrediction({})).toThrow(/no prediction/)
    expect(() => normalisePrediction(null)).toThrow(ApiError)
  })

  it('defaults optional fields rather than failing', () => {
    const result = normalisePrediction({ prediction: 'Normal' })
    expect(result.confidence).toBeNull()
    expect(result.model).toBe('unknown')
    expect(result.elapsedMs).toBeNull()
  })
})
