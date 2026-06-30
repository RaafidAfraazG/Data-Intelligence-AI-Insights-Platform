"""
app/models/__init__.py
Expose models for convenient imports.
"""
from app.models.product import Product
from app.models.review import Review
from app.models.source import Source
from app.models.metadata import ProductMetadata
from app.models.search_history import SearchHistory

__all__ = ["Product", "Review", "Source", "ProductMetadata", "SearchHistory"]
