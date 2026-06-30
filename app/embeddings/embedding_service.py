"""
app/embeddings/embedding_service.py
=====================================
Generates dense vector embeddings using Sentence Transformers.

Model: all-MiniLM-L6-v2
  - 384-dimensional embeddings
  - Fast and lightweight (good for a student portfolio)
  - Excellent for semantic similarity tasks

The model is loaded ONCE at module import time (singleton pattern).
Subsequent calls reuse the loaded model — no cold-start overhead.
"""

import logging
from typing import Any

from app.config.settings import settings

logger = logging.getLogger(__name__)

# ── Load model once ───────────────────────────────────────────────────────────
_model = None


def _get_model():
    """Lazy-load the SentenceTransformer model (downloaded on first use)."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading embedding model: %s", settings.EMBEDDING_MODEL)
            _model = SentenceTransformer(settings.EMBEDDING_MODEL)
            logger.info("Embedding model loaded successfully.")
        except ImportError:
            logger.error(
                "sentence-transformers is not installed. "
                "Run: pip install sentence-transformers"
            )
        except Exception as exc:
            logger.error("Failed to load embedding model: %s", exc)
    return _model


# ── Public API ────────────────────────────────────────────────────────────────

def get_embedding(text: str) -> list[float]:
    """
    Generate a 384-dimensional embedding vector for a single text string.

    Parameters
    ----------
    text : str
        The input text (product name, review, description, search query, etc.)

    Returns
    -------
    list[float]
        A 384-dimensional embedding vector, or an empty list on failure.
    """
    model = _get_model()
    if model is None or not text:
        return []

    try:
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    except Exception as exc:
        logger.error("Embedding generation failed: %s", exc)
        return []


def get_batch_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of texts in a single batched call.
    Much faster than calling get_embedding() in a loop for large datasets.

    Parameters
    ----------
    texts : list[str]
        List of input texts.

    Returns
    -------
    list[list[float]]
        List of embedding vectors in the same order as the input texts.
        Items that fail will be represented as empty lists.
    """
    model = _get_model()
    if model is None or not texts:
        return [[] for _ in texts]

    try:
        embeddings = model.encode(texts, convert_to_numpy=True, batch_size=32, show_progress_bar=False)
        return [e.tolist() for e in embeddings]
    except Exception as exc:
        logger.error("Batch embedding generation failed: %s", exc)
        return [[] for _ in texts]


def build_product_text(product: dict[str, Any]) -> str:
    """
    Combine product fields into a single string suitable for embedding.
    Concatenating name + brand + category + description gives richer semantics
    than embedding just the name.
    """
    parts = [
        product.get("name") or "",
        product.get("brand") or "",
        product.get("category") or "",
        product.get("description") or "",
    ]
    return " ".join(p for p in parts if p).strip()
