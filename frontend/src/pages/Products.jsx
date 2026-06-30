import { useState, useEffect } from 'react'
import { getProducts, searchProducts } from '../api/api'

function StarRating({ rating }) {
  if (!rating) return <span className="text-slate-400">—</span>
  const rounded = Math.round(rating)
  return (
    <span className="text-yellow-500 text-sm">
      {'★'.repeat(rounded)}{'☆'.repeat(5 - rounded)}
      <span className="text-slate-500 text-xs ml-1">{rating.toFixed(1)}</span>
    </span>
  )
}

function SentimentBadge({ label }) {
  if (!label) return null
  const cls = label === 'positive' ? 'badge-green' : label === 'negative' ? 'badge-red' : 'badge-yellow'
  return <span className={`badge ${cls}`}>{label}</span>
}

export default function Products() {
  const [products, setProducts] = useState([])
  const [total, setTotal]       = useState(0)
  const [page, setPage]         = useState(1)
  const [loading, setLoading]   = useState(true)
  const [error, setError]       = useState(null)
  const [searchQ, setSearchQ]   = useState('')
  const [searching, setSearching] = useState(false)

  const PAGE_SIZE = 20

  const loadProducts = async (p = 1) => {
    setLoading(true)
    setError(null)
    try {
      const res = await getProducts(p, PAGE_SIZE)
      const d = res.data
      setProducts(d?.items || [])
      setTotal(d?.total || 0)
      setPage(p)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadProducts(1) }, [])

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!searchQ.trim()) { loadProducts(1); return }
    setSearching(true)
    setError(null)
    try {
      const res = await searchProducts(searchQ.trim())
      setProducts(res.data || [])
      setTotal(res.data?.length || 0)
    } catch (err) {
      setError(err.message)
    } finally {
      setSearching(false)
    }
  }

  const totalPages = Math.ceil(total / PAGE_SIZE)

  return (
    <div className="space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-bold text-slate-800">Products</h2>
          <p className="text-sm text-slate-500">{total} total products in database</p>
        </div>
        <form onSubmit={handleSearch} className="flex gap-2">
          <input
            type="text"
            placeholder="Search by name…"
            value={searchQ}
            onChange={(e) => setSearchQ(e.target.value)}
            className="input w-48 text-sm"
          />
          <button type="submit" disabled={searching} className="btn-secondary text-sm">
            {searching ? '…' : 'Search'}
          </button>
          {searchQ && (
            <button type="button" onClick={() => { setSearchQ(''); loadProducts(1) }} className="btn-secondary text-sm">
              Clear
            </button>
          )}
        </form>
      </div>

      {error && <div className="card p-4 border-red-200 bg-red-50"><p className="text-sm text-red-600">{error}</p></div>}

      {loading ? (
        <div className="card animate-pulse divide-y divide-slate-100">
          {[1,2,3,4,5].map(i => <div key={i} className="h-12 bg-slate-100 m-1 rounded" />)}
        </div>
      ) : (
        <div className="card overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                {['#','Name','Brand','Category','Price','Rating','Reviews'].map(h => (
                  <th key={h} className="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {products.map((p, i) => (
                <tr key={p.id} className="hover:bg-slate-50 transition-colors">
                  <td className="px-4 py-3 text-slate-400 text-xs">{(page - 1) * PAGE_SIZE + i + 1}</td>
                  <td className="px-4 py-3 font-medium text-slate-800 max-w-[200px] truncate">{p.name}</td>
                  <td className="px-4 py-3 text-slate-500">{p.brand || '—'}</td>
                  <td className="px-4 py-3">
                    {p.category ? <span className="badge badge-blue">{p.category}</span> : '—'}
                  </td>
                  <td className="px-4 py-3 text-slate-700">
                    {p.price ? `₹${p.price.toLocaleString()}` : '—'}
                  </td>
                  <td className="px-4 py-3"><StarRating rating={p.rating} /></td>
                  <td className="px-4 py-3 text-slate-500">{p.review_count ?? '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {products.length === 0 && (
            <div className="py-12 text-center text-slate-400 text-sm">No products found.</div>
          )}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between text-sm">
          <p className="text-slate-500">Page {page} of {totalPages}</p>
          <div className="flex gap-2">
            <button onClick={() => loadProducts(page - 1)} disabled={page === 1} className="btn-secondary disabled:opacity-40">
              ← Previous
            </button>
            <button onClick={() => loadProducts(page + 1)} disabled={page >= totalPages} className="btn-secondary disabled:opacity-40">
              Next →
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
