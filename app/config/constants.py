"""
app/config/constants.py
=======================
Application-wide constants.
Add new constants here; never scatter magic values across modules.
"""

# ── Pagination ────────────────────────────────────────────────────────────────
DEFAULT_PAGE_SIZE: int = 20
MAX_PAGE_SIZE: int = 100

# ── Product categories (used for normalisation) ───────────────────────────────
KNOWN_CATEGORIES: list[str] = [
    "electronics",
    "clothing",
    "home & kitchen",
    "books",
    "sports & outdoors",
    "beauty & personal care",
    "toys & games",
    "health & wellness",
    "automotive",
    "other",
]

# ── Supported scraper types ───────────────────────────────────────────────────
SCRAPER_TYPES: list[str] = ["playwright", "beautifulsoup", "csv"]

# ── Supported export formats ──────────────────────────────────────────────────
EXPORT_FORMATS: list[str] = ["csv", "json"]

# ── Currency symbols to strip during price normalisation ─────────────────────
CURRENCY_SYMBOLS: list[str] = ["$", "€", "£", "¥", "₹", "₩"]

# ── HTTP request headers used by scrapers ────────────────────────────────────
DEFAULT_HEADERS: dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# ── Sentiment labels ──────────────────────────────────────────────────────────
SENTIMENT_POSITIVE: str = "positive"
SENTIMENT_NEUTRAL: str = "neutral"
SENTIMENT_NEGATIVE: str = "negative"

# VADER compound score thresholds
VADER_POSITIVE_THRESHOLD: float = 0.05
VADER_NEGATIVE_THRESHOLD: float = -0.05

# ── NLP defaults ──────────────────────────────────────────────────────────────
DEFAULT_TOP_KEYWORDS: int = 10
DEFAULT_TOP_TOPICS: int = 5
DEFAULT_TOPIC_WORDS: int = 8

# ── ChromaDB collection names ─────────────────────────────────────────────────
CHROMA_PRODUCTS_COLLECTION: str = "products"
CHROMA_REVIEWS_COLLECTION: str = "reviews"

# ── Gemini prompt limits ──────────────────────────────────────────────────────
MAX_REVIEW_CHARS_FOR_SUMMARY: int = 8000   # Truncate review text before sending to Gemini
MAX_CONTEXT_DOCS_FOR_QA: int = 5            # Number of ChromaDB results used as QA context
