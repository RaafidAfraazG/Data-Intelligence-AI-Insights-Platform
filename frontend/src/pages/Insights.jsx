import { useState } from 'react'
import {
  getProductInsights,
  compareProducts,
  askQuestion,
  getDashboardInsights,
} from '../api/api'
import InsightCard from '../components/InsightCard'

export default function Insights() {
  // ── Executive Summary ────────────────────────────────────────────────────
  const [execSummary, setExecSummary] = useState('')
  const [execLoading, setExecLoading] = useState(false)

  const loadExecSummary = async () => {
    setExecLoading(true)
    try {
      const res = await getDashboardInsights()
      setExecSummary(res.data?.executive_summary || 'No summary generated.')
    } catch (err) {
      setExecSummary(`Error: ${err.message}`)
    } finally {
      setExecLoading(false)
    }
  }

  // ── Product Insights ─────────────────────────────────────────────────────
  const [productId, setProductId]   = useState('')
  const [insights, setInsights]     = useState(null)
  const [insightsLoading, setInsightsLoading] = useState(false)
  const [insightsError, setInsightsError]     = useState(null)

  const loadInsights = async () => {
    if (!productId) return
    setInsightsLoading(true)
    setInsightsError(null)
    try {
      const res = await getProductInsights(parseInt(productId))
      setInsights(res.data)
    } catch (err) {
      setInsightsError(err.message)
    } finally {
      setInsightsLoading(false)
    }
  }

  // ── Product Comparison ───────────────────────────────────────────────────
  const [idA, setIdA]           = useState('')
  const [idB, setIdB]           = useState('')
  const [comparison, setComparison] = useState(null)
  const [compLoading, setCompLoading] = useState(false)

  const runComparison = async () => {
    if (!idA || !idB) return
    setCompLoading(true)
    try {
      const res = await compareProducts(parseInt(idA), parseInt(idB))
      setComparison(res.data)
    } catch (err) {
      setComparison({ comparison: `Error: ${err.message}` })
    } finally {
      setCompLoading(false)
    }
  }

  // ── Q&A ──────────────────────────────────────────────────────────────────
  const [question, setQuestion] = useState('')
  const [answer, setAnswer]     = useState(null)
  const [qaLoading, setQaLoading] = useState(false)

  const handleQA = async (e) => {
    e.preventDefault()
    if (!question.trim()) return
    setQaLoading(true)
    try {
      const res = await askQuestion(question.trim())
      setAnswer(res.data)
    } catch (err) {
      setAnswer({ answer: `Error: ${err.message}` })
    } finally {
      setQaLoading(false)
    }
  }

  return (
    <div className="space-y-8 max-w-4xl">
      <h2 className="text-lg font-bold text-slate-800">AI Insights</h2>

      {/* ── Executive Summary ───────────────────────────────────────────── */}
      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-700">📋 Executive Summary</h3>
          <button onClick={loadExecSummary} disabled={execLoading} className="btn-primary text-xs px-3 py-1.5">
            {execLoading ? 'Generating…' : 'Generate'}
          </button>
        </div>
        <InsightCard title="AI Executive Summary" content={execSummary} icon="📋" loading={execLoading} />
      </section>

      {/* ── Product Insights ────────────────────────────────────────────── */}
      <section className="space-y-3">
        <h3 className="text-sm font-semibold text-slate-700">🎯 Product Insights</h3>
        <div className="flex gap-2">
          <input
            type="number"
            placeholder="Product ID"
            value={productId}
            onChange={(e) => setProductId(e.target.value)}
            className="input w-36 text-sm"
          />
          <button onClick={loadInsights} disabled={insightsLoading || !productId} className="btn-primary text-sm">
            {insightsLoading ? 'Loading…' : 'Analyse'}
          </button>
        </div>
        {insightsError && <p className="text-sm text-red-500">{insightsError}</p>}
        {insights && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <InsightCard title="Strengths"                icon="✅" content={insights.strengths} />
            <InsightCard title="Weaknesses"               icon="⚠️" content={insights.weaknesses} />
            <InsightCard title="Customer Pain Points"     icon="😤" content={insights.pain_points} />
            <InsightCard title="Marketing Recommendations" icon="📢" content={insights.marketing_recommendations} />
            {insights.seo_keywords?.length > 0 && (
              <div className="sm:col-span-2 card p-4">
                <p className="text-xs font-semibold text-slate-500 mb-2">🔑 SEO Keywords</p>
                <div className="flex flex-wrap gap-1.5">
                  {insights.seo_keywords.map((kw) => (
                    <span key={kw} className="badge badge-blue">{kw}</span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </section>

      {/* ── Product Comparison ──────────────────────────────────────────── */}
      <section className="space-y-3">
        <h3 className="text-sm font-semibold text-slate-700">⚖️ Compare Products</h3>
        <div className="flex gap-2 flex-wrap">
          <input type="number" placeholder="Product A ID" value={idA}
            onChange={(e) => setIdA(e.target.value)} className="input w-36 text-sm" />
          <input type="number" placeholder="Product B ID" value={idB}
            onChange={(e) => setIdB(e.target.value)} className="input w-36 text-sm" />
          <button onClick={runComparison} disabled={compLoading || !idA || !idB} className="btn-primary text-sm">
            {compLoading ? 'Comparing…' : 'Compare'}
          </button>
        </div>
        {comparison && (
          <div className="card p-5">
            <p className="text-xs text-slate-500 mb-2">
              {comparison.product_a?.name} vs {comparison.product_b?.name}
            </p>
            <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-line">
              {comparison.comparison}
            </p>
          </div>
        )}
      </section>

      {/* ── Q&A ─────────────────────────────────────────────────────────── */}
      <section className="space-y-3">
        <h3 className="text-sm font-semibold text-slate-700">💬 Ask a Question</h3>
        <form onSubmit={handleQA} className="flex gap-2">
          <input
            type="text"
            placeholder='e.g. "What are the biggest complaints about laptops?"'
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="input flex-1 text-sm"
          />
          <button type="submit" disabled={qaLoading || !question.trim()} className="btn-primary text-sm shrink-0">
            {qaLoading ? 'Thinking…' : 'Ask'}
          </button>
        </form>
        {answer && (
          <div className="card p-5 border-l-4 border-primary-500">
            <p className="text-xs text-slate-400 mb-2">Answer (context used: {answer.context_used} documents)</p>
            <p className="text-sm text-slate-700 leading-relaxed">{answer.answer}</p>
          </div>
        )}
      </section>
    </div>
  )
}
