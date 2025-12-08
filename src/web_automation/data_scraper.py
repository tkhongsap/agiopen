"""
Data Scraper - Extract structured data from web pages.
"""

from dataclasses import dataclass
from typing import Any, Optional
import json


@dataclass
class ScrapeTarget:
    """Defines what data to scrape from a page."""
    name: str
    description: str
    expected_type: str = "text"  # text, number, list, table


@dataclass
class ScrapeResult:
    """Result of a scraping operation."""
    success: bool
    url: str
    data: dict[str, Any]
    errors: list[str]
    screenshot_path: Optional[str] = None


class DataScraper:
    """
    Extract data from web pages using Lux.

    Example:
        scraper = DataScraper()
        result = await scraper.scrape(
            url="https://example.com/product/123",
            targets=[
                ScrapeTarget("product_name", "The main product title"),
                ScrapeTarget("price", "The product price", expected_type="number"),
                ScrapeTarget("features", "List of product features", expected_type="list"),
            ]
        )
    """

    def __init__(
        self,
        max_steps: int = 30,
        model: str = "lux-thinker-1",
        verbose: bool = False
    ):
        self.max_steps = max_steps
        self.model = model
        self.verbose = verbose

    async def scrape(
        self,
        url: str,
        targets: list[ScrapeTarget],
        wait_for_load: bool = True
    ) -> ScrapeResult:
        """
        Scrape specified data from a URL.

        Args:
            url: The URL to scrape
            targets: List of ScrapeTarget defining what to extract
            wait_for_load: Whether to wait for page to fully load

        Returns:
            ScrapeResult with extracted data
        """
        try:
            from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

            agent = AsyncDefaultAgent(max_steps=self.max_steps, model=self.model)

            # Build extraction instructions
            target_instructions = self._build_target_instructions(targets)

            instruction = f"""
            Navigate to {url}
            {"Wait for the page to fully load." if wait_for_load else ""}

            Extract the following information:
            {target_instructions}

            After extracting all data, copy it to clipboard in JSON format.
            """

            completed = await agent.execute(
                instruction,
                action_handler=AsyncPyautoguiActionHandler(),
                image_provider=AsyncScreenshotMaker(),
            )

            # Note: In a real implementation, you would retrieve the clipboard content
            # This is a simplified example
            return ScrapeResult(
                success=completed,
                url=url,
                data={t.name: None for t in targets},  # Placeholder
                errors=[]
            )

        except ImportError:
            return ScrapeResult(
                success=False,
                url=url,
                data={},
                errors=["oagi package not installed. Run: pip install oagi"]
            )
        except Exception as e:
            return ScrapeResult(
                success=False,
                url=url,
                data={},
                errors=[str(e)]
            )

    def _build_target_instructions(self, targets: list[ScrapeTarget]) -> str:
        """Build instruction text for each scrape target."""
        instructions = []
        for i, target in enumerate(targets, 1):
            type_hint = ""
            if target.expected_type == "number":
                type_hint = " (extract as a number)"
            elif target.expected_type == "list":
                type_hint = " (extract as a list of items)"
            elif target.expected_type == "table":
                type_hint = " (extract as tabular data)"

            instructions.append(f"{i}. {target.name}: {target.description}{type_hint}")

        return "\n".join(instructions)

    async def scrape_multiple(
        self,
        urls: list[str],
        targets: list[ScrapeTarget]
    ) -> list[ScrapeResult]:
        """
        Scrape the same data from multiple URLs.

        Args:
            urls: List of URLs to scrape
            targets: Data targets to extract from each URL

        Returns:
            List of ScrapeResult for each URL
        """
        results = []
        for url in urls:
            result = await self.scrape(url=url, targets=targets)
            results.append(result)

        return results

    async def scrape_table(
        self,
        url: str,
        table_description: str,
        include_headers: bool = True
    ) -> ScrapeResult:
        """
        Specialized method for scraping tabular data.

        Args:
            url: The URL containing the table
            table_description: Description to identify the table
            include_headers: Whether to include table headers

        Returns:
            ScrapeResult with table data
        """
        try:
            from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

            agent = AsyncDefaultAgent(max_steps=self.max_steps, model=self.model)

            instruction = f"""
            Navigate to {url}

            Find the table: {table_description}

            Extract all data from the table:
            {"1. Include the header row" if include_headers else "1. Skip the header row"}
            2. Extract each row as a separate record
            3. Format as JSON array

            Copy the extracted data to clipboard.
            """

            completed = await agent.execute(
                instruction,
                action_handler=AsyncPyautoguiActionHandler(),
                image_provider=AsyncScreenshotMaker(),
            )

            return ScrapeResult(
                success=completed,
                url=url,
                data={"table": []},  # Placeholder
                errors=[]
            )

        except Exception as e:
            return ScrapeResult(
                success=False,
                url=url,
                data={},
                errors=[str(e)]
            )
