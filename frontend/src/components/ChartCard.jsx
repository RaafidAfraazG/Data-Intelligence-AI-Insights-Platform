/**
 * ChartCard — wraps a Recharts chart with a title and optional description.
 *
 * Props:
 *   title       (string)
 *   description (string)   — optional subtitle
 *   children    (ReactNode) — the chart component
 *   className   (string)   — extra Tailwind classes
 */
export default function ChartCard({ title, description, children, className = '' }) {
  return (
    <div className={`card p-5 ${className}`}>
      <div className="mb-4">
        <h3 className="text-sm font-semibold text-slate-700">{title}</h3>
        {description && (
          <p className="text-xs text-slate-400 mt-0.5">{description}</p>
        )}
      </div>
      {children}
    </div>
  )
}
