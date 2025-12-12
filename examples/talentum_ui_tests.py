#!/usr/bin/env python3
"""
TalentMatch AI - UI Testing with OAGI TaskerAgent

This example demonstrates using the TaskerAgent framework to automate
UI testing of the TalentMatch AI web application.

Based on the official oagi-lux-samples repository pattern.

Application URL: https://talentum.tkhongsap.io/

Usage:
    python talentum_ui_tests.py --test-navigation
    python talentum_ui_tests.py --test-search
    python talentum_ui_tests.py --test-shortlists
    python talentum_ui_tests.py --test-summaries
    python talentum_ui_tests.py --test-history
    python talentum_ui_tests.py --test-admin
    python talentum_ui_tests.py --all
"""

import asyncio
import argparse
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum
import sys
import os
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file in project root
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path)

try:
    from oagi import AsyncDefaultAgent
    from oagi import AsyncPyautoguiActionHandler, AsyncScreenshotMaker
except ImportError:
    print("Error: oagi package not installed. Run: pip install oagi")
    sys.exit(1)


# =============================================================================
# CONFIGURATION
# =============================================================================

APP_URL = "https://talentum.tkhongsap.io/"
PAGES = {
    "search": APP_URL,
    "shortlists": f"{APP_URL}shortlists",
    "summaries": f"{APP_URL}summaries",
    "history": f"{APP_URL}history",
    "admin": f"{APP_URL}admin",
}


# =============================================================================
# DATA STRUCTURES
# =============================================================================

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
    steps_completed: int = 0
    total_steps: int = 0
    error_message: Optional[str] = None


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


# =============================================================================
# TEST CASE DEFINITIONS
# =============================================================================

def generate_navigation_tests() -> List[TestCase]:
    """Generate test cases for sidebar navigation."""
    return [
        TestCase(
            name="navigation_all_pages",
            description="Test navigation to all main pages via sidebar",
            steps=[
                f"Navigate to {APP_URL}",
                "Wait for the page to fully load",
                "Verify the TalentMatch logo is visible in the sidebar",
                "Click on the 'Search' link in the sidebar navigation",
                "Verify the search page loads with 'Find Your Perfect Candidates' heading",
                "Click on the 'Shortlists' link in the sidebar navigation",
                "Verify the URL changes to /shortlists and 'My Shortlists' heading appears",
                "Click on the 'Summaries' link in the sidebar navigation",
                "Verify the URL changes to /summaries and 'Candidate Summaries' heading appears",
                "Click on the 'History' link in the sidebar navigation",
                "Verify the URL changes to /history and 'Search History' heading appears",
                "Click on the 'Admin' link in the sidebar navigation",
                "Verify the URL changes to /admin and 'Admin Settings' heading appears",
                "Click back on 'Search' to return to the home page",
            ],
            expected_result="All navigation links work and load correct pages",
            category="navigation"
        ),
        TestCase(
            name="sidebar_toggle",
            description="Test sidebar collapse/expand functionality",
            steps=[
                f"Navigate to {APP_URL}",
                "Wait for the page to fully load",
                "Locate the Toggle Sidebar button (hamburger icon) in the header",
                "Click the Toggle Sidebar button",
                "Verify the sidebar collapses (becomes narrower or icons only)",
                "Click the Toggle Sidebar button again",
                "Verify the sidebar expands back to full width",
            ],
            expected_result="Sidebar toggles between collapsed and expanded states",
            category="navigation"
        ),
        TestCase(
            name="header_elements",
            description="Test header elements including language selector and theme toggle",
            steps=[
                f"Navigate to {APP_URL}",
                "Wait for the page to fully load",
                "Verify the language selector showing 'US English' is visible in the header",
                "Click on the language selector dropdown",
                "Verify dropdown opens with language options",
                "Click elsewhere to close the dropdown",
                "Look for a theme toggle button (sun/moon icon) in the header",
                "Verify the user profile section is visible at the bottom of sidebar",
            ],
            expected_result="Header elements are functional and accessible",
            category="navigation"
        ),
    ]


