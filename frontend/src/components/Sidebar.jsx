import { NavLink } from 'react-router-dom'

const links = [
  { to: '/dashboard', label: 'Dashboard',  icon: '📊' },
  { to: '/search',    label: 'Search',     icon: '🔍' },
  { to: '/products',  label: 'Products',   icon: '🛒' },
  { to: '/insights',  label: 'AI Insights',icon: '🧠' },
  { to: '/reports',   label: 'Reports',    icon: '📄' },
]

export default function Sidebar() {
  return (
    <aside className="w-60 bg-white border-r border-slate-200 flex flex-col shrink-0">
      {/* Brand */}
      <div className="px-5 py-5 border-b border-slate-200">
        <span className="text-lg font-bold text-primary-700 leading-tight">
          🧠 Market<br />
          <span className="font-normal text-slate-500 text-sm">Intelligence Platform</span>
        </span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {links.map(({ to, label, icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors duration-150 ${
                isActive
                  ? 'bg-primary-50 text-primary-700'
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-800'
              }`
            }
          >
            <span className="text-base">{icon}</span>
            {label}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="px-5 py-4 border-t border-slate-200">
        <p className="text-xs text-slate-400">CS Portfolio Project v0.2.0</p>
      </div>
    </aside>
  )
}
