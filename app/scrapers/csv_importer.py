"""
app/scrapers/csv_importer.py
==============================
Imports product data from a CSV file using Pandas.

Supported columns (optional — missing columns default to None):
  name, brand, category, price, rating, review_count, description, source

Usage:
    importer = CSVImporter()
    rows = importer.load("uploads/my_products.csv")
"""

import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

# Columns we expect (subset will be selected if present)
EXPECTED_COLUMNS = [
    "name", "brand", "category", "price",
    "rating", "review_count", "description", "source",
]


class CSVImporter:
    """Reads a CSV file and returns a list of product dicts."""

    def load(self, file_path: str) -> list[dict[str, Any]]:
        """
        Read a CSV from *file_path* and return rows as a list of dicts.
        Columns not in EXPECTED_COLUMNS are kept as extra metadata.

        Parameters
        ----------
        file_path : str
            Absolute or relative path to the CSV file.

        Returns
        -------
        list[dict]
            Each dict represents one product row.
        """
        logger.info("Loading CSV from: %s", file_path)

        try:
            df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip")
        except FileNotFoundError:
            logger.error("CSV file not found: %s", file_path)
            return []
        except Exception as exc:
            logger.error("Failed to read CSV %s: %s", file_path, exc)
            return []

        logger.info("Loaded %d rows from CSV.", len(df))

        # Normalise column names: strip whitespace and lowercase
        df.columns = df.columns.str.strip().str.lower()

        # Replace NaN with None for JSON-compatibility
        df = df.where(pd.notnull(df), None)

        return df.to_dict(orient="records")
