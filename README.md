<div align="center">
  <h1>🧠 AI Market Intelligence Platform</h1>
  <p>A full-stack AI-powered platform for e-commerce data aggregation, NLP analysis, and semantic search.</p>
</div>

---

## 📖 Project Overview

The **AI Market Intelligence Platform** is a modern web application that collects product data from e-commerce websites, cleans and normalises it, and applies a comprehensive AI intelligence pipeline to extract actionable market insights.

This project was built as a final-year Computer Science portfolio project, demonstrating production-ready backend architecture, applied Machine Learning (NLP/Embeddings), LLM integration (RAG), and a modern React frontend.

---

## ✨ Key Features

1. **Robust Data Pipeline**
   - Playwright/BeautifulSoup scrapers for automated data collection.
   - Pandas-based cleaning module for deduplication and text normalization.
   - Support for bulk CSV data imports.

2. **Advanced NLP & Machine Learning**
   - **Sentiment Analysis**: VADER (NLTK) for review classification.
   - **Keyword Extraction**: TF-IDF scoring via scikit-learn.
   - **Topic Modeling**: LDA clustering to discover hidden consumer themes.

3. **Semantic Search & Vector Database**
   - `sentence-transformers` (`all-MiniLM-L6-v2`) used to embed products and reviews.
   - **ChromaDB** used for blazing-fast semantic similarity search (Cosine).

4. **Generative AI (Google Gemini)**
   - **Retrieval-Augmented Generation (RAG)**: Ask questions about the product dataset.
   - **Automated Summaries**: AI-generated executive summaries and product comparisons.
   - **Market Reports**: Automated generation of comprehensive Markdown reports.

5. **Modern Interactive Dashboard**
   - Built with **React**, **Vite**, and **TailwindCSS**.
   - Interactive data visualizations using **Recharts**.
   - Full integration with the FastAPI backend via Axios.

---

## 🏛️ Architecture

The backend follows a strict layered architecture pattern for maximum maintainability:

```text
API Layer  →  Service Layer  →  Repository Layer  →  PostgreSQL Database
                  ↓
           AI Intelligence Layer (NLP + Embeddings + ChromaDB + Gemini)
                  ↓
           React Frontend (Vite + TailwindCSS)
```

*(See the `docs/` folder for detailed Architecture Diagrams, ERDs, and API References).*

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ai-market-intelligence.git
cd "AI Market Intelligence Platform"
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate            # Windows
source venv/bin/activate         # macOS / Linux

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers (for scraping)
playwright install chromium

# Set up environment variables
cp .env.example .env
# Edit .env: Add your PostgreSQL URL and GEMINI_API_KEY
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Database Seeding (Sample Data)
To quickly test the platform without scraping, use the provided sample data:
```bash
# From the root directory
python scripts/seed.py
```
*This populates PostgreSQL with 30 sample products and 45 realistic reviews.*

---

## 🚀 Running the Platform

You need two terminals to run the platform locally.

**Terminal 1 (FastAPI Backend):**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- Swagger API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

**Terminal 2 (React Frontend):**
```bash
cd frontend
npm run dev
```
- Interactive Dashboard: [http://localhost:5173](http://localhost:5173)

---

## 📸 Screenshots

*(Replace these placeholders with actual screenshots of your running application)*

| Dashboard Overview | Semantic Search |
| :---: | :---: |
| ![Dashboard](https://via.placeholder.com/600x400.png?text=Dashboard+Screenshot) | ![Search](https://via.placeholder.com/600x400.png?text=Semantic+Search) |
| **Product Insights** | **Market Reports** |
| ![Insights](https://via.placeholder.com/600x400.png?text=AI+Insights) | ![Reports](https://via.placeholder.com/600x400.png?text=Generated+Reports) |

---

## 📡 API Overview

The platform exposes over 30 RESTful endpoints. Here is a high-level summary:

- `/api/v1/products`: Standard CRUD operations.
- `/api/v1/scrape/*`: Trigger URL scrapers and CSV uploads.
- `/api/v1/dashboard/*`: Pre-aggregated data for frontend charts.
- `/api/v1/ai/*`: NLP triggers, vector embeddings, Gemini Q&A.
- `/api/v1/agents/*`: Trigger autonomous analysis pipelines.

*For full details, see the Swagger UI or `docs/api_reference.md`.*

---

## 🧪 Testing

The backend includes a comprehensive pytest suite that runs against an in-memory SQLite database (no PostgreSQL required for testing).

```bash
pytest tests/ -v
```

---

## 🔜 Future Scope

While the platform is feature-complete for a portfolio project, future enterprise enhancements could include:
- **Authentication**: JWT-based user login and role-based access control.
- **Task Queues**: Offload heavy scraping and AI tasks to Celery + Redis.
- **Containerization**: Full Docker support with Docker Compose.
- **Time-Series Analysis**: Tracking product price changes over time.

---

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy 2.0, Pydantic v2
- **Database**: PostgreSQL (Relational), ChromaDB (Vector)
- **Machine Learning**: NLTK, scikit-learn, SentenceTransformers
- **Generative AI**: Google Gemini API (`gemini-1.5-flash`)
- **Frontend**: React, Vite, TailwindCSS, Recharts
- **Data processing**: Pandas, BeautifulSoup, Playwright

---
<div align="center">
  <p>Built with ❤️ by a Computer Science Student.</p>
</div>
