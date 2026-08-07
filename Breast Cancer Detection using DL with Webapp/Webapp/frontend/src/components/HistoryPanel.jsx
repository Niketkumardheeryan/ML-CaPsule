import {
  formatConfidence,
  formatRelativeTime,
  toneForPrediction,
} from '../lib/format.js'
import { usePredictionStore } from '../store/usePredictionStore.js'

export default function HistoryPanel() {
  const history = usePredictionStore((state) => state.history)
  const clearHistory = usePredictionStore((state) => state.clearHistory)
  const removeFromHistory = usePredictionStore((state) => state.removeFromHistory)

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6 dark:border-slate-800 dark:bg-slate-900">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-sm font-semibold tracking-wide text-slate-500 uppercase dark:text-slate-400">
          Recent scans
        </h2>
        {history.length > 0 ? (
          <button
            type="button"
            onClick={clearHistory}
            className="text-xs font-medium text-slate-500 transition hover:text-rose-600 dark:text-slate-400"
          >
            Clear all
          </button>
        ) : null}
      </div>

      {history.length === 0 ? (
        <p className="mt-4 text-sm text-slate-500 dark:text-slate-400">
          Nothing yet. Results are stored on this device, so they stay readable offline.
        </p>
      ) : (
        <ul className="mt-4 divide-y divide-slate-100 dark:divide-slate-800">
          {history.map((entry) => {
            const tone = toneForPrediction(entry.prediction)
            return (
              <li key={entry.id} className="flex items-center gap-3 py-3">
                <span
                  className={`rounded-md px-2 py-1 text-xs font-semibold ${tone.badge}`}
                >
                  {tone.label}
                </span>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm text-slate-700 dark:text-slate-200">
                    {entry.fileName}
                  </p>
                  <p className="text-xs text-slate-400">
                    {formatRelativeTime(entry.at)}
                    {entry.confidence != null
                      ? ` · ${formatConfidence(entry.confidence)}`
                      : ''}
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => removeFromHistory(entry.id)}
                  aria-label={`Remove ${entry.fileName} from history`}
                  className="rounded p-1 text-slate-400 transition hover:bg-slate-100 hover:text-rose-600 dark:hover:bg-slate-800"
                >
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    className="h-4 w-4"
                  >
                    <path strokeLinecap="round" d="M6 6l12 12M18 6 6 18" />
                  </svg>
                </button>
              </li>
            )
          })}
        </ul>
      )}
    </section>
  )
}
