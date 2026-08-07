import {
  formatConfidence,
  rankProbabilities,
  toneForPrediction,
} from '../lib/format.js'
import { usePredictionStore } from '../store/usePredictionStore.js'

export default function ResultCard() {
  const status = usePredictionStore((state) => state.status)
  const result = usePredictionStore((state) => state.result)
  const queuedAt = usePredictionStore((state) => state.queuedAt)

  if (status === 'queued') {
    return (
      <section className="rounded-2xl border border-amber-300 bg-amber-50 p-5 dark:border-amber-500/30 dark:bg-amber-500/10">
        <h2 className="text-sm font-semibold text-amber-800 dark:text-amber-300">
          Queued
        </h2>
        <p className="mt-1 text-sm text-amber-700 dark:text-amber-200/80">
          You are offline, so this scan is waiting. It will be sent automatically the
          moment the connection returns.
        </p>
        {queuedAt ? (
          <p className="mt-2 text-xs text-amber-600 dark:text-amber-300/70">
            Queued at {new Date(queuedAt).toLocaleTimeString()}
          </p>
        ) : null}
      </section>
    )
  }

  if (status !== 'success' || !result) return null

  const tone = toneForPrediction(result.prediction)
  const ranked = rankProbabilities(result.probabilities)

  return (
    <section
      className={`rounded-2xl border border-slate-200 bg-white p-5 shadow-sm ring-1 sm:p-6 dark:border-slate-800 dark:bg-slate-900 ${tone.ring}`}
    >
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-sm font-semibold tracking-wide text-slate-500 uppercase dark:text-slate-400">
          Result
        </h2>
        <span className="text-xs text-slate-400">
          {result.model}
          {result.elapsedMs != null ? ` · ${Math.round(result.elapsedMs)} ms` : ''}
        </span>
      </div>

      <div className="mt-3 flex flex-wrap items-baseline gap-3">
        <span
          className={`rounded-full px-3 py-1 text-lg font-semibold ${tone.badge}`}
        >
          {tone.label}
        </span>
        {result.confidence != null ? (
          <span className="text-sm text-slate-500 dark:text-slate-400">
            {formatConfidence(result.confidence)} confidence
          </span>
        ) : null}
      </div>

      {ranked.length > 0 ? (
        <dl className="mt-5 space-y-3">
          {ranked.map(([name, value]) => {
            const rowTone = toneForPrediction(name)
            return (
              <div key={name}>
                <div className="flex items-center justify-between text-sm">
                  <dt className="text-slate-600 dark:text-slate-300">{name}</dt>
                  <dd className="font-medium tabular-nums">
                    {formatConfidence(value)}
                  </dd>
                </div>
                <div className="mt-1 h-2 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
                  <div
                    className={`h-full rounded-full transition-[width] duration-500 ${rowTone.bar}`}
                    style={{ width: `${Math.round(Math.min(Math.max(value, 0), 1) * 100)}%` }}
                  />
                </div>
              </div>
            )
          })}
        </dl>
      ) : null}

      <p className="mt-5 rounded-lg bg-slate-50 px-3 py-2 text-xs leading-relaxed text-slate-500 dark:bg-slate-800/60 dark:text-slate-400">
        Research and educational use only. This is not a medical diagnosis — always
        consult a qualified clinician.
      </p>
    </section>
  )
}
