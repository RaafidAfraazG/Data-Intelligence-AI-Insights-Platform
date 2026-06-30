"""
app/repositories/base.py
========================
Generic base repository with reusable CRUD helpers.

Subclasses only need to specify the model class:

    class ProductRepository(BaseRepository[Product]):
        model = Product
"""

from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session
from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Provides get, get_all, create, update, and delete for any SQLAlchemy model.
    Subclasses can extend this with model-specific query methods.
    """

    model: Type[ModelType]

    def __init__(self, db: Session) -> None:
        self.db = db

    # ── Read ──────────────────────────────────────────────────────────────────

    def get(self, record_id: int) -> ModelType | None:
        """Fetch a single record by primary key. Returns None if not found."""
        return self.db.get(self.model, record_id)

    def get_all(self, skip: int = 0, limit: int = 20) -> list[ModelType]:
        """Return a paginated list of records, oldest first."""
        return (
            self.db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(self) -> int:
        """Return total number of records in the table."""
        return self.db.query(self.model).count()

    # ── Create ────────────────────────────────────────────────────────────────

    def create(self, data: dict) -> ModelType:
        """
        Create a new record from a plain dictionary.
        The dictionary keys must match the model's column names.
        """
        instance = self.model(**data)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, record_id: int, data: dict) -> ModelType | None:
        """
        Update an existing record with the provided fields.
        Only keys present in *data* are updated (partial update).
        Returns None if the record does not exist.
        """
        instance = self.get(record_id)
        if instance is None:
            return None

        for field, value in data.items():
            if hasattr(instance, field) and value is not None:
                setattr(instance, field, value)

        self.db.commit()
        self.db.refresh(instance)
        return instance

    # ── Delete ────────────────────────────────────────────────────────────────

    def delete(self, record_id: int) -> bool:
        """
        Delete a record by primary key.
        Returns True if deleted, False if not found.
        """
        instance = self.get(record_id)
        if instance is None:
            return False

        self.db.delete(instance)
        self.db.commit()
        return True
