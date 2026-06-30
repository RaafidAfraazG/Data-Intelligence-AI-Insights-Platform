"""
app/api/routes/dashboard.py
=============================
Dashboard API endpoints — return frontend-ready JSON for the React dashboard.

GET /api/v1/dashboard/overview    — summary stats
GET /api/v1/dashboard/sentiment   — sentiment distribution
GET /api/v1/dashboard/keywords    — top keywords
GET /api/v1/dashboard/topics      — discussion topics
GET /api/v1/dashboard/competitors — brand comparison
GET /api/v1/dashboard/insights    — AI executive summary
GET /api/v1/dashboard/search      — semantic search
"""

import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.session import get_db
from app.repositories.product import ProductRepository
from app.repositories.review import ReviewRepository
from app.services.search_service import SearchService
from app.services.insight_service import InsightService
from app.nlp.sentiment import product_sentiment_summary
from app.nlp.keywords import extract_keywords
from app.nlp.topics import extract_topics
from app.models.product import Product
from app.core.response import success_response

router = APIRouter(prefix="/dashboard")
logger = logging.getLogger(__name__)


@router.get("/overview", summary="Dashboard overview statistics")
def dashboard_overview(db: Session = Depends(get_db)):
    """Return high-level statistics: product count, review count, avg rating."""
    product_repo = ProductRepository(db)
    review_repo = ReviewRepository(db)

    total_products = product_repo.count()
    total_reviews = review_repo.count()

    # Average rating across all products
    avg_rating_result = db.query(func.avg(Product.rating)).scalar()
    avg_rating = round(float(avg_rating_result), 2) if avg_rating_result else 0.0

    # Reviews with sentiment
    reviews = review_repo.get_all(skip=0, limit=500)
    review_texts = [r.review_text for r in reviews if r.review_text]
    sentiment = product_sentiment_summary(review_texts)

    return success_response(data={
        "total_products": total_products,
        "total_reviews": total_reviews,
        "average_rating": avg_rating,
        "overall_sentiment": sentiment["overall_label"],
        "sentiment_score": sentiment["average_score"],
    })


@router.get("/sentiment", summary="Sentiment distribution across all reviews")
def dashboard_sentiment(db: Session = Depends(get_db)):
    """Return a breakdown of positive/neutral/negative reviews."""
    review_repo = ReviewRepository(db)
    reviews = review_repo.get_all(skip=0, limit=1000)
    review_texts = [r.review_text for r in reviews if r.review_text]
    sentiment = product_sentiment_summary(review_texts)

    # Build chart-friendly format for Recharts
    distribution = sentiment["distribution"]
    chart_data = [
        {"name": "Positive", "value": distribution.get("positive", 0), "color": "#22c55e"},
        {"name": "Neutral",  "value": distribution.get("neutral", 0),  "color": "#f59e0b"},
        {"name": "Negative", "value": distribution.get("negative", 0), "color": "#ef4444"},
    ]
    return success_response(data={
        "chart_data": chart_data,
        "average_score": sentiment["average_score"],
        "overall_label": sentiment["overall_label"],
        "total_reviews": sentiment["total_reviews"],
    })


@router.get("/keywords", summary="Top keywords from all reviews")
def dashboard_keywords(
    top_n: int = Query(default=20, ge=5, le=50),
    db: Session = Depends(get_db),
):
    """Return the most frequent keywords across all reviews (TF-IDF)."""
    review_repo = ReviewRepository(db)
    reviews = review_repo.get_all(skip=0, limit=1000)
    review_texts = [r.review_text for r in reviews if r.review_text]

    keywords = extract_keywords(review_texts, top_n=top_n)
    # Chart-ready format
    chart_data = [{"keyword": k["keyword"], "score": k["score"]} for k in keywords]
    return success_response(data={"keywords": chart_data})


@router.get("/topics", summary="Discussion topics extracted from reviews")
def dashboard_topics(db: Session = Depends(get_db)):
    """Return LDA topic clusters from all review text."""
    review_repo = ReviewRepository(db)
    reviews = review_repo.get_all(skip=0, limit=1000)
    review_texts = [r.review_text for r in reviews if r.review_text]

    topics = extract_topics(review_texts, n_topics=5)
    return success_response(data={"topics": topics})


@router.get("/competitors", summary="Brand comparison — avg rating and review count")
def dashboard_competitors(db: Session = Depends(get_db)):
    """Return per-brand aggregated rating and review counts for competitor charts."""
    results = (
        db.query(
            Product.brand,
            func.avg(Product.rating).label("avg_rating"),
            func.avg(Product.price).label("avg_price"),
            func.count(Product.id).label("product_count"),
            func.sum(Product.review_count).label("total_reviews"),
        )
        .filter(Product.brand.isnot(None))
        .group_by(Product.brand)
        .order_by(func.avg(Product.rating).desc())
        .limit(10)
        .all()
    )

    chart_data = [
        {
            "brand": r.brand,
            "avg_rating": round(float(r.avg_rating), 2) if r.avg_rating else 0,
            "avg_price": round(float(r.avg_price), 2) if r.avg_price else 0,
            "product_count": r.product_count,
            "total_reviews": int(r.total_reviews or 0),
        }
        for r in results
    ]
    return success_response(data={"competitors": chart_data})


@router.get("/insights", summary="AI-generated executive summary")
def dashboard_insights(db: Session = Depends(get_db)):
    """Generate and return an AI executive summary of the whole dataset."""
    product_repo = ProductRepository(db)
    products = product_repo.get_all(skip=0, limit=20)
    product_ids = [p.id for p in products]

    insight_svc = InsightService(db)
    summary = insight_svc.generate_executive_summary(product_ids)

    return success_response(data={"executive_summary": summary})


@router.get("/search", summary="Semantic product search for dashboard")
def dashboard_search(
    q: str = Query(..., min_length=1, description="Natural-language search query"),
    n: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Perform a semantic search and return ranked results for the dashboard."""
    search_svc = SearchService(db)
    results = search_svc.semantic_search_products(query=q, n=n)
    return success_response(data={"query": q, "results": results, "count": len(results)})
