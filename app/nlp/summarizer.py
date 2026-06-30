"""
app/nlp/summarizer.py
======================
AI-powered text summarization using Google Gemini.

Generates:
  - Product summaries (name, brand, category, price, rating → concise paragraph)
  - Review summaries (aggregate all reviews → customer sentiment paragraph)

Gracefully falls back to a placeholder if GEMINI_API_KEY is not set.
"""

import logging
from typing import Any

from app.config.settings import settings
from app.config.constants import MAX_REVIEW_CHARS_FOR_SUMMARY

logger = logging.getLogger(__name__)


def _get_gemini_client():
    """Return a configured Gemini GenerativeModel, or None if key is missing."""
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not set. Summaries will be unavailable.")
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        return genai.GenerativeModel(settings.GEMINI_MODEL)
    except ImportError:
        logger.error("google-generativeai is not installed. Run: pip install google-generativeai")
        return None
    except Exception as exc:
        logger.error("Failed to initialise Gemini client: %s", exc)
        return None


def _call_gemini(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the text response.
    Returns a placeholder string on any failure.
    """
    model = _get_gemini_client()
    if model is None:
        return "Summary unavailable — Gemini API key not configured."
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as exc:
        logger.error("Gemini API call failed: %s", exc)
        return "Summary generation failed. Please try again."


# ── Product Summary ───────────────────────────────────────────────────────────

def summarize_product(product: dict[str, Any]) -> str:
    """
    Generate a 2–3 sentence product summary using Gemini.

    Parameters
    ----------
    product : dict
        Keys: name, brand, category, price, rating, review_count, description

    Returns
    -------
    str
        A concise AI-generated product summary.
    """
    name        = product.get("name", "Unknown Product")
    brand       = product.get("brand") or "Unknown Brand"
    category    = product.get("category") or "General"
    price       = product.get("price")
    rating      = product.get("rating")
    review_count= product.get("review_count")
    description = product.get("description") or ""

    price_str  = f"₹{price:,.2f}" if price else "price not listed"
    rating_str = f"{rating}/5 ({review_count} reviews)" if rating else "no rating"
    desc_str   = description[:500] if description else "No description available."

    prompt = f"""You are a concise product analyst. Write a 2–3 sentence factual summary of the following product.
Focus on what the product is, its key value proposition, and what customers think of it.

Product Name: {name}
Brand: {brand}
Category: {category}
Price: {price_str}
Rating: {rating_str}
Description: {desc_str}

Write a clear, professional summary in 2–3 sentences only. Do not add bullet points or headers."""

    return _call_gemini(prompt)


# ── Review Summary ────────────────────────────────────────────────────────────

def summarize_reviews(review_texts: list[str]) -> str:
    """
    Generate a concise summary of what customers are saying across multiple reviews.

    Parameters
    ----------
    review_texts : list[str]
        Raw review text strings for a product.

    Returns
    -------
    str
        A paragraph summarizing recurring themes, praise, and complaints.
    """
    if not review_texts:
        return "No reviews available to summarize."

    # Concatenate reviews and truncate to avoid token limits
    combined = "\n\n".join(f"- {r}" for r in review_texts if r)
    if len(combined) > MAX_REVIEW_CHARS_FOR_SUMMARY:
        combined = combined[:MAX_REVIEW_CHARS_FOR_SUMMARY] + "\n...[truncated]"

    prompt = f"""You are a customer insights analyst. Read the following product reviews and write a 
concise 2–3 sentence summary capturing:
1. What customers love about the product
2. Common complaints or issues
3. The overall sentiment

Reviews:
{combined}

Write the summary in plain paragraph form. Be objective and factual."""

    return _call_gemini(prompt)
