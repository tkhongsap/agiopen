#!/usr/bin/env python3
"""
Nuclear Player QA Testing Example

This example demonstrates using the TaskerAgent framework to automate
UI testing of the Nuclear Player desktop application.

Based on the official oagi-lux-samples repository pattern.

This showcases Lux's ability to test desktop applications (not just browsers).

Prerequisites:
    - Nuclear Player must be installed on the system
    - https://nuclear.js.org/

Usage:
    python nuclear_player_qa.py --verify-all-pages
    python nuclear_player_qa.py --test-playback
    python nuclear_player_qa.py --test-search
"""

import asyncio
import argparse
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from oagi import TaskerAgent
    from oagi import AsyncPyautoguiActionHandler, AsyncScreenshotMaker
except ImportError:
    print("Error: oagi package not installed. Run: pip install oagi")
    sys.exit(1)


class TestStatus(Enum):
    """Status of a test case."""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class TestCase:
    """Definition of a single test case."""
    name: str
    description: str
    steps: List[str]
    expected_result: str
    category: str = "general"


@dataclass
class TestResult:
    """Result of a single test case execution."""
    test_name: str
    status: TestStatus
    duration: float
    error_message: Optional[str] = None
    screenshots: List[str] = field(default_factory=list)


@dataclass
class TestReport:
    """Complete test report."""
    total_tests: int
    passed: int
    failed: int
    skipped: int
    errors: int
    duration: float
    results: List[TestResult] = field(default_factory=list)
    timestamp: str = ""


# Define sidebar navigation test cases
SIDEBAR_BUTTONS = [
    "Library",
    "Playlists",
    "Favorites",
    "Downloads",
    "Settings",
    "About"
]


def generate_sidebar_tests() -> List[TestCase]:
    """Generate test cases for all sidebar buttons."""
    tests = []
    for button in SIDEBAR_BUTTONS:
        tests.append(TestCase(
            name=f"sidebar_{button.lower()}_navigation",
            description=f"Test navigation to {button} page via sidebar",
            steps=[
                f"Locate the '{button}' button in the left sidebar",
                f"Click the '{button}' button",
                f"Wait for the {button} page to load",
                f"Verify the {button} page content is displayed correctly",
                "Take a screenshot for verification"
            ],
            expected_result=f"The {button} page should load with appropriate content displayed",
            category="navigation"
        ))
    return tests


def generate_playback_tests() -> List[TestCase]:
    """Generate test cases for playback functionality."""
    return [
        TestCase(
            name="search_and_play",
            description="Search for a song and play it",
            steps=[
                "Click on the search bar at the top",
                "Type 'test song' in the search field",
                "Press Enter to search",
                "Wait for search results to load",
                "Click on the first result to play",
                "Verify the playback controls appear at the bottom",
                "Verify the progress bar is moving"
            ],
            expected_result="Song should start playing with visible playback controls",
            category="playback"
        ),
        TestCase(
            name="pause_resume",
            description="Test pause and resume functionality",
            steps=[
                "Ensure a song is currently playing",
                "Click the pause button in the playback controls",
                "Verify playback has stopped (progress bar not moving)",
                "Click the play button",
                "Verify playback has resumed"
            ],
            expected_result="Playback should pause and resume correctly",
            category="playback"
        ),
        TestCase(
            name="volume_control",
            description="Test volume slider functionality",
            steps=[
                "Locate the volume slider in the playback controls",
                "Drag the volume slider to 50%",
                "Verify the volume icon updates",
                "Drag the volume slider to 0% (mute)",
                "Verify the mute icon is displayed",
                "Drag the volume slider to 100%"
            ],
            expected_result="Volume should change visually and the icon should update",
            category="playback"
        ),
        TestCase(
            name="skip_next_previous",
            description="Test skip forward and backward controls",
            steps=[
                "Ensure there are multiple songs in the queue",
                "Note the current song name",
                "Click the 'Next' button",
                "Verify a different song is now playing",
                "Click the 'Previous' button",
                "Verify the original song resumes"
            ],
            expected_result="Skip controls should navigate between songs",
            category="playback"
        )
    ]


def generate_search_tests() -> List[TestCase]:
    """Generate test cases for search functionality."""
    return [
        TestCase(
            name="basic_search",
            description="Test basic search functionality",
            steps=[
                "Click on the search bar",
                "Type 'Beatles' in the search field",
                "Press Enter",
                "Wait for results to load",
                "Verify search results are displayed",
                "Verify results contain 'Beatles' related content"
            ],
            expected_result="Search results should appear with relevant content",
            category="search"
        ),
        TestCase(
            name="empty_search",
            description="Test behavior with empty search",
            steps=[
                "Click on the search bar",
                "Clear any existing text",
                "Press Enter with empty search field",
                "Observe the behavior"
            ],
            expected_result="App should handle empty search gracefully",
            category="search"
        ),
        TestCase(
            name="special_characters_search",
            description="Test search with special characters",
            steps=[
                "Click on the search bar",
                "Type 'test!@#$%' in the search field",
                "Press Enter",
                "Verify no crash or error occurs",
                "Observe the search results or empty state"
            ],
            expected_result="App should handle special characters without crashing",
            category="search"
        )
    ]


