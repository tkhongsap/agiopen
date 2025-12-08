# Lux Use Cases Implementation Guide

This guide covers implementing the three main use cases: Web Automation, QA Testing, and Data Entry/Processing.

## Table of Contents

1. [Official Examples](#official-examples)
2. [Web Automation](#web-automation)
3. [QA Testing](#qa-testing)
4. [Data Entry/Processing](#data-entryprocessing)

---

## Official Examples

These examples are based on the official `oagi-lux-samples` repository patterns.

### CVS Appointment Booking (Official Pattern)

**Scenario:** Automate flu shot appointment scheduling on CVS.com using Tasker mode.

```python
from oagi import TaskerAgent
from dataclasses import dataclass

@dataclass
class AppointmentInfo:
    first_name: str
    last_name: str
    phone: str
    email: str
    birthdate: str  # Format: YYYY-MM-DD
    zip_code: str

async def book_cvs_appointment(info: AppointmentInfo):
    """
    Book a flu shot appointment at CVS.
    Based on official oagi-lux-samples/tasker_examples/cvs_appointment.py
    """
    tasker = TaskerAgent(
        max_steps=50,
        model="lux-tasker-1",
        retry_on_failure=True,
        max_retries=3
    )

    steps = [
        # Navigate to CVS immunizations page
        "Navigate to https://www.cvs.com/immunizations/flu",
        "Wait for page to fully load",

        # Start scheduling
        "Click 'Schedule an appointment' button",

        # Location selection
        f"Enter '{info.zip_code}' in the location/zip code search field",
        "Click 'Search' or press Enter",
        "Wait for locations to load",
        "Click on the first available CVS location",

        # Date/time selection
        "Select the earliest available date",
        "Select the first available time slot",
        "Click 'Continue' or 'Next'",

        # Personal information
        f"Enter '{info.first_name}' in the First Name field",
        f"Enter '{info.last_name}' in the Last Name field",
        f"Enter '{info.phone}' in the Phone Number field",
        f"Enter '{info.email}' in the Email field",
        f"Enter '{info.birthdate}' in the Date of Birth field",

        # Confirmation
        "Review the appointment details",
        "Check any required consent checkboxes",
        "Click 'Confirm Appointment' or 'Submit'"
    ]

    result = await tasker.execute(steps=steps)
    return result

# Usage
info = AppointmentInfo(
    first_name="John",
    last_name="Doe",
    phone="555-123-4567",
    email="john.doe@example.com",
    birthdate="1990-01-15",
    zip_code="10001"
)
result = await book_cvs_appointment(info)
```

### Amazon Product Search (Official Pattern)

**Scenario:** Search Amazon for products and extract data using Tasker mode.

```python
from oagi import TaskerAgent

async def search_amazon_products(
    product_query: str,
    sort_by: str = "best_sellers",
    max_products: int = 10
):
    """
    Search Amazon and extract product information.
    Based on official oagi-lux-samples/tasker_examples/amazon_search.py
    """
    tasker = TaskerAgent(
        max_steps=40,
        model="lux-tasker-1",
        retry_on_failure=True
    )

    sort_options = {
        "best_sellers": "Best Sellers",
        "price_low_high": "Price: Low to High",
        "price_high_low": "Price: High to Low",
        "avg_rating": "Avg. Customer Review",
        "newest": "Newest Arrivals"
    }

    sort_label = sort_options.get(sort_by, "Best Sellers")

    steps = [
        # Navigate to Amazon
        "Navigate to https://www.amazon.com",
        "Wait for page to fully load",

        # Search for product
        f"Click on the search box at the top of the page",
        f"Type '{product_query}'",
        "Press Enter or click the search button",
        "Wait for search results to load",

        # Sort results
        f"Click on the 'Sort by' dropdown",
        f"Select '{sort_label}' from the dropdown",
        "Wait for results to refresh",

        # Extract product data
        f"For the top {max_products} products visible on the page:",
        "  - Extract the product name/title",
        "  - Extract the price",
        "  - Extract the star rating",
        "  - Extract the number of reviews",
        "Format the extracted data as JSON",
        "Copy the JSON data to clipboard"
    ]

    result = await tasker.execute(steps=steps)
    return result

# Usage
result = await search_amazon_products(
    product_query="wireless noise cancelling headphones",
    sort_by="best_sellers",
    max_products=5
)
```

### Nuclear Player QA Testing (Official Pattern)

**Scenario:** Automated UI testing for the Nuclear Player desktop application.

```python
from oagi import TaskerAgent
from typing import List

async def test_nuclear_player_ui(
    sidebar_buttons: List[str] = None,
    screenshot_dir: str = "./qa_screenshots"
):
    """
    Run UI tests on Nuclear Player desktop application.
    Based on official oagi-lux-samples/tasker_examples/nuclear_player_qa.py

    Requires: Nuclear Player application to be installed and running.
    """
    if sidebar_buttons is None:
        sidebar_buttons = [
            "Dashboard",
            "Library",
            "Playlists",
            "Favorites",
            "Downloads",
            "Equalizer",
            "Settings",
            "About"
        ]

    tasker = TaskerAgent(
        max_steps=100,
        model="lux-tasker-1",
        retry_on_failure=True,
        max_retries=2
    )

    steps = [
        # Ensure Nuclear Player is in focus
        "Click on the Nuclear Player window to ensure it's in focus",
        "Wait for the application to be ready"
    ]

    # Generate test steps for each sidebar button
    for button in sidebar_buttons:
        steps.extend([
            f"Locate the '{button}' button in the sidebar",
            f"Click the '{button}' button",
            f"Wait for the {button} page to load completely",
            f"Verify that the {button} page is displayed correctly",
            f"Check for any error messages or loading issues",
            f"Take a screenshot and save as '{screenshot_dir}/{button.lower()}_page.png'"
        ])

    # Final verification
    steps.extend([
        "Return to the Dashboard/Home page",
        "Verify the application is still responsive",
        "Report any pages that failed to load correctly"
    ])

    result = await tasker.execute(steps=steps)
    return result

# Usage
result = await test_nuclear_player_ui(
    sidebar_buttons=["Library", "Playlists", "Settings"],
    screenshot_dir="./test_screenshots"
)
```

---

## Web Automation

### Overview

Web automation with Lux enables browser-based tasks like form filling, data scraping, and research workflows.

### Use Case 1: Form Filling

**Scenario:** Automatically fill out web forms with provided data.

```python
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

async def fill_contact_form(form_data: dict):
    """
    Fill a contact form with the provided data.

    Args:
        form_data: Dictionary with keys like 'name', 'email', 'message'
    """
    agent = AsyncDefaultAgent(max_steps=20)

    # Build instruction from form data
    instruction = f"""
    Fill out the contact form on the current page with:
    - Name: {form_data.get('name', '')}
    - Email: {form_data.get('email', '')}
    - Phone: {form_data.get('phone', '')}
    - Message: {form_data.get('message', '')}
    Then click the Submit button.
    """

    completed = await agent.execute(
        instruction,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

    return {
        "success": completed,
        "form_data": form_data
    }

# Usage
result = await fill_contact_form({
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "message": "Hello, I have a question about your services."
})
```

### Use Case 2: Data Scraping

**Scenario:** Extract structured data from web pages.

```python
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

async def scrape_product_data(url: str, fields: list):
    """
    Scrape product information from an e-commerce page.

    Args:
        url: The product page URL
        fields: List of fields to extract (e.g., ['name', 'price', 'description'])
    """
    agent = AsyncDefaultAgent(max_steps=30, model="lux-thinker-1")

    instruction = f"""
    1. Navigate to {url}
    2. Extract the following information:
       {', '.join(fields)}
    3. Copy the extracted data to clipboard in JSON format
    """

    completed = await agent.execute(
        instruction,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

    return completed

# Usage
await scrape_product_data(
    url="https://example.com/product/123",
    fields=["product_name", "price", "rating", "description"]
)
```

### Use Case 3: Web Research

**Scenario:** Conduct multi-step research across multiple websites.

```python
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

async def conduct_research(topic: str, sources: int = 3):
    """
    Research a topic across multiple sources and compile findings.

    Args:
        topic: The research topic
        sources: Number of sources to consult
    """
    # Use Thinker mode for complex, multi-step goals
    agent = AsyncDefaultAgent(max_steps=50, model="lux-thinker-1")

    instruction = f"""
    Research the following topic: "{topic}"

    Steps:
    1. Search Google for "{topic}"
    2. Visit {sources} different reputable sources
    3. For each source, extract key points
    4. Compile a summary of findings
    5. Save the summary to a text file on the desktop
    """

    completed = await agent.execute(
        instruction,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

    return completed

# Usage
await conduct_research("Latest developments in computer vision AI", sources=5)
```

---

## QA Testing

### Overview

QA testing with Lux enables automated UI testing, validation, and regression testing workflows.

### Use Case 1: UI Test Execution

**Scenario:** Run a sequence of UI tests with explicit steps.

```python
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

async def run_login_test(credentials: dict, expected_result: str):
    """
    Test the login functionality of a web application.

    Args:
        credentials: Dictionary with 'username' and 'password'
        expected_result: Expected outcome ('success' or 'error')
    """
    # Use Tasker mode for scripted sequences
    agent = AsyncDefaultAgent(max_steps=15, model="lux-tasker-1")

    test_steps = f"""
    Execute the following test steps:

    1. Navigate to the login page
    2. Enter username: {credentials['username']}
    3. Enter password: {credentials['password']}
    4. Click the Login button
    5. Verify the result matches expected: {expected_result}
    6. Take a screenshot of the result
    """

    completed = await agent.execute(
        test_steps,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

    return {
        "test_name": "login_test",
        "completed": completed,
        "expected": expected_result
    }

# Usage - Valid credentials
await run_login_test(
    credentials={"username": "testuser", "password": "validpass"},
    expected_result="success"
)

# Usage - Invalid credentials (negative test)
await run_login_test(
    credentials={"username": "testuser", "password": "wrongpass"},
    expected_result="error"
)
```

### Use Case 2: Visual Regression Testing

**Scenario:** Compare UI states before and after changes.

```python
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker
import hashlib

async def visual_regression_test(page_url: str, test_name: str):
    """
    Capture screenshots for visual regression comparison.

    Args:
        page_url: URL to test
        test_name: Name for the test case
    """
    agent = AsyncDefaultAgent(max_steps=10, model="lux-actor-1")
    screenshot_maker = AsyncScreenshotMaker()

    # Navigate and capture
    await agent.execute(
        f"Navigate to {page_url}",
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=screenshot_maker,
    )

    # Capture screenshot
    screenshot = await screenshot_maker.capture()

    # Save with test name
    screenshot_path = f"screenshots/{test_name}_current.png"
    screenshot.save(screenshot_path)

    return {
        "test_name": test_name,
        "screenshot_path": screenshot_path,
        "url": page_url
    }

# Usage
await visual_regression_test(
    page_url="https://myapp.com/dashboard",
    test_name="dashboard_layout"
)
```

### Use Case 3: End-to-End Workflow Testing

**Scenario:** Test a complete user workflow across multiple pages.

```python
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

async def test_checkout_workflow(product_id: str, user_data: dict):
    """
    Test the complete checkout workflow.

    Args:
        product_id: Product to purchase
        user_data: User information for checkout
    """
    # Use Thinker mode for complex workflows
    agent = AsyncDefaultAgent(max_steps=50, model="lux-thinker-1")

    workflow = f"""
    Test the complete checkout workflow:

    Phase 1 - Product Selection:
    1. Navigate to product page for ID: {product_id}
    2. Verify product is available
    3. Click "Add to Cart"
    4. Verify cart shows 1 item

    Phase 2 - Checkout:
    5. Click "Proceed to Checkout"
    6. Fill shipping address:
       - Name: {user_data['name']}
       - Address: {user_data['address']}
       - City: {user_data['city']}
    7. Click "Continue to Payment"

    Phase 3 - Payment (Test Mode):
    8. Select "Test Payment" option
    9. Enter test card number: 4111 1111 1111 1111
    10. Click "Place Order"

    Phase 4 - Verification:
    11. Verify order confirmation page appears
    12. Capture order number
    13. Take screenshot of confirmation
    """

    completed = await agent.execute(
        workflow,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

    return {
        "test_name": "checkout_workflow",
        "completed": completed,
        "product_id": product_id
    }

# Usage
await test_checkout_workflow(
    product_id="SKU-12345",
    user_data={
        "name": "Test User",
        "address": "123 Test Street",
        "city": "Test City"
    }
)
```

---

## Data Entry/Processing

### Overview

Data entry/processing with Lux enables bulk data input, extraction, and report generation.

### Use Case 1: Bulk Data Entry

**Scenario:** Enter multiple records into a system.

```python
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker
import asyncio

async def bulk_data_entry(records: list, form_url: str):
    """
    Enter multiple records into a form-based system.

    Args:
        records: List of dictionaries containing data to enter
        form_url: URL of the data entry form
    """
    agent = AsyncDefaultAgent(max_steps=30, model="lux-actor-1")
    results = []

    for i, record in enumerate(records):
        instruction = f"""
        Data Entry - Record {i + 1} of {len(records)}:

        1. Navigate to {form_url}
        2. Fill the form with:
           {format_record(record)}
        3. Click Save/Submit
        4. Wait for confirmation
        5. Click "Add New" to prepare for next record
        """

        completed = await agent.execute(
            instruction,
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker(),
        )

        results.append({
            "record_index": i,
            "success": completed,
            "data": record
        })

        # Brief pause between entries
        await asyncio.sleep(1)

    return {
        "total_records": len(records),
        "successful": sum(1 for r in results if r["success"]),
        "results": results
    }

def format_record(record: dict) -> str:
    """Format a record dictionary for the instruction."""
    return "\n".join(f"   - {k}: {v}" for k, v in record.items())

# Usage
records = [
    {"name": "John Doe", "email": "john@example.com", "department": "Sales"},
    {"name": "Jane Smith", "email": "jane@example.com", "department": "Marketing"},
    {"name": "Bob Wilson", "email": "bob@example.com", "department": "Engineering"},
]

result = await bulk_data_entry(records, "https://mycrm.com/contacts/new")
print(f"Entered {result['successful']} of {result['total_records']} records")
```

### Use Case 2: Data Extraction from Reports

**Scenario:** Extract data from dashboard or report pages.

```python
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

async def extract_dashboard_data(dashboard_url: str, metrics: list):
    """
    Extract specific metrics from a dashboard.

    Args:
        dashboard_url: URL of the dashboard
        metrics: List of metric names to extract
    """
    # Use Thinker mode for complex extraction
    agent = AsyncDefaultAgent(max_steps=40, model="lux-thinker-1")

    instruction = f"""
    Extract dashboard metrics:

    1. Navigate to {dashboard_url}
    2. Wait for dashboard to fully load
    3. For each of the following metrics, find and note the value:
       {chr(10).join(f'   - {m}' for m in metrics)}
    4. If any metric has a trend indicator (up/down), note that too
    5. Export the data:
       - Click Export button if available, OR
       - Select all relevant data and copy to clipboard
    6. Take a screenshot of the dashboard
    """

    completed = await agent.execute(
        instruction,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

    return {
        "dashboard_url": dashboard_url,
        "metrics_requested": metrics,
        "completed": completed
    }

# Usage
await extract_dashboard_data(
    dashboard_url="https://analytics.myapp.com/dashboard",
    metrics=[
        "Total Revenue",
        "Active Users",
        "Conversion Rate",
        "Average Order Value",
        "Customer Acquisition Cost"
    ]
)
```

### Use Case 3: Report Generation

**Scenario:** Generate reports from multiple data sources.

```python
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

async def generate_monthly_report(
    data_sources: list,
    report_template: str,
    output_path: str
):
    """
    Generate a monthly report by gathering data from multiple sources.

    Args:
        data_sources: List of URLs/applications to gather data from
        report_template: Path to report template
        output_path: Where to save the generated report
    """
    # Use Thinker mode for complex multi-step tasks
    agent = AsyncDefaultAgent(max_steps=100, model="lux-thinker-1")

    sources_instructions = "\n".join(
        f"   {i+1}. {source['name']}: {source['url']}"
        for i, source in enumerate(data_sources)
    )

    instruction = f"""
    Generate Monthly Report:

    Phase 1 - Data Collection:
    Gather data from the following sources:
{sources_instructions}

    For each source:
    - Navigate to the URL
    - Export or copy the relevant data
    - Save to a temporary location

    Phase 2 - Report Assembly:
    1. Open the report template: {report_template}
    2. Insert collected data into appropriate sections
    3. Update date range to current month
    4. Generate any charts/graphs from the data

    Phase 3 - Finalization:
    1. Review the report for completeness
    2. Save the report to: {output_path}
    3. Create a PDF version
    """

    completed = await agent.execute(
        instruction,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

    return {
        "completed": completed,
        "output_path": output_path,
        "sources_processed": len(data_sources)
    }

# Usage
await generate_monthly_report(
    data_sources=[
        {"name": "Sales Dashboard", "url": "https://sales.myapp.com"},
        {"name": "Marketing Analytics", "url": "https://marketing.myapp.com"},
        {"name": "Customer Support", "url": "https://support.myapp.com/metrics"},
    ],
    report_template="/templates/monthly_report.docx",
    output_path="/reports/2025/december_report.docx"
)
```

---

## Best Practices for All Use Cases

### 1. Choose the Right Mode

| Use Case | Recommended Mode | Reason |
|----------|------------------|--------|
| Simple clicks/form fills | Actor | Fast execution |
| Complex multi-step tasks | Thinker | Auto-decomposition |
| Scripted sequences | Tasker | Maximum control |

### 2. Handle Errors Gracefully

```python
async def safe_execute(agent, task, max_retries=3):
    """Execute a task with retry logic."""
    for attempt in range(max_retries):
        try:
            return await agent.execute(task, ...)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### 3. Log Execution Steps

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lux_automation")

# Agent with verbose logging
agent = AsyncDefaultAgent(max_steps=20, verbose=True)
```

### 4. Validate Results

```python
async def execute_with_validation(agent, task, validation_func):
    """Execute and validate the result."""
    result = await agent.execute(task, ...)

    if result and validation_func:
        is_valid = await validation_func()
        return {"completed": result, "validated": is_valid}

    return {"completed": result, "validated": None}
```
