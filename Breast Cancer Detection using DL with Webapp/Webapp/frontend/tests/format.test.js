import { describe, expect, it } from 'vitest'

import {
  MAX_FILE_BYTES,
  formatBytes,
  formatConfidence,
  formatRelativeTime,
  rankProbabilities,
  toneForPrediction,
  validateImageFile,
} from '../src/lib/format.js'

describe('formatConfidence', () => {
  it('renders a probability as a percentage', () => {
    expect(formatConfidence(0.9312)).toBe('93.1%')
    expect(formatConfidence(1)).toBe('100.0%')
    expect(formatConfidence(0)).toBe('0.0%')
  })

  it('clamps values that fall outside 0..1', () => {
    expect(formatConfidence(1.4)).toBe('100.0%')
    expect(formatConfidence(-0.2)).toBe('0.0%')
  })

  it('degrades gracefully on bad input', () => {
    expect(formatConfidence(undefined)).toBe('—')
    expect(formatConfidence(Number.NaN)).toBe('—')
    expect(formatConfidence('0.9')).toBe('—')
  })
})

describe('formatBytes', () => {
  it('scales through the units', () => {
    expect(formatBytes(512)).toBe('512 B')
    expect(formatBytes(2048)).toBe('2.0 KB')
    expect(formatBytes(5 * 1024 * 1024)).toBe('5.0 MB')
  })

  it('rejects nonsense', () => {
    expect(formatBytes(-1)).toBe('—')
    expect(formatBytes('big')).toBe('—')
  })
})

describe('formatRelativeTime', () => {
  const now = new Date('2026-08-01T12:00:00Z').getTime()

  it('describes recent moments', () => {
    expect(formatRelativeTime(now - 5_000, now)).toBe('just now')
    expect(formatRelativeTime(now - 12 * 60_000, now)).toBe('12 min ago')
    expect(formatRelativeTime(now - 3 * 3_600_000, now)).toBe('3 h ago')
    expect(formatRelativeTime(now - 2 * 86_400_000, now)).toBe('2 d ago')
  })

  it('handles a missing timestamp', () => {
    expect(formatRelativeTime(null, now)).toBe('—')
  })
})

describe('toneForPrediction', () => {
  it('marks malignant as the highest severity', () => {
    expect(toneForPrediction('Malignant').severity).toBe('high')
    expect(toneForPrediction('Benign').severity).toBe('medium')
    expect(toneForPrediction('Normal').severity).toBe('low')
  })

  it('falls back for an unexpected label', () => {
    const tone = toneForPrediction('Something else')
    expect(tone.severity).toBe('unknown')
    expect(tone.label).toBe('Something else')
  })
})

describe('validateImageFile', () => {
  const file = (type, size) => ({ name: 'scan.png', type, size })

  it('accepts supported image types within the size limit', () => {
    expect(validateImageFile(file('image/png', 1024)).ok).toBe(true)
    expect(validateImageFile(file('image/jpeg', 1024)).ok).toBe(true)
  })

  it('rejects an unsupported type', () => {
    const result = validateImageFile(file('application/pdf', 1024))
    expect(result.ok).toBe(false)
    expect(result.error).toMatch(/Unsupported format/)
  })

  it('rejects a file over the size limit', () => {
    const result = validateImageFile(file('image/png', MAX_FILE_BYTES + 1))
    expect(result.ok).toBe(false)
    expect(result.error).toMatch(/limit is/)
  })

  it('rejects a missing file', () => {
    expect(validateImageFile(null).ok).toBe(false)
  })
})

describe('rankProbabilities', () => {
  it('sorts classes from most to least likely', () => {
    expect(
      rankProbabilities({ Benign: 0.2, Malignant: 0.7, Normal: 0.1 })
    ).toEqual([
      ['Malignant', 0.7],
      ['Benign', 0.2],
      ['Normal', 0.1],
    ])
  })

  it('drops non-numeric entries and tolerates nothing at all', () => {
    expect(rankProbabilities({ Benign: 0.5, Broken: 'x' })).toEqual([['Benign', 0.5]])
    expect(rankProbabilities(null)).toEqual([])
  })
})
