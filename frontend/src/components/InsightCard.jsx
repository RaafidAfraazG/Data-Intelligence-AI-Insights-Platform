/**
 * InsightCard — displays an AI-generated insight block.
 *
 * Props:
 *   title    (string)
 *   content  (string)   — the AI-generated text
 *   icon     (string)   — emoji icon
 *   loading  (boolean)
 */
export default function InsightCard({ title, content, icon = '🧠', loading = false }) {
  return (
    <div className="card p-5">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-lg">{icon}</span>
        <h3 className="text-sm font-semibold text-slate-700">{title}</h3>
      </div>

      {loading ? (
        <div className="space-y-2 animate-pulse">
          <div className="h-3 bg-slate-200 rounded w-full" />
          <div className="h-3 bg-slate-200 rounded w-5/6" />
          <div className="h-3 bg-slate-200 rounded w-4/6" />
        </div>
      ) : (
        <p className="text-sm text-slate-600 leading-relaxed whitespace-pre-line">
          {content || 'No insight available.'}
        </p>
      )}
    </div>
  )
}
