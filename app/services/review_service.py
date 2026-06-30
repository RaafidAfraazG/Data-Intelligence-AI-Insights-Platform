"""
app/services/review_service.py
================================
Business logic for reviews.
Placeholder — full implementation in a future prompt.
"""

import logging
from sqlalchemy.orm import Session

from app.repositories.review import ReviewRepository
from app.schemas.review import ReviewCreate
from app.models.review import Review

logger = logging.getLogger(__name__)


class ReviewService:
    """Handles all review-related business operations."""

    def __init__(self, db: Session) -> None:
        self.repo = ReviewRepository(db)

    def get_reviews(self, skip: int = 0, limit: int = 20) -> list[Review]:
        """Return a paginated list of reviews."""
        return self.repo.get_all(skip=skip, limit=limit)

    def get_reviews_for_product(self, product_id: int) -> list[Review]:
        """Return all reviews associated with a product."""
        return self.repo.get_by_product(product_id)

    def create_review(self, data: ReviewCreate) -> Review:
        """Create a new review record."""
        review = self.repo.create(data.model_dump())
        logger.info("Created review id=%d for product_id=%d.", review.id, review.product_id)
        return review

    def get_review(self, review_id: int) -> Review | None:
        """Return a single review by ID."""
        return self.repo.get(review_id)

    # TODO: add sentiment analysis once NLP module is implemented