def generate_search_tests() -> List[TestCase]:
    """Generate test cases for search functionality."""
    return [
        TestCase(
            name="search_basic",
            description="Test basic search functionality",
            steps=[
                f"Navigate to {APP_URL}",
                "Wait for the search page to fully load",
                "Verify the search input field with placeholder 'Search for candidates' is visible",
                "Click on the search input field",
                "Type 'Python developer in Bangkok' in the search field",
                "Click the 'Search' button",
                "Wait for search results to load",
                "Verify search results appear showing candidate cards or a results list",
            ],
            expected_result="Search returns relevant candidate results",
            category="search"
        ),
        TestCase(
            name="search_filters_experience",
            description="Test experience filter slider",
            steps=[
                f"Navigate to {APP_URL}",
                "Wait for the page to fully load",
                "Locate the 'Experience (years)' filter section on the left sidebar",
                "Verify the experience slider is visible with range 0-20+ years",
                "Drag the minimum slider handle to approximately 2 years",
                "Drag the maximum slider handle to approximately 10 years",
                "Verify the slider values update",
            ],
            expected_result="Experience slider filter can be adjusted",
            category="search"
        ),
        TestCase(
            name="search_filters_location",
            description="Test location filter checkboxes",
            steps=[
                f"Navigate to {APP_URL}",
                "Wait for the page to fully load",
                "Locate the 'Location' filter section",
                "Click the 'Bangkok' checkbox to select it",
                "Verify the Bangkok checkbox is now checked",
                "Click the 'Tokyo' checkbox to select it",
                "Verify both Bangkok and Tokyo checkboxes are checked",
                "Click the 'Bangkok' checkbox again to deselect it",
                "Verify only Tokyo checkbox remains checked",
            ],
            expected_result="Location checkboxes can be selected and deselected",
            category="search"
        ),
        TestCase(
            name="search_filters_skills",
            description="Test skills filter selection",
            steps=[
                f"Navigate to {APP_URL}",
                "Wait for the page to fully load",
                "Locate the 'Skills' filter section",
                "Click on the 'Python' skill tag to select it",
                "Verify Python skill tag is highlighted or selected",
                "Click on the 'JavaScript' skill tag to add another skill",
                "Find the 'Add custom skill...' input field",
                "Click on the custom skill input",
                "Type 'TensorFlow' and press Enter",
                "Verify TensorFlow appears as a selected skill",
            ],
            expected_result="Skills can be selected and custom skills can be added",
            category="search"
        ),
        TestCase(
            name="search_options",
            description="Test search options dropdowns",
            steps=[
                f"Navigate to {APP_URL}",
                "Wait for the page to fully load",
                "Find the 'Scoring Profile' dropdown showing 'Balanced'",
                "Click on the Scoring Profile dropdown",
                "Verify dropdown opens with scoring options",
                "Select a different option if available",
                "Find the 'Results' dropdown showing '10'",
                "Click on the Results dropdown",
                "Verify dropdown opens with result count options",
                "Select '20' from the dropdown",
            ],
            expected_result="Search option dropdowns work correctly",
            category="search"
        ),
        TestCase(
            name="upload_jd",
            description="Test Upload JD button functionality",
            steps=[
                f"Navigate to {APP_URL}",
                "Wait for the page to fully load",
                "Find the 'Upload JD' button in the search area",
                "Click the 'Upload JD' button",
                "Verify a file upload modal or dialog appears",
                "Close the upload modal by clicking the close button or pressing Escape",
                "Verify the modal is closed and search page is visible",
            ],
            expected_result="Upload JD button opens file upload interface",
            category="search"
        ),
    ]


