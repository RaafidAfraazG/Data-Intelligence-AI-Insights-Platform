# API Reference

The AI Market Intelligence Platform exposes a RESTful API powered by FastAPI.

**Base URL**: `http://localhost:8000/api/v1`

---

## 🛒 Products

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/products` | List all products (paginated) |
| `POST` | `/products` | Create a new product |
| `GET` | `/products/{id}` | Get product details by ID |
| `PUT` | `/products/{id}` | Update product information |
| `DELETE` | `/products/{id}` | Delete a product and its reviews |
| `GET` | `/products/search?q={query}` | Exact/partial keyword search on product name |

## 💬 Reviews

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/reviews` | List all reviews |
| `GET` | `/products/{id}/reviews` | List all reviews for a specific product |
| `POST` | `/reviews` | Add a review for a product |

## 🧠 AI & NLP

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/ai/sentiment` | Analyze sentiment of text using VADER |
| `POST` | `/ai/keywords` | Extract top TF-IDF keywords |
| `POST` | `/ai/topics` | Discover themes using LDA topic modeling |
| `POST` | `/ai/summarize/product/{id}` | Generate a Gemini summary of a product |
| `POST` | `/ai/summarize/reviews/{id}` | Generate a Gemini summary of all reviews |
| `GET` | `/ai/insights/{id}` | Get AI strengths, weaknesses, and marketing insights |
| `POST` | `/ai/compare` | Compare two products using AI |
| `POST` | `/ai/answer` | Ask a natural language question (RAG over ChromaDB) |
| `POST` | `/ai/embed/product/{id}` | Index a single product and its reviews in ChromaDB |
| `POST` | `/ai/embed/all` | Index everything in the database into ChromaDB |

## 📊 Dashboard

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/dashboard/overview` | KPI stats (Total products, avg rating, overall sentiment) |
| `GET` | `/dashboard/sentiment` | Pie chart data for overall sentiment distribution |
| `GET` | `/dashboard/keywords` | Bar chart data for top keywords across the platform |
| `GET` | `/dashboard/topics` | Aggregate LDA topics across the platform |
| `GET` | `/dashboard/competitors` | Average ratings grouped by brand |
| `GET` | `/dashboard/insights` | AI-generated executive market summary |
| `GET` | `/dashboard/search?q={query}` | Semantic vector search using ChromaDB |

## 🤖 Agents & Reports

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/agents/collect` | Trigger scraping agent |
| `POST` | `/agents/insights` | Trigger NLP + Embedding AI pipeline |
| `POST` | `/agents/report` | Generate a full Markdown report |
| `GET` | `/export/csv` | Download product database as CSV |
| `GET` | `/export/json` | Download product database as JSON |
