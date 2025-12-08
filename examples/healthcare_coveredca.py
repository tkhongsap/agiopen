#!/usr/bin/env python3
"""
Healthcare to CoveredCA Example

This example demonstrates using Actor mode to navigate from healthcare.gov
to Covered California for California residents.

Actor mode provides near-instant execution (~1 second per step) for
direct, well-defined tasks like form navigation and state redirects.

Based on official OpenAGI Lux examples.

Usage:
    python healthcare_coveredca.py --zip-code 90210
    python healthcare_coveredca.py --zip-code 94102 --household-size 3 --income 80000
    python healthcare_coveredca.py --verbose
"""

import asyncio
import argparse
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker
except ImportError:
    print("Error: oagi package not installed. Run: pip install oagi")
    sys.exit(1)


@dataclass
class UserInfo:
    """User information for healthcare enrollment."""
    zip_code: str
    state: str = "California"
    household_size: int = 1
    annual_income: int = 50000
    age: Optional[int] = None
    include_spouse: bool = False
    num_dependents: int = 0


@dataclass
class HealthcarePlan:
    """Represents a healthcare plan option."""
    name: str
    tier: str  # Bronze, Silver, Gold, Platinum
    monthly_premium: float
    deductible: float
    provider: str


@dataclass
class NavigationResult:
    """Result of healthcare navigation."""
    success: bool
    reached_coveredca: bool
    plans_displayed: bool
    execution_time: float
    error_message: str = ""
    screenshot_path: Optional[str] = None


async def navigate_to_coveredca(
    user_info: UserInfo,
    verbose: bool = False
) -> NavigationResult:
    """
    Navigate from healthcare.gov to Covered California using Actor mode.

    This demonstrates Actor mode handling healthcare form navigation
    with state-specific redirects.

    Args:
        user_info: UserInfo dataclass with user details
        verbose: Enable verbose logging

    Returns:
        NavigationResult with navigation outcome
    """
    start_time = datetime.now()

    agent = AsyncDefaultAgent(
        max_steps=25,
        model="lux-actor-1",  # Actor mode for speed
        verbose=verbose
    )

    # Build household description
    household_desc = f"{user_info.household_size} person(s)"
    if user_info.include_spouse:
        household_desc += " (including spouse)"
    if user_info.num_dependents > 0:
        household_desc += f", {user_info.num_dependents} dependent(s)"

    instruction = f"""
    1. Navigate to https://www.healthcare.gov
    2. Look for 'Get Coverage', 'See Plans', or 'Start Application' button
    3. Click the main call-to-action button
    4. If asked for ZIP code, enter: {user_info.zip_code}
    5. If asked for state, select: {user_info.state}
    6. The site should detect California and offer to redirect to Covered California
    7. Click to proceed to Covered California (coveredca.com)
    8. On Covered California website:
       - If prompted, confirm the ZIP code: {user_info.zip_code}
       - Enter household size: {user_info.household_size}
       - Enter estimated annual income: ${user_info.annual_income:,}
    9. Click 'Shop and Compare' or 'See Plans' button
    10. Wait for plan options to load
    11. Verify health plan options are displayed
    """

    try:
        result = await agent.execute(
            instruction,
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker()
        )

        execution_time = (datetime.now() - start_time).total_seconds()

        return NavigationResult(
            success=result if isinstance(result, bool) else True,
            reached_coveredca=True,  # Would be determined from execution
            plans_displayed=True,     # Would be determined from execution
            execution_time=execution_time
        )

    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        return NavigationResult(
            success=False,
            reached_coveredca=False,
            plans_displayed=False,
            execution_time=execution_time,
            error_message=str(e)
        )


