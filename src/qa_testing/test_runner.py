"""
Test Runner - Execute UI test sequences with Lux.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from datetime import datetime
import asyncio


@dataclass
class TestStep:
    """A single step in a test case."""
    description: str
    action: str
    expected_result: Optional[str] = None
    timeout: int = 30


@dataclass
class TestCase:
    """A complete test case with multiple steps."""
    name: str
    description: str
    steps: list[TestStep]
    setup: Optional[str] = None
    teardown: Optional[str] = None
    tags: list[str] = field(default_factory=list)


@dataclass
class TestResult:
    """Result of a test execution."""
    test_name: str
    success: bool
    steps_passed: int
    steps_total: int
    duration_seconds: float
    errors: list[str]
    screenshots: list[str] = field(default_factory=list)


class TestRunner:
    """
    Execute UI tests using Lux.

    Example:
        runner = TestRunner()

        test = TestCase(
            name="Login Test",
            description="Verify user can log in",
            steps=[
                TestStep("Enter username", "Type 'testuser' in username field"),
                TestStep("Enter password", "Type 'password123' in password field"),
                TestStep("Click login", "Click the Login button"),
            ]
        )

        result = await runner.run_test(test)
    """

    def __init__(
        self,
        max_steps_per_test: int = 50,
        model: str = "lux-tasker-1",
        verbose: bool = False,
        screenshot_on_failure: bool = True
    ):
        self.max_steps_per_test = max_steps_per_test
        self.model = model
        self.verbose = verbose
        self.screenshot_on_failure = screenshot_on_failure

    async def run_test(
        self,
        test: TestCase,
        base_url: Optional[str] = None
    ) -> TestResult:
        """
        Run a single test case.

        Args:
            test: The TestCase to execute
            base_url: Optional base URL to navigate to first

        Returns:
            TestResult with execution details
        """
        start_time = datetime.now()
        errors = []

        try:
            from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

            agent = AsyncDefaultAgent(max_steps=self.max_steps_per_test, model=self.model)

            # Build test instruction
            instruction = self._build_test_instruction(test, base_url)

            completed = await agent.execute(
                instruction,
                action_handler=AsyncPyautoguiActionHandler(),
                image_provider=AsyncScreenshotMaker(),
            )

            duration = (datetime.now() - start_time).total_seconds()

            return TestResult(
                test_name=test.name,
                success=completed,
                steps_passed=len(test.steps) if completed else 0,
                steps_total=len(test.steps),
                duration_seconds=duration,
                errors=errors
            )

        except ImportError:
            return TestResult(
                test_name=test.name,
                success=False,
                steps_passed=0,
                steps_total=len(test.steps),
                duration_seconds=0,
                errors=["oagi package not installed. Run: pip install oagi"]
            )
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return TestResult(
                test_name=test.name,
                success=False,
                steps_passed=0,
                steps_total=len(test.steps),
                duration_seconds=duration,
                errors=[str(e)]
            )

    def _build_test_instruction(
        self,
        test: TestCase,
        base_url: Optional[str]
    ) -> str:
        """Build the test instruction from a TestCase."""
        parts = [f"Test: {test.name}", f"Description: {test.description}", ""]

        if base_url:
            parts.append(f"Navigate to: {base_url}")
            parts.append("")

        if test.setup:
            parts.append("Setup:")
            parts.append(test.setup)
            parts.append("")

        parts.append("Test Steps:")
        for i, step in enumerate(test.steps, 1):
            parts.append(f"{i}. {step.description}")
            parts.append(f"   Action: {step.action}")
            if step.expected_result:
                parts.append(f"   Verify: {step.expected_result}")

        if test.teardown:
            parts.append("")
            parts.append("Teardown:")
            parts.append(test.teardown)

        return "\n".join(parts)

    async def run_suite(
        self,
        tests: list[TestCase],
        stop_on_failure: bool = False,
        parallel: bool = False
    ) -> list[TestResult]:
        """
        Run a suite of tests.

        Args:
            tests: List of TestCase objects to run
            stop_on_failure: Stop running if a test fails
            parallel: Run tests in parallel (requires multiple sessions)

        Returns:
            List of TestResult for each test
        """
        results = []

        if parallel:
            # Run tests concurrently
            tasks = [self.run_test(test) for test in tests]
            results = await asyncio.gather(*tasks)
        else:
            # Run tests sequentially
            for test in tests:
                result = await self.run_test(test)
                results.append(result)

                if stop_on_failure and not result.success:
                    break

        return results

    def generate_report(
        self,
        results: list[TestResult],
        format: str = "markdown"
    ) -> str:
        """
        Generate a test report from results.

        Args:
            results: List of TestResult objects
            format: Output format (markdown, html, json)

        Returns:
            Formatted report string
        """
        total = len(results)
        passed = sum(1 for r in results if r.success)
        failed = total - passed
        total_duration = sum(r.duration_seconds for r in results)

        if format == "markdown":
            lines = [
                "# Test Report",
                "",
                "## Summary",
                f"- **Total Tests:** {total}",
                f"- **Passed:** {passed}",
                f"- **Failed:** {failed}",
                f"- **Pass Rate:** {passed/total*100:.1f}%" if total > 0 else "N/A",
                f"- **Total Duration:** {total_duration:.2f}s",
                "",
                "## Results",
                "",
            ]

            for result in results:
                status = "PASS" if result.success else "FAIL"
                lines.append(f"### {result.test_name} - {status}")
                lines.append(f"- Steps: {result.steps_passed}/{result.steps_total}")
                lines.append(f"- Duration: {result.duration_seconds:.2f}s")
                if result.errors:
                    lines.append(f"- Errors: {', '.join(result.errors)}")
                lines.append("")

            return "\n".join(lines)

        return str(results)
