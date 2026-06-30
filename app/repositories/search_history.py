"""
app/repositories/search_history.py
====================================
SearchHistory-specific database queries.
"""

from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.search_history import SearchHistory


class SearchHistoryRepository(BaseRepository[SearchHistory]):
    model = SearchHistory

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def get_recent(self, limit: int = 10) -> list[SearchHistory]:
        """Return the most recent search queries."""
        return (
            self.db.query(SearchHistory)
            .order_by(SearchHistory.timestamp.desc())
            .limit(limit)
            .all()
        )
