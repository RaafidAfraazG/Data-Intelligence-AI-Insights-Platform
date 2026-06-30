"""
app/scrapers/base_scraper.py
=============================
Abstract base class that every scraper must inherit from.

Defines the interface so that scrapers are interchangeable.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """
    All scrapers must implement `scrape(url)` and return a list of dicts,
    where each dict represents one raw product record.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def scrape(self, url: str) -> list[dict[str, Any]]:
        """
        Scrape the given URL and return raw product data.

        Parameters
        ----------
        url : str
            The URL to scrape.

        Returns
        -------
        list[dict]
            Each dict should have keys matching Product fields where possible:
            name, brand, category, price, rating, review_count, description.
        """
        ...

    def _log_start(self, url: str) -> None:
        self.logger.info("Starting scrape for URL: %s", url)

    def _log_done(self, url: str, count: int) -> None:
        self.logger.info("Finished scraping %s — %d items found.", url, count)
