"""
app/schemas/product.py
======================
Pydantic schemas for the Product model.

- ProductCreate  → used when creating a new product (POST body)
- ProductUpdate  → used when updating an existing product (PUT/PATCH body)
- ProductRead    → used when returning a product to the client
- ProductListResponse → paginated list wrapper
"""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# ── Create ────────────────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=500, description="Product name")
    brand: str | None = Field(None, max_length=200)
    category: str | None = Field(None, max_length=200)
    price: float | None = Field(None, ge=0)
    rating: float | None = Field(None, ge=0, le=5)
    review_count: int | None = Field(None, ge=0)
    description: str | None = None
    source: str | None = Field(None, max_length=500)


# ── Update ────────────────────────────────────────────────────────────────────

class ProductUpdate(BaseModel):
    """All fields are optional for a partial update."""
    name: str | None = Field(None, min_length=1, max_length=500)
    brand: str | None = None
    category: str | None = None
    price: float | None = Field(None, ge=0)
    rating: float | None = Field(None, ge=0, le=5)
    review_count: int | None = Field(None, ge=0)
    description: str | None = None
    source: str | None = None


# ── Read ──────────────────────────────────────────────────────────────────────

class ProductRead(BaseModel):
    """Returned to the client. Includes database-generated fields."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    brand: str | None
    category: str | None
    price: float | None
    rating: float | None
    review_count: int | None
    description: str | None
    source: str | None
    created_at: datetime


# ── List Response ─────────────────────────────────────────────────────────────

class ProductListResponse(BaseModel):
    """Wraps a list of products with pagination metadata."""
    total: int
    page: int
    page_size: int
    items: list[ProductRead]