async def run_test(test: TestCase, verbose: bool = False) -> TestResult:
    """
    Execute a single test case using TaskerAgent.

    Args:
        test: TestCase to execute
        verbose: Enable verbose logging

    Returns:
        TestResult with execution details
    """
    start_time = datetime.now()

    tasker = TaskerAgent(
        max_steps=len(test.steps) + 5,  # Extra steps for verification
        model="lux-tasker-1",
        retry_on_failure=True,
        max_retries=2,
        timeout_per_step=15,
        verbose=verbose
    )

    try:
        result = await tasker.execute(
            steps=test.steps,
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker(),
        )

        duration = (datetime.now() - start_time).total_seconds()

        if result.success:
            return TestResult(
                test_name=test.name,
                status=TestStatus.PASSED,
                duration=duration
            )
        else:
            return TestResult(
                test_name=test.name,
                status=TestStatus.FAILED,
                duration=duration,
                error_message=str(result.errors) if hasattr(result, 'errors') else "Test steps failed"
            )

    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        return TestResult(
            test_name=test.name,
            status=TestStatus.ERROR,
            duration=duration,
            error_message=str(e)
        )


async def run_test_suite(tests: List[TestCase], verbose: bool = False) -> TestReport:
    """
    Run a suite of test cases.

    Args:
        tests: List of TestCase to execute
        verbose: Enable verbose logging

    Returns:
        TestReport with all results
    """
    start_time = datetime.now()
    results = []

    print(f"\nRunning {len(tests)} test(s)...\n")

    for i, test in enumerate(tests, 1):
        print(f"[{i}/{len(tests)}] {test.name}")
        print(f"        {test.description}")

        result = await run_test(test, verbose)
        results.append(result)

        status_symbol = {
            TestStatus.PASSED: "[PASS]",
            TestStatus.FAILED: "[FAIL]",
            TestStatus.SKIPPED: "[SKIP]",
            TestStatus.ERROR: "[ERROR]"
        }

        print(f"        {status_symbol[result.status]} ({result.duration:.2f}s)")
        if result.error_message:
            print(f"        Error: {result.error_message}")

        # Brief pause between tests
        if i < len(tests):
            await asyncio.sleep(1)

    total_duration = (datetime.now() - start_time).total_seconds()

    return TestReport(
        total_tests=len(tests),
        passed=sum(1 for r in results if r.status == TestStatus.PASSED),
        failed=sum(1 for r in results if r.status == TestStatus.FAILED),
        skipped=sum(1 for r in results if r.status == TestStatus.SKIPPED),
        errors=sum(1 for r in results if r.status == TestStatus.ERROR),
        duration=total_duration,
        results=results,
        timestamp=datetime.now().isoformat()
    )


def print_report(report: TestReport):
    """Print a formatted test report."""
    print("\n" + "=" * 60)
    print("TEST REPORT")
    print("=" * 60)
    print(f"\nTimestamp: {report.timestamp}")
    print(f"Duration: {report.duration:.2f} seconds")
    print(f"\nResults:")
    print(f"  Total:   {report.total_tests}")
    print(f"  Passed:  {report.passed}")
    print(f"  Failed:  {report.failed}")
    print(f"  Errors:  {report.errors}")
    print(f"  Skipped: {report.skipped}")

    pass_rate = (report.passed / report.total_tests * 100) if report.total_tests > 0 else 0
    print(f"\nPass Rate: {pass_rate:.1f}%")

    if report.failed > 0 or report.errors > 0:
        print("\nFailed/Error Tests:")
        for result in report.results:
            if result.status in (TestStatus.FAILED, TestStatus.ERROR):
                print(f"  - {result.test_name}: {result.error_message}")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Nuclear Player QA Testing using Lux TaskerAgent"
    )
    parser.add_argument("--verify-all-pages", action="store_true",
                        help="Test all sidebar navigation pages")
    parser.add_argument("--test-playback", action="store_true",
                        help="Test playback functionality")
    parser.add_argument("--test-search", action="store_true",
                        help="Test search functionality")
    parser.add_argument("--all", action="store_true",
                        help="Run all test suites")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")

    return parser.parse_args()


async def main():
    """Main entry point."""
    args = parse_args()

    # Collect tests based on arguments
    tests = []

    if args.all or args.verify_all_pages:
        tests.extend(generate_sidebar_tests())

    if args.all or args.test_playback:
        tests.extend(generate_playback_tests())

    if args.all or args.test_search:
        tests.extend(generate_search_tests())

    # Default to sidebar tests if nothing specified
    if not tests:
        print("No test suite specified. Running sidebar navigation tests by default.")
        tests = generate_sidebar_tests()

    print("=" * 60)
    print("Nuclear Player QA Testing - TaskerAgent Example")
    print("=" * 60)
    print(f"\nTest Categories:")

    categories = set(t.category for t in tests)
    for cat in sorted(categories):
        count = sum(1 for t in tests if t.category == cat)
        print(f"  - {cat}: {count} test(s)")

    # Verify Nuclear Player is running
    print("\nNote: Ensure Nuclear Player is running before starting tests.")
    print("      Download from: https://nuclear.js.org/")

    # Run test suite
    report = await run_test_suite(tests, verbose=args.verbose)

    # Print report
    print_report(report)

    # Return exit code based on results
    return 0 if report.failed == 0 and report.errors == 0 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
