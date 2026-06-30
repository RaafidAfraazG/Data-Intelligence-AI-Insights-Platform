"""
app/nlp/sentiment.py
=====================
Sentiment analysis using VADER (Valence Aware Dictionary and sEntiment Reasoner).

VADER is ideal for short product reviews:
- Rule-based (no training required)
- Works offline
- Handles slang, punctuation emphasis, and emoticons

Compound score ranges:
  >= 0.05  → positive
  <= -0.05 → negative
  else     → neutral
"""

import logging
from typing import Any

import nltk
from app.config.constants import (
    SENTIMENT_POSITIVE,
    SENTIMENT_NEUTRAL,
    SENTIMENT_NEGATIVE,
    VADER_POSITIVE_THRESHOLD,
    VADER_NEGATIVE_THRESHOLD,
)

logger = logging.getLogger(__name__)

# ── Download VADER lexicon (once) ─────────────────────────────────────────────
try:
    nltk.download("vader_lexicon", quiet=True)
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    _ANALYZER = SentimentIntensityAnalyzer()
except Exception as exc:
    logger.error("VADER not available: %s", exc)
    _ANALYZER = None


# ── Single-text analysis ──────────────────────────────────────────────────────

def analyze_sentiment(text: str) -> dict[str, Any]:
    """
    Analyze the sentiment of a single text string.

    Returns
    -------
    dict with keys:
        label    (str)   — "positive" | "neutral" | "negative"
        score    (float) — compound score in [-1, 1]
        positive (float) — proportion of positive tokens
        neutral  (float) — proportion of neutral tokens
        negative (float) — proportion of negative tokens
    """
    if not text or not isinstance(text, str) or _ANALYZER is None:
        return _neutral_result()

    scores = _ANALYZER.polarity_scores(text)
    compound = scores["compound"]

    if compound >= VADER_POSITIVE_THRESHOLD:
        label = SENTIMENT_POSITIVE
    elif compound <= VADER_NEGATIVE_THRESHOLD:
        label = SENTIMENT_NEGATIVE
    else:
        label = SENTIMENT_NEUTRAL

    return {
        "label": label,
        "score": round(compound, 4),
        "positive": round(scores["pos"], 4),
        "neutral": round(scores["neu"], 4),
        "negative": round(scores["neg"], 4),
    }


# ── Batch analysis ────────────────────────────────────────────────────────────

def analyze_batch(texts: list[str]) -> list[dict[str, Any]]:
    """
    Analyze sentiment for a list of texts.
    Returns a list of result dicts in the same order as inputs.
    """
    return [analyze_sentiment(t) for t in texts]


# ── Product-level aggregation ─────────────────────────────────────────────────

def product_sentiment_summary(review_texts: list[str]) -> dict[str, Any]:
    """
    Compute an aggregated sentiment summary for a set of review texts.

    Returns
    -------
    dict with keys:
        average_score   (float)  — mean compound score across all reviews
        overall_label   (str)    — dominant sentiment label
        distribution    (dict)   — count of positive / neutral / negative reviews
        total_reviews   (int)
    """
    if not review_texts:
        return {
            "average_score": 0.0,
            "overall_label": SENTIMENT_NEUTRAL,
            "distribution": {SENTIMENT_POSITIVE: 0, SENTIMENT_NEUTRAL: 0, SENTIMENT_NEGATIVE: 0},
            "total_reviews": 0,
        }

    results = analyze_batch(review_texts)

    scores = [r["score"] for r in results]
    average_score = round(sum(scores) / len(scores), 4)

    distribution = {SENTIMENT_POSITIVE: 0, SENTIMENT_NEUTRAL: 0, SENTIMENT_NEGATIVE: 0}
    for r in results:
        distribution[r["label"]] += 1

    # Overall label = whichever bucket has the most reviews
    overall_label = max(distribution, key=distribution.__getitem__)

    return {
        "average_score": average_score,
        "overall_label": overall_label,
        "distribution": distribution,
        "total_reviews": len(review_texts),
    }


# ── Helpers ───────────────────────────────────────────────────────────────────

def _neutral_result() -> dict[str, Any]:
    return {
        "label": SENTIMENT_NEUTRAL,
        "score": 0.0,
        "positive": 0.0,
        "neutral": 1.0,
        "negative": 0.0,
    }
