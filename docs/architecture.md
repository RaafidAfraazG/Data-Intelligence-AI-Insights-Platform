# System Architecture

The AI Market Intelligence Platform follows a classic multi-tier architecture, augmented with an AI Intelligence Layer.

## High-Level Architecture

```mermaid
graph TD
    %% Define Styles
    classDef client fill:#3b82f6,stroke:#1d4ed8,stroke-width:2px,color:#fff
    classDef api fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff
    classDef ai fill:#8b5cf6,stroke:#6d28d9,stroke-width:2px,color:#fff
    classDef data fill:#f59e0b,stroke:#b45309,stroke-width:2px,color:#fff
    classDef ext fill:#64748b,stroke:#334155,stroke-width:2px,color:#fff

    %% Components
    Client[React Dashboard<br>Vite, Tailwind]:::client
    
    API[FastAPI Router Layer]:::api
    Service[Service Layer]:::api
    Repo[Repository Layer]:::api
    
    Scraper[Scraping Module<br>Playwright, BS4]:::ext
    
    NLP[NLP Module<br>VADER, TF-IDF]:::ai
    Embed[Embedding Service<br>SentenceTransformers]:::ai
    Agents[AI Agents<br>Data, Insights, Reports]:::ai
    
    PG[(PostgreSQL<br>SQLAlchemy)]:::data
    Chroma[(ChromaDB<br>Vector Store)]:::data
    Gemini[Google Gemini API]:::ext
    
    %% Relationships
    Client <-->|REST / JSON| API
    
    API --> Service
    Service --> Repo
    Repo <--> PG
    
    Service --> Scraper
    Scraper -->|Internet| Web[Websites]
    
    Service --> NLP
    Service --> Embed
    Service --> Agents
    
    Embed <--> Chroma
    Agents --> Gemini
    NLP --> Gemini
```

## Application Layers

1. **API Layer (`app/api/routes`)**: Defines REST endpoints, validates incoming JSON using Pydantic, and returns formatted responses.
2. **Service Layer (`app/services`)**: Orchestrates business logic. It combines multiple repositories or external tools (like AI or Scraping) to fulfill a request.
3. **Repository Layer (`app/repositories`)**: Abstracts database interactions. Extends a generic CRUD base class with model-specific SQL queries.
4. **AI Intelligence Layer (`app/nlp`, `app/embeddings`, `app/agents`)**: Handles text preprocessing, semantic embeddings, sentiment analysis, and interaction with the Google Gemini LLM.
