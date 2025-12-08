"""
Report Generator - Extract and compile reports from data sources.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class ReportFormat(Enum):
    """Output formats for reports."""
    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"
    DOCX = "docx"
    JSON = "json"


@dataclass
class DataSource:
    """A data source for the report."""
    name: str
    url: str
    extraction_instructions: str


@dataclass
class ReportConfig:
    """Configuration for report generation."""
    title: str
    sources: list[DataSource]
    output_format: ReportFormat = ReportFormat.MARKDOWN
    template_path: Optional[str] = None
    include_screenshots: bool = False
    date_range: Optional[str] = None


@dataclass
class ReportResult:
    """Result of report generation."""
    success: bool
    output_path: Optional[str]
    sources_processed: int
    errors: list[str] = field(default_factory=list)


class ReportGenerator:
    """
    Generate reports from multiple data sources using Lux.

    Example:
        generator = ReportGenerator()

        config = ReportConfig(
            title="Monthly Sales Report",
            sources=[
                DataSource(
                    name="Sales Dashboard",
                    url="https://sales.example.com/dashboard",
                    extraction_instructions="Extract total revenue, units sold, and top products"
                ),
                DataSource(
                    name="Customer Analytics",
                    url="https://analytics.example.com",
                    extraction_instructions="Extract new customers, churn rate, NPS score"
                )
            ],
            output_format=ReportFormat.MARKDOWN
        )

        result = await generator.generate(config, output_path="reports/monthly.md")
    """

    def __init__(
        self,
        max_steps: int = 100,
        model: str = "lux-thinker-1",
        verbose: bool = False
    ):
        self.max_steps = max_steps
        self.model = model
        self.verbose = verbose

    async def generate(
        self,
        config: ReportConfig,
        output_path: str
    ) -> ReportResult:
        """
        Generate a report from multiple data sources.

        Args:
            config: ReportConfig with sources and settings
            output_path: Where to save the generated report

        Returns:
            ReportResult with generation details
        """
        try:
            from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

            agent = AsyncDefaultAgent(max_steps=self.max_steps, model=self.model)

            # Build comprehensive instruction
            instruction = self._build_report_instruction(config, output_path)

            completed = await agent.execute(
                instruction,
                action_handler=AsyncPyautoguiActionHandler(),
                image_provider=AsyncScreenshotMaker(),
            )

            return ReportResult(
                success=completed,
                output_path=output_path if completed else None,
                sources_processed=len(config.sources)
            )

        except ImportError:
            return ReportResult(
                success=False,
                output_path=None,
                sources_processed=0,
                errors=["oagi package not installed. Run: pip install oagi"]
            )
        except Exception as e:
            return ReportResult(
                success=False,
                output_path=None,
                sources_processed=0,
                errors=[str(e)]
            )

    def _build_report_instruction(
        self,
        config: ReportConfig,
        output_path: str
    ) -> str:
        """Build comprehensive report generation instruction."""
        parts = [
            f"Generate Report: {config.title}",
            ""
        ]

        if config.date_range:
            parts.append(f"Date Range: {config.date_range}")
            parts.append("")

        # Phase 1: Data Collection
        parts.append("PHASE 1 - DATA COLLECTION:")
        parts.append("")

        for i, source in enumerate(config.sources, 1):
            parts.append(f"Source {i}: {source.name}")
            parts.append(f"  URL: {source.url}")
            parts.append(f"  Extract: {source.extraction_instructions}")
            if config.include_screenshots:
                parts.append(f"  Take a screenshot of the data")
            parts.append("")

        # Phase 2: Report Assembly
        parts.append("PHASE 2 - REPORT ASSEMBLY:")
        parts.append("")

        if config.template_path:
            parts.append(f"1. Open the template at: {config.template_path}")
            parts.append("2. Fill in the extracted data in appropriate sections")
        else:
            parts.append("1. Create a new document")
            parts.append(f"2. Add title: {config.title}")
            parts.append("3. For each data source, create a section with the extracted data")

        parts.append("")

        # Phase 3: Finalization
        parts.append("PHASE 3 - FINALIZATION:")
        parts.append("")
        parts.append(f"1. Format the report as {config.output_format.value}")
        parts.append(f"2. Save to: {output_path}")
        parts.append("3. Verify the file was saved successfully")

        return "\n".join(parts)

    async def extract_dashboard_metrics(
        self,
        url: str,
        metrics: list[str],
        output_format: str = "json"
    ) -> dict:
        """
        Extract specific metrics from a dashboard.

        Args:
            url: Dashboard URL
            metrics: List of metric names to extract
            output_format: Format for extracted data

        Returns:
            Dictionary of extracted metrics
        """
        try:
            from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

            agent = AsyncDefaultAgent(max_steps=30, model="lux-actor-1")

            metrics_list = "\n".join(f"- {m}" for m in metrics)

            instruction = f"""
            Navigate to {url}
            Wait for dashboard to fully load.

            Extract the following metrics:
            {metrics_list}

            Copy the extracted values to clipboard in {output_format} format.
            """

            completed = await agent.execute(
                instruction,
                action_handler=AsyncPyautoguiActionHandler(),
                image_provider=AsyncScreenshotMaker(),
            )

            # In real implementation, parse clipboard content
            return {
                "success": completed,
                "metrics": {m: None for m in metrics}
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metrics": {}
            }

    async def schedule_report(
        self,
        config: ReportConfig,
        output_path: str,
        schedule: str
    ) -> dict:
        """
        Schedule a report for recurring generation.

        Note: This is a placeholder for scheduling functionality.
        In production, you would integrate with a task scheduler.

        Args:
            config: ReportConfig for the report
            output_path: Where to save reports
            schedule: Cron-style schedule (e.g., "0 9 * * 1" for Monday 9am)

        Returns:
            Schedule confirmation
        """
        # This would integrate with a scheduler like APScheduler or Celery
        return {
            "scheduled": True,
            "report_title": config.title,
            "schedule": schedule,
            "output_path": output_path,
            "note": "Scheduling requires external scheduler integration"
        }

    async def compare_reports(
        self,
        report_paths: list[str],
        comparison_metrics: list[str]
    ) -> dict:
        """
        Compare metrics across multiple reports.

        Args:
            report_paths: Paths to reports to compare
            comparison_metrics: Metrics to compare

        Returns:
            Comparison results
        """
        try:
            from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

            agent = AsyncDefaultAgent(max_steps=50, model="lux-thinker-1")

            paths_list = "\n".join(f"- {p}" for p in report_paths)
            metrics_list = "\n".join(f"- {m}" for m in comparison_metrics)

            instruction = f"""
            Compare the following reports:
            {paths_list}

            For each report, extract these metrics:
            {metrics_list}

            Create a comparison table showing the metrics side by side.
            Highlight any significant differences.
            """

            completed = await agent.execute(
                instruction,
                action_handler=AsyncPyautoguiActionHandler(),
                image_provider=AsyncScreenshotMaker(),
            )

            return {
                "success": completed,
                "reports_compared": len(report_paths),
                "metrics_compared": comparison_metrics
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
