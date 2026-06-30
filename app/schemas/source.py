"""
app/schemas/source.py
=====================
Pydantic schemas for the Source model.
"""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SourceCreate(BaseModel):
    url: str = Field(..., max_length=2000, description="URL that was scraped")
    source_type: str | None = Field(None, max_length=50)


class SourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    source_type: str | None
    collected_at: datetime
