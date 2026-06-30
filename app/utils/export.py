"""
app/utils/export.py
====================
Utility functions for exporting data to CSV and JSON files.
These are thin wrappers around pandas to keep service code clean.
"""

import json
import logging
import os
from typing import Any

import pandas as pd

from app.config.settings import settings

logger = logging.getLogger(__name__)


def _ensure_export_dir() -> None:
    """Create the exports directory if it doesn't exist."""
    os.makedirs(settings.EXPORTS_DIR, exist_ok=True)


def export_to_csv(data: list[dict[str, Any]], file_path: str) -> str:
    """
    Write a list of dicts to a CSV file.

    Parameters
    ----------
    data : list[dict]
        The records to export.
    file_path : str
        Destination file path.

    Returns
    -------
    str
        The resolved file path.
    """
    _ensure_export_dir()

    if not data:
        logger.warning("export_to_csv called with empty data. Writing empty file.")

    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False, encoding="utf-8")
    logger.info("Exported %d records to CSV: %s", len(df), file_path)
    return file_path


def export_to_json(data: list[dict[str, Any]], file_path: str) -> str:
    """
    Write a list of dicts to a JSON file (pretty-printed).

    Parameters
    ----------
    data : list[dict]
        The records to export.
    file_path : str
        Destination file path.

    Returns
    -------
    str
        The resolved file path.
    """
    _ensure_export_dir()

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    logger.info("Exported %d records to JSON: %s", len(data), file_path)
    return file_path
