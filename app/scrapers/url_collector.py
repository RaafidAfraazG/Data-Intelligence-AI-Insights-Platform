"""
app/scrapers/url_collector.py
==============================
Discovers product URLs from a base/category page.

Useful for building a queue of URLs to pass to the scrapers.

Usage:
    collector = URLCollector()
    urls = collector.collect("https://example.com/category/electronics")
"""

import logging

import requests
from bs4 import BeautifulSoup

from app.config.constants import DEFAULT_HEADERS
from app.config.settings import settings

logger = logging.getLogger(__name__)


class URLCollector:
    """
    Crawls a category/listing page and returns a list of individual
    product page URLs found on it.
    """

    def collect(self, base_url: str) -> list[str]:
        """
        Fetch *base_url* and extract all <a> href links that look like
        product URLs.

        Returns
        -------
        list[str]
            Absolute URLs found on the page.
        """
        logger.info("Collecting URLs from: %s", base_url)
        urls: list[str] = []

        try:
            response = requests.get(
                base_url,
                headers=DEFAULT_HEADERS,
                timeout=settings.SCRAPING_TIMEOUT,
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # ── TODO: Customise selector to target product links ───────────────
            # By default we collect all <a> tags with href; you'll want to
            # filter these to product-specific paths for each target site.
            for a_tag in soup.select("a[href]"):
                href = a_tag["href"]
                if href.startswith("http"):
                    urls.append(href)
                elif href.startswith("/"):
                    # Build an absolute URL from the relative path
                    from urllib.parse import urlparse
                    parsed = urlparse(base_url)
                    urls.append(f"{parsed.scheme}://{parsed.netloc}{href}")

        except requests.RequestException as exc:
            logger.error("URL collection failed for %s: %s", base_url, exc)

        logger.info("Collected %d URLs from %s.", len(urls), base_url)
        return urls

    def add_manual_urls(self, urls: list[str]) -> list[str]:
        """
        Accept manually-provided URLs directly.
        Performs basic validation before returning.
        """
        valid = [u for u in urls if u.startswith("http")]
        if len(valid) != len(urls):
            logger.warning(
                "%d URL(s) were skipped (must start with http).",
                len(urls) - len(valid),
            )
        return valid
