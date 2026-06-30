"""
app/preprocessing/cleaner.py
=============================
Standalone data-cleaning utility functions.

Each function is pure (no side effects) and can be unit-tested independently.
They operate on pandas DataFrames or individual string/float values.

No NLP or AI is used here — only deterministic preprocessing.
"""

import re
import logging
from typing import Any

import pandas as pd
import numpy as np

from app.config.constants import KNOWN_CATEGORIES, CURRENCY_SYMBOLS

logger = logging.getLogger(__name__)


# ── DataFrame-level functions ─────────────────────────────────────────────────

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove exact duplicate rows from a DataFrame.
    If a 'name' column exists, also deduplicate by name (keeping first).
    """
    before = len(df)
    df = df.drop_duplicates()

    if "name" in df.columns:
        df = df.drop_duplicates(subset=["name"], keep="first")

    after = len(df)
    logger.debug("remove_duplicates: %d → %d rows.", before, after)
    return df.reset_index(drop=True)


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill or drop missing values using sensible defaults:
    - Numeric columns: fill NaN with the column median
    - String columns:  fill NaN with an empty string
    - Drop rows where 'name' is missing (a product must have a name)
    """
    if "name" in df.columns:
        df = df.dropna(subset=["name"])

    for col in df.select_dtypes(include=[np.number]).columns:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)

    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].fillna("")

    return df


# ── Scalar / per-value functions ──────────────────────────────────────────────

def normalize_price(value: Any) -> float | None:
    """
    Convert a price string or number to a clean float.

    Examples
    --------
    normalize_price("$12.99")  → 12.99
    normalize_price("€ 1,299") → 1299.0
    normalize_price(None)       → None
    """
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()

    # Remove known currency symbols
    for symbol in CURRENCY_SYMBOLS:
        text = text.replace(symbol, "")

    # Remove thousands separators and extra spaces
    text = text.replace(",", "").strip()

    try:
        return float(text)
    except ValueError:
        logger.debug("normalize_price: could not parse %r", value)
        return None


def clean_html(text: Any) -> str:
    """
    Strip HTML tags from a string.

    Example
    -------
    clean_html("<p>Hello <b>world</b></p>") → "Hello world"
    """
    if not text or not isinstance(text, str):
        return ""
    # Remove HTML tags
    clean = re.sub(r"<[^>]+>", " ", text)
    # Collapse whitespace
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def normalize_text(text: Any) -> str:
    """
    Lowercase, strip, and collapse extra whitespace in a string.

    Example
    -------
    normalize_text("  Apple  iPhone  15  ") → "apple iphone 15"
    """
    if not text or not isinstance(text, str):
        return ""
    return re.sub(r"\s+", " ", text.strip().lower())


def remove_special_characters(text: Any, keep_spaces: bool = True) -> str:
    """
    Remove non-alphanumeric characters from a string.

    Parameters
    ----------
    text : Any
        Input string.
    keep_spaces : bool
        If True, whitespace characters are preserved.

    Example
    -------
    remove_special_characters("Hello, World! #2") → "Hello World 2"
    """
    if not text or not isinstance(text, str):
        return ""
    pattern = r"[^a-zA-Z0-9\s]" if keep_spaces else r"[^a-zA-Z0-9]"
    return re.sub(pattern, "", text).strip()


def standardize_categories(category: Any) -> str:
    """
    Map a raw category string to one of the KNOWN_CATEGORIES.
    Falls back to 'other' if no match is found.

    Example
    -------
    standardize_categories("ELECTRONICS") → "electronics"
    standardize_categories("Gadgets")     → "electronics"
    """
    if not category or not isinstance(category, str):
        return "other"

    cat_lower = category.strip().lower()

    # Direct match
    if cat_lower in KNOWN_CATEGORIES:
        return cat_lower

    # Partial match — first KNOWN_CATEGORY that appears as a substring
    for known in KNOWN_CATEGORIES:
        if known in cat_lower or cat_lower in known:
            return known

    return "other"
