#!/usr/bin/env python3
"""
CVS Appointment Booking Example

This example demonstrates using the TaskerAgent framework to automate
flu shot appointment scheduling on CVS.com.

Based on the official oagi-lux-samples repository pattern.

Usage:
    python cvs_appointment_booking.py \
        --first-name "John" \
        --last-name "Doe" \
        --phone "555-123-4567" \
        --email "john.doe@example.com" \
        --birthdate "1990-01-15" \
        --zip-code "10001"
"""

import asyncio
import argparse
from dataclasses import dataclass
from typing import Optional
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


@dataclass
class AppointmentInfo:
    """Personal information for CVS appointment booking."""
    first_name: str
    last_name: str
    phone: str
    email: str
    birthdate: str  # Format: YYYY-MM-DD
    zip_code: str
    preferred_date: Optional[str] = None  # Format: YYYY-MM-DD
    preferred_time: Optional[str] = None  # e.g., "morning", "afternoon", "evening"


async def book_cvs_appointment(info: AppointmentInfo, verbose: bool = False) -> dict:
    """
    Book a flu shot appointment on CVS.com using TaskerAgent.

    Args:
        info: AppointmentInfo dataclass with personal details
        verbose: Enable verbose logging

    Returns:
        dict with booking result status and details
    """
    # Initialize TaskerAgent with configuration
    tasker = TaskerAgent(
        max_steps=50,
        model="lux-tasker-1",
        retry_on_failure=True,
        max_retries=3,
        timeout_per_step=30,
        verbose=verbose
    )

    # Define the step-by-step task sequence
    steps = [
        # Navigation
        "Navigate to https://www.cvs.com/immunizations/flu",
        "Wait for the page to fully load",
        "Click on 'Schedule an appointment' button",

        # Location search
        f"Enter zip code '{info.zip_code}' in the location search field",
        "Click the 'Search' or 'Find' button",
        "Wait for location results to load",

        # Select location
        "Click on the first available CVS location from the results",
        "Verify the location details are displayed",

        # Date/time selection
        "Click on 'Select a date' or similar date picker",
        f"Select the {'earliest available' if not info.preferred_date else info.preferred_date} date",
        f"Select {'any available' if not info.preferred_time else info.preferred_time} time slot",
        "Click 'Continue' or 'Next' to proceed",

        # Personal information
        f"Enter '{info.first_name}' in the First Name field",
        f"Enter '{info.last_name}' in the Last Name field",
        f"Enter '{info.phone}' in the Phone Number field",
        f"Enter '{info.email}' in the Email field",
        f"Enter '{info.birthdate}' in the Date of Birth field",

        # Review and confirm
        "Review the appointment details",
        "Check any required consent checkboxes",
        "Click 'Schedule Appointment' or 'Confirm' button",

        # Verification
        "Wait for confirmation page to load",
        "Verify appointment confirmation message is displayed",
    ]

    # Execute the task sequence
    result = await tasker.execute(
        steps=steps,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

    return {
        "success": result.success,
        "steps_completed": result.steps_completed,
        "total_steps": len(steps),
        "execution_time": result.execution_time,
        "final_state": result.final_state,
        "errors": result.errors if hasattr(result, 'errors') else []
    }


async def book_with_retry(info: AppointmentInfo, max_attempts: int = 3) -> dict:
    """
    Attempt to book appointment with retry logic.

    Args:
        info: AppointmentInfo dataclass with personal details
        max_attempts: Maximum number of booking attempts

    Returns:
        dict with final booking result
    """
    for attempt in range(1, max_attempts + 1):
        print(f"\nAttempt {attempt}/{max_attempts}...")

        try:
            result = await book_cvs_appointment(info, verbose=True)

            if result["success"]:
                print(f"Booking successful on attempt {attempt}!")
                return result
            else:
                print(f"Attempt {attempt} failed: {result.get('errors', 'Unknown error')}")

        except Exception as e:
            print(f"Attempt {attempt} raised exception: {e}")

        if attempt < max_attempts:
            print("Waiting before retry...")
            await asyncio.sleep(5)

    return {
        "success": False,
        "message": f"Failed after {max_attempts} attempts",
        "errors": ["Max retry attempts exceeded"]
    }


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Book a CVS flu shot appointment using Lux TaskerAgent"
    )
    parser.add_argument("--first-name", required=True, help="First name")
    parser.add_argument("--last-name", required=True, help="Last name")
    parser.add_argument("--phone", required=True, help="Phone number")
    parser.add_argument("--email", required=True, help="Email address")
    parser.add_argument("--birthdate", required=True, help="Birth date (YYYY-MM-DD)")
    parser.add_argument("--zip-code", required=True, help="ZIP code for location search")
    parser.add_argument("--preferred-date", help="Preferred date (YYYY-MM-DD)")
    parser.add_argument("--preferred-time", choices=["morning", "afternoon", "evening"],
                        help="Preferred time of day")
    parser.add_argument("--max-attempts", type=int, default=3, help="Max retry attempts")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    return parser.parse_args()


async def main():
    """Main entry point."""
    args = parse_args()

    # Create appointment info from arguments
    info = AppointmentInfo(
        first_name=args.first_name,
        last_name=args.last_name,
        phone=args.phone,
        email=args.email,
        birthdate=args.birthdate,
        zip_code=args.zip_code,
        preferred_date=args.preferred_date,
        preferred_time=args.preferred_time
    )

    print("=" * 60)
    print("CVS Appointment Booking - TaskerAgent Example")
    print("=" * 60)
    print(f"\nBooking for: {info.first_name} {info.last_name}")
    print(f"Location: {info.zip_code}")
    print(f"Contact: {info.phone} / {info.email}")
    print("")

    # Execute booking with retry
    result = await book_with_retry(info, max_attempts=args.max_attempts)

    # Print results
    print("\n" + "=" * 60)
    print("BOOKING RESULT")
    print("=" * 60)
    print(f"Success: {result['success']}")
    if result.get('steps_completed'):
        print(f"Steps: {result['steps_completed']}/{result.get('total_steps', 'N/A')}")
    if result.get('execution_time'):
        print(f"Time: {result['execution_time']:.2f} seconds")
    if result.get('errors'):
        print(f"Errors: {result['errors']}")

    return 0 if result['success'] else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
