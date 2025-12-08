"""
OpenAGI Lux Computer Use Automation Library

This package provides modules for automating computer tasks using the Lux model:
- web_automation: Browser-based automation (forms, scraping, research)
- qa_testing: Automated UI testing and validation
- data_processing: Data entry and report generation
"""

from .config import Config, get_config

__version__ = "0.1.0"
__all__ = ["Config", "get_config"]
