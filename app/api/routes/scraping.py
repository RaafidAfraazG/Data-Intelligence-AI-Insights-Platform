"""
app/api/routes/scraping.py
===========================
REST endpoints for triggering scraping jobs.

POST /scrape/url  — scrape a single URL
POST /scrape/csv  — upload and import a CSV file
POST /scrape/urls — collect URLs from a base page
"""

import logging
import os
import shutil

from fastapi import APIRouter, Depends, UploadFile, File, Body
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.scraping_service import ScrapingService
from app.core.response import success_response
from app.config.settings import settings

router = APIRouter(prefix="/scrape")
logger = logging.getLogger(__name__)


@router.post("/url", summary="Scrape a single URL")
def scrape_url(
    url: str = Body(..., embed=True, description="URL to scrape"),
    scraper_type: str = Body(default="beautifulsoup", embed=True),
    db: Session = Depends(get_db),
):
    """
    Trigger a scraping job for a single URL.
    Supported scraper_type values: 'beautifulsoup', 'playwright'
    """
    service = ScrapingService(db)
    result = service.scrape_url(url=url, scraper_type=scraper_type)
    return success_response(data=result, message="Scraping job completed.")


@router.post("/csv", summary="Upload and import a CSV file")
def import_csv(
    file: UploadFile = File(..., description="CSV file containing product data"),
    db: Session = Depends(get_db),
):
    """
    Upload a CSV file and import it as product data.
    The file is saved to the uploads directory and processed immediately.
    """
    os.makedirs(settings.UPLOADS_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOADS_DIR, file.filename or "upload.csv")

    # Save the uploaded file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    service = ScrapingService(db)
    result = service.import_csv(file_path)
    return success_response(data=result, message="CSV imported successfully.")


@router.post("/urls", summary="Collect URLs from a base page")
def collect_urls(
    base_url: str = Body(..., embed=True, description="Base URL to crawl for product links"),
    db: Session = Depends(get_db),
):
    """
    Crawl a category/listing page and return all discovered product URLs.
    Useful for building a scraping queue.
    """
    service = ScrapingService(db)
    urls = service.collect_urls(base_url)
    return success_response(
        data={"base_url": base_url, "urls": urls, "count": len(urls)},
        message=f"Discovered {len(urls)} URLs.",
    )
