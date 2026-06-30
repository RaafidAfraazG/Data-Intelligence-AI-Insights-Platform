"""
app/agents/data_collector_agent.py
=====================================
DataCollectorAgent — coordinates scraping and data cleaning.

This agent:
1. Accepts a list of URLs and/or a CSV file path
2. Runs ScrapingService to collect raw data
3. Runs CleaningService to normalize and deduplicate
4. Returns a summary of what was collected and cleaned

Design note: This is a simple Python class, not an autonomous loop.
The user triggers it explicitly via an API endpoint.
"""

import logging
from typing import Any

from sqlalchemy.orm import Session

from app.services.scraping_service import ScrapingService
from app.services.cleaning_service import CleaningService

logger = logging.getLogger(__name__)


class DataCollectorAgent:
    """
    Coordinates data collection from URLs and/or CSV files.
    Produces cleaned, deduplicated product data ready for analysis.
    """

    def __init__(self, db: Session) -> None:
        self.db = db
        self.scraping_svc = ScrapingService(db)
        self.cleaning_svc = CleaningService()

    def run(
        self,
        urls: list[str] | None = None,
        csv_path: str | None = None,
        scraper_type: str = "beautifulsoup",
    ) -> dict[str, Any]:
        """
        Run the full data collection pipeline.

        Parameters
        ----------
        urls : list[str] | None
            List of product page URLs to scrape.
        csv_path : str | None
            Path to a CSV file to import.
        scraper_type : str
            'beautifulsoup' or 'playwright'

        Returns
        -------
        dict with keys: urls_scraped, csv_imported, raw_items, cleaned_items, summary
        """
        logger.info(
            "DataCollectorAgent starting. urls=%d, csv=%s",
            len(urls or []),
            csv_path,
        )

        raw_items: list[dict] = []
        urls_scraped = 0
        csv_rows = 0

        # ── Step 1: Scrape URLs ───────────────────────────────────────────────
        for url in (urls or []):
            try:
                result = self.scraping_svc.scrape_url(url=url, scraper_type=scraper_type)
                urls_scraped += 1
                logger.info("Scraped URL: %s — items_found: %d", url, result.get("items_found", 0))
            except Exception as exc:
                logger.error("Failed to scrape URL %s: %s", url, exc)

        # ── Step 2: Import CSV ────────────────────────────────────────────────
        if csv_path:
            try:
                result = self.scraping_svc.import_csv(csv_path)
                csv_rows = result.get("rows_found", 0)
                logger.info("CSV import complete. Rows: %d", csv_rows)
            except Exception as exc:
                logger.error("CSV import failed: %s", exc)

        # ── Step 3: Clean collected data ──────────────────────────────────────
        cleaned = []
        if raw_items:
            cleaned = self.cleaning_svc.clean_products(raw_items)

        summary = (
            f"Scraped {urls_scraped} URL(s), imported {csv_rows} CSV row(s). "
            f"Cleaned {len(cleaned)} records."
        )
        logger.info("DataCollectorAgent complete: %s", summary)

        return {
            "urls_scraped": urls_scraped,
            "csv_imported": csv_rows,
            "raw_items": len(raw_items),
            "cleaned_items": len(cleaned),
            "summary": summary,
        }
