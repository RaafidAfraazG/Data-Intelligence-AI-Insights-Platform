/**
 * StatCard — a single KPI card with an icon, label, value, and optional trend.
 *
 * Props:
 *   title   (string)
 *   value   (string | number)
 *   icon    (string)  — emoji
 *   color   (string)  — Tailwind color name: 'blue' | 'green' | 'yellow' | 'purple' | 'red'
 *   sub     (string)  — optional small subtitle text
 */
const colorMap = {
  blue:   { bg: 'bg-blue-50',   icon: 'bg-blue-100 text-blue-600'   },
  green:  { bg: 'bg-green-50',  icon: 'bg-green-100 text-green-600'  },
  yellow: { bg: 'bg-yellow-50', icon: 'bg-yellow-100 text-yellow-600' },
  purple: { bg: 'bg-purple-50', icon: 'bg-purple-100 text-purple-600' },
  red:    { bg: 'bg-red-50',    icon: 'bg-red-100 text-red-600'     },
}

export default function StatCard({ title, value, icon, color = 'blue', sub }) {
  const colors = colorMap[color] || colorMap.blue
  return (
    <div className={`card p-5 flex items-start gap-4 ${colors.bg}`}>
      <div className={`w-11 h-11 rounded-xl flex items-center justify-center text-xl shrink-0 ${colors.icon}`}>
        {icon}
      </div>
      <div className="min-w-0">
        <p className="text-xs font-medium text-slate-500 truncate">{title}</p>
        <p className="text-2xl font-bold text-slate-800 mt-0.5">{value ?? '—'}</p>
        {sub && <p className="text-xs text-slate-400 mt-0.5 truncate">{sub}</p>}
      </div>
    </div>
  )
}
