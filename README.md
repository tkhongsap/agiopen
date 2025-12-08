# OpenAGI Lux Computer Use

A Python library for computer automation using OpenAGI's Lux model - the world's best foundation computer-use model.

## Overview

This project provides a comprehensive framework for implementing computer use automation using the Lux model. It includes modules for:

- **Web Automation** - Form filling, data scraping, web research
- **QA Testing** - Automated UI testing, validation, regression testing
- **Data Processing** - Bulk data entry, report generation

## Lux Model Performance

| Model | Online-Mind2Web Score |
|-------|----------------------|
| **Lux (OpenAGI)** | **83.6** |
| Google Gemini CUA | 69.0 |
| OpenAI Operator | 61.3 |
| Anthropic Claude Sonnet 4 | 61.0 |

**Key Advantages:**
- ~1 second per step (3x faster than competitors)
- 10x cheaper per token
- Works across any desktop application (not browser-only)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/agiopen.git
cd agiopen

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API key:
```bash
OAGI_API_KEY=your_api_key_here
```

Get your API key at [developer.agiopen.org](https://developer.agiopen.org)

## Quick Start

```python
import asyncio
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

async def main():
    agent = AsyncDefaultAgent(max_steps=10)

    completed = await agent.execute(
        "Open Chrome and search Google for 'OpenAGI Lux'",
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

    print(f"Task completed: {completed}")

asyncio.run(main())
```

## Project Structure

```
agiopen/
├── docs/                    # Documentation
│   ├── lux-overview.md      # Model overview and capabilities
│   ├── sdk-reference.md     # SDK API reference
│   ├── use-cases.md         # Implementation guides
│   └── api-examples.md      # Code snippets
├── src/                     # Source code
│   ├── config.py            # Configuration management
│   ├── web_automation/      # Web automation modules
│   ├── qa_testing/          # QA testing modules
│   └── data_processing/     # Data processing modules
├── examples/                # Demo scripts
│   ├── basic_usage.py
│   ├── web_automation_demo.py
│   ├── qa_testing_demo.py
│   └── data_processing_demo.py
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
└── README.md                # This file
```

## Three Operating Modes

### Actor Mode (`lux-actor-1`)
Fast execution for clearly-specified tasks (~1 second per step).

```python
agent = AsyncDefaultAgent(max_steps=10, model="lux-actor-1")
await agent.execute("Click the Submit button")
```

### Thinker Mode (`lux-thinker-1`)
Handles complex, multi-step goals with automatic decomposition.

```python
agent = AsyncDefaultAgent(max_steps=50, model="lux-thinker-1")
await agent.execute("Research AI trends and create a summary report")
```

### Tasker Mode (`lux-tasker-1`)
Maximum control with explicit task lists and retry logic.

```python
agent = AsyncDefaultAgent(max_steps=30, model="lux-tasker-1")
await agent.execute("""
Execute these steps:
1. Navigate to the dashboard
2. Export the report
3. Save to Downloads folder
""")
```

## Use Case Examples

### Web Automation

```python
from src.web_automation import FormFiller
from src.web_automation.form_filler import FormField

filler = FormFiller()
result = await filler.fill_form(
    url="https://example.com/contact",
    fields=[
        FormField("Name", "John Doe"),
        FormField("Email", "john@example.com"),
    ]
)
```

### QA Testing

```python
from src.qa_testing import TestRunner, TestCase
from src.qa_testing.test_runner import TestStep

runner = TestRunner()
test = TestCase(
    name="Login Test",
    description="Verify login flow",
    steps=[
        TestStep("Enter credentials", "Type username and password"),
        TestStep("Submit", "Click login button"),
    ]
)
result = await runner.run_test(test)
```

### Data Processing

```python
from src.data_processing import BulkDataEntry
from src.data_processing.bulk_entry import EntryRecord

entry = BulkDataEntry()
result = await entry.enter_records(
    url="https://crm.example.com/contacts/new",
    records=[
        EntryRecord({"Name": "John", "Email": "john@example.com"}),
        EntryRecord({"Name": "Jane", "Email": "jane@example.com"}),
    ]
)
```

## Running Examples

```bash
# Basic usage
python examples/basic_usage.py

# Web automation demo
python examples/web_automation_demo.py

# QA testing demo
python examples/qa_testing_demo.py

# Data processing demo
python examples/data_processing_demo.py
```

### Official Tasker Mode Examples

```bash
# CVS Appointment Booking
python examples/cvs_appointment_booking.py \
    --first-name "John" \
    --last-name "Doe" \
    --phone "555-123-4567" \
    --email "john@example.com" \
    --birthdate "1990-01-15" \
    --zip-code "10001"

# Amazon Product Search
python examples/amazon_product_search.py \
    --product "wireless headphones" \
    --sort-by "best-sellers" \
    --max-products 10

# Nuclear Player QA Testing
python examples/nuclear_player_qa.py --verify-all-pages
python examples/nuclear_player_qa.py --test-playback
python examples/nuclear_player_qa.py --all
```

### Official Actor Mode Examples

```bash
# AAPL Insider Activity (NASDAQ)
python examples/aapl_insider_activity.py --symbol AAPL
python examples/aapl_insider_activity.py --symbols AAPL MSFT GOOGL

# Healthcare to CoveredCA
python examples/healthcare_coveredca.py --zip-code 90210
python examples/healthcare_coveredca.py --zip-code 94102 --household-size 3 --income 80000

# Nike Shopping
python examples/nike_shopping.py --product "running shoes" --size 10
python examples/nike_shopping.py --product "air max" --size 9 --color black --add-to-cart
```

## CLI Usage

```bash
# Simple task
oagi agent run "Go to google.com" --model lux-actor-1

# Complex task
oagi agent run "Research AI news and summarize" --model lux-thinker-1

# With verbose output
oagi agent run "Fill the contact form" --verbose
```

## Documentation

See the `docs/` directory for detailed documentation:

- [Lux Overview](docs/lux-overview.md) - Model capabilities and modes
- [SDK Reference](docs/sdk-reference.md) - API documentation
- [Use Cases](docs/use-cases.md) - Implementation guides
- [API Examples](docs/api-examples.md) - Code snippets
- [Official Examples](docs/official-examples.md) - Complete official examples from OpenAGI
- [OSGym Setup](docs/osgym-setup.md) - Infrastructure setup guide

## Resources

- [OpenAGI Website](https://agiopen.org)
- [Developer Console](https://developer.agiopen.org)
- [GitHub Organization](https://github.com/agiopen-org)
- [Discord Community](https://discord.gg/PVAtX8PzxK)
- [OSGym Paper](https://arxiv.org/abs/2511.11672)

## License

MIT License - See LICENSE file for details.
