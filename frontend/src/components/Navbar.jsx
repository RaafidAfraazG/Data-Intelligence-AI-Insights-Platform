import { useLocation } from 'react-router-dom'

const titles = {
  '/dashboard': 'Dashboard Overview',
  '/search':    'Semantic Search',
  '/products':  'Products',
  '/insights':  'AI Insights',
  '/reports':   'Reports',
}

export default function Navbar() {
  const { pathname } = useLocation()
  const title = titles[pathname] || 'AI Market Intelligence'

  return (
    <header className="h-14 bg-white border-b border-slate-200 flex items-center px-6 shrink-0">
      <h1 className="text-base font-semibold text-slate-800">{title}</h1>
      <div className="ml-auto flex items-center gap-3">
        <span className="text-xs text-slate-400 hidden sm:block">
          Powered by Gemini · VADER · ChromaDB
        </span>
        <div className="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center text-white text-xs font-bold">
          AI
        </div>
      </div>
    </header>
  )
}
