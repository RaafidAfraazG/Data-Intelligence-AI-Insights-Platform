"""
app/repositories/source.py
===========================
Source-specific database queries.
"""

from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.source import Source


class SourceRepository(BaseRepository[Source]):
    model = Source

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get_by_url(self, url: str) -> Source | None:
        """Return a source record by exact URL, or None."""
        return self.db.query(Source).filter(Source.url == url).first()

    def get_by_type(self, source_type: str) -> list[Source]:
        """Return all sources of a given type (e.g., 'playwright')."""
        return (
            self.db.query(Source)
            .filter(Source.source_type == source_type)
            .all()
        )
