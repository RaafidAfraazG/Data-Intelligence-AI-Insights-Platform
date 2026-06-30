"""
app/services/scraping_service.py
=================================
Orchestrates scraping operations.
Delegates to the appropriate scraper class based on input type.
Business logic will be expanded in a future prompt.
"""

import logging
from sqlalchemy.orm import Session

from app.scrapers.playwright_scraper import PlaywrightScraper
from app.scrapers.bs4_scraper import BeautifulSoupScraper
from app.scrapers.csv_importer import CSVImporter
from app.scrapers.url_collector import URLCollector
from app.repositories.source import SourceRepository
from app.schemas.source import SourceCreate

logger = logging.getLogger(__name__)


class ScrapingService:
    """Co-ordinates scraping jobs and records data sources."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.source_repo = SourceRepository(db)

    def scrape_url(self, url: str, scraper_type: str = "beautifulsoup") -> dict:
        """
        Trigger a scraping job for a given URL.
        Returns raw scraped data — cleaning and persistence happen separately.
        """
        logger.info("Scraping URL=%r using scraper_type=%r.", url, scraper_type)

        # Record the source
        existing = self.source_repo.get_by_url(url)
        if not existing:
            self.source_repo.create(
                SourceCreate(url=url, source_type=scraper_type).model_dump()
            )

        # TODO: Route to PlaywrightScraper for JS-heavy pages
        if scraper_type == "playwright":
            scraper = PlaywrightScraper()
        else:
            scraper = BeautifulSoupScraper()

        raw_data = scraper.scrape(url)
        logger.info("Scraping completed for URL=%r. Items returned: %d.", url, len(raw_data))
        return {"url": url, "scraper": scraper_type, "items_found": len(raw_data)}

    def import_csv(self, file_path: str) -> dict:
        """
        Import product data from a CSV file.
        Returns a summary of how many records were found.
        """
        logger.info("Importing CSV from path=%r.", file_path)
        importer = CSVImporter()
        rows = importer.load(file_path)
        logger.info("CSV import complete. Rows found: %d.", len(rows))
        return {"file": file_path, "rows_found": len(rows)}

    def collect_urls(self, base_url: str) -> list[str]:
        """
        Discover product URLs from a given base URL.
        Placeholder — real logic added in a future prompt.
        """
        collector = URLCollector()
        return collector.collect(base_url)
