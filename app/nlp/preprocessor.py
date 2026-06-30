"""
app/nlp/preprocessor.py
========================
Core NLP preprocessing utilities.

Uses NLTK for tokenization, stopword removal, and lemmatization.
Each function is small and independently testable.

First-time setup (downloads happen once, cached locally):
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
"""

import logging
import re

import nltk

logger = logging.getLogger(__name__)

# ── Download required NLTK data (silent if already present) ──────────────────
for _resource in ["punkt", "punkt_tab", "stopwords", "wordnet", "averaged_perceptron_tagger"]:
    try:
        nltk.download(_resource, quiet=True)
    except Exception:
        pass

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

_STOP_WORDS = set(stopwords.words("english"))
_LEMMATIZER = WordNetLemmatizer()


# ── Individual steps ──────────────────────────────────────────────────────────

def clean_raw(text: str) -> str:
    """Remove HTML tags, URLs, and excessive whitespace from raw text."""
    text = re.sub(r"<[^>]+>", " ", text)              # strip HTML tags
    text = re.sub(r"http\S+|www\.\S+", " ", text)      # strip URLs
    text = re.sub(r"\s+", " ", text).strip()
    return text


def lowercase(text: str) -> str:
    """Convert text to lowercase."""
    return text.lower()


def tokenize(text: str) -> list[str]:
    """
    Split text into word tokens using NLTK's word tokenizer.
    Also strips punctuation tokens.
    """
    tokens = word_tokenize(text)
    # Keep only alphabetic tokens (removes numbers and punctuation)
    return [t for t in tokens if t.isalpha()]


def remove_stopwords(tokens: list[str]) -> list[str]:
    """Remove common English stopwords from a token list."""
    return [t for t in tokens if t not in _STOP_WORDS]


def lemmatize(tokens: list[str]) -> list[str]:
    """Reduce each token to its base/lemma form (e.g. 'running' → 'run')."""
    return [_LEMMATIZER.lemmatize(t) for t in tokens]


# ── Full pipeline ─────────────────────────────────────────────────────────────

def full_pipeline(text: str) -> list[str]:
    """
    Run the complete NLP preprocessing pipeline on a text string.

    Steps: clean → lowercase → tokenize → remove stopwords → lemmatize

    Parameters
    ----------
    text : str
        Raw input text (may contain HTML, URLs, etc.)

    Returns
    -------
    list[str]
        Cleaned, lemmatized tokens ready for NLP tasks.
    """
    if not text or not isinstance(text, str):
        return []

    text = clean_raw(text)
    text = lowercase(text)
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize(tokens)
    return tokens


def tokens_to_string(tokens: list[str]) -> str:
    """Join a token list back into a space-separated string."""
    return " ".join(tokens)
