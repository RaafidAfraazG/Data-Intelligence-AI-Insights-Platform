"""
app/services/product_service.py
================================
Business logic for products.

Currently contains placeholder methods — business logic will be added in a
future prompt. Services sit between API routes and repositories: they
orchestrate data flow and can call multiple repositories if needed.
"""

import logging
from sqlalchemy.orm import Session

from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead, ProductListResponse
from app.models.product import Product

logger = logging.getLogger(__name__)


class ProductService:
    """Handles all product-related business operations."""

    def __init__(self, db: Session) -> None:
        self.repo = ProductRepository(db)

    def get_products(self, page: int = 1, page_size: int = 20) -> ProductListResponse:
        """Return a paginated list of products."""
        skip = (page - 1) * page_size
        items = self.repo.get_all(skip=skip, limit=page_size)
        total = self.repo.count()
        logger.info("Fetched %d products (page=%d).", len(items), page)
        return ProductListResponse(
            total=total,
            page=page,
            page_size=page_size,
            items=[ProductRead.model_validate(p) for p in items],
        )

    def get_product(self, product_id: int) -> Product | None:
        """Return a single product by ID."""
        return self.repo.get(product_id)

    def create_product(self, data: ProductCreate) -> Product:
        """Create and persist a new product."""
        product = self.repo.create(data.model_dump())
        logger.info("Created product id=%d name=%r.", product.id, product.name)
        return product

    def update_product(self, product_id: int, data: ProductUpdate) -> Product | None:
        """Partially update a product. Returns None if not found."""
        # Exclude fields that were not sent (None means 'not provided')
        updates = {k: v for k, v in data.model_dump().items() if v is not None}
        return self.repo.update(product_id, updates)

    def delete_product(self, product_id: int) -> bool:
        """Delete a product. Returns True if deleted, False if not found."""
        return self.repo.delete(product_id)

    def search_products(self, query: str, page: int = 1, page_size: int = 20) -> list[Product]:
        """Search products by name. (AI-powered search will be added later.)"""
        skip = (page - 1) * page_size
        # TODO: Replace with semantic search in a future prompt
        return self.repo.search_by_name(query, skip=skip, limit=page_size)
