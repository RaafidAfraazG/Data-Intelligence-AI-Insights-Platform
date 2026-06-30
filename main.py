"""
AI Market Intelligence Platform
================================
Main application entry point.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import products, reviews, scraping, cleaning, export
from app.api.routes import dashboard, ai, agents
from app.core.exceptions import register_exception_handlers
from app.config.settings import settings
from app.config.logging_config import setup_logging
from app.database.session import engine
from app.database import base  # noqa: F401 — ensures models are registered


# ── Startup / Shutdown ────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting AI Market Intelligence Platform...")

    # Create all database tables on startup
    from app.database.base import Base
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ensured.")

    yield

    logger.info("Shutting down AI Market Intelligence Platform.")


# ── App Metadata ──────────────────────────────────────────────────────────────
tags_metadata = [
    {
        "name": "Dashboard",
        "description": "Pre-aggregated statistics and chart data for the React dashboard frontend.",
    },
    {
        "name": "Products",
        "description": "CRUD operations for products scraped or imported into the system.",
    },
    {
        "name": "Reviews",
        "description": "CRUD operations for user reviews linked to products.",
    },
    {
        "name": "AI & NLP",
        "description": "Text analysis, sentiment scoring, Gemini LLM integrations, and semantic search.",
    },
    {
        "name": "Agents",
        "description": "Trigger automated pipelines for scraping, insights, and report generation.",
    },
    {
        "name": "Scraping & Export",
        "description": "Triggers for Playwright/BS4 scrapers and data export functions.",
    }
]


# ── App Factory ───────────────────────────────────────────────────────────────

def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Market Intelligence API",
        description=(
            "A comprehensive AI-powered platform for collecting, cleaning, and analysing e-commerce data. "
            "Features include NLP processing, semantic vector search via ChromaDB, and Generative AI insights using Google Gemini."
        ),
        version=settings.APP_VERSION,
        openapi_tags=tags_metadata,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS — allow all origins for local development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(products.router, prefix="/api/v1", tags=["Products"])
    app.include_router(reviews.router,  prefix="/api/v1", tags=["Reviews"])
    app.include_router(scraping.router, prefix="/api/v1", tags=["Scraping"])
    app.include_router(cleaning.router, prefix="/api/v1", tags=["Cleaning"])
    app.include_router(export.router,   prefix="/api/v1", tags=["Export"])
    # ── AI Intelligence Layer ──────────────────────────────────────────────────
    app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard"])
    app.include_router(ai.router,        prefix="/api/v1", tags=["AI & NLP"])
    app.include_router(agents.router,    prefix="/api/v1", tags=["Agents"])

    # Register global exception handlers
    register_exception_handlers(app)

    return app


app = create_app()


# ── Health Check ──────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "AI Market Intelligence Platform is running."}


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
