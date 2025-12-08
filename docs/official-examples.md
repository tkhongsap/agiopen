# Official Lux Examples

This document contains the official examples from the OpenAGI Lux documentation and the [oagi-lux-samples](https://github.com/agiopen-org/oagi-lux-samples) repository.

## Table of Contents

1. [Examples Overview](#examples-overview)
2. [Tasker Mode Examples](#tasker-mode-examples)
   - [CVS Appointment Booking](#cvs-appointment-booking)
   - [Amazon Data Crawling](#amazon-data-crawling)
   - [Software QA Testing](#software-qa-testing)
3. [Actor Mode Examples](#actor-mode-examples)
   - [AAPL Insider Activity](#aapl-insider-activity)
   - [Healthcare to CoveredCA](#healthcare-to-coveredca)
   - [Nike Shopping](#nike-shopping)
4. [Setup Instructions](#setup-instructions)

---

## Examples Overview

Lux provides three operational modes, each suited for different automation scenarios:

| Mode | Speed | Best For | Examples |
|------|-------|----------|----------|
| **Actor** | ~1 sec/step | Quick, well-defined tasks | AAPL Insider, Nike Shopping, Healthcare |
| **Thinker** | Variable | Complex, multi-step goals | Research, Analysis |
| **Tasker** | Variable | Scripted workflows with retry | CVS Booking, Amazon Crawling, QA Testing |

### Key Components

All examples use these core components from the OAGI SDK:

```python
from oagi import (
    TaskerAgent,           # For Tasker mode workflows
    AsyncDefaultAgent,     # For Actor/Thinker mode
    AsyncPyautoguiActionHandler,  # Executes UI actions
    AsyncScreenshotMaker,  # Captures screenshots
    AsyncAgentObserver,    # Records execution history
)
```

---

## Tasker Mode Examples

Tasker mode executes step-by-step instructions with strict control and retry logic.

### CVS Appointment Booking

**Purpose:** Automate flu shot appointment scheduling on CVS.com.

**Source:** [oagi-lux-samples/tasker_examples/cvs_appointment_booking/](https://github.com/agiopen-org/oagi-lux-samples)

**Features:**
- Form filling automation
- Multi-step navigation
- Location-based search
- Personal information handling
- Retry on failure

#### Command Line Usage

```bash
python tasker_examples/cvs_appointment_booking/cvs_tasker.py \
    --first_name "John" \
    --last_name "Doe" \
    --email "john@example.com" \
    --birthday "01-15-1990" \
    --zip_code "10001"
```

#### Python Implementation

```python
import asyncio
from dataclasses import dataclass
from oagi import TaskerAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

@dataclass
class AppointmentInfo:
    first_name: str
    last_name: str
    email: str
    birthday: str  # Format: MM-DD-YYYY
    zip_code: str
    phone: str = ""

async def book_cvs_appointment(info: AppointmentInfo):
    """Book a CVS flu shot appointment using Tasker mode."""

    tasker = TaskerAgent(
        max_steps=50,
        model="lux-tasker-1",
        retry_on_failure=True,
        max_retries=3
    )

    # Define step-by-step workflow
    steps = [
        "Navigate to https://www.cvs.com/immunizations/flu",
        "Click on 'Schedule an appointment' button",
        f"Enter zip code '{info.zip_code}' in the location search",
        "Click Search button",
        "Select the first available CVS location",
        "Click on 'Select a time' or available date",
        "Choose the earliest available time slot",
        "Click Continue",
        f"Enter '{info.first_name}' in the First Name field",
        f"Enter '{info.last_name}' in the Last Name field",
        f"Enter '{info.email}' in the Email field",
        f"Enter '{info.birthday}' in the Date of Birth field",
        "Check required consent checkboxes",
        "Click 'Schedule Appointment' button",
        "Verify confirmation message is displayed"
    ]

    result = await tasker.execute(
        steps=steps,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker()
    )

    return result

# Usage
async def main():
    info = AppointmentInfo(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        birthday="01-15-1990",
        zip_code="10001"
    )
    result = await book_cvs_appointment(info)
    print(f"Booking {'successful' if result.success else 'failed'}")

asyncio.run(main())
```

---

### Amazon Data Crawling

**Purpose:** Web scraping workflow that searches Amazon, sorts by best sellers, and collects product information.

**Source:** [oagi-lux-samples/tasker_examples/amazon_scraping/](https://github.com/agiopen-org/oagi-lux-samples)

**Features:**
- Autonomous product search
- Sorting by various criteria (best sellers, price, rating)
- Data extraction from product listings
- Configurable via command-line arguments

#### Command Line Usage

```bash
python tasker_examples/amazon_scraping/amazon_scraping.py \
    --product_name "wireless headphones" \
    --experiment_name "headphones_test" \
    --output_dir "./results"
```

#### Python Implementation

```python
import asyncio
from dataclasses import dataclass
from typing import List, Optional
from oagi import TaskerAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

@dataclass
class ProductData:
    name: str
    price: str
    rating: Optional[str] = None
    review_count: Optional[str] = None
    is_prime: bool = False
    is_bestseller: bool = False

@dataclass
class SearchConfig:
    product_name: str
    max_results: int = 10
    sort_by: str = "best-sellers"  # relevance, price-low, price-high, best-sellers, rating

async def crawl_amazon_products(config: SearchConfig) -> List[ProductData]:
    """Crawl Amazon for product data using Tasker mode."""

    tasker = TaskerAgent(
        max_steps=30,
        model="lux-tasker-1",
        retry_on_failure=True,
        max_retries=2
    )

    steps = [
        "Navigate to https://www.amazon.com",
        f"Type '{config.product_name}' in the search box",
        "Click the search button",
        "Wait for results to load",
        f"Click on 'Sort by' dropdown and select '{config.sort_by}'",
        "Wait for sorted results to load",
        f"For the top {config.max_results} products, extract:",
        "  - Product title",
        "  - Price",
        "  - Star rating",
        "  - Number of reviews",
        "  - Prime badge (yes/no)",
        "  - Best Seller badge (yes/no)",
        "Copy extracted data to clipboard"
    ]

    result = await tasker.execute(
        steps=steps,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker()
    )

    # Parse results from clipboard/execution data
    products = []  # Would be populated from result data

    return products

# Usage
async def main():
    config = SearchConfig(
        product_name="wireless headphones",
        max_results=10,
        sort_by="best-sellers"
    )
    products = await crawl_amazon_products(config)

    for i, product in enumerate(products, 1):
        print(f"{i}. {product.name} - {product.price}")

asyncio.run(main())
```

---

### Software QA Testing

**Purpose:** Automate UI testing of the Nuclear Player desktop application.

**Source:** [oagi-lux-samples/tasker_examples/software_qa_with_nuclear/](https://github.com/agiopen-org/oagi-lux-samples)

**Features:**
- Desktop application testing (not browser-only)
- Clicks through all sidebar buttons
- Verifies each page loads correctly
- Execution logging and reporting

**Prerequisites:**
- Nuclear Player must be installed: https://nuclear.js.org/

#### Command Line Usage

```bash
python tasker_examples/software_qa_with_nuclear/software_qa.py
```

#### Python Implementation

```python
import asyncio
from dataclasses import dataclass
from typing import List
from enum import Enum
from oagi import TaskerAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

class TestStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class TestCase:
    name: str
    steps: List[str]
    expected_result: str

@dataclass
class TestResult:
    test_name: str
    status: TestStatus
    error_message: str = ""

# Define sidebar buttons to test
SIDEBAR_BUTTONS = [
    "Library",
    "Playlists",
    "Favorites",
    "Downloads",
    "Settings",
    "About"
]

async def run_nuclear_qa_tests() -> List[TestResult]:
    """Run QA tests on Nuclear Player using Tasker mode."""

    results = []

    for button in SIDEBAR_BUTTONS:
        tasker = TaskerAgent(
            max_steps=10,
            model="lux-tasker-1",
            retry_on_failure=True,
            max_retries=2
        )

        steps = [
            f"Click the '{button}' button in the left sidebar",
            f"Wait for the {button} page to load",
            f"Verify the {button} page content is displayed",
            "Take a screenshot for verification"
        ]

        result = await tasker.execute(
            steps=steps,
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker()
        )

        test_result = TestResult(
            test_name=f"Sidebar Navigation: {button}",
            status=TestStatus.PASSED if result.success else TestStatus.FAILED,
            error_message="" if result.success else str(result.errors)
        )
        results.append(test_result)

        print(f"[{'PASS' if result.success else 'FAIL'}] {button}")

    return results

# Usage
async def main():
    print("Nuclear Player QA Testing")
    print("=" * 40)

    results = await run_nuclear_qa_tests()

    passed = sum(1 for r in results if r.status == TestStatus.PASSED)
    failed = sum(1 for r in results if r.status == TestStatus.FAILED)

    print("=" * 40)
    print(f"Results: {passed} passed, {failed} failed")

asyncio.run(main())
```

---

## Actor Mode Examples

Actor mode provides fast execution (~1 second per step) for well-defined tasks.

### AAPL Insider Activity

**Purpose:** Navigate to NASDAQ's website and find Apple's insider activity data.

**Mode:** Actor (fast, direct tasks)

**Features:**
- Near-instant execution speed
- Financial data extraction
- Direct, well-defined navigation

#### CLI Usage

```bash
oagi agent run "Go to nasdaq.com, search for AAPL, and find insider activity data" \
    --model lux-actor-1
```

#### Python Implementation

```python
import asyncio
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

async def get_aapl_insider_activity():
    """
    Fetch AAPL insider activity from NASDAQ using Actor mode.

    This demonstrates how Actor mode handles direct, well-defined tasks
    with near-instant speed (~1 second per step).
    """

    agent = AsyncDefaultAgent(
        max_steps=15,
        model="lux-actor-1",  # Actor mode for speed
        verbose=True
    )

    instruction = """
    1. Navigate to https://www.nasdaq.com
    2. Search for 'AAPL' in the stock search
    3. Click on Apple Inc. (AAPL) from results
    4. Find and click on 'Insider Activity' tab
    5. Extract the recent insider trading data:
       - Insider name
       - Transaction type (Buy/Sell)
       - Shares traded
       - Transaction date
       - Share price
    6. Copy the data to clipboard
    """

    result = await agent.execute(
        instruction,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker()
    )

    return result

# Usage
async def main():
    print("Fetching AAPL Insider Activity from NASDAQ...")
    result = await get_aapl_insider_activity()
    print(f"Task {'completed' if result else 'failed'}")

asyncio.run(main())
```

---

### Healthcare to CoveredCA

**Purpose:** Navigate healthcare.gov and redirect to Covered California for California residents.

**Mode:** Actor (fast, direct tasks)

**Features:**
- Form filling automation
- State-based redirection handling
- Healthcare enrollment assistance

#### CLI Usage

```bash
oagi agent run "Go to healthcare.gov, enter California as the state, and navigate to CoveredCA" \
    --model lux-actor-1
```

#### Python Implementation

```python
import asyncio
from dataclasses import dataclass
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

@dataclass
class UserInfo:
    state: str
    zip_code: str
    household_size: int = 1
    annual_income: int = 50000

async def navigate_to_coveredca(user_info: UserInfo):
    """
    Navigate from healthcare.gov to Covered California using Actor mode.

    This demonstrates Actor mode handling healthcare form navigation
    with state-specific redirects.
    """

    agent = AsyncDefaultAgent(
        max_steps=20,
        model="lux-actor-1",
        verbose=True
    )

    instruction = f"""
    1. Navigate to https://www.healthcare.gov
    2. Click 'Get Coverage' or 'See Plans'
    3. Enter ZIP code: {user_info.zip_code}
    4. Select state: {user_info.state}
    5. If redirected to state marketplace (Covered California), follow the redirect
    6. On Covered California:
       - Enter household size: {user_info.household_size}
       - Enter estimated annual income: ${user_info.annual_income:,}
    7. Click 'See Plans' or 'Get Quote'
    8. Wait for plan options to load
    """

    result = await agent.execute(
        instruction,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker()
    )

    return result

# Usage
async def main():
    user = UserInfo(
        state="California",
        zip_code="90210",
        household_size=2,
        annual_income=75000
    )

    print("Navigating Healthcare.gov to CoveredCA...")
    result = await navigate_to_coveredca(user)
    print(f"Navigation {'completed' if result else 'failed'}")

asyncio.run(main())
```

---

### Nike Shopping

**Purpose:** Automate product browsing and cart operations on Nike.com.

**Mode:** Actor (fast, direct tasks)

**Features:**
- E-commerce navigation
- Product filtering
- Size selection
- Cart management

#### CLI Usage

```bash
oagi agent run "Go to nike.com, search for running shoes, filter by size 10, and add the first result to cart" \
    --model lux-actor-1
```

#### Python Implementation

```python
import asyncio
from dataclasses import dataclass
from typing import Optional
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

@dataclass
class ShoppingConfig:
    product_type: str
    size: str
    color: Optional[str] = None
    max_price: Optional[float] = None
    add_to_cart: bool = True

async def shop_nike(config: ShoppingConfig):
    """
    Browse and shop on Nike.com using Actor mode.

    This demonstrates Actor mode handling e-commerce workflows
    with product filtering and cart operations.
    """

    agent = AsyncDefaultAgent(
        max_steps=25,
        model="lux-actor-1",
        verbose=True
    )

    # Build filter instructions
    filters = []
    if config.size:
        filters.append(f"Filter by size: {config.size}")
    if config.color:
        filters.append(f"Filter by color: {config.color}")
    if config.max_price:
        filters.append(f"Filter by max price: ${config.max_price}")

    filter_text = "\n   - ".join(filters) if filters else "No filters"

    instruction = f"""
    1. Navigate to https://www.nike.com
    2. Search for '{config.product_type}'
    3. Wait for search results to load
    4. Apply filters:
       - {filter_text}
    5. Click on the first product in results
    6. Wait for product page to load
    7. Select size: {config.size}
    {'8. Click "Add to Bag" button' if config.add_to_cart else '8. Note the product details'}
    {'9. Verify item was added to cart' if config.add_to_cart else ''}
    """

    result = await agent.execute(
        instruction,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker()
    )

    return result

# Usage
async def main():
    config = ShoppingConfig(
        product_type="running shoes",
        size="10",
        color="black",
        max_price=150.00,
        add_to_cart=True
    )

    print(f"Shopping on Nike.com for {config.product_type}...")
    result = await shop_nike(config)
    print(f"Shopping {'completed' if result else 'failed'}")

asyncio.run(main())
```

---

## Setup Instructions

### 1. Install Dependencies

```bash
# Clone the samples repository
git clone https://github.com/agiopen-org/oagi-lux-samples.git
cd oagi-lux-samples

# Install requirements
pip install -r tasker_examples/requirements.txt

# Or install the SDK directly
pip install oagi
```

### 2. Configure API Key

```bash
# Set environment variable
export OAGI_API_KEY="your-api-key-here"

# Or create .env file
echo 'OAGI_API_KEY=your-api-key-here' > .env
```

### 3. Run Examples

```bash
# Tasker Mode Examples
python tasker_examples/amazon_scraping/amazon_scraping.py --product_name "laptop"
python tasker_examples/cvs_appointment_booking/cvs_tasker.py --first_name "John" --last_name "Doe"
python tasker_examples/software_qa_with_nuclear/software_qa.py

# Actor Mode Examples (via CLI)
oagi agent run "Go to nasdaq.com, search AAPL" --model lux-actor-1
oagi agent run "Go to nike.com, search running shoes" --model lux-actor-1
```

### 4. Export Results

```bash
# Export to HTML report
oagi agent run "Your task here" --export html --export-file report.html

# Export to Markdown
oagi agent run "Your task here" --export markdown --export-file report.md

# Export to JSON
oagi agent run "Your task here" --export json --export-file results.json
```

---

## Resources

| Resource | URL |
|----------|-----|
| Main Website | https://agiopen.org |
| Developer Console | https://developer.agiopen.org |
| Samples Repository | https://github.com/agiopen-org/oagi-lux-samples |
| Python SDK | https://github.com/agiopen-org/oagi-python |
| Discord Community | https://discord.gg/PVAtX8PzxK |
