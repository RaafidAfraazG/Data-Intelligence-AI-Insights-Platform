"""
app/schemas/review.py
=====================
Pydantic schemas for the Review model.
"""

from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict


class ReviewCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    review_text: str | None = None
    rating: float | None = Field(None, ge=0, le=5)
    reviewer: str | None = Field(None, max_length=300)
    review_date: date | None = None


class ReviewRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    review_text: str | None
    rating: float | None
    reviewer: str | None
    review_date: date | None
    created_at: datetime
