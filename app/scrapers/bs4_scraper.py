"""
app/scrapers/bs4_scraper.py
============================
BeautifulSoup + Requests scraper for static HTML pages.

Suitable for e-commerce pages that serve fully-rendered HTML.

Usage:
    scraper = BeautifulSoupScraper()
    data = scraper.scrape("https://example.com/products")
"""

import logging
from typing import Any

import requests
from bs4 import BeautifulSoup

from app.scrapers.base_scraper import BaseScraper
from app.config.constants import DEFAULT_HEADERS
from app.config.settings import settings

logger = logging.getLogger(__name__)


class BeautifulSoupScraper(BaseScraper):
    """
    Fetches a page with the requests library and parses it with
    BeautifulSoup. Best for static/server-rendered HTML pages.
    """

    def scrape(self, url: str) -> list[dict[str, Any]]:
        """
        Fetch the URL and parse product data from the HTML.
        Returns an empty list until site-specific selectors are added.
        """
        self._log_start(url)
        results: list[dict[str, Any]] = []

        try:
            response = requests.get(
                url,
                headers=DEFAULT_HEADERS,
                timeout=settings.SCRAPING_TIMEOUT,
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # ── TODO: Add site-specific selectors here ────────────────────────
            # Example for a generic product listing page:
            # for card in soup.select(".product-item"):
            #     name_tag = card.select_one(".product-name")
            #     price_tag = card.select_one(".product-price")
            #     results.append({
            #         "name": name_tag.get_text(strip=True) if name_tag else None,
            #         "price": price_tag.get_text(strip=True) if price_tag else None,
            #         "source": url,
            #     })

            logger.debug("Parsed HTML from %s (status=%d).", url, response.status_code)

        except requests.RequestException as exc:
            logger.error("HTTP request failed for %s: %s", url, exc)

        self._log_done(url, len(results))
        return results
