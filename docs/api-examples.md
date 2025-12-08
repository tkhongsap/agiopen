# Lux API Examples

Ready-to-use code snippets for common automation tasks.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Basic Operations](#basic-operations)
3. [Web Navigation](#web-navigation)
4. [Form Interactions](#form-interactions)
5. [Data Operations](#data-operations)
6. [Advanced Patterns](#advanced-patterns)
7. [CLI Examples](#cli-examples)
8. [OSGym API Reference](#osgym-api-reference)
9. [Action Format](#action-format)
10. [Python OSGym Client](#python-osgym-client)

---

## Quick Start

### Minimal Setup

```python
import asyncio
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

async def main():
    # Create agent
    agent = AsyncDefaultAgent(max_steps=10)

    # Execute task
    completed = await agent.execute(
        "Open Chrome and navigate to google.com",
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

    print(f"Task completed: {completed}")

# Run
asyncio.run(main())
```

### With Configuration

```python
import asyncio
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker, ImageConfig
import os

# Set API key (if not in environment)
os.environ["OAGI_API_KEY"] = "your_api_key_here"

async def main():
    # Configure image optimization
    image_config = ImageConfig(
        max_width=1920,
        max_height=1080,
        quality=85,
        format="png"
    )

    # Create components
    agent = AsyncDefaultAgent(
        max_steps=20,
        model="lux-actor-1",
        verbose=True
    )
    action_handler = AsyncPyautoguiActionHandler(
        move_duration=0.3,
        click_delay=0.1
    )
    screenshot_maker = AsyncScreenshotMaker(config=image_config)

    # Execute
    completed = await agent.execute(
        "Your task here",
        action_handler=action_handler,
        image_provider=screenshot_maker,
    )

    return completed

asyncio.run(main())
```

---

## Basic Operations

### Click at Coordinates

```python
from oagi import AsyncPyautoguiActionHandler

handler = AsyncPyautoguiActionHandler()

# Single click
await handler.click(x=500, y=300)

# Double click
await handler.double_click(x=500, y=300)

# Right click
await handler.right_click(x=500, y=300)
```

### Type Text

```python
from oagi import AsyncPyautoguiActionHandler

handler = AsyncPyautoguiActionHandler(type_interval=0.05)

# Type text
await handler.type_text("Hello, World!")

# Type with special characters
await handler.type_text("user@example.com")

# Press specific keys
await handler.press_key("enter")
await handler.press_key("tab")
await handler.press_key("escape")
```

### Keyboard Shortcuts

```python
from oagi import AsyncPyautoguiActionHandler

handler = AsyncPyautoguiActionHandler()

# Copy (Ctrl+C)
await handler.hotkey("ctrl", "c")

# Paste (Ctrl+V)
await handler.hotkey("ctrl", "v")

# Select All (Ctrl+A)
await handler.hotkey("ctrl", "a")

# Save (Ctrl+S)
await handler.hotkey("ctrl", "s")

# New Tab (Ctrl+T)
await handler.hotkey("ctrl", "t")
```

### Scroll

```python
from oagi import AsyncPyautoguiActionHandler

handler = AsyncPyautoguiActionHandler()

# Scroll down
await handler.scroll(clicks=3, direction="down")

# Scroll up
await handler.scroll(clicks=3, direction="up")

# Scroll to specific position
await handler.scroll_to(x=500, y=1000)
```

### Drag and Drop

```python
from oagi import AsyncPyautoguiActionHandler

handler = AsyncPyautoguiActionHandler()

# Drag from one point to another
await handler.drag(
    start_x=100,
    start_y=100,
    end_x=300,
    end_y=200,
    duration=0.5
)
```

---

## Web Navigation

### Navigate to URL

```python
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

async def navigate_to_url(url: str):
    agent = AsyncDefaultAgent(max_steps=5, model="lux-actor-1")

    await agent.execute(
        f"Navigate to {url}",
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )
```

### Search on Google

```python
async def google_search(query: str):
    agent = AsyncDefaultAgent(max_steps=10, model="lux-actor-1")

    await agent.execute(
        f"Go to Google and search for '{query}'",
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )
```

### Navigate Multiple Pages

```python
async def multi_page_navigation(urls: list):
    agent = AsyncDefaultAgent(max_steps=30, model="lux-thinker-1")

    url_list = "\n".join(f"- {url}" for url in urls)

    await agent.execute(
        f"""
        Visit each of these pages in order:
        {url_list}

        For each page, wait for it to fully load before moving to the next.
        """,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )
```

---

## Form Interactions

### Fill Text Input

```python
async def fill_text_field(field_label: str, value: str):
    agent = AsyncDefaultAgent(max_steps=5, model="lux-actor-1")

    await agent.execute(
        f"Click on the '{field_label}' field and type '{value}'",
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )
```

### Select from Dropdown

```python
async def select_dropdown(dropdown_label: str, option: str):
    agent = AsyncDefaultAgent(max_steps=5, model="lux-actor-1")

    await agent.execute(
        f"Click the '{dropdown_label}' dropdown and select '{option}'",
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )
```

### Check/Uncheck Checkbox

```python
async def toggle_checkbox(checkbox_label: str, should_check: bool):
    action = "check" if should_check else "uncheck"
    agent = AsyncDefaultAgent(max_steps=5, model="lux-actor-1")

    await agent.execute(
        f"{action.capitalize()} the '{checkbox_label}' checkbox",
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )
```

### Complete Form

```python
async def complete_form(form_data: dict):
    agent = AsyncDefaultAgent(max_steps=20, model="lux-actor-1")

    field_instructions = "\n".join(
        f"- {field}: {value}" for field, value in form_data.items()
    )

    await agent.execute(
        f"""
        Fill out the form with the following values:
        {field_instructions}

        Then click the Submit button.
        """,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

# Usage
await complete_form({
    "First Name": "John",
    "Last Name": "Doe",
    "Email": "john@example.com",
    "Phone": "123-456-7890",
    "Message": "This is a test message."
})
```

---

## Data Operations

### Copy Text to Clipboard

```python
async def copy_element_text(element_description: str):
    agent = AsyncDefaultAgent(max_steps=10, model="lux-actor-1")

    await agent.execute(
        f"""
        1. Find the {element_description}
        2. Select all its text (triple-click or Ctrl+A)
        3. Copy to clipboard (Ctrl+C)
        """,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )
```

### Extract Table Data

```python
async def extract_table(table_description: str):
    agent = AsyncDefaultAgent(max_steps=15, model="lux-thinker-1")

    await agent.execute(
        f"""
        1. Locate the {table_description}
        2. Select all rows in the table
        3. Copy the data (Ctrl+C)
        4. The data should now be in clipboard
        """,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )
```

### Download File

```python
async def download_file(button_text: str, wait_seconds: int = 10):
    agent = AsyncDefaultAgent(max_steps=10, model="lux-actor-1")

    await agent.execute(
        f"""
        1. Click the '{button_text}' button to start download
        2. Wait {wait_seconds} seconds for download to complete
        3. Verify download started (check for download notification)
        """,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )
```

### Upload File

```python
async def upload_file(file_path: str, upload_button: str = "Upload"):
    agent = AsyncDefaultAgent(max_steps=15, model="lux-actor-1")

    await agent.execute(
        f"""
        1. Click the '{upload_button}' button
        2. In the file dialog, navigate to: {file_path}
        3. Select the file and click Open
        4. Wait for upload to complete
        """,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )
```

---

## Advanced Patterns

### Conditional Execution

```python
async def conditional_task(check_condition: str, if_true: str, if_false: str):
    agent = AsyncDefaultAgent(max_steps=20, model="lux-thinker-1")

    await agent.execute(
        f"""
        First, check: {check_condition}

        If the condition is true:
        {if_true}

        If the condition is false:
        {if_false}
        """,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

# Usage
await conditional_task(
    check_condition="Is the user logged in? (Look for 'Welcome' message)",
    if_true="Click on 'My Account' to view profile",
    if_false="Click 'Login' button and enter credentials"
)
```

### Loop Through Items

```python
async def process_list_items(item_selector: str, action_per_item: str):
    agent = AsyncDefaultAgent(max_steps=50, model="lux-thinker-1")

    await agent.execute(
        f"""
        For each {item_selector} on the page:
        1. Click on the item
        2. {action_per_item}
        3. Go back to the list
        4. Move to the next item

        Continue until all items are processed.
        """,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )
```

### Error Recovery

```python
async def task_with_recovery(main_task: str, recovery_action: str):
    agent = AsyncDefaultAgent(max_steps=30, model="lux-thinker-1")

    await agent.execute(
        f"""
        Try to: {main_task}

        If an error occurs or the task fails:
        1. {recovery_action}
        2. Try the main task again

        If it fails twice, stop and report the error.
        """,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )
```

### Parallel Tasks (Multiple Browsers)

```python
import asyncio

async def parallel_tasks(tasks: list):
    """Execute multiple tasks in parallel (requires multiple browser instances)."""

    async def run_task(task: str, task_id: int):
        agent = AsyncDefaultAgent(max_steps=20, model="lux-actor-1")
        return await agent.execute(
            f"[Task {task_id}] {task}",
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker(),
        )

    # Note: Requires separate browser/desktop sessions
    results = await asyncio.gather(*[
        run_task(task, i) for i, task in enumerate(tasks)
    ])

    return results
```

### Scheduled Execution

```python
import asyncio
from datetime import datetime, timedelta

async def scheduled_task(task: str, run_at: datetime):
    """Execute a task at a scheduled time."""

    now = datetime.now()
    if run_at > now:
        wait_seconds = (run_at - now).total_seconds()
        print(f"Waiting {wait_seconds} seconds until scheduled time...")
        await asyncio.sleep(wait_seconds)

    agent = AsyncDefaultAgent(max_steps=20, model="lux-actor-1")
    return await agent.execute(
        task,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

# Usage - Run task in 1 hour
await scheduled_task(
    "Generate daily report from dashboard",
    run_at=datetime.now() + timedelta(hours=1)
)
```

---

## CLI Examples

### Basic Agent Run

```bash
# Simple task
oagi agent run "Click the submit button"

# With specific model
oagi agent run "Research AI trends" --model lux-thinker-1

# With max steps
oagi agent run "Fill out the form" --max-steps 30

# Verbose output
oagi agent run "Navigate to example.com" --verbose
```

### Export Results

```bash
# Export to HTML
oagi agent run "Complete checkout" --export report.html --format html

# Export to Markdown
oagi agent run "Test login flow" --export report.md --format markdown

# Export to JSON
oagi agent run "Scrape data" --export data.json --format json
```

### Dry Run (Preview)

```bash
# Preview without executing
oagi agent run "Delete all files" --dry-run
```

### Using Tasker Mode with File

```bash
# Create tasks.json
cat > tasks.json << 'EOF'
{
  "steps": [
    "Open browser",
    "Navigate to google.com",
    "Search for 'OpenAGI Lux'",
    "Click first result"
  ]
}
EOF

# Run with Tasker
oagi agent run --tasker-file tasks.json --model lux-tasker-1
```

### Batch Processing

```bash
# Process multiple URLs from file
cat urls.txt | while read url; do
  oagi agent run "Navigate to $url and take a screenshot" --export "screenshots/${url//\//_}.png"
done
```

---

## OSGym API Reference

OSGym is the distributed data engine used for training and running Lux models. It exposes REST endpoints on port 20000 for managing virtual machine environments.

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/reset` | POST | Initialize new environment with task configuration |
| `/step` | POST | Execute an action in the environment |
| `/shutdown` | POST | Shut down and release a VM |
| `/screenshot` | GET | Get screenshot of current VM state |

### Reset Environment

Initialize a new environment with task configuration:

```bash
curl -X POST http://localhost:20000/reset \
  -H "Content-Type: application/json" \
  -d '{
    "task_config": {
      "task_id": "web_navigation_001",
      "instruction": "Navigate to google.com and search for AI news",
      "timeout": 120
    },
    "vm_options": {
      "display": ":1",
      "resolution": "1920x1080"
    }
  }'
```

**Response:**
```json
{
  "vm_id": 0,
  "status": "ready",
  "screenshot_url": "/screenshot?vm_id=0"
}
```

### Execute Action

Execute an action in the environment:

```bash
curl -X POST http://localhost:20000/step \
  -H "Content-Type: application/json" \
  -d '{
    "action": "<|think_start|>I need to click on the search button located at coordinates (500, 300)<|think_end|><|action_start|>click(500,300)<|action_end|>",
    "vm_id": 0
  }'
```

**Response:**
```json
{
  "success": true,
  "screenshot": "base64_encoded_image...",
  "done": false,
  "reward": 0.0
}
```

### Get Screenshot

Retrieve the current screenshot of a VM:

```bash
curl -X GET "http://localhost:20000/screenshot?vm_id=0" \
  --output screenshot.png
```

### Shutdown VM

Release a VM when done:

```bash
curl -X POST http://localhost:20000/shutdown \
  -H "Content-Type: application/json" \
  -d '{
    "vm_id": 0
  }'
```

---

## Action Format

OSGym uses a structured action format with thinking and action sections:

### Format Structure

```
<|think_start|>[reasoning]<|think_end|><|action_start|>[action]<|action_end|>
```

### Supported Actions

| Action | Syntax | Description |
|--------|--------|-------------|
| Click | `click(x, y)` | Single click at coordinates |
| Double Click | `double_click(x, y)` | Double click at coordinates |
| Right Click | `right_click(x, y)` | Right click at coordinates |
| Type | `type("text")` | Type text at current cursor |
| Press Key | `press("key")` | Press a specific key |
| Scroll | `scroll(direction, amount)` | Scroll up/down |
| Drag | `drag(x1, y1, x2, y2)` | Drag from point to point |
| Wait | `wait(seconds)` | Wait for specified duration |

### Action Examples

**Click Action:**
```
<|think_start|>The search button is located in the center of the page at approximately (960, 540). I will click it to submit the search.<|think_end|><|action_start|>click(960,540)<|action_end|>
```

**Type Action:**
```
<|think_start|>I need to enter the search query in the text field. I'll type "artificial intelligence news".<|think_end|><|action_start|>type("artificial intelligence news")<|action_end|>
```

**Keyboard Shortcut:**
```
<|think_start|>I need to open a new tab using the keyboard shortcut Ctrl+T.<|think_end|><|action_start|>press("ctrl+t")<|action_end|>
```

**Scroll Action:**
```
<|think_start|>The content I need is below the visible area. I'll scroll down to see more.<|think_end|><|action_start|>scroll("down", 3)<|action_end|>
```

---

## Python OSGym Client

Here's a Python client for interacting with OSGym:

```python
import httpx
import base64
from typing import Optional
from dataclasses import dataclass

@dataclass
class StepResult:
    success: bool
    screenshot: bytes
    done: bool
    reward: float

class OSGymClient:
    def __init__(self, base_url: str = "http://localhost:20000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
        self.vm_id: Optional[int] = None

    async def reset(self, task_config: dict) -> int:
        """Initialize a new environment."""
        response = await self.client.post(
            f"{self.base_url}/reset",
            json={"task_config": task_config}
        )
        data = response.json()
        self.vm_id = data["vm_id"]
        return self.vm_id

    async def step(self, action: str) -> StepResult:
        """Execute an action."""
        response = await self.client.post(
            f"{self.base_url}/step",
            json={"action": action, "vm_id": self.vm_id}
        )
        data = response.json()
        return StepResult(
            success=data["success"],
            screenshot=base64.b64decode(data["screenshot"]),
            done=data["done"],
            reward=data.get("reward", 0.0)
        )

    async def screenshot(self) -> bytes:
        """Get current screenshot."""
        response = await self.client.get(
            f"{self.base_url}/screenshot",
            params={"vm_id": self.vm_id}
        )
        return response.content

    async def shutdown(self):
        """Release the VM."""
        await self.client.post(
            f"{self.base_url}/shutdown",
            json={"vm_id": self.vm_id}
        )
        self.vm_id = None

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

# Usage
async def main():
    client = OSGymClient()

    try:
        # Initialize environment
        await client.reset({
            "task_id": "test_001",
            "instruction": "Search for weather on Google"
        })

        # Execute actions
        result = await client.step(
            "<|think_start|>Opening browser<|think_end|>"
            "<|action_start|>click(100, 50)<|action_end|>"
        )

        if result.success:
            print("Action executed successfully")

        # Get screenshot
        screenshot = await client.screenshot()
        with open("current_state.png", "wb") as f:
            f.write(screenshot)

    finally:
        await client.shutdown()
        await client.close()
```

---

## Environment Setup Script

```bash
#!/bin/bash
# setup_lux.sh - Setup script for Lux development

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install oagi python-dotenv

# Create .env file
cat > .env << 'EOF'
OAGI_API_KEY=your_api_key_here
OAGI_BASE_URL=https://api.agiopen.org
EOF

echo "Setup complete! Edit .env with your API key."
```
