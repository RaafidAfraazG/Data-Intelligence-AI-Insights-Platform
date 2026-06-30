"""
app/api/routes/cleaning.py
===========================
REST endpoints for data cleaning.

POST /clean — clean a list of raw product records
"""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Any

from app.database.session import get_db
from app.services.cleaning_service import CleaningService
from app.core.response import success_response

router = APIRouter(prefix="/clean")
logger = logging.getLogger(__name__)


class CleanRequest(BaseModel):
    """Request body for the cleaning endpoint."""
    products: list[dict[str, Any]]


@router.post("", summary="Clean raw product data")
def clean_products(payload: CleanRequest, db: Session = Depends(get_db)):
    """
    Accept a list of raw product dictionaries and run the full
    cleaning pipeline on them.

    Returns the cleaned records. Does NOT persist to the database —
    the caller decides what to do with the cleaned data.
    """
    service = CleaningService()
    cleaned = service.clean_products(payload.products)
    return success_response(
        data={"cleaned_count": len(cleaned), "products": cleaned},
        message=f"Cleaned {len(cleaned)} product records.",
    )