def generate_shortlists_tests() -> List[TestCase]:
    """Generate test cases for shortlists page."""
    return [
        TestCase(
            name="shortlists_page",
            description="Test shortlists page elements and functionality",
            steps=[
                f"Navigate to {PAGES['shortlists']}",
                "Wait for the page to fully load",
                "Verify the 'My Shortlists' heading is displayed",
                "Verify the subtitle 'Organize and manage your candidate shortlists' is visible",
                "Find the '+ Create Shortlist' button",
                "Click the '+ Create Shortlist' button",
                "Verify a create shortlist modal or form appears",
                "Close the modal by clicking close button or pressing Escape",
                "Look for existing shortlist cards on the page",
                "If a shortlist card exists, verify it shows the shortlist name",
                "Verify the shortlist card shows candidate count",
                "Verify candidate avatar icons are displayed on the card",
                "Verify the shortlist card shows a date",
            ],
            expected_result="Shortlists page displays correctly with management options",
            category="shortlists"
        ),
        TestCase(
            name="shortlist_interaction",
            description="Test interaction with shortlist cards",
            steps=[
                f"Navigate to {PAGES['shortlists']}",
                "Wait for the page to fully load",
                "If there is an existing shortlist card, click on it",
                "Verify the shortlist expands or shows more details",
                "Look for candidate information within the expanded view",
                "Click elsewhere or on a collapse button to close the expanded view",
            ],
            expected_result="Shortlist cards are interactive and show details",
            category="shortlists"
        ),
    ]


def generate_summaries_tests() -> List[TestCase]:
    """Generate test cases for summaries page."""
    return [
        TestCase(
            name="summaries_page",
            description="Test summaries page table and functionality",
            steps=[
                f"Navigate to {PAGES['summaries']}",
                "Wait for the page to fully load",
                "Verify the 'Candidate Summaries' heading is displayed",
                "Verify the subtitle 'Manage post-interview candidate briefs' is visible",
                "Find the search input with placeholder 'Search by candidate name...'",
                "Verify the 'All Summaries' filter button is visible",
                "Verify the table has columns: Candidate, Role, English, Expected Salary, Updated",
                "If there are rows in the table, verify data is displayed correctly",
            ],
            expected_result="Summaries page displays table with correct columns",
            category="summaries"
        ),
        TestCase(
            name="summaries_interaction",
            description="Test summaries table interactions",
            steps=[
                f"Navigate to {PAGES['summaries']}",
                "Wait for the page to fully load",
                "Click on the search input field",
                "Type 'test' in the search field",
                "Verify the table filters or shows matching results",
                "Clear the search field",
                "Click on the 'All Summaries' filter button",
                "Verify filter options appear",
                "If there's a table row with a 3-dot menu, click on it",
                "Verify a context menu appears with options",
            ],
            expected_result="Summaries table search and filters work correctly",
            category="summaries"
        ),
    ]


def generate_history_tests() -> List[TestCase]:
    """Generate test cases for history page."""
    return [
        TestCase(
            name="history_page",
            description="Test history page display and functionality",
            steps=[
                f"Navigate to {PAGES['history']}",
                "Wait for the page to fully load",
                "Verify the 'Search History' heading is displayed",
                "Verify the subtitle 'View and reuse your previous searches' is visible",
                "Look for history items in a list format",
                "If history items exist, verify each shows the search query text",
                "Verify history items show the source type (e.g., 'JD Upload')",
                "Verify history items show results count (e.g., '10 results')",
                "Verify history items show date and time",
            ],
            expected_result="History page displays previous searches correctly",
            category="history"
        ),
        TestCase(
            name="history_reuse",
            description="Test reusing a search from history",
            steps=[
                f"Navigate to {PAGES['history']}",
                "Wait for the page to fully load",
                "If there are history items, click on the first one",
                "Verify the search is reused or details are shown",
                "Check if you're redirected to search page with the query populated",
            ],
            expected_result="History items can be clicked to reuse searches",
            category="history"
        ),
    ]


def generate_admin_tests() -> List[TestCase]:
    """Generate test cases for admin page."""
    return [
        TestCase(
            name="admin_page",
            description="Test admin settings page display",
            steps=[
                f"Navigate to {PAGES['admin']}",
                "Wait for the page to fully load",
                "Verify the 'Admin Settings' heading is displayed",
                "Verify the subtitle 'Manage system settings and data operations' is visible",
                "Find the 'AI Embeddings' section",
                "Verify the description about vector embeddings is visible",
                "Verify the 'Total Resumes' stat is displayed with a number",
                "Verify the 'With Embeddings' stat is displayed",
                "Verify the 'Without Embeddings' stat is displayed",
                "Verify the 'Coverage' percentage is displayed",
                "Verify the coverage progress bar is visible",
                "Find the 'Regenerate Embeddings' button",
                "Verify the button is visible and appears clickable",
            ],
            expected_result="Admin page displays all settings and stats correctly",
            category="admin"
        ),
    ]


