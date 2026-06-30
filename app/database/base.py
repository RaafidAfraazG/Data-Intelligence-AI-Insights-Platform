"""
app/database/base.py
====================
Declarative base that all SQLAlchemy models must inherit from.
Importing this module also imports all models so that
Base.metadata.create_all() picks them up.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""
    pass


# ── Import models here so they are registered with Base.metadata ──────────────
# These imports must come AFTER the Base class definition.
from app.models.product import Product          # noqa: E402, F401
from app.models.review import Review            # noqa: E402, F401
from app.models.source import Source            # noqa: E402, F401
from app.models.metadata import ProductMetadata # noqa: E402, F401
from app.models.search_history import SearchHistory  # noqa: E402, F401
