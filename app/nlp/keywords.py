"""
app/nlp/keywords.py
====================
Keyword extraction using TF-IDF (Term Frequency–Inverse Document Frequency).

TF-IDF ranks words that are frequent in a document but rare across documents —
exactly what we want to find distinctive product/review keywords.

Uses scikit-learn's TfidfVectorizer which is fast and needs no GPU.
"""

import logging
from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from app.nlp.preprocessor import full_pipeline, tokens_to_string
from app.config.constants import DEFAULT_TOP_KEYWORDS

logger = logging.getLogger(__name__)


def extract_keywords(
    texts: list[str],
    top_n: int = DEFAULT_TOP_KEYWORDS,
    preprocess: bool = True,
) -> list[dict[str, Any]]:
    """
    Extract the top-N keywords from a collection of text documents using TF-IDF.

    Parameters
    ----------
    texts : list[str]
        A list of text documents (e.g. all reviews for a product).
    top_n : int
        Number of top keywords to return.
    preprocess : bool
        If True, run the full NLP pipeline (tokenize, stopwords, lemmatize)
        on each text before vectorizing.

    Returns
    -------
    list[dict]
        Each dict has keys: keyword (str), score (float).
        Sorted by score descending.
    """
    if not texts:
        return []

    # Preprocess each document
    if preprocess:
        processed = [tokens_to_string(full_pipeline(t)) for t in texts]
        # Filter out empty strings that result from very short / all-stopword texts
        processed = [p for p in processed if p.strip()]
    else:
        processed = [t for t in texts if t.strip()]

    if not processed:
        return []

    try:
        vectorizer = TfidfVectorizer(
            max_features=200,          # Consider only top 200 words by frequency
            ngram_range=(1, 2),        # Unigrams and bigrams (e.g. "battery life")
            min_df=1,                  # Word must appear in at least 1 doc
            sublinear_tf=True,         # Apply log normalisation to term frequencies
        )
        tfidf_matrix = vectorizer.fit_transform(processed)
    except ValueError as exc:
        logger.warning("TF-IDF vectorization failed: %s", exc)
        return []

    # Sum TF-IDF scores across all documents for each term
    scores = np.asarray(tfidf_matrix.sum(axis=0)).flatten()
    feature_names = vectorizer.get_feature_names_out()

    # Sort by score descending and take top_n
    top_indices = scores.argsort()[::-1][:top_n]

    return [
        {"keyword": feature_names[i], "score": round(float(scores[i]), 4)}
        for i in top_indices
    ]


def extract_single(text: str, top_n: int = 5) -> list[str]:
    """
    Extract the top-N keywords from a single text string.

    Returns a flat list of keyword strings (no scores).
    Useful for quick per-product tagging.
    """
    results = extract_keywords([text], top_n=top_n)
    return [r["keyword"] for r in results]
