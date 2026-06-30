"""
app/nlp/topics.py
==================
Topic extraction using Latent Dirichlet Allocation (LDA).

LDA discovers hidden "topics" — groups of words that tend to appear together.
For example, reviews of a laptop might produce topics like:
  ["battery", "life", "hour", "charge", "fast"]
  ["screen", "display", "resolution", "bright", "color"]

Uses scikit-learn's LDA implementation — CPU only, no GPU needed.
"""

import logging
from typing import Any

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

from app.nlp.preprocessor import full_pipeline, tokens_to_string
from app.config.constants import DEFAULT_TOP_TOPICS, DEFAULT_TOPIC_WORDS

logger = logging.getLogger(__name__)


def extract_topics(
    texts: list[str],
    n_topics: int = DEFAULT_TOP_TOPICS,
    n_words: int = DEFAULT_TOPIC_WORDS,
    preprocess: bool = True,
) -> list[dict[str, Any]]:
    """
    Extract the top discussion topics from a collection of texts using LDA.

    Parameters
    ----------
    texts : list[str]
        List of review/description texts.
    n_topics : int
        Number of topics to discover.
    n_words : int
        Number of representative words per topic.
    preprocess : bool
        Apply NLP pipeline before vectorizing.

    Returns
    -------
    list[dict]
        Each dict: { "topic_id": int, "words": list[str] }
    """
    if not texts or len(texts) < 2:
        logger.warning("extract_topics requires at least 2 texts. Got %d.", len(texts))
        return []

    # Preprocess
    if preprocess:
        processed = [tokens_to_string(full_pipeline(t)) for t in texts]
        processed = [p for p in processed if p.strip()]
    else:
        processed = [t for t in texts if t.strip()]

    if len(processed) < 2:
        return []

    try:
        # Count-vectorize (LDA works with raw counts, not TF-IDF)
        vectorizer = CountVectorizer(
            max_features=500,
            min_df=1,
            max_df=0.95,
        )
        doc_term_matrix = vectorizer.fit_transform(processed)

        # Fit LDA
        lda = LatentDirichletAllocation(
            n_components=min(n_topics, len(processed)),  # can't have more topics than docs
            random_state=42,
            max_iter=10,
        )
        lda.fit(doc_term_matrix)

        feature_names = vectorizer.get_feature_names_out()

        topics = []
        for topic_idx, topic_vector in enumerate(lda.components_):
            top_word_indices = topic_vector.argsort()[::-1][:n_words]
            words = [feature_names[i] for i in top_word_indices]
            topics.append({"topic_id": topic_idx + 1, "words": words})

        return topics

    except Exception as exc:
        logger.error("LDA topic extraction failed: %s", exc)
        return []
