"""
app/config/settings.py
======================
Central application configuration loaded from environment variables.
Uses python-dotenv to read from a .env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    All application settings in one place.
    Add new settings here as the project grows.
    """

    # ── App ───────────────────────────────────────────────────────────────────
    APP_NAME: str = os.getenv("APP_NAME", "AI Market Intelligence Platform")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/market_intelligence",
    )

    # ── Logging ───────────────────────────────────────────────────────────────
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")

    # ── Scraping ──────────────────────────────────────────────────────────────
    SCRAPING_TIMEOUT: int = int(os.getenv("SCRAPING_TIMEOUT", "30"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))

    # ── Export ────────────────────────────────────────────────────────────────
    EXPORTS_DIR: str = os.getenv("EXPORTS_DIR", "exports")
    UPLOADS_DIR: str = os.getenv("UPLOADS_DIR", "uploads")

    # ── Gemini AI ─────────────────────────────────────────────────────────────
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # ── Embeddings ────────────────────────────────────────────────────────────
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # ── ChromaDB (embedded, no server needed) ─────────────────────────────────
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "chroma_db")

    # ── Reports ───────────────────────────────────────────────────────────────
    REPORTS_DIR: str = os.getenv("REPORTS_DIR", "reports")


# Single shared instance used across the application
settings = Settings()
