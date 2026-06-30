"""
app/api/routes/export.py
=========================
REST endpoints for exporting data.

GET /export/csv   — export all products as a CSV download
GET /export/json  — export all products as a JSON download
"""

import logging
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.export_service import ExportService
from app.utils.helpers import build_export_filename

router = APIRouter(prefix="/export")
logger = logging.getLogger(__name__)


@router.get("/csv", summary="Export all products as CSV")
def export_csv(db: Session = Depends(get_db)):
    """
    Export all products from the database to a CSV file and return it
    as a file download.
    """
    service = ExportService(db)
    file_path = build_export_filename("products", "csv")
    service.export_products_csv(file_path)
    logger.info("Sending CSV export: %s", file_path)
    return FileResponse(
        path=file_path,
        media_type="text/csv",
        filename="products.csv",
    )


@router.get("/json", summary="Export all products as JSON")
def export_json(db: Session = Depends(get_db)):
    """
    Export all products from the database to a JSON file and return it
    as a file download.
    """
    service = ExportService(db)
    file_path = build_export_filename("products", "json")
    service.export_products_json(file_path)
    logger.info("Sending JSON export: %s", file_path)
    return FileResponse(
        path=file_path,
        media_type="application/json",
        filename="products.json",
    )