# =============================================================================
# TEST EXECUTION
# =============================================================================

async def run_test(test: TestCase, verbose: bool = False) -> TestResult:
    """
    Execute a single test case using AsyncDefaultAgent.

    Args:
        test: TestCase to execute
        verbose: Enable verbose logging

    Returns:
        TestResult with execution details
    """
    start_time = datetime.now()

    # Build instruction from test steps
    instruction = build_instruction(test)

    # Use AsyncDefaultAgent for task execution
    agent = AsyncDefaultAgent(
        max_steps=len(test.steps) + 10,  # Extra steps for verification
        model="lux-actor-1",
    )

    try:
        # Execute the test instruction
        completed = await agent.execute(
            instruction,
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker(),
        )

        duration = (datetime.now() - start_time).total_seconds()

        if completed:
            return TestResult(
                test_name=test.name,
                status=TestStatus.PASSED,
                duration=duration,
                steps_completed=len(test.steps),
                total_steps=len(test.steps)
            )
        else:
            return TestResult(
                test_name=test.name,
                status=TestStatus.FAILED,
                duration=duration,
                steps_completed=0,
                total_steps=len(test.steps),
                error_message="Test did not complete successfully"
            )

    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        return TestResult(
            test_name=test.name,
            status=TestStatus.ERROR,
            duration=duration,
            steps_completed=0,
            total_steps=len(test.steps),
            error_message=str(e)
        )


def build_instruction(test: TestCase) -> str:
    """
    Build a natural language instruction from test case steps.

    Args:
        test: TestCase with steps to convert

    Returns:
        Single instruction string for the agent
    """
    parts = [
        f"Test: {test.name}",
        f"Description: {test.description}",
        "",
        "Execute the following steps in order:",
    ]

    for i, step in enumerate(test.steps, 1):
        parts.append(f"{i}. {step}")

    parts.append("")
    parts.append(f"Expected result: {test.expected_result}")

    return "\n".join(parts)


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
    print("-" * 60)

    for i, test in enumerate(tests, 1):
        print(f"\n[{i}/{len(tests)}] {test.name}")
        print(f"         {test.description}")
        print(f"         Steps: {len(test.steps)}")

        result = await run_test(test, verbose)
        results.append(result)

        status_symbol = {
            TestStatus.PASSED: "✅ PASS",
            TestStatus.FAILED: "❌ FAIL",
            TestStatus.SKIPPED: "⏭️ SKIP",
            TestStatus.ERROR: "⚠️ ERROR"
        }

        print(f"         Result: {status_symbol[result.status]} ({result.duration:.2f}s)")
        if result.error_message:
            print(f"         Error: {result.error_message[:100]}...")

        # Brief pause between tests
        if i < len(tests):
            await asyncio.sleep(2)

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


# =============================================================================
# REPORT GENERATION
# =============================================================================

