import { useState } from 'react'
import { dashboardSearch } from '../api/api'

function StarRating({ rating }) {
  if (!rating) return <span className="text-slate-400 text-xs">No rating</span>
  return (
    <span className="text-yellow-500 text-sm">
      {'★'.repeat(Math.round(rating))}{'☆'.repeat(5 - Math.round(rating))}
      <span className="text-slate-500 text-xs ml-1">{rating.toFixed(1)}</span>
    </span>
  )
}

export default function Search() {
  const [query, setQuery]     = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)
  const [searched, setSearched] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return
    setLoading(true)
    setError(null)
    setSearched(true)
    try {
      const res = await dashboardSearch(query.trim(), 12)
      setResults(res.data?.results || [])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h2 className="text-lg font-bold text-slate-800">Semantic Search</h2>
        <p className="text-sm text-slate-500 mt-1">
          Ask in natural language — powered by sentence embeddings and ChromaDB.
        </p>
      </div>

      {/* ── Search bar ─────────────────────────────────────────────────────── */}
      <form onSubmit={handleSearch} className="flex gap-3">
        <input
          id="search-input"
          type="text"
          placeholder='e.g. "gaming laptops with great battery life"'
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="input flex-1 text-sm"
        />
        <button
          type="submit"
          disabled={loading}
          className="btn-primary shrink-0 min-w-[90px]"
        >
          {loading ? 'Searching…' : '🔍 Search'}
        </button>
      </form>

      {/* ── Example queries ────────────────────────────────────────────────── */}
      <div className="flex flex-wrap gap-2">
        {[
          'Products similar to iPhone 15',
          'Budget smartphones under 15000',
          'Products with excellent battery life',
          'Best rated headphones',
        ].map((ex) => (
          <button
            key={ex}
            onClick={() => setQuery(ex)}
            className="text-xs px-3 py-1.5 rounded-full border border-slate-200 text-slate-500 hover:border-primary-400 hover:text-primary-600 transition-colors"
          >
            {ex}
          </button>
        ))}
      </div>

      {/* ── Results ────────────────────────────────────────────────────────── */}
      {error && (
        <div className="card p-4 border-red-200 bg-red-50">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {searched && !loading && results.length === 0 && !error && (
        <div className="card p-8 text-center">
          <p className="text-slate-500 text-sm">
            No results found. Make sure products are indexed via{' '}
            <code className="text-xs bg-slate-100 px-1 rounded">POST /api/v1/ai/embed/all</code>.
          </p>
        </div>
      )}

      {results.length > 0 && (
        <div>
          <p className="text-xs text-slate-500 mb-3">{results.length} results found</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {results.map((p) => (
              <div key={p.id} className="card p-4 hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start gap-2">
                  <div className="min-w-0">
                    <h3 className="text-sm font-semibold text-slate-800 truncate">{p.name}</h3>
                    <p className="text-xs text-slate-500 mt-0.5">{p.brand || 'Unknown brand'}</p>
                  </div>
                  {p.similarity_score != null && (
                    <span className="badge badge-blue shrink-0">
                      {Math.round(p.similarity_score * 100)}% match
                    </span>
                  )}
                </div>
                <div className="mt-2 flex items-center gap-3">
                  <StarRating rating={p.rating} />
                  {p.price && (
                    <span className="text-sm font-medium text-slate-700">₹{p.price.toLocaleString()}</span>
                  )}
                </div>
                {p.category && (
                  <span className="badge badge-blue mt-2 text-xs">{p.category}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
