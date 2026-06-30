import { useState, useEffect } from 'react'
import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
} from 'recharts'
import StatCard from '../components/StatCard'
import ChartCard from '../components/ChartCard'
import {
  getDashboardOverview,
  getDashboardSentiment,
  getDashboardKeywords,
  getDashboardCompetitors,
} from '../api/api'

// ── Helpers ───────────────────────────────────────────────────────────────────

function useApi(fn, deps = []) {
  const [data, setData]     = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError]   = useState(null)

  useEffect(() => {
    setLoading(true)
    fn()
      .then((res) => setData(res.data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps)

  return { data, loading, error }
}

function Skeleton({ className = 'h-40' }) {
  return <div className={`animate-pulse bg-slate-200 rounded-xl ${className}`} />
}

// ── Component ─────────────────────────────────────────────────────────────────

export default function Dashboard() {
  const overview    = useApi(getDashboardOverview)
  const sentiment   = useApi(getDashboardSentiment)
  const keywords    = useApi(() => getDashboardKeywords(12))
  const competitors = useApi(getDashboardCompetitors)

  const ov = overview.data

  return (
    <div className="space-y-6">
      <h2 className="text-lg font-bold text-slate-800">Overview</h2>

      {/* ── KPI cards ─────────────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {overview.loading ? (
          [1,2,3,4].map(i => <Skeleton key={i} className="h-24" />)
        ) : overview.error ? (
          <p className="text-red-500 col-span-4 text-sm">{overview.error}</p>
        ) : (
          <>
            <StatCard title="Total Products"   value={ov?.total_products}   icon="🛒" color="blue"   />
            <StatCard title="Total Reviews"    value={ov?.total_reviews}    icon="💬" color="purple" />
            <StatCard title="Average Rating"   value={ov?.average_rating ? `${ov.average_rating}/5` : '—'} icon="⭐" color="yellow" />
            <StatCard title="Overall Sentiment" value={ov?.overall_sentiment ? ov.overall_sentiment.charAt(0).toUpperCase() + ov.overall_sentiment.slice(1) : '—'}
              icon={ov?.overall_sentiment === 'positive' ? '😊' : ov?.overall_sentiment === 'negative' ? '😞' : '😐'}
              color={ov?.overall_sentiment === 'positive' ? 'green' : ov?.overall_sentiment === 'negative' ? 'red' : 'yellow'}
              sub={`Score: ${ov?.sentiment_score ?? '—'}`}
            />
          </>
        )}
      </div>

      {/* ── Charts row ────────────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

        {/* Sentiment Pie Chart */}
        <ChartCard title="Sentiment Distribution" description="Across all reviews">
          {sentiment.loading ? <Skeleton /> : sentiment.error ? (
            <p className="text-sm text-red-500">{sentiment.error}</p>
          ) : (
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={sentiment.data?.chart_data || []}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {(sentiment.data?.chart_data || []).map((entry) => (
                    <Cell key={entry.name} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          )}
        </ChartCard>

        {/* Competitor Bar Chart */}
        <ChartCard title="Competitor Ratings" description="Average rating by brand (top 10)">
          {competitors.loading ? <Skeleton /> : competitors.error ? (
            <p className="text-sm text-red-500">{competitors.error}</p>
          ) : (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={competitors.data?.competitors || []} margin={{ top: 5, right: 10, left: 0, bottom: 40 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="brand" tick={{ fontSize: 11 }} angle={-35} textAnchor="end" />
                <YAxis domain={[0, 5]} tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="avg_rating" name="Avg Rating" fill="#3b82f6" radius={[4,4,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </ChartCard>
      </div>

      {/* ── Keywords bar chart ────────────────────────────────────────────── */}
      <ChartCard title="Top Keywords" description="TF-IDF keyword frequency across all reviews">
        {keywords.loading ? <Skeleton className="h-52" /> : keywords.error ? (
          <p className="text-sm text-red-500">{keywords.error}</p>
        ) : (
          <ResponsiveContainer width="100%" height={220}>
            <BarChart
              data={keywords.data?.keywords || []}
              layout="vertical"
              margin={{ top: 5, right: 30, left: 80, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis type="number" tick={{ fontSize: 11 }} />
              <YAxis type="category" dataKey="keyword" tick={{ fontSize: 11 }} width={75} />
              <Tooltip />
              <Bar dataKey="score" name="TF-IDF Score" fill="#8b5cf6" radius={[0,4,4,0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </ChartCard>
    </div>
  )
}
