"""
app/services/export_service.py
================================
Handles exporting data to CSV and JSON files.
Delegates to utility functions in app/utils/export.py.
"""

import logging
from sqlalchemy.orm import Session

from app.repositories.product import ProductRepository
from app.utils.export import export_to_csv, export_to_json

logger = logging.getLogger(__name__)


class ExportService:
    """Fetches data and writes it to the requested export format."""

    def __init__(self, db: Session) -> None:
        self.product_repo = ProductRepository(db)

    def export_products_csv(self, file_path: str) -> str:
        """Fetch all products and export to a CSV file. Returns the file path."""
        products = self.product_repo.get_all(skip=0, limit=10_000)
        data = [
            {
                "id": p.id,
                "name": p.name,
                "brand": p.brand,
                "category": p.category,
                "price": p.price,
                "rating": p.rating,
                "review_count": p.review_count,
                "source": p.source,
                "created_at": str(p.created_at),
            }
            for p in products
        ]
        export_to_csv(data, file_path)
        logger.info("Exported %d products to CSV: %s", len(data), file_path)
        return file_path

    def export_products_json(self, file_path: str) -> str:
        """Fetch all products and export to a JSON file. Returns the file path."""
        products = self.product_repo.get_all(skip=0, limit=10_000)
        data = [
            {
                "id": p.id,
                "name": p.name,
                "brand": p.brand,
                "category": p.category,
                "price": p.price,
                "rating": p.rating,
                "review_count": p.review_count,
                "source": p.source,
                "created_at": str(p.created_at),
            }
            for p in products
        ]
        export_to_json(data, file_path)
        logger.info("Exported %d products to JSON: %s", len(data), file_path)
        return file_path
