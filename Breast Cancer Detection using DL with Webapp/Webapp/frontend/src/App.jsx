import { useCallback, useEffect, useRef, useState } from 'react'

import Header from './components/Header.jsx'
import HistoryPanel from './components/HistoryPanel.jsx'
import InstallPrompt from './components/InstallPrompt.jsx'
import OfflineBanner from './components/OfflineBanner.jsx'
import ResultCard from './components/ResultCard.jsx'
import UploadCard from './components/UploadCard.jsx'
import useOnlineStatus from './hooks/useOnlineStatus.js'
import { fetchHealth, predictImage } from './lib/api.js'
import { usePredictionStore } from './store/usePredictionStore.js'

export default function App() {
  const online = useOnlineStatus()
  const [modelLoaded, setModelLoaded] = useState(false)

  // The File itself never enters the store: it is not serialisable and would
  // break persistence. The store keeps only its metadata.
  const fileRef = useRef(null)
  const previewUrlRef = useRef(null)

  const theme = usePredictionStore((state) => state.theme)
  const status = usePredictionStore((state) => state.status)
  const selectFile = usePredictionStore((state) => state.selectFile)
  const startPrediction = usePredictionStore((state) => state.startPrediction)
  const queueOffline = usePredictionStore((state) => state.queueOffline)
  const predictionSucceeded = usePredictionStore((state) => state.predictionSucceeded)
  const predictionFailed = usePredictionStore((state) => state.predictionFailed)

  // Reflect the persisted theme on <html> so Tailwind's dark variant applies.
  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])

  useEffect(() => {
    let cancelled = false
    if (!online) {
      setModelLoaded(false)
      return undefined
    }
    fetchHealth().then((health) => {
      if (!cancelled) setModelLoaded(health.modelLoaded)
    })
    return () => {
      cancelled = true
    }
  }, [online])

  const handleFileChosen = useCallback(
    (file) => {
      if (previewUrlRef.current) URL.revokeObjectURL(previewUrlRef.current)
      const url = URL.createObjectURL(file)
      previewUrlRef.current = url
      fileRef.current = file
      selectFile(file, url)
    },
    [selectFile]
  )

  const runPrediction = useCallback(async () => {
    const file = fileRef.current
    if (!file) {
      predictionFailed('Choose an ultrasound image first.')
      return
    }
    if (!navigator.onLine) {
      queueOffline()
      return
    }

    startPrediction()
    try {
      predictionSucceeded(await predictImage(file))
    } catch (error) {
      predictionFailed(error?.message || 'Prediction failed.')
    }
  }, [predictionFailed, predictionSucceeded, queueOffline, startPrediction])

  // Anything queued while offline is sent as soon as the connection returns.
  useEffect(() => {
    if (online && status === 'queued') runPrediction()
  }, [online, status, runPrediction])

  // Release the last object URL when the app unmounts.
  useEffect(
    () => () => {
      if (previewUrlRef.current) URL.revokeObjectURL(previewUrlRef.current)
    },
    []
  )

  return (
    <div className="min-h-full">
      <Header online={online} modelLoaded={modelLoaded} />
      <OfflineBanner online={online} />

      <main className="mx-auto max-w-5xl px-4 py-6 sm:px-6 sm:py-8">
        <div className="mb-6 space-y-4">
          <InstallPrompt />
          <div>
            <h2 className="text-2xl font-bold tracking-tight sm:text-3xl">
              Analyse an ultrasound scan
            </h2>
            <p className="mt-1 max-w-2xl text-sm text-slate-600 dark:text-slate-400">
              Upload a breast ultrasound image and the deep-learning model classifies it
              as benign, malignant or normal. Works on any screen size, installs to your
              home screen, and keeps working when the network does not.
            </p>
          </div>
        </div>

        <div className="grid gap-5 lg:grid-cols-2">
          <div className="space-y-5">
            <UploadCard
              online={online}
              onPredict={runPrediction}
              onFileChosen={handleFileChosen}
            />
          </div>
          <div className="space-y-5">
            <ResultCard />
            <HistoryPanel />
          </div>
        </div>

        <footer className="mt-10 border-t border-slate-200 pt-5 text-xs text-slate-500 dark:border-slate-800 dark:text-slate-400">
          <p>
            Breast Cancer Detection · React + Vite + Tailwind + Zustand · installable,
            offline-first PWA.
          </p>
          <p className="mt-1">
            Model served by the existing Flask backend at <code>/api/predict</code>.
          </p>
        </footer>
      </main>
    </div>
  )
}