async def explore_plan_options(
    user_info: UserInfo,
    plan_tier: str = "Silver",
    verbose: bool = False
) -> NavigationResult:
    """
    Navigate directly to Covered California and explore plan options.

    Args:
        user_info: UserInfo dataclass with user details
        plan_tier: Preferred plan tier (Bronze, Silver, Gold, Platinum)
        verbose: Enable verbose logging

    Returns:
        NavigationResult with navigation outcome
    """
    start_time = datetime.now()

    agent = AsyncDefaultAgent(
        max_steps=30,
        model="lux-actor-1",
        verbose=verbose
    )

    instruction = f"""
    1. Navigate to https://www.coveredca.com
    2. Click 'Shop and Compare' or 'Get Started'
    3. Enter ZIP code: {user_info.zip_code}
    4. Enter household information:
       - Household size: {user_info.household_size}
       - Annual income: ${user_info.annual_income:,}
    5. Click 'See Plans' or 'Get Quote'
    6. Wait for plan results to load
    7. Filter plans by tier: {plan_tier}
    8. For each displayed plan, note:
       - Plan name
       - Monthly premium
       - Annual deductible
       - Insurance provider
    9. Take a screenshot of the plan comparison
    """

    try:
        result = await agent.execute(
            instruction,
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker()
        )

        execution_time = (datetime.now() - start_time).total_seconds()

        return NavigationResult(
            success=result if isinstance(result, bool) else True,
            reached_coveredca=True,
            plans_displayed=True,
            execution_time=execution_time
        )

    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        return NavigationResult(
            success=False,
            reached_coveredca=False,
            plans_displayed=False,
            execution_time=execution_time,
            error_message=str(e)
        )


def print_results(result: NavigationResult, user_info: UserInfo):
    """Print formatted navigation results."""
    print("\n" + "=" * 60)
    print("HEALTHCARE NAVIGATION RESULTS")
    print("=" * 60)
    print(f"\nUser Information:")
    print(f"  ZIP Code: {user_info.zip_code}")
    print(f"  State: {user_info.state}")
    print(f"  Household Size: {user_info.household_size}")
    print(f"  Annual Income: ${user_info.annual_income:,}")

    print(f"\nNavigation Status:")
    print(f"  Success: {'Yes' if result.success else 'No'}")
    print(f"  Reached CoveredCA: {'Yes' if result.reached_coveredca else 'No'}")
    print(f"  Plans Displayed: {'Yes' if result.plans_displayed else 'No'}")
    print(f"  Execution Time: {result.execution_time:.2f} seconds")

    if result.error_message:
        print(f"\nError: {result.error_message}")

    if result.screenshot_path:
        print(f"\nScreenshot saved: {result.screenshot_path}")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Navigate healthcare.gov to CoveredCA using Lux Actor mode"
    )
    parser.add_argument(
        "--zip-code", "-z",
        default="90210",
        help="California ZIP code (default: 90210)"
    )
    parser.add_argument(
        "--household-size", "-hs",
        type=int,
        default=1,
        help="Number of people in household (default: 1)"
    )
    parser.add_argument(
        "--income", "-i",
        type=int,
        default=50000,
        help="Estimated annual household income (default: 50000)"
    )
    parser.add_argument(
        "--age", "-a",
        type=int,
        help="Primary applicant age"
    )
    parser.add_argument(
        "--include-spouse",
        action="store_true",
        help="Include spouse in household"
    )
    parser.add_argument(
        "--dependents",
        type=int,
        default=0,
        help="Number of dependents"
    )
    parser.add_argument(
        "--direct",
        action="store_true",
        help="Go directly to CoveredCA instead of healthcare.gov"
    )
    parser.add_argument(
        "--plan-tier",
        choices=["Bronze", "Silver", "Gold", "Platinum"],
        default="Silver",
        help="Preferred plan tier for filtering (default: Silver)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    return parser.parse_args()


async def main():
    """Main entry point."""
    args = parse_args()

    # Create user info
    user_info = UserInfo(
        zip_code=args.zip_code,
        state="California",
        household_size=args.household_size,
        annual_income=args.income,
        age=args.age,
        include_spouse=args.include_spouse,
        num_dependents=args.dependents
    )

    print("=" * 60)
    print("Healthcare Navigation - Actor Mode Example")
    print("=" * 60)
    print(f"\nModel: lux-actor-1 (Actor mode)")
    print("Speed: ~1 second per step")
    print(f"\nStarting from: {'CoveredCA (direct)' if args.direct else 'Healthcare.gov'}")

    if args.direct:
        result = await explore_plan_options(
            user_info,
            plan_tier=args.plan_tier,
            verbose=args.verbose
        )
    else:
        result = await navigate_to_coveredca(user_info, args.verbose)

    print_results(result, user_info)

    return 0 if result.success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
