"""
Web Research - Conduct multi-step research across websites.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ResearchResult:
    """Result of a research operation."""
    success: bool
    topic: str
    sources_visited: int
    summary: Optional[str]
    errors: list[str]
    output_path: Optional[str] = None


class WebResearcher:
    """
    Conduct web research using Lux.

    Example:
        researcher = WebResearcher()
        result = await researcher.research(
            topic="Latest developments in quantum computing",
            num_sources=5,
            output_format="markdown"
        )
    """

    def __init__(
        self,
        max_steps: int = 50,
        model: str = "lux-thinker-1",
        verbose: bool = False
    ):
        self.max_steps = max_steps
        self.model = model
        self.verbose = verbose

    async def research(
        self,
        topic: str,
        num_sources: int = 3,
        search_engine: str = "google",
        output_format: str = "markdown",
        save_to_file: Optional[str] = None
    ) -> ResearchResult:
        """
        Conduct research on a topic across multiple sources.

        Args:
            topic: The research topic
            num_sources: Number of sources to consult
            search_engine: Search engine to use (google, bing, duckduckgo)
            output_format: Format for the summary (markdown, text, json)
            save_to_file: Optional file path to save results

        Returns:
            ResearchResult with findings
        """
        try:
            from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

            agent = AsyncDefaultAgent(max_steps=self.max_steps, model=self.model)

            save_instruction = ""
            if save_to_file:
                save_instruction = f"\n6. Save the compiled research to: {save_to_file}"

            instruction = f"""
            Research Topic: "{topic}"

            Steps:
            1. Go to {search_engine}.com and search for "{topic}"
            2. Visit {num_sources} reputable sources from the search results
            3. For each source:
               - Read the main content
               - Note key points and findings
               - Record the source URL
            4. Compile all findings into a comprehensive summary
            5. Format the summary as {output_format}{save_instruction}
            """

            completed = await agent.execute(
                instruction,
                action_handler=AsyncPyautoguiActionHandler(),
                image_provider=AsyncScreenshotMaker(),
            )

            return ResearchResult(
                success=completed,
                topic=topic,
                sources_visited=num_sources,
                summary=None,  # Would be populated from actual execution
                errors=[],
                output_path=save_to_file
            )

        except ImportError:
            return ResearchResult(
                success=False,
                topic=topic,
                sources_visited=0,
                summary=None,
                errors=["oagi package not installed. Run: pip install oagi"]
            )
        except Exception as e:
            return ResearchResult(
                success=False,
                topic=topic,
                sources_visited=0,
                summary=None,
                errors=[str(e)]
            )

    async def compare_sources(
        self,
        topic: str,
        sources: list[str],
        comparison_criteria: list[str]
    ) -> ResearchResult:
        """
        Compare information across specific sources.

        Args:
            topic: The topic to compare
            sources: List of URLs to compare
            comparison_criteria: Aspects to compare

        Returns:
            ResearchResult with comparison
        """
        try:
            from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

            agent = AsyncDefaultAgent(max_steps=self.max_steps, model=self.model)

            sources_list = "\n".join(f"   - {url}" for url in sources)
            criteria_list = "\n".join(f"   - {c}" for c in comparison_criteria)

            instruction = f"""
            Compare information about "{topic}" across these sources:
            {sources_list}

            For each source, extract information about:
            {criteria_list}

            Then create a comparison table showing how each source differs.
            """

            completed = await agent.execute(
                instruction,
                action_handler=AsyncPyautoguiActionHandler(),
                image_provider=AsyncScreenshotMaker(),
            )

            return ResearchResult(
                success=completed,
                topic=topic,
                sources_visited=len(sources),
                summary=None,
                errors=[]
            )

        except Exception as e:
            return ResearchResult(
                success=False,
                topic=topic,
                sources_visited=0,
                summary=None,
                errors=[str(e)]
            )

    async def fact_check(
        self,
        claim: str,
        num_sources: int = 3
    ) -> ResearchResult:
        """
        Fact-check a claim using multiple sources.

        Args:
            claim: The claim to verify
            num_sources: Number of sources to check

        Returns:
            ResearchResult with fact-check findings
        """
        try:
            from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

            agent = AsyncDefaultAgent(max_steps=self.max_steps, model=self.model)

            instruction = f"""
            Fact-check the following claim: "{claim}"

            Steps:
            1. Search for information related to this claim
            2. Visit {num_sources} reputable sources
            3. For each source, note:
               - Whether it supports, refutes, or is neutral on the claim
               - Key evidence provided
            4. Compile a summary indicating the overall verdict
            """

            completed = await agent.execute(
                instruction,
                action_handler=AsyncPyautoguiActionHandler(),
                image_provider=AsyncScreenshotMaker(),
            )

            return ResearchResult(
                success=completed,
                topic=f"Fact-check: {claim}",
                sources_visited=num_sources,
                summary=None,
                errors=[]
            )

        except Exception as e:
            return ResearchResult(
                success=False,
                topic=f"Fact-check: {claim}",
                sources_visited=0,
                summary=None,
                errors=[str(e)]
            )
