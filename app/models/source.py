"""
app/models/source.py
====================
SQLAlchemy model for a data source (a URL that was scraped).
"""

from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(2000), nullable=False, unique=True)
    source_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # e.g. "playwright", "beautifulsoup", "csv"
    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Source id={self.id} url={self.url!r}>"
