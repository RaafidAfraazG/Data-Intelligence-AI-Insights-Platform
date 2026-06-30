"""
app/agents/insight_generator_agent.py
=======================================
InsightGeneratorAgent — runs the full AI analysis pipeline for a set of products.

Pipeline:
  1. Fetch products + reviews from PostgreSQL
  2. Run NLP (sentiment, keywords, topics)
  3. Generate and store embeddings in ChromaDB
  4. Generate AI insights via InsightService (Gemini)
  5. Return a structured insight report dict
"""

import logging
from typing import Any

from sqlalchemy.orm import Session

from app.repositories.product import ProductRepository
from app.repositories.review import ReviewRepository
from app.nlp.sentiment import product_sentiment_summary
from app.nlp.keywords import extract_keywords
from app.nlp.topics import extract_topics
from app.embeddings.embedding_service import get_embedding, build_product_text
from app.embeddings.vector_store import product_store, review_store
from app.services.insight_service import InsightService

logger = logging.getLogger(__name__)


class InsightGeneratorAgent:
    """
    Runs NLP analysis, embedding indexing, and AI insight generation
    for a list of product IDs.
    """

    def __init__(self, db: Session) -> None:
        self.db = db
        self.product_repo = ProductRepository(db)
        self.review_repo = ReviewRepository(db)
        self.insight_svc = InsightService(db)

    def run(self, product_ids: list[int]) -> dict[str, Any]:
        """
        Execute the complete AI insight pipeline.

        Parameters
        ----------
        product_ids : list[int]
            IDs of products to analyse.

        Returns
        -------
        dict with keys:
            products_analysed, reviews_analysed,
            sentiment_summary, top_keywords, topics,
            executive_summary, indexed_to_chromadb
        """
        logger.info("InsightGeneratorAgent starting for %d products.", len(product_ids))

        all_review_texts: list[str] = []
        indexed_count = 0

        # ── Step 1: Collect review texts + build embeddings ───────────────────
        for pid in product_ids:
            product = self.product_repo.get(pid)
            if not product:
                continue

            # Build and store product embedding
            product_text = build_product_text({
                "name": product.name,
                "brand": product.brand,
                "category": product.category,
                "description": product.description,
            })
            embedding = get_embedding(product_text)
            if embedding:
                product_store.update(
                    doc_id=str(product.id),
                    text=product_text,
                    embedding=embedding,
                    metadata={
                        "name": product.name or "",
                        "brand": product.brand or "",
                        "category": product.category or "",
                        "price": str(product.price or ""),
                        "rating": str(product.rating or ""),
                    },
                )
                indexed_count += 1

            # Collect + embed reviews
            reviews = self.review_repo.get_by_product(pid)
            for review in reviews:
                if review.review_text:
                    all_review_texts.append(review.review_text)
                    review_embedding = get_embedding(review.review_text)
                    if review_embedding:
                        review_store.update(
                            doc_id=str(review.id),
                            text=review.review_text,
                            embedding=review_embedding,
                            metadata={
                                "product_id": str(review.product_id),
                                "rating": str(review.rating or ""),
                                "reviewer": review.reviewer or "",
                            },
                        )

        # ── Step 2: NLP analysis ──────────────────────────────────────────────
        sentiment_summary = product_sentiment_summary(all_review_texts)
        top_keywords = extract_keywords(all_review_texts, top_n=10)
        topics = extract_topics(all_review_texts, n_topics=5)

        # ── Step 3: AI executive summary ──────────────────────────────────────
        exec_summary = self.insight_svc.generate_executive_summary(product_ids)

        logger.info(
            "InsightGeneratorAgent complete. indexed=%d, reviews=%d",
            indexed_count, len(all_review_texts)
        )

        return {
            "products_analysed": len(product_ids),
            "reviews_analysed": len(all_review_texts),
            "sentiment_summary": sentiment_summary,
            "top_keywords": top_keywords,
            "topics": topics,
            "executive_summary": exec_summary,
            "indexed_to_chromadb": indexed_count,
        }
