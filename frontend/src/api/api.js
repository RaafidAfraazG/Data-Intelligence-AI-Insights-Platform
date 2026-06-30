/**
 * src/api/api.js
 * ==============
 * Centralized Axios API service for all FastAPI backend calls.
 *
 * Usage:
 *   import api from '../api/api'
 *   const data = await api.getDashboardOverview()
 */

import axios from 'axios'

// In development, Vite proxies /api → http://localhost:8000
// In production, set VITE_API_BASE_URL in .env
const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

const http = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

// ── Response interceptor — unwrap .data.data ──────────────────────────────────
http.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message =
      error.response?.data?.error ||
      error.response?.data?.detail ||
      error.message ||
      'An unexpected error occurred'
    return Promise.reject(new Error(message))
  }
)

// ── Dashboard ──────────────────────────────────────────────────────────────────

export const getDashboardOverview   = () => http.get('/dashboard/overview')
export const getDashboardSentiment  = () => http.get('/dashboard/sentiment')
export const getDashboardKeywords   = (top_n = 20) => http.get('/dashboard/keywords', { params: { top_n } })
export const getDashboardTopics     = () => http.get('/dashboard/topics')
export const getDashboardCompetitors= () => http.get('/dashboard/competitors')
export const getDashboardInsights   = () => http.get('/dashboard/insights')
export const dashboardSearch        = (q, n = 10) => http.get('/dashboard/search', { params: { q, n } })

// ── Products ──────────────────────────────────────────────────────────────────

export const getProducts   = (page = 1, page_size = 20) =>
  http.get('/products', { params: { page, page_size } })

export const getProduct    = (id) => http.get(`/products/${id}`)
export const createProduct = (data) => http.post('/products', data)
export const updateProduct = (id, data) => http.put(`/products/${id}`, data)
export const deleteProduct = (id) => http.delete(`/products/${id}`)
export const searchProducts= (q, page = 1) => http.get('/products/search', { params: { q, page } })

// ── Reviews ───────────────────────────────────────────────────────────────────

export const getReviews           = (skip = 0, limit = 20) => http.get('/reviews', { params: { skip, limit } })
export const getProductReviews    = (productId) => http.get(`/products/${productId}/reviews`)

// ── AI & NLP ──────────────────────────────────────────────────────────────────

export const analyzeSentiment  = (texts) => http.post('/ai/sentiment', { texts })
export const extractKeywords   = (texts, top_n = 10) => http.post('/ai/keywords', { texts }, { params: { top_n } })
export const extractTopics     = (texts, n_topics = 5) => http.post('/ai/topics', { texts }, { params: { n_topics } })
export const summarizeProduct  = (id) => http.post(`/ai/summarize/product/${id}`)
export const summarizeReviews  = (id) => http.post(`/ai/summarize/reviews/${id}`)
export const getProductInsights= (id) => http.get(`/ai/insights/${id}`)
export const compareProducts   = (product_a_id, product_b_id) =>
  http.post('/ai/compare', { product_a_id, product_b_id })
export const askQuestion       = (question) => http.post('/ai/answer', { question })
export const embedProduct      = (id) => http.post(`/ai/embed/product/${id}`)
export const embedAll          = () => http.post('/ai/embed/all')

// ── Agents ────────────────────────────────────────────────────────────────────

export const runCollectorAgent = (payload) => http.post('/agents/collect', payload)
export const runInsightAgent   = (product_ids) => http.post('/agents/insights', { product_ids })
export const runReportAgent    = (product_ids = null) =>
  http.post('/agents/report', { product_ids })

// ── Export ────────────────────────────────────────────────────────────────────

export const exportCSV  = () => window.open(`${BASE_URL}/export/csv`, '_blank')
export const exportJSON = () => window.open(`${BASE_URL}/export/json`, '_blank')
