"""
app/scrapers/__init__.py
"""
from app.scrapers.base_scraper import BaseScraper
from app.scrapers.playwright_scraper import PlaywrightScraper
from app.scrapers.bs4_scraper import BeautifulSoupScraper
from app.scrapers.csv_importer import CSVImporter
from app.scrapers.url_collector import URLCollector

__all__ = [
    "BaseScraper",
    "PlaywrightScraper",
    "BeautifulSoupScraper",
    "CSVImporter",
    "URLCollector",
]
