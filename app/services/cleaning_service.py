"""
app/services/cleaning_service.py
==================================
Orchestrates data cleaning/preprocessing.
Delegates to the cleaner utility functions in app/preprocessing/cleaner.py.
"""

import logging
from typing import Any

from app.preprocessing import cleaner

logger = logging.getLogger(__name__)


class CleaningService:
    """Applies data-cleaning steps to raw scraped data."""

    def clean_products(self, raw_products: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Run a full cleaning pipeline on a list of raw product dictionaries.
        Steps are applied sequentially.
        """
        logger.info("Cleaning %d raw product records.", len(raw_products))

        import pandas as pd
        df = pd.DataFrame(raw_products)

        df = cleaner.remove_duplicates(df)
        df["price"] = df["price"].apply(cleaner.normalize_price) if "price" in df.columns else df.get("price")
        df = cleaner.handle_missing_values(df)

        if "name" in df.columns:
            df["name"] = df["name"].apply(cleaner.normalize_text)
        if "description" in df.columns:
            df["description"] = df["description"].apply(cleaner.clean_html)
        if "category" in df.columns:
            df["category"] = df["category"].apply(cleaner.standardize_categories)

        cleaned = df.to_dict(orient="records")
        logger.info("Cleaning complete. %d records after dedup.", len(cleaned))
        return cleaned
