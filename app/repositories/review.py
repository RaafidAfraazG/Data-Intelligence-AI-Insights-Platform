"""
app/repositories/review.py
===========================
Review-specific database queries.
"""

from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.review import Review


class ReviewRepository(BaseRepository[Review]):
    model = Review

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get_by_product(self, product_id: int, skip: int = 0, limit: int = 20) -> list[Review]:
        """Return all reviews for a specific product."""
        return (
            self.db.query(Review)
            .filter(Review.product_id == product_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_by_product(self, product_id: int) -> int:
        """Return the number of reviews for a specific product."""
        return (
            self.db.query(Review)
            .filter(Review.product_id == product_id)
            .count()
        )
