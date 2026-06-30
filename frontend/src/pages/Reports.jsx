import { useState } from 'react'
import { runReportAgent, runInsightAgent, embedAll, exportCSV, exportJSON } from '../api/api'

function ActionCard({ title, description, icon, onClick, loading, loadingText, variant = 'primary' }) {
  return (
    <div className="card p-5 space-y-3">
      <div className="flex items-center gap-2">
        <span className="text-2xl">{icon}</span>
        <div>
          <h3 className="text-sm font-semibold text-slate-800">{title}</h3>
          <p className="text-xs text-slate-500">{description}</p>
        </div>
      </div>
      <button
        onClick={onClick}
        disabled={loading}
        className={loading ? 'btn-secondary w-full opacity-60' : variant === 'primary' ? 'btn-primary w-full' : 'btn-secondary w-full'}
      >
        {loading ? loadingText : `Run ${title}`}
      </button>
    </div>
  )
}

export default function Reports() {
  const [reportResult, setReportResult] = useState(null)
  const [reportLoading, setReportLoading] = useState(false)

  const [indexResult, setIndexResult]   = useState(null)
  const [indexLoading, setIndexLoading] = useState(false)

  const [insightResult, setInsightResult] = useState(null)
  const [insightLoading, setInsightLoading] = useState(false)

  const [log, setLog] = useState([])
  const addLog = (msg) => setLog((prev) => [`${new Date().toLocaleTimeString()} — ${msg}`, ...prev])

  const handleReport = async () => {
    setReportLoading(true)
    addLog('Generating report…')
    try {
      const res = await runReportAgent()
      setReportResult(res.data)
      addLog(`✅ Report saved: ${res.data?.file_path}`)
    } catch (err) {
      addLog(`❌ Report failed: ${err.message}`)
    } finally {
      setReportLoading(false)
    }
  }

  const handleEmbedAll = async () => {
    setIndexLoading(true)
    addLog('Indexing all products and reviews into ChromaDB…')
    try {
      const res = await embedAll()
      setIndexResult(res.data)
      addLog(`✅ Indexed ${res.data?.products_indexed} products, ${res.data?.reviews_indexed} reviews.`)
    } catch (err) {
      addLog(`❌ Indexing failed: ${err.message}`)
    } finally {
      setIndexLoading(false)
    }
  }

  const handleInsights = async () => {
    setInsightLoading(true)
    addLog('Running AI insight pipeline on all products…')
    try {
      const res = await runInsightAgent([])
      setInsightResult(res.data)
      addLog(`✅ Insight pipeline complete. Reviews analysed: ${res.data?.reviews_analysed}`)
    } catch (err) {
      addLog(`❌ Insight pipeline failed: ${err.message}`)
    } finally {
      setInsightLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-bold text-slate-800">Reports & Data Actions</h2>
        <p className="text-sm text-slate-500 mt-1">Generate reports, index embeddings, and export your data.</p>
      </div>

      {/* ── Action cards ───────────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <ActionCard
          title="Generate Report"
          description="Create a full Markdown market intelligence report saved to reports/"
          icon="📄"
          onClick={handleReport}
          loading={reportLoading}
          loadingText="Generating report…"
        />
        <ActionCard
          title="Index Embeddings"
          description="Embed all products and reviews into ChromaDB for semantic search"
          icon="🗂️"
          onClick={handleEmbedAll}
          loading={indexLoading}
          loadingText="Indexing…"
          variant="secondary"
        />
        <ActionCard
          title="Run AI Pipeline"
          description="Run NLP analysis, embeddings, and Gemini insights on all products"
          icon="🤖"
          onClick={handleInsights}
          loading={insightLoading}
          loadingText="Running pipeline…"
          variant="secondary"
        />
      </div>

      {/* ── Export ─────────────────────────────────────────────────────────── */}
      <div className="card p-5">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">📥 Export Dataset</h3>
        <div className="flex gap-3">
          <button onClick={exportCSV}  className="btn-secondary text-sm">⬇ Download CSV</button>
          <button onClick={exportJSON} className="btn-secondary text-sm">⬇ Download JSON</button>
        </div>
      </div>

      {/* ── Report Result ───────────────────────────────────────────────────── */}
      {reportResult && (
        <div className="card p-5 border-l-4 border-green-500">
          <p className="text-sm font-semibold text-green-700 mb-1">✅ Report Generated</p>
          <p className="text-xs text-slate-500">File: <code className="bg-slate-100 px-1 rounded">{reportResult.file_path}</code></p>
          <p className="text-xs text-slate-500 mt-0.5">Products included: {reportResult.products_included}</p>
          {reportResult.report_preview && (
            <pre className="mt-3 text-xs text-slate-600 bg-slate-50 rounded p-3 overflow-auto max-h-40 whitespace-pre-wrap">
              {reportResult.report_preview}
            </pre>
          )}
        </div>
      )}

      {/* ── Index Result ─────────────────────────────────────────────────── */}
      {indexResult && (
        <div className="card p-4 border-l-4 border-blue-500">
          <p className="text-sm font-semibold text-blue-700">✅ ChromaDB Index Updated</p>
          <p className="text-xs text-slate-500 mt-1">
            Products: {indexResult.products_indexed} · Reviews: {indexResult.reviews_indexed}
          </p>
        </div>
      )}

      {/* ── Activity Log ─────────────────────────────────────────────────── */}
      {log.length > 0 && (
        <div className="card p-4">
          <h3 className="text-xs font-semibold text-slate-500 mb-2">Activity Log</h3>
          <div className="space-y-1 max-h-48 overflow-y-auto">
            {log.map((entry, i) => (
              <p key={i} className="text-xs text-slate-600 font-mono">{entry}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
