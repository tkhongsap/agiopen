"""
QA Testing Demo

Demonstrates QA testing capabilities:
- Test execution
- UI validation
- Visual regression testing
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.qa_testing import TestRunner, TestCase, UIValidator
from src.qa_testing.test_runner import TestStep
from src.qa_testing.ui_validator import ValidationRule, ValidationType

load_dotenv()


async def demo_login_test():
    """Demonstrate login test execution."""
    print("\n" + "=" * 50)
    print("Demo: Login Test")
    print("=" * 50)

    runner = TestRunner(max_steps_per_test=30, model="lux-tasker-1")

    # Define a login test case
    login_test = TestCase(
        name="User Login Test",
        description="Verify that users can log in with valid credentials",
        steps=[
            TestStep(
                description="Navigate to login page",
                action="Go to the login page",
                expected_result="Login form is displayed"
            ),
            TestStep(
                description="Enter username",
                action="Enter 'testuser@example.com' in the email field",
                expected_result="Email is entered correctly"
            ),
            TestStep(
                description="Enter password",
                action="Enter 'password123' in the password field",
                expected_result="Password is masked and entered"
            ),
            TestStep(
                description="Click login button",
                action="Click the 'Sign In' button",
                expected_result="User is redirected to dashboard"
            ),
            TestStep(
                description="Verify login success",
                action="Check for welcome message or user profile icon",
                expected_result="Dashboard is displayed with user info"
            ),
        ],
        tags=["authentication", "smoke"]
    )

    print(f"\nRunning test: {login_test.name}")
    print(f"Steps: {len(login_test.steps)}")

    result = await runner.run_test(
        login_test,
        base_url="https://example.com/login"  # Replace with actual URL
    )

    print(f"\nResult: {'PASS' if result.success else 'FAIL'}")
    print(f"Steps passed: {result.steps_passed}/{result.steps_total}")
    print(f"Duration: {result.duration_seconds:.2f}s")
    if result.errors:
        print(f"Errors: {result.errors}")


async def demo_ui_validation():
    """Demonstrate UI validation capabilities."""
    print("\n" + "=" * 50)
    print("Demo: UI Validation")
    print("=" * 50)

    validator = UIValidator(max_steps=20, model="lux-actor-1")

    # Define validation rules
    rules = [
        ValidationRule(
            ValidationType.ELEMENT_EXISTS,
            "Login button"
        ),
        ValidationRule(
            ValidationType.ELEMENT_EXISTS,
            "Sign Up link"
        ),
        ValidationRule(
            ValidationType.TEXT_CONTAINS,
            "Page header",
            "Welcome"
        ),
        ValidationRule(
            ValidationType.ELEMENT_ENABLED,
            "Email input field"
        ),
    ]

    print("\nValidating the following rules:")
    for rule in rules:
        print(f"  - {rule.validation_type.value}: {rule.target}")
        if rule.expected_value:
            print(f"    Expected: {rule.expected_value}")

    results = await validator.validate(
        url="https://example.com",  # Replace with actual URL
        rules=rules
    )

    print("\nResults:")
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"  [{status}] {result.rule.validation_type.value}: {result.rule.target}")
        if result.error_message:
            print(f"        Error: {result.error_message}")


async def demo_test_suite():
    """Demonstrate running a test suite."""
    print("\n" + "=" * 50)
    print("Demo: Test Suite Execution")
    print("=" * 50)

    runner = TestRunner(max_steps_per_test=20, model="lux-actor-1")

    # Define multiple test cases
    tests = [
        TestCase(
            name="Homepage Load Test",
            description="Verify homepage loads correctly",
            steps=[
                TestStep("Navigate to homepage", "Go to the main website"),
                TestStep("Check page loaded", "Verify the logo is visible"),
            ],
            tags=["smoke"]
        ),
        TestCase(
            name="Navigation Test",
            description="Verify main navigation works",
            steps=[
                TestStep("Click Products link", "Click on 'Products' in navigation"),
                TestStep("Verify products page", "Check products listing is displayed"),
            ],
            tags=["navigation"]
        ),
        TestCase(
            name="Search Test",
            description="Verify search functionality",
            steps=[
                TestStep("Enter search term", "Type 'test' in search box"),
                TestStep("Submit search", "Press Enter or click search button"),
                TestStep("Verify results", "Check that search results appear"),
            ],
            tags=["search", "smoke"]
        ),
    ]

    print(f"\nRunning test suite with {len(tests)} tests...")

    results = await runner.run_suite(tests, stop_on_failure=False)

    # Generate report
    report = runner.generate_report(results, format="markdown")
    print("\n" + report)


async def demo_element_check():
    """Demonstrate quick element checking."""
    print("\n" + "=" * 50)
    print("Demo: Quick Element Check")
    print("=" * 50)

    validator = UIValidator(max_steps=10, model="lux-actor-1")

    url = "https://example.com"  # Replace with actual URL

    # Quick checks
    checks = [
        ("Login button", "Check if login button exists"),
        ("Navigation menu", "Check if navigation is visible"),
        ("Footer", "Check if footer is present"),
    ]

    print(f"\nChecking elements on: {url}")

    for element, description in checks:
        print(f"\n{description}...")
        result = await validator.check_element_exists(url, element)
        status = "Found" if result.passed else "Not found"
        print(f"  {element}: {status}")


async def main():
    """Run all QA testing demos."""
    print("=" * 60)
    print("   QA Testing Demonstration")
    print("   Using OpenAGI Lux Model")
    print("=" * 60)

    # Check for API key
    if not os.getenv("OAGI_API_KEY"):
        print("\nWarning: OAGI_API_KEY not set.")
        print("Set it with: export OAGI_API_KEY='your_key_here'")
        print("Get your key at: https://developer.agiopen.org\n")

    # Run demos
    await demo_login_test()
    await demo_ui_validation()
    await demo_test_suite()
    await demo_element_check()

    print("\n" + "=" * 60)
    print("All QA testing demos completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
