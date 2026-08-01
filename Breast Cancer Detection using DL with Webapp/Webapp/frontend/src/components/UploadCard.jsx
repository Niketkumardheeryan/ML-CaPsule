import { useCallback, useRef, useState } from 'react'

import { formatBytes, validateImageFile } from '../lib/format.js'
import { usePredictionStore } from '../store/usePredictionStore.js'

export default function UploadCard({ online, onPredict, onFileChosen }) {
  const inputRef = useRef(null)
  const [dragging, setDragging] = useState(false)

  const status = usePredictionStore((state) => state.status)
  const file = usePredictionStore((state) => state.file)
  const previewUrl = usePredictionStore((state) => state.previewUrl)
  const error = usePredictionStore((state) => state.error)
  const clearSelection = usePredictionStore((state) => state.clearSelection)
  const predictionFailed = usePredictionStore((state) => state.predictionFailed)

  const busy = status === 'loading'

  const handleFiles = useCallback(
    (files) => {
      const candidate = files?.[0]
      const { ok, error: message } = validateImageFile(candidate)
      if (!ok) {
        predictionFailed(message)
        return
      }
      onFileChosen(candidate)
    },
    [onFileChosen, predictionFailed]
  )

  const onDrop = (event) => {
    event.preventDefault()
    setDragging(false)
    handleFiles(event.dataTransfer.files)
  }

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6 dark:border-slate-800 dark:bg-slate-900">
      <h2 className="text-sm font-semibold tracking-wide text-slate-500 uppercase dark:text-slate-400">
        Upload ultrasound image
      </h2>

      <div
        onDragOver={(event) => {
          event.preventDefault()
          setDragging(true)
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        className={`mt-4 rounded-xl border-2 border-dashed transition ${
          dragging
            ? 'border-pink-500 bg-pink-50 dark:bg-pink-500/10'
            : 'border-slate-300 dark:border-slate-700'
        }`}
      >
        {previewUrl ? (
          <div className="flex flex-col items-center gap-3 p-4">
            <img
              src={previewUrl}
              alt="Selected ultrasound scan"
              className="max-h-56 w-auto rounded-lg object-contain shadow-sm"
            />
            <p className="max-w-full truncate text-sm text-slate-600 dark:text-slate-300">
              {file?.name}
              {file?.size ? (
                <span className="text-slate-400"> · {formatBytes(file.size)}</span>
              ) : null}
            </p>
          </div>
        ) : (
          <button
            type="button"
            onClick={() => inputRef.current?.click()}
            className="flex w-full flex-col items-center gap-2 px-4 py-10 text-center focus-visible:ring-2 focus-visible:ring-pink-500 focus-visible:outline-none"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.6"
              className="h-10 w-10 text-slate-400"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 16V4m0 0L8 8m4-4 4 4M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"
              />
            </svg>
            <span className="text-sm font-medium">Tap to choose, or drag an image here</span>
            <span className="text-xs text-slate-500 dark:text-slate-400">
              PNG, JPEG, WebP or BMP · up to 8 MB
            </span>
          </button>
        )}

        <input
          ref={inputRef}
          type="file"
          accept="image/png,image/jpeg,image/webp,image/bmp"
          className="sr-only"
          onChange={(event) => handleFiles(event.target.files)}
        />
      </div>

      {error ? (
        <p
          role="alert"
          className="mt-3 rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-700 dark:bg-rose-500/10 dark:text-rose-300"
        >
          {error}
        </p>
      ) : null}

      <div className="mt-4 flex flex-col gap-2 sm:flex-row">
        <button
          type="button"
          onClick={onPredict}
          disabled={!file || busy}
          className="inline-flex flex-1 items-center justify-center gap-2 rounded-xl bg-linear-to-r from-pink-600 to-rose-600 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:from-pink-700 hover:to-rose-700 focus-visible:ring-2 focus-visible:ring-pink-500 focus-visible:ring-offset-2 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 dark:focus-visible:ring-offset-slate-900"
        >
          {busy ? (
            <>
              <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                <circle
                  cx="12"
                  cy="12"
                  r="9"
                  stroke="currentColor"
                  strokeWidth="3"
                  className="opacity-25"
                />
                <path
                  d="M21 12a9 9 0 0 0-9-9"
                  stroke="currentColor"
                  strokeWidth="3"
                  strokeLinecap="round"
                />
              </svg>
              Analysing…
            </>
          ) : online ? (
            'Analyse image'
          ) : (
            'Queue for when online'
          )}
        </button>

        {file ? (
          <button
            type="button"
            onClick={clearSelection}
            disabled={busy}
            className="rounded-xl border border-slate-300 px-4 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50 disabled:opacity-50 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            Clear
          </button>
        ) : null}
      </div>
    </section>
  )
}
