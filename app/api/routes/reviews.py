"""
app/api/routes/reviews.py
==========================
REST endpoints for Reviews.

GET  /reviews          — list all reviews (paginated)
POST /reviews          — create a new review
GET  /reviews/{id}     — get a single review
GET  /products/{id}/reviews — get all reviews for a product
"""

import logging
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.review_service import ReviewService
from app.schemas.review import ReviewCreate, ReviewRead
from app.core.exceptions import NotFoundException
from app.core.response import success_response

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/reviews", summary="List all reviews")
def list_reviews(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Return a paginated list of all reviews."""
    service = ReviewService(db)
    reviews = service.get_reviews(skip=skip, limit=limit)
    data = [ReviewRead.model_validate(r).model_dump() for r in reviews]
    return success_response(data=data, message=f"{len(data)} reviews retrieved.")


@router.post("/reviews", summary="Create a review", status_code=201)
def create_review(payload: ReviewCreate, db: Session = Depends(get_db)):
    """Create a new review for a product."""
    service = ReviewService(db)
    review = service.create_review(payload)
    return success_response(
        data=ReviewRead.model_validate(review).model_dump(),
        message="Review created.",
        status_code=201,
    )


@router.get("/reviews/{review_id}", summary="Get a review by ID")
def get_review(review_id: int, db: Session = Depends(get_db)):
    """Return a single review by ID."""
    service = ReviewService(db)
    review = service.get_review(review_id)
    if review is None:
        raise NotFoundException("Review", review_id)
    return success_response(data=ReviewRead.model_validate(review).model_dump())


@router.get("/products/{product_id}/reviews", summary="Get reviews for a product")
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    """Return all reviews associated with a specific product."""
    service = ReviewService(db)
    reviews = service.get_reviews_for_product(product_id)
    data = [ReviewRead.model_validate(r).model_dump() for r in reviews]
    return success_response(
        data=data,
        message=f"{len(data)} reviews found for product {product_id}.",
    )
