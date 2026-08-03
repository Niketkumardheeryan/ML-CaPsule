import { useEffect, useState } from 'react'

/**
 * Surfaces the browser's own "add to home screen" flow. The event only fires on
 * browsers that support installation and when the app is not installed yet, so
 * the banner simply never appears elsewhere.
 */
export default function InstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState(null)
  const [dismissed, setDismissed] = useState(false)

  useEffect(() => {
    const capture = (event) => {
      event.preventDefault()
      setDeferredPrompt(event)
    }
    const installed = () => setDeferredPrompt(null)

    window.addEventListener('beforeinstallprompt', capture)
    window.addEventListener('appinstalled', installed)
    return () => {
      window.removeEventListener('beforeinstallprompt', capture)
      window.removeEventListener('appinstalled', installed)
    }
  }, [])

  if (!deferredPrompt || dismissed) return null

  return (
    <div className="flex flex-wrap items-center gap-3 rounded-2xl border border-pink-200 bg-pink-50 px-4 py-3 dark:border-pink-500/30 dark:bg-pink-500/10">
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-pink-900 dark:text-pink-200">
          Install this app
        </p>
        <p className="text-xs text-pink-700 dark:text-pink-300/80">
          Add it to your home screen for faster, offline-capable access.
        </p>
      </div>
      <button
        type="button"
        onClick={async () => {
          deferredPrompt.prompt()
          await deferredPrompt.userChoice
          setDeferredPrompt(null)
        }}
        className="rounded-lg bg-pink-600 px-3 py-2 text-sm font-semibold text-white transition hover:bg-pink-700"
      >
        Install
      </button>
      <button
        type="button"
        onClick={() => setDismissed(true)}
        className="rounded-lg px-2 py-2 text-sm text-pink-700 transition hover:bg-pink-100 dark:text-pink-300 dark:hover:bg-pink-500/10"
      >
        Not now
      </button>
    </div>
  )
}
