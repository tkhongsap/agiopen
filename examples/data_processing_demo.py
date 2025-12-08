"""
Data Processing Demo

Demonstrates data processing capabilities:
- Bulk data entry
- Report generation
- Data extraction
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_processing import BulkDataEntry, ReportGenerator
from src.data_processing.bulk_entry import EntryRecord
from src.data_processing.report_generator import ReportConfig, DataSource, ReportFormat

load_dotenv()


async def demo_bulk_data_entry():
    """Demonstrate bulk data entry capabilities."""
    print("\n" + "=" * 50)
    print("Demo: Bulk Data Entry")
    print("=" * 50)

    entry = BulkDataEntry(
        max_steps_per_record=20,
        model="lux-actor-1",
        delay_between_records=1.0
    )

    # Sample records to enter
    records = [
        EntryRecord(data={
            "First Name": "John",
            "Last Name": "Doe",
            "Email": "john.doe@example.com",
            "Department": "Engineering",
            "Phone": "+1-555-0101"
        }),
        EntryRecord(data={
            "First Name": "Jane",
            "Last Name": "Smith",
            "Email": "jane.smith@example.com",
            "Department": "Marketing",
            "Phone": "+1-555-0102"
        }),
        EntryRecord(data={
            "First Name": "Bob",
            "Last Name": "Wilson",
            "Email": "bob.wilson@example.com",
            "Department": "Sales",
            "Phone": "+1-555-0103"
        }),
    ]

    print(f"\nEntering {len(records)} records...")
    for i, record in enumerate(records, 1):
        print(f"\nRecord {i}:")
        for field, value in record.data.items():
            print(f"  - {field}: {value}")

    result = await entry.enter_records(
        url="https://crm.example.com/contacts/new",  # Replace with actual URL
        records=records,
        submit_button_text="Save Contact",
        new_record_button_text="Add New Contact"
    )

    print(f"\nResult:")
    print(f"  Total records: {result.total_records}")
    print(f"  Successful: {result.successful}")
    print(f"  Failed: {result.failed}")
    if result.errors:
        print(f"  Errors: {result.errors}")


async def demo_report_generation():
    """Demonstrate report generation capabilities."""
    print("\n" + "=" * 50)
    print("Demo: Report Generation")
    print("=" * 50)

    generator = ReportGenerator(max_steps=100, model="lux-thinker-1")

    # Configure report
    config = ReportConfig(
        title="Monthly Business Report - December 2025",
        sources=[
            DataSource(
                name="Sales Dashboard",
                url="https://sales.example.com/dashboard",
                extraction_instructions="Extract total revenue, units sold, top 5 products, and month-over-month growth"
            ),
            DataSource(
                name="Marketing Analytics",
                url="https://marketing.example.com/analytics",
                extraction_instructions="Extract website traffic, conversion rate, top traffic sources, and campaign performance"
            ),
            DataSource(
                name="Customer Support Metrics",
                url="https://support.example.com/metrics",
                extraction_instructions="Extract total tickets, resolution time, customer satisfaction score, and common issues"
            ),
        ],
        output_format=ReportFormat.MARKDOWN,
        include_screenshots=True,
        date_range="December 1-31, 2025"
    )

    print(f"\nGenerating report: {config.title}")
    print(f"Data sources:")
    for source in config.sources:
        print(f"  - {source.name}: {source.url}")
    print(f"Output format: {config.output_format.value}")

    result = await generator.generate(
        config=config,
        output_path="reports/december_2025_report.md"
    )

    print(f"\nResult: {'Success' if result.success else 'Failed'}")
    print(f"Sources processed: {result.sources_processed}")
    if result.output_path:
        print(f"Output saved to: {result.output_path}")
    if result.errors:
        print(f"Errors: {result.errors}")


async def demo_dashboard_extraction():
    """Demonstrate dashboard metric extraction."""
    print("\n" + "=" * 50)
    print("Demo: Dashboard Metric Extraction")
    print("=" * 50)

    generator = ReportGenerator(max_steps=30, model="lux-actor-1")

    metrics = [
        "Total Revenue",
        "Active Users",
        "Conversion Rate",
        "Average Order Value",
        "Customer Acquisition Cost",
        "Net Promoter Score"
    ]

    print(f"\nExtracting metrics from dashboard:")
    for metric in metrics:
        print(f"  - {metric}")

    result = await generator.extract_dashboard_metrics(
        url="https://analytics.example.com/dashboard",  # Replace with actual URL
        metrics=metrics,
        output_format="json"
    )

    print(f"\nResult: {'Success' if result.get('success') else 'Failed'}")
    if result.get('metrics'):
        print("Extracted metrics:")
        for metric, value in result['metrics'].items():
            print(f"  - {metric}: {value}")


async def demo_csv_import():
    """Demonstrate importing data from CSV."""
    print("\n" + "=" * 50)
    print("Demo: CSV Data Import")
    print("=" * 50)

    entry = BulkDataEntry(max_steps_per_record=15, model="lux-actor-1")

    # Field mapping: CSV column -> Form field
    field_mapping = {
        "name": "Full Name",
        "email": "Email Address",
        "phone": "Phone Number",
        "company": "Company Name",
        "role": "Job Title"
    }

    print("\nField mapping (CSV -> Form):")
    for csv_col, form_field in field_mapping.items():
        print(f"  {csv_col} -> {form_field}")

    # Note: In a real scenario, you would have an actual CSV file
    print("\nNote: This demo requires a CSV file at 'data/contacts.csv'")
    print("Example CSV format:")
    print("  name,email,phone,company,role")
    print("  John Doe,john@example.com,+1-555-0101,Acme Inc,Manager")

    # Uncomment below to actually run:
    # result = await entry.enter_from_csv(
    #     url="https://crm.example.com/contacts/new",
    #     csv_path="data/contacts.csv",
    #     field_mapping=field_mapping
    # )
    # print(f"\nResult: {result.successful}/{result.total_records} records imported")


async def demo_record_update():
    """Demonstrate updating existing records."""
    print("\n" + "=" * 50)
    print("Demo: Record Update")
    print("=" * 50)

    entry = BulkDataEntry(max_steps_per_record=25, model="lux-thinker-1")

    # Records to update (with identifiers)
    records = [
        EntryRecord(
            identifier="john.doe@example.com",
            data={
                "Email": "john.doe@example.com",
                "Phone": "+1-555-9999",
                "Department": "Senior Engineering"
            }
        ),
        EntryRecord(
            identifier="jane.smith@example.com",
            data={
                "Email": "jane.smith@example.com",
                "Phone": "+1-555-8888",
                "Department": "Marketing Director"
            }
        ),
    ]

    print(f"\nUpdating {len(records)} records...")
    for record in records:
        print(f"\n  Identifier: {record.identifier}")
        for field, value in record.data.items():
            if field != "Email":  # Don't show the identifier twice
                print(f"    {field}: {value}")

    result = await entry.update_records(
        search_url="https://crm.example.com/contacts",  # Replace with actual URL
        records=records,
        search_field="Email",
        update_fields=["Phone", "Department"]
    )

    print(f"\nResult:")
    print(f"  Total: {result.total_records}")
    print(f"  Updated: {result.successful}")
    print(f"  Failed: {result.failed}")


async def main():
    """Run all data processing demos."""
    print("=" * 60)
    print("   Data Processing Demonstration")
    print("   Using OpenAGI Lux Model")
    print("=" * 60)

    # Check for API key
    if not os.getenv("OAGI_API_KEY"):
        print("\nWarning: OAGI_API_KEY not set.")
        print("Set it with: export OAGI_API_KEY='your_key_here'")
        print("Get your key at: https://developer.agiopen.org\n")

    # Run demos
    await demo_bulk_data_entry()
    await demo_report_generation()
    await demo_dashboard_extraction()
    await demo_csv_import()
    await demo_record_update()

    print("\n" + "=" * 60)
    print("All data processing demos completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
