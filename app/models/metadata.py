"""
app/models/metadata.py
=======================
SQLAlchemy model for flexible key-value metadata attached to a product.
Useful for storing extra fields that don't fit the fixed Product schema.
"""

from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.product import Product


class ProductMetadata(Base):
    __tablename__ = "product_metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True
    )
    key: Mapped[str] = mapped_column(String(200), nullable=False)
    value: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Relationships ─────────────────────────────────────────────────────────
    product: Mapped["Product"] = relationship("Product", back_populates="metadata_entries")

    def __repr__(self) -> str:
        return f"<ProductMetadata product_id={self.product_id} key={self.key!r}>"
