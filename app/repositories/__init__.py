"""
app/repositories/__init__.py
"""
from app.repositories.product import ProductRepository
from app.repositories.review import ReviewRepository
from app.repositories.source import SourceRepository
from app.repositories.search_history import SearchHistoryRepository

__all__ = [
    "ProductRepository",
    "ReviewRepository",
    "SourceRepository",
    "SearchHistoryRepository",
]
