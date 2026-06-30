"""
app/services/qa_service.py
============================
Question Answering using Gemini + ChromaDB retrieval (RAG pattern).

Flow:
  User question
       ↓
  SearchService.get_context_for_qa()   ← retrieves relevant product/review texts
       ↓
  Build a grounded prompt with that context
       ↓
  Gemini generates an answer based only on the retrieved context
       ↓
  Return answer

This is a simple Retrieval-Augmented Generation (RAG) implementation — 
a core concept in modern AI applications, great for a portfolio project.
"""

import logging
from typing import Any

from sqlalchemy.orm import Session

from app.services.search_service import SearchService
from app.repositories.product import ProductRepository
from app.repositories.review import ReviewRepository
from app.config.settings import settings

logger = logging.getLogger(__name__)


def _call_gemini(prompt: str) -> str:
    """Call Gemini and return response text, or a fallback string."""
    if not settings.GEMINI_API_KEY:
        return "QA unavailable — GEMINI_API_KEY is not configured."
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as exc:
        logger.error("Gemini QA call failed: %s", exc)
        return "Unable to generate an answer at this time."


class QAService:
    """Answers natural-language questions about products using RAG + Gemini."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.search_svc = SearchService(db)
        self.product_repo = ProductRepository(db)
        self.review_repo = ReviewRepository(db)

    def answer_question(self, question: str) -> dict[str, Any]:
        """
        Answer a free-form question about any product in the database.

        Example questions:
          "Which competitor has better ratings?"
          "What are the biggest complaints about Samsung phones?"
          "Products with excellent battery life"

        Returns
        -------
        dict: { question, answer, context_used (count) }
        """
        logger.info("QA: question=%r", question)

        context_texts = self.search_svc.get_context_for_qa(question)

        if not context_texts:
            return {
                "question": question,
                "answer": (
                    "I couldn't find relevant data to answer this question. "
                    "Make sure products and reviews have been indexed."
                ),
                "context_used": 0,
            }

        context_block = "\n".join(f"  {i+1}. {t}" for i, t in enumerate(context_texts))

        prompt = f"""You are a market intelligence assistant. Answer the user's question using ONLY 
the context provided below. If the context doesn't contain enough information, say so clearly.
Do not make up information that is not in the context.

Context (from product database):
{context_block}

Question: {question}

Provide a clear, concise answer in 2–4 sentences."""

        answer = _call_gemini(prompt)

        return {
            "question": question,
            "answer": answer,
            "context_used": len(context_texts),
        }

    def compare_products(self, product_a_id: int, product_b_id: int) -> dict[str, Any]:
        """
        Generate a structured comparison of two products.

        Fetches both products + their reviews, then asks Gemini to compare them.

        Returns
        -------
        dict: { product_a, product_b, comparison (str) }
        """
        logger.info("Comparing products %d and %d", product_a_id, product_b_id)
        product_a = self.product_repo.get(product_a_id)
        product_b = self.product_repo.get(product_b_id)

        if not product_a or not product_b:
            logger.warning("One or both products not found: %d, %d", product_a_id, product_b_id)
            return {
                "error": "One or both products not found.",
                "product_a_id": product_a_id,
                "product_b_id": product_b_id,
            }

        reviews_a = self.review_repo.get_by_product(product_a_id)
        reviews_b = self.review_repo.get_by_product(product_b_id)

        def product_block(product, reviews) -> str:
            review_sample = " | ".join(
                r.review_text for r in reviews[:5] if r.review_text
            ) or "No reviews available."
            return (
                f"Name: {product.name}\n"
                f"Brand: {product.brand or 'N/A'}\n"
                f"Category: {product.category or 'N/A'}\n"
                f"Price: {product.price or 'N/A'}\n"
                f"Rating: {product.rating or 'N/A'} ({product.review_count or 0} reviews)\n"
                f"Sample reviews: {review_sample}"
            )

        prompt = f"""You are a product comparison analyst. Compare the following two products objectively.

=== Product A ===
{product_block(product_a, reviews_a)}

=== Product B ===
{product_block(product_b, reviews_b)}

Write a structured comparison covering:
1. Price vs. Value
2. Customer satisfaction (based on ratings and reviews)
3. Key strengths of each
4. Which product you would recommend and why

Keep your response concise (4–6 sentences or a short bullet list)."""

        comparison = _call_gemini(prompt)

        return {
            "product_a": {"id": product_a.id, "name": product_a.name},
            "product_b": {"id": product_b.id, "name": product_b.name},
            "comparison": comparison,
        }
