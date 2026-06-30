"""
app/api/routes/ai.py
=====================
AI/NLP endpoints — expose all AI capabilities as REST APIs.

POST /api/v1/ai/sentiment                    — analyze sentiment of texts
POST /api/v1/ai/keywords                     — extract keywords
POST /api/v1/ai/topics                       — extract topics
POST /api/v1/ai/summarize/product/{id}       — product summary via Gemini
POST /api/v1/ai/summarize/reviews/{id}       — review summary via Gemini
GET  /api/v1/ai/insights/{product_id}        — full insight package
POST /api/v1/ai/compare                      — compare two products
POST /api/v1/ai/answer                       — QA endpoint
POST /api/v1/ai/embed/product/{id}           — embed and index a single product
POST /api/v1/ai/embed/all                    — embed all products + reviews
"""

import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.nlp.sentiment import analyze_batch, product_sentiment_summary
from app.nlp.keywords import extract_keywords
from app.nlp.topics import extract_topics
from app.nlp.summarizer import summarize_product, summarize_reviews
from app.services.insight_service import InsightService
from app.services.qa_service import QAService
from app.embeddings.embedding_service import get_embedding, build_product_text
from app.embeddings.vector_store import product_store, review_store
from app.repositories.product import ProductRepository
from app.repositories.review import ReviewRepository
from app.core.exceptions import NotFoundException
from app.core.response import success_response

router = APIRouter(prefix="/ai")
logger = logging.getLogger(__name__)


# ── Request schemas ───────────────────────────────────────────────────────────

class TextsRequest(BaseModel):
    texts: list[str]

class CompareRequest(BaseModel):
    product_a_id: int
    product_b_id: int

class QuestionRequest(BaseModel):
    question: str


# ── NLP endpoints ─────────────────────────────────────────────────────────────

@router.post("/sentiment", summary="Analyze sentiment of a list of texts")
def analyze_sentiment(payload: TextsRequest):
    """
    Run VADER sentiment analysis on each provided text.
    Returns per-text results plus an aggregated summary.
    """
    results = analyze_batch(payload.texts)
    summary = product_sentiment_summary(payload.texts)
    return success_response(data={"individual": results, "summary": summary})


@router.post("/keywords", summary="Extract TF-IDF keywords from texts")
def get_keywords(payload: TextsRequest, top_n: int = 10):
    """Extract the top keywords from a collection of texts."""
    keywords = extract_keywords(payload.texts, top_n=top_n)
    return success_response(data={"keywords": keywords})


@router.post("/topics", summary="Extract discussion topics using LDA")
def get_topics(payload: TextsRequest, n_topics: int = 5):
    """Discover hidden discussion topics in a collection of texts."""
    topics = extract_topics(payload.texts, n_topics=n_topics)
    return success_response(data={"topics": topics})


# ── Summarization endpoints ───────────────────────────────────────────────────

@router.post("/summarize/product/{product_id}", summary="Summarize a product with Gemini")
def summarize_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    """Generate a 2–3 sentence AI summary of a product."""
    product_repo = ProductRepository(db)
    product = product_repo.get(product_id)
    if not product:
        raise NotFoundException("Product", product_id)

    product_dict = {
        "name": product.name,
        "brand": product.brand,
        "category": product.category,
        "price": product.price,
        "rating": product.rating,
        "review_count": product.review_count,
        "description": product.description,
    }
    summary = summarize_product(product_dict)
    return success_response(data={"product_id": product_id, "summary": summary})


@router.post("/summarize/reviews/{product_id}", summary="Summarize reviews for a product")
def summarize_reviews_endpoint(product_id: int, db: Session = Depends(get_db)):
    """Generate an AI summary of all customer reviews for a product."""
    review_repo = ReviewRepository(db)
    reviews = review_repo.get_by_product(product_id)
    review_texts = [r.review_text for r in reviews if r.review_text]

    summary = summarize_reviews(review_texts)
    return success_response(data={
        "product_id": product_id,
        "review_count": len(review_texts),
        "summary": summary,
    })


# ── Insight endpoints ─────────────────────────────────────────────────────────

