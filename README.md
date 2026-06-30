<div align="center">

# 🧠 AI Market Intelligence Platform

**An AI-powered platform for collecting, analyzing, and searching e-commerce market data using NLP, semantic search, and LLMs.**

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-orange)
![Gemini](https://img.shields.io/badge/Gemini-LLM-purple)

</div>

---

# 📖 Overview

AI Market Intelligence Platform is an end-to-end data intelligence system that automatically collects product and customer review data from multiple sources, cleans and structures it, performs NLP analysis, enables semantic search using vector embeddings, and generates AI-powered business insights.

This project demonstrates the complete **Data Intelligence pipeline**, from data collection to AI-driven analytics, using modern backend engineering and machine learning tools.

---

# ✨ Features

### 📊 Data Collection
- Web scraping using Playwright & BeautifulSoup
- Customer review collection
- Competitor product collection
- Blog article scraping
- Manual URL input
- CSV import

### 🧹 Data Processing
- Duplicate removal
- Missing value handling
- HTML cleaning
- Price normalization
- Category standardization
- Text normalization

### 🤖 AI & NLP
- Sentiment Analysis
- Keyword Extraction
- Topic Modeling
- Product & Review Summaries
- AI-generated Business Insights

### 🔍 Semantic Search
- Sentence Transformer Embeddings
- ChromaDB Vector Database
- Similar Product Search
- Natural Language Question Answering

### 📈 Dashboard
- Product Analytics
- Sentiment Distribution
- Keyword Trends
- Competitor Comparison
- AI Insights
- Report Generation

---

# 🏗️ Architecture

```text
             React Dashboard
                    │
                    ▼
             FastAPI Backend
                    │
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
 Scrapers      NLP Pipeline    AI Services
     │              │              │
     └──────────────┼──────────────┘
                    ▼
         PostgreSQL + ChromaDB
                    │
                    ▼
             Gemini API (LLM)
```

---

# 🛠️ Tech Stack

| Category | Technologies |
|-----------|--------------|
| Backend | FastAPI, Python, SQLAlchemy |
| Frontend | React, Vite, Tailwind CSS |
| Database | PostgreSQL, ChromaDB |
| AI | Gemini API, Sentence Transformers |
| NLP | NLTK, Scikit-learn |
| Data | Pandas, NumPy |
| Scraping | Playwright, BeautifulSoup |

---

# 📂 Project Structure

```text
AI Market Intelligence Platform
│
├── app/
├── frontend/
├── data/
├── docs/
├── reports/
├── scripts/
├── tests/
├── requirements.txt
└── README.md
```

---

# 🚀 Getting Started

## Backend

```bash
git clone https://github.com/RaafidAfraazG/Data-Intelligence-AI-Insights-Platform.git

cd Data-Intelligence-AI-Insights-Platform

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt

playwright install chromium

uvicorn main:app --reload
```

Swagger API:

```
http://localhost:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```
http://localhost:5173
```
# 📡 API Modules

- Product Management
- Review Management
- Web Scraping
- Data Cleaning
- Dashboard Analytics
- Semantic Search
- AI Insights
- Report Generation
# 🔮 Future Improvements

- Authentication
- Docker Deployment
- Scheduled Data Collection
- Advanced Analytics
- Time-series Price Tracking

---
