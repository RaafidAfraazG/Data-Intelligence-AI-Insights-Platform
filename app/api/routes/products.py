"""
app/api/routes/products.py
===========================
REST endpoints for Products.

GET  /products        — list all products (paginated)
POST /products        — create a new product
GET  /products/{id}  — get a single product by ID
PUT  /products/{id}  — update a product
DELETE /products/{id} — delete a product
GET  /products/search — search products by name
"""

import logging
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead
from app.core.exceptions import NotFoundException
from app.core.response import success_response

router = APIRouter(prefix="/products")
logger = logging.getLogger(__name__)


@router.get("", summary="List all products")
def list_products(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    """Return a paginated list of all products."""
    service = ProductService(db)
    result = service.get_products(page=page, page_size=page_size)
    return success_response(data=result.model_dump(), message="Products retrieved.")


@router.post("", summary="Create a new product", status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product record."""
    service = ProductService(db)
    product = service.create_product(payload)
    return success_response(
        data=ProductRead.model_validate(product).model_dump(),
        message="Product created.",
        status_code=201,
    )


@router.get("/search", summary="Search products by name")
def search_products(
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Search products by name (keyword match)."""
    service = ProductService(db)
    products = service.search_products(query=q, page=page, page_size=page_size)
    data = [ProductRead.model_validate(p).model_dump() for p in products]
    return success_response(data=data, message=f"Found {len(data)} products matching '{q}'.")


@router.get("/{product_id}", summary="Get a product by ID")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Return a single product by its database ID."""
    service = ProductService(db)
    product = service.get_product(product_id)
    if product is None:
        raise NotFoundException("Product", product_id)
    return success_response(data=ProductRead.model_validate(product).model_dump())


@router.put("/{product_id}", summary="Update a product")
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    """Partially update a product."""
    service = ProductService(db)
    product = service.update_product(product_id, payload)
    if product is None:
        raise NotFoundException("Product", product_id)
    return success_response(
        data=ProductRead.model_validate(product).model_dump(),
        message="Product updated.",
    )


@router.delete("/{product_id}", summary="Delete a product")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Permanently delete a product and its associated reviews."""
    service = ProductService(db)
    deleted = service.delete_product(product_id)
    if not deleted:
        raise NotFoundException("Product", product_id)
    return success_response(message=f"Product {product_id} deleted.")
