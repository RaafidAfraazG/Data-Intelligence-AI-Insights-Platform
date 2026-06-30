"""
app/schemas/search_history.py
==============================
Pydantic schemas for the SearchHistory model.
"""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SearchHistoryCreate(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)


class SearchHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    query: str
    timestamp: datetime
