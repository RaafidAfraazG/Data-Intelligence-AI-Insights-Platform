# Database Schema

The platform uses **PostgreSQL** as the primary relational database, managed via **SQLAlchemy 2.0 ORM**.

## Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    PRODUCT ||--o{ REVIEW : has
    PRODUCT ||--o{ PRODUCT_METADATA : has
    PRODUCT {
        int id PK
        string name
        string brand
        string category
        float price
        float rating
        int review_count
        text description
        string source
        datetime created_at
    }
    
    REVIEW {
        int id PK
        int product_id FK
        string reviewer
        float rating
        text review_text
        date review_date
        datetime created_at
    }
    
    PRODUCT_METADATA {
        int id PK
        int product_id FK
        string key
        string value
    }
    
    SEARCH_HISTORY {
        int id PK
        string query
        datetime timestamp
        int results_count
    }
    
    SOURCE {
        int id PK
        string domain
        string base_url
        boolean is_active
        datetime last_scraped
    }
```

## Vector Database

In addition to PostgreSQL, the platform uses **ChromaDB** (an embedded vector database stored in the `chroma_db/` directory).

- **Collection**: `market_intel_collection`
- **Embeddings**: Generated using `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions).
- **Metadata Stored**:
  - `type`: Either `product` or `review`
  - `id`: The PostgreSQL primary key corresponding to the record
  - `brand`, `category`: Stored for filtering
