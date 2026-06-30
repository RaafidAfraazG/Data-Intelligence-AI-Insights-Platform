"""
app/utils/helpers.py
======================
Small general-purpose helper functions used across the application.
"""

import os
from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return the current UTC time as a timezone-aware datetime object."""
    return datetime.now(timezone.utc)


def build_export_filename(prefix: str, extension: str) -> str:
    """
    Generate a timestamped filename for an export file.

    Example
    -------
    build_export_filename("products", "csv") → "exports/products_20240615_142300.csv"
    """
    from app.config.settings import settings

    timestamp = utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.{extension}"
    return os.path.join(settings.EXPORTS_DIR, filename)


def paginate(total: int, page: int, page_size: int) -> dict:
    """
    Build a pagination metadata dict.

    Returns
    -------
    dict
        Keys: total, page, page_size, total_pages, has_next, has_prev
    """
    total_pages = max(1, -(-total // page_size))  # ceiling division
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
