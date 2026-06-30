"""
app/database/session.py
=======================
SQLAlchemy engine and session factory.

Usage inside a route or service:
    from app.database.session import get_db

    def my_route(db: Session = Depends(get_db)):
        ...
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.config.settings import settings

# ── Engine ────────────────────────────────────────────────────────────────────
engine = create_engine(
    settings.DATABASE_URL,
    # Use a connection pool suitable for a single-process FastAPI app.
    pool_pre_ping=True,   # Detect stale connections before using them
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG,  # Log SQL in debug mode — very helpful while developing
)

# ── Session Factory ───────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# ── Dependency ────────────────────────────────────────────────────────────────
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a database session per request
    and always closes it afterwards, even on errors.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