@router.get("/insights/{product_id}", summary="Generate full AI insight package for a product")
def get_product_insights(product_id: int, db: Session = Depends(get_db)):
    """Generate strengths, weaknesses, pain points, and marketing recommendations."""
    product_repo = ProductRepository(db)
    if not product_repo.get(product_id):
        raise NotFoundException("Product", product_id)

    insight_svc = InsightService(db)
    return success_response(data={
        "product_id": product_id,
        "strengths": insight_svc.generate_product_strengths(product_id),
        "weaknesses": insight_svc.generate_product_weaknesses(product_id),
        "pain_points": insight_svc.generate_pain_points(product_id),
        "marketing_recommendations": insight_svc.generate_marketing_recommendations(product_id),
        "seo_keywords": insight_svc.generate_seo_keywords(product_id),
    })


@router.post("/compare", summary="Compare two products with AI")
def compare_products(payload: CompareRequest, db: Session = Depends(get_db)):
    """Generate a structured AI comparison of two products."""
    qa_svc = QAService(db)
    result = qa_svc.compare_products(payload.product_a_id, payload.product_b_id)
    return success_response(data=result)


# ── QA endpoint ───────────────────────────────────────────────────────────────

@router.post("/answer", summary="Ask a natural-language question about products")
def answer_question(payload: QuestionRequest, db: Session = Depends(get_db)):
    """
    RAG-powered QA: embeds question, retrieves context from ChromaDB,
    and generates a grounded answer using Gemini.
    """
    qa_svc = QAService(db)
    result = qa_svc.answer_question(payload.question)
    return success_response(data=result)


# ── Embedding endpoints ───────────────────────────────────────────────────────

@router.post("/embed/product/{product_id}", summary="Embed and index a single product")
def embed_product(product_id: int, db: Session = Depends(get_db)):
    """Generate an embedding for a product and store it in ChromaDB."""
    product_repo = ProductRepository(db)
    product = product_repo.get(product_id)
    if not product:
        raise NotFoundException("Product", product_id)

    text = build_product_text({
        "name": product.name,
        "brand": product.brand,
        "category": product.category,
        "description": product.description,
    })
    embedding = get_embedding(text)

    if not embedding:
        return success_response(
            data={"product_id": product_id, "indexed": False},
            message="Embedding model unavailable.",
        )

    success = product_store.update(
        doc_id=str(product_id),
        text=text,
        embedding=embedding,
        metadata={
            "name": product.name or "",
            "brand": product.brand or "",
            "category": product.category or "",
            "price": str(product.price or ""),
            "rating": str(product.rating or ""),
        },
    )
    return success_response(data={"product_id": product_id, "indexed": success})


@router.post("/embed/all", summary="Embed all products and reviews into ChromaDB")
def embed_all(db: Session = Depends(get_db)):
    """
    Batch-embed all products and reviews and store in ChromaDB.
    Run this once after importing data to enable semantic search.
    """
    product_repo = ProductRepository(db)
    review_repo = ReviewRepository(db)

    products = product_repo.get_all(skip=0, limit=10_000)
    reviews = review_repo.get_all(skip=0, limit=50_000)

    products_indexed = 0
    reviews_indexed = 0

    for product in products:
        text = build_product_text({
            "name": product.name,
            "brand": product.brand,
            "category": product.category,
            "description": product.description,
        })
        embedding = get_embedding(text)
        if embedding:
            product_store.update(
                doc_id=str(product.id),
                text=text,
                embedding=embedding,
                metadata={
                    "name": product.name or "",
                    "brand": product.brand or "",
                    "category": product.category or "",
                    "price": str(product.price or ""),
                    "rating": str(product.rating or ""),
                },
            )
            products_indexed += 1

    for review in reviews:
        if not review.review_text:
            continue
        embedding = get_embedding(review.review_text)
        if embedding:
            review_store.update(
                doc_id=str(review.id),
                text=review.review_text,
                embedding=embedding,
                metadata={
                    "product_id": str(review.product_id),
                    "rating": str(review.rating or ""),
                    "reviewer": review.reviewer or "",
                },
            )
            reviews_indexed += 1

    return success_response(data={
        "products_indexed": products_indexed,
        "reviews_indexed": reviews_indexed,
        "message": "Embedding complete. Semantic search is now available.",
    })
