"""
app/repositories/product.py
============================
Product-specific database queries.
Extends BaseRepository with search and filter helpers.
"""

from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.product import Product


class ProductRepository(BaseRepository[Product]):
    model = Product

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def search_by_name(self, query: str, skip: int = 0, limit: int = 20) -> list[Product]:
        """Return products whose name contains the query string (case-insensitive)."""
        return (
            self.db.query(Product)
            .filter(Product.name.ilike(f"%{query}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def filter_by_category(self, category: str, skip: int = 0, limit: int = 20) -> list[Product]:
        """Return products belonging to a specific category."""
        return (
            self.db.query(Product)
            .filter(Product.category.ilike(f"%{category}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def filter_by_price_range(
        self, min_price: float, max_price: float, skip: int = 0, limit: int = 20
    ) -> list[Product]:
        """Return products whose price falls within [min_price, max_price]."""
        return (
            self.db.query(Product)
            .filter(Product.price >= min_price, Product.price <= max_price)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_source(self, source: str) -> list[Product]:
        """Return all products scraped from a given source URL."""
        return (
            self.db.query(Product)
            .filter(Product.source.ilike(f"%{source}%"))
            .all()
        )
