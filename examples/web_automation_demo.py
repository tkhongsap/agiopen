"""
Web Automation Demo

Demonstrates web automation capabilities:
- Form filling
- Data scraping
- Web research
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.web_automation import FormFiller, DataScraper, WebResearcher
from src.web_automation.form_filler import FormField
from src.web_automation.data_scraper import ScrapeTarget

load_dotenv()


async def demo_form_filling():
    """Demonstrate form filling capabilities."""
    print("\n" + "=" * 50)
    print("Demo: Form Filling")
    print("=" * 50)

    filler = FormFiller(max_steps=20, model="lux-actor-1")

    # Example: Fill a contact form
    fields = [
        FormField("First Name", "John"),
        FormField("Last Name", "Doe"),
        FormField("Email", "john.doe@example.com"),
        FormField("Phone", "+1-555-123-4567"),
        FormField("Message", "Hello! I'm interested in learning more about your services.", field_type="textarea"),
        FormField("Subscribe to newsletter", True, field_type="checkbox"),
    ]

    print("\nFilling contact form with:")
    for field in fields:
        print(f"  - {field.name}: {field.value}")

    result = await filler.fill_form(
        url="https://example.com/contact",  # Replace with actual URL
        fields=fields,
        submit=True
    )

    print(f"\nResult: {'Success' if result.success else 'Failed'}")
    print(f"Fields filled: {result.fields_filled}")
    if result.errors:
        print(f"Errors: {result.errors}")


async def demo_data_scraping():
    """Demonstrate data scraping capabilities."""
    print("\n" + "=" * 50)
    print("Demo: Data Scraping")
    print("=" * 50)

    scraper = DataScraper(max_steps=30, model="lux-thinker-1")

    # Example: Scrape product information
    targets = [
        ScrapeTarget("product_name", "The main product title/name"),
        ScrapeTarget("price", "The product price", expected_type="number"),
        ScrapeTarget("rating", "Customer rating or review score", expected_type="number"),
        ScrapeTarget("description", "Product description text"),
        ScrapeTarget("features", "List of product features", expected_type="list"),
    ]

    print("\nScraping product page for:")
    for target in targets:
        print(f"  - {target.name}: {target.description}")

    result = await scraper.scrape(
        url="https://example.com/product/123",  # Replace with actual URL
        targets=targets
    )

    print(f"\nResult: {'Success' if result.success else 'Failed'}")
    print(f"URL: {result.url}")
    if result.errors:
        print(f"Errors: {result.errors}")


async def demo_web_research():
    """Demonstrate web research capabilities."""
    print("\n" + "=" * 50)
    print("Demo: Web Research")
    print("=" * 50)

    researcher = WebResearcher(max_steps=50, model="lux-thinker-1")

    topic = "Latest developments in AI computer use agents 2025"

    print(f"\nResearching topic: {topic}")
    print("Consulting 3 sources...")

    result = await researcher.research(
        topic=topic,
        num_sources=3,
        search_engine="google",
        output_format="markdown"
    )

    print(f"\nResult: {'Success' if result.success else 'Failed'}")
    print(f"Sources visited: {result.sources_visited}")
    if result.errors:
        print(f"Errors: {result.errors}")


async def demo_fact_check():
    """Demonstrate fact-checking capabilities."""
    print("\n" + "=" * 50)
    print("Demo: Fact Checking")
    print("=" * 50)

    researcher = WebResearcher(max_steps=40, model="lux-thinker-1")

    claim = "The Lux model by OpenAGI achieved an 83.6 score on the Online-Mind2Web benchmark"

    print(f"\nFact-checking claim: {claim}")

    result = await researcher.fact_check(
        claim=claim,
        num_sources=3
    )

    print(f"\nResult: {'Success' if result.success else 'Failed'}")
    print(f"Sources checked: {result.sources_visited}")
    if result.errors:
        print(f"Errors: {result.errors}")


async def main():
    """Run all web automation demos."""
    print("=" * 60)
    print("   Web Automation Demonstration")
    print("   Using OpenAGI Lux Model")
    print("=" * 60)

    # Check for API key
    if not os.getenv("OAGI_API_KEY"):
        print("\nWarning: OAGI_API_KEY not set.")
        print("Set it with: export OAGI_API_KEY='your_key_here'")
        print("Get your key at: https://developer.agiopen.org\n")

    # Run demos
    await demo_form_filling()
    await demo_data_scraping()
    await demo_web_research()
    await demo_fact_check()

    print("\n" + "=" * 60)
    print("All demos completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
