"""
Web Automation Module

Provides tools for browser-based automation tasks:
- Form filling
- Data scraping
- Web research
"""

from .form_filler import FormFiller
from .data_scraper import DataScraper
from .web_research import WebResearcher

__all__ = ["FormFiller", "DataScraper", "WebResearcher"]
