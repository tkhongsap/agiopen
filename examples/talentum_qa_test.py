"""
Talentum Web Application QA Testing

Comprehensive QA testing for https://talentum.tkhongsap.io/
Tests include:
- UI validation (element existence, clickability, text display)
- Navigation between pages
- Systematic functionality testing
"""

import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.qa_testing import TestRunner, TestCase, UIValidator
from src.qa_testing.test_runner import TestStep
from src.qa_testing.ui_validator import ValidationRule, ValidationType

load_dotenv()

# Configuration
APP_URL = "https://talentum.tkhongsap.io/"
TEST_RESULTS = []


def log_result(test_name: str, status: str, details: str = ""):
    """Log test result with timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    result = {
        "timestamp": timestamp,
        "test": test_name,
        "status": status,
        "details": details
    }
    TEST_RESULTS.append(result)
    status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"[{timestamp}] {status_emoji} {test_name}: {status}")
    if details:
        print(f"           Details: {details}")


async def test_ui_validation():
    """
    Test 1: UI Validation
    - Check if key elements exist
    - Verify elements are clickable
    - Validate correct text display
    """
    print("\n" + "=" * 60)
    print("TEST 1: UI VALIDATION")
    print("=" * 60)

    validator = UIValidator(max_steps=30, model="lux-actor-1")

    # Define UI validation rules for Talentum app
    ui_rules = [
        # Header/Navigation elements
        ValidationRule(
            ValidationType.ELEMENT_EXISTS,
            "Logo or brand name 'Talentum'"
        ),
        ValidationRule(
            ValidationType.ELEMENT_EXISTS,
            "Navigation menu or header"
        ),
        ValidationRule(
            ValidationType.ELEMENT_EXISTS,
            "User profile icon or menu (since logged in)"
        ),
        # Main content area
        ValidationRule(
            ValidationType.ELEMENT_EXISTS,
            "Main content area or dashboard"
        ),
        # Interactive elements
        ValidationRule(
            ValidationType.ELEMENT_ENABLED,
            "Any clickable button or link"
        ),
    ]

    print(f"\nValidating UI elements on: {APP_URL}")
    print("-" * 40)

    try:
        results = await validator.validate(
            url=APP_URL,
            rules=ui_rules
        )

        passed = 0
        failed = 0
        for result in results:
            if result.passed:
                passed += 1
                log_result(
                    f"UI: {result.rule.target}",
                    "PASS"
                )
            else:
                failed += 1
                log_result(
                    f"UI: {result.rule.target}",
                    "FAIL",
                    result.error_message or "Element not found or not as expected"
                )

        print(f"\nUI Validation Summary: {passed} passed, {failed} failed")

    except Exception as e:
        log_result("UI Validation", "ERROR", str(e))


async def test_navigation():
    """
    Test 2: Navigation Testing
    - Navigate between different pages/sections
    - Verify page transitions work correctly
    """
    print("\n" + "=" * 60)
    print("TEST 2: NAVIGATION TESTING")
    print("=" * 60)

    runner = TestRunner(max_steps_per_test=50, model="lux-actor-1", verbose=True)

    navigation_test = TestCase(
        name="Talentum Navigation Test",
        description="Test navigation between different pages and sections",
        steps=[
            TestStep(
                description="Verify homepage loaded",
                action=f"Look at the current page ({APP_URL}) and confirm it has loaded. Identify the main sections visible.",
                expected_result="Homepage is fully loaded with navigation elements visible"
            ),
            TestStep(
                description="Identify navigation menu items",
                action="Look for navigation menu items, sidebar links, or main menu options. List what navigation options are available.",
                expected_result="Navigation options are identified"
            ),
            TestStep(
                description="Click first navigation item",
                action="Click on the first available navigation link or menu item (could be Dashboard, Home, or any main menu item)",
                expected_result="Page navigates to the selected section"
            ),
            TestStep(
                description="Verify navigation succeeded",
                action="Confirm the page has changed or content has updated. Check for page title or heading changes.",
                expected_result="New page/section is displayed"
            ),
            TestStep(
                description="Navigate to another section",
                action="Click on a different navigation item to go to another section of the app",
                expected_result="Successfully navigated to another section"
            ),
            TestStep(
                description="Return to home/dashboard",
                action="Click on the logo, 'Home', or 'Dashboard' link to return to the main page",
                expected_result="Returned to the home page or dashboard"
            ),
        ],
        tags=["navigation", "core"]
    )

    print(f"\nRunning navigation test on: {APP_URL}")
    print("-" * 40)

    try:
        result = await runner.run_test(
            navigation_test,
            base_url=APP_URL
        )

        status = "PASS" if result.success else "FAIL"
        log_result(
            "Navigation Test",
            status,
            f"Steps passed: {result.steps_passed}/{result.steps_total}, Duration: {result.duration_seconds:.2f}s"
        )

        if result.errors:
            for error in result.errors:
                print(f"  ⚠️ Error: {error}")

    except Exception as e:
        log_result("Navigation Test", "ERROR", str(e))


async def test_systematic_functionality():
    """
    Test 3: Systematic Functionality Testing
    - Test core app features
    - Capture state at each step
    """
    print("\n" + "=" * 60)
    print("TEST 3: SYSTEMATIC FUNCTIONALITY TESTING")
    print("=" * 60)

    runner = TestRunner(
        max_steps_per_test=60,
        model="lux-actor-1",
        verbose=True,
        screenshot_on_failure=True
    )

    functionality_test = TestCase(
        name="Talentum Functionality Test",
        description="Systematically test core functionality of the Talentum application",
        steps=[
            # Step 1: App State Assessment
            TestStep(
                description="Assess current app state",
                action="Examine the current state of the Talentum app. Describe what you see - the main sections, any data displayed, user interface elements.",
                expected_result="Current app state is documented"
            ),
            # Step 2: Identify interactive elements
            TestStep(
                description="Identify interactive elements",
                action="Look for buttons, links, forms, dropdowns, or any interactive elements on the current page. List them.",
                expected_result="Interactive elements are identified"
            ),
            # Step 3: Test a button or action
            TestStep(
                description="Test a primary action button",
                action="Find and click a primary action button (like 'Add', 'Create', 'New', 'Submit', or similar). If a modal or form appears, note it.",
                expected_result="Button is clickable and responds appropriately"
            ),
            # Step 4: Check for forms
            TestStep(
                description="Test form interaction (if any)",
                action="If there's a form visible, click on an input field to test if it's focusable and accepts input. If no form, look for search or filter functionality.",
                expected_result="Form elements are interactive"
            ),
            # Step 5: Test any dropdown/select
            TestStep(
                description="Test dropdown or menu",
                action="Find any dropdown menu, select box, or expandable menu and click to open it. Verify it expands.",
                expected_result="Dropdown opens and shows options"
            ),
            # Step 6: Check responsive elements
            TestStep(
                description="Verify page responsiveness",
                action="Scroll down the page to see if there's more content. Check if the page scrolls smoothly and content loads properly.",
                expected_result="Page scrolls and content is accessible"
            ),
            # Step 7: Final state check
            TestStep(
                description="Final state verification",
                action="Navigate back to the main view/dashboard and confirm the app is in a stable state. Report any issues observed.",
                expected_result="App is in stable state"
            ),
        ],
        tags=["functionality", "core", "comprehensive"]
    )

    print(f"\nRunning functionality test on: {APP_URL}")
    print("-" * 40)

    try:
        result = await runner.run_test(
            functionality_test,
            base_url=APP_URL
        )

        status = "PASS" if result.success else "FAIL"
        log_result(
            "Functionality Test",
            status,
            f"Steps passed: {result.steps_passed}/{result.steps_total}, Duration: {result.duration_seconds:.2f}s"
        )

        if result.errors:
            for error in result.errors:
                print(f"  ⚠️ Error: {error}")

    except Exception as e:
        log_result("Functionality Test", "ERROR", str(e))


async def test_element_checks():
    """
    Test 4: Quick Element Checks
    - Verify specific elements exist and are functional
    """
    print("\n" + "=" * 60)
    print("TEST 4: ELEMENT EXISTENCE CHECKS")
    print("=" * 60)

    validator = UIValidator(max_steps=20, model="lux-actor-1")

    # Elements to check for
    elements_to_check = [
        ("Logo/Brand", "Company logo or 'Talentum' branding"),
        ("User Avatar", "User profile picture or avatar"),
        ("Main Menu", "Primary navigation menu"),
        ("Content Area", "Main content or dashboard area"),
        ("Footer", "Page footer if visible"),
    ]

    print(f"\nChecking elements on: {APP_URL}")
    print("-" * 40)

    for element_name, element_desc in elements_to_check:
        try:
            result = await validator.check_element_exists(APP_URL, element_desc)
            status = "PASS" if result.passed else "FAIL"
            log_result(f"Element: {element_name}", status)
        except Exception as e:
            log_result(f"Element: {element_name}", "ERROR", str(e))


def generate_final_report():
    """Generate a comprehensive test report."""
    print("\n")
    print("=" * 60)
    print("           QA TEST REPORT - TALENTUM")
    print("=" * 60)
    print(f"Application: {APP_URL}")
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    passed = sum(1 for r in TEST_RESULTS if r["status"] == "PASS")
    failed = sum(1 for r in TEST_RESULTS if r["status"] == "FAIL")
    errors = sum(1 for r in TEST_RESULTS if r["status"] == "ERROR")
    total = len(TEST_RESULTS)

    print(f"\n📊 SUMMARY:")
    print(f"   Total Tests: {total}")
    print(f"   ✅ Passed:   {passed}")
    print(f"   ❌ Failed:   {failed}")
    print(f"   ⚠️  Errors:   {errors}")
    print(f"   Pass Rate:  {(passed/total*100) if total > 0 else 0:.1f}%")

    print(f"\n📋 DETAILED RESULTS:")
    print("-" * 60)
    for result in TEST_RESULTS:
        status_emoji = "✅" if result["status"] == "PASS" else "❌" if result["status"] == "FAIL" else "⚠️"
        print(f"[{result['timestamp']}] {status_emoji} {result['test']}")
        if result["details"]:
            print(f"              └─ {result['details']}")

    print("\n" + "=" * 60)
    print("           END OF QA TEST REPORT")
    print("=" * 60)


async def main():
    """Run all QA tests for Talentum application."""
    print("=" * 60)
    print("   TALENTUM QA TESTING SUITE")
    print("   https://talentum.tkhongsap.io/")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check for API key
    if not os.getenv("OAGI_API_KEY"):
        print("\n⚠️  Warning: OAGI_API_KEY not set.")
        print("Set it with: $env:OAGI_API_KEY='your_key_here'")
        print("Get your key at: https://developer.agiopen.org\n")
        print("Continuing with tests anyway (may fail without API key)...\n")

    # Run all tests
    try:
        # Test 1: UI Validation
        await test_ui_validation()

        # Test 2: Navigation
        await test_navigation()

        # Test 3: Systematic Functionality
        await test_systematic_functionality()

        # Test 4: Element Checks
        await test_element_checks()

    except Exception as e:
        print(f"\n❌ Test suite encountered an error: {e}")

    # Generate final report
    generate_final_report()


if __name__ == "__main__":
    asyncio.run(main())