def print_report(report: TestReport):
    """Print a formatted test report."""
    print("\n")
    print("=" * 60)
    print("         TALENTMATCH AI - UI TEST REPORT")
    print("=" * 60)
    print(f"\nApplication: {APP_URL}")
    print(f"Timestamp: {report.timestamp}")
    print(f"Duration: {report.duration:.2f} seconds")

    print(f"\n📊 SUMMARY:")
    print(f"   Total Tests: {report.total_tests}")
    print(f"   ✅ Passed:   {report.passed}")
    print(f"   ❌ Failed:   {report.failed}")
    print(f"   ⚠️  Errors:   {report.errors}")
    print(f"   ⏭️  Skipped:  {report.skipped}")

    pass_rate = (report.passed / report.total_tests * 100) if report.total_tests > 0 else 0
    print(f"\n   Pass Rate: {pass_rate:.1f}%")

    # Group by category
    categories = {}
    for result in report.results:
        cat = result.test_name.split('_')[0]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(result)

    print(f"\n📋 RESULTS BY CATEGORY:")
    print("-" * 60)

    for cat, cat_results in categories.items():
        cat_passed = sum(1 for r in cat_results if r.status == TestStatus.PASSED)
        cat_total = len(cat_results)
        print(f"\n{cat.upper()}: {cat_passed}/{cat_total} passed")

        for result in cat_results:
            status_emoji = {
                TestStatus.PASSED: "✅",
                TestStatus.FAILED: "❌",
                TestStatus.ERROR: "⚠️",
                TestStatus.SKIPPED: "⏭️"
            }
            print(f"  {status_emoji[result.status]} {result.test_name} ({result.duration:.2f}s)")
            if result.error_message:
                print(f"     └─ {result.error_message[:80]}...")

    if report.failed > 0 or report.errors > 0:
        print(f"\n⚠️ FAILED/ERROR TESTS:")
        print("-" * 60)
        for result in report.results:
            if result.status in (TestStatus.FAILED, TestStatus.ERROR):
                print(f"  • {result.test_name}")
                print(f"    Steps: {result.steps_completed}/{result.total_steps}")
                if result.error_message:
                    print(f"    Error: {result.error_message}")

    print("\n" + "=" * 60)
    print("         END OF TEST REPORT")
    print("=" * 60)


# =============================================================================
# CLI INTERFACE
# =============================================================================

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="TalentMatch AI UI Testing using Lux TaskerAgent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python talentum_ui_tests.py --all
    python talentum_ui_tests.py --test-navigation
    python talentum_ui_tests.py --test-search --verbose
    python talentum_ui_tests.py --test-shortlists --test-summaries
        """
    )

    parser.add_argument("--test-navigation", action="store_true",
                        help="Run navigation tests (sidebar, header)")
    parser.add_argument("--test-search", action="store_true",
                        help="Run search functionality tests")
    parser.add_argument("--test-shortlists", action="store_true",
                        help="Run shortlists page tests")
    parser.add_argument("--test-summaries", action="store_true",
                        help="Run summaries page tests")
    parser.add_argument("--test-history", action="store_true",
                        help="Run history page tests")
    parser.add_argument("--test-admin", action="store_true",
                        help="Run admin page tests")
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

    if args.all or args.test_navigation:
        tests.extend(generate_navigation_tests())

    if args.all or args.test_search:
        tests.extend(generate_search_tests())

    if args.all or args.test_shortlists:
        tests.extend(generate_shortlists_tests())

    if args.all or args.test_summaries:
        tests.extend(generate_summaries_tests())

    if args.all or args.test_history:
        tests.extend(generate_history_tests())

    if args.all or args.test_admin:
        tests.extend(generate_admin_tests())

    # Default to navigation tests if nothing specified
    if not tests:
        print("No test suite specified. Running navigation tests by default.")
        print("Use --help to see available options.\n")
        tests = generate_navigation_tests()

    print("=" * 60)
    print("   TALENTMATCH AI - UI TESTING WITH OAGI TASKERAGENT")
    print("=" * 60)
    print(f"\nApplication: {APP_URL}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Show test categories
    categories = set(t.category for t in tests)
    print(f"\nTest Categories:")
    for cat in sorted(categories):
        count = sum(1 for t in tests if t.category == cat)
        print(f"  • {cat}: {count} test(s)")

    print(f"\nTotal: {len(tests)} test(s)")

    # Check API key
    api_key = os.getenv("OAGI_API_KEY")
    if not api_key:
        print("\n⚠️  Warning: OAGI_API_KEY not set in environment.")
        print("   Set it with: export OAGI_API_KEY='your_key_here'")
        print("   Or in PowerShell: $env:OAGI_API_KEY='your_key_here'")
        print("   Get your key at: https://developer.agiopen.org\n")

    # Run test suite
    report = await run_test_suite(tests, verbose=args.verbose)

    # Print report
    print_report(report)

    # Return exit code based on results
    return 0 if report.failed == 0 and report.errors == 0 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
