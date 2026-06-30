"""
app/services/search_service.py
================================
Semantic search powered by embeddings + ChromaDB.

Instead of simple keyword matching (already in ProductRepository),
this service embeds the user's query and finds products/reviews
that are *semantically* similar — even if exact words don't match.

Example:
  query: "gaming laptops under 70000"
  → Finds products related to gaming, performance, laptops even if the
    exact phrase doesn't appear in the product name.
"""

import logging
from typing import Any

from sqlalchemy.orm import Session

from app.embeddings.embedding_service import get_embedding
from app.embeddings.vector_store import product_store, review_store
from app.repositories.product import ProductRepository
from app.repositories.review import ReviewRepository
from app.config.constants import MAX_CONTEXT_DOCS_FOR_QA

logger = logging.getLogger(__name__)


class SearchService:
    """Semantic search across products and reviews using ChromaDB."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.product_repo = ProductRepository(db)
        self.review_repo = ReviewRepository(db)

    def semantic_search_products(
        self, query: str, n: int = 10
    ) -> list[dict[str, Any]]:
        """
        Find products semantically similar to the query.

        Steps:
        1. Embed the query text
        2. Search ChromaDB for similar product embeddings
        3. Fetch full product records from PostgreSQL
        4. Return ranked results

        Parameters
        ----------
        query : str   — natural-language search query
        n : int       — number of results to return

        Returns
        -------
        list[dict]  — ranked product records with a 'similarity_score' field
        """
        logger.info("Semantic product search: query=%r, n=%d", query, n)

        query_embedding = get_embedding(query)
        if not query_embedding:
            logger.warning("Could not embed query, falling back to keyword search.")
            return self._keyword_fallback(query, n)

        chroma_results = product_store.search(query_embedding, n_results=n)

        if not chroma_results:
            logger.info("No ChromaDB results for query=%r. Is the index populated?", query)
            return []

        results = []
        for item in chroma_results:
            try:
                product_id = int(item["id"])
                product = self.product_repo.get(product_id)
                if product:
                    results.append({
                        "id": product.id,
                        "name": product.name,
                        "brand": product.brand,
                        "category": product.category,
                        "price": product.price,
                        "rating": product.rating,
                        "review_count": product.review_count,
                        "source": product.source,
                        "similarity_score": round(1 - item["distance"], 4),
                    })
            except (ValueError, TypeError):
                continue

        return results

    def semantic_search_reviews(
        self, query: str, n: int = 10
    ) -> list[dict[str, Any]]:
        """
        Find reviews semantically similar to the query.
        Useful for finding all reviews that mention a specific pain point.
        """
        logger.info("Semantic review search: query=%r, n=%d", query, n)

        query_embedding = get_embedding(query)
        if not query_embedding:
            return []

        chroma_results = review_store.search(query_embedding, n_results=n)

        results = []
        for item in chroma_results:
            try:
                review_id = int(item["id"])
                review = self.review_repo.get(review_id)
                if review:
                    results.append({
                        "id": review.id,
                        "product_id": review.product_id,
                        "review_text": review.review_text,
                        "rating": review.rating,
                        "reviewer": review.reviewer,
                        "similarity_score": round(1 - item["distance"], 4),
                    })
            except (ValueError, TypeError):
                continue

        return results

    def get_context_for_qa(self, question: str) -> list[str]:
        """
        Retrieve the most relevant product and review texts for a QA question.
        Used by QAService to build the Gemini prompt context.
        """
        query_embedding = get_embedding(question)
        if not query_embedding:
            return []

        product_results = product_store.search(query_embedding, n_results=MAX_CONTEXT_DOCS_FOR_QA)
        review_results = review_store.search(query_embedding, n_results=MAX_CONTEXT_DOCS_FOR_QA)

        context = []
        for item in product_results:
            context.append(f"[Product] {item['text']}")
        for item in review_results:
            context.append(f"[Review] {item['text']}")

        return context

    # ── Fallback ──────────────────────────────────────────────────────────────

    def _keyword_fallback(self, query: str, n: int) -> list[dict[str, Any]]:
        """Simple keyword fallback when embeddings are unavailable."""
        products = self.product_repo.search_by_name(query, skip=0, limit=n)
        return [
            {
                "id": p.id,
                "name": p.name,
                "brand": p.brand,
                "category": p.category,
                "price": p.price,
                "rating": p.rating,
                "review_count": p.review_count,
                "source": p.source,
                "similarity_score": None,
            }
            for p in products
        ]
