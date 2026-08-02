export default function OfflineBanner({ online }) {
  if (online) return null

  return (
    <div
      role="status"
      className="border-b border-amber-300 bg-amber-100 px-4 py-2 text-center text-sm text-amber-900 dark:border-amber-500/30 dark:bg-amber-500/15 dark:text-amber-200"
    >
      <span className="font-medium">Offline.</span> The app and your past results stay
      available — new scans are queued and sent automatically when you reconnect.
    </div>
  )
}
