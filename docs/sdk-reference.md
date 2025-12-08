# OAGI Python SDK Reference

## Installation

The OAGI Python SDK requires Python 3.10 or higher.

### Installation Options

```bash
# Full package (all features)
pip install oagi

# Minimal (httpx, pydantic only)
pip install oagi-core

# With desktop automation (pyautogui, pillow)
pip install oagi-core[desktop]

# With server support (FastAPI, Socket.IO)
pip install oagi-core[server]
```

### Dependencies

| Package | Full | Core | Desktop | Server |
|---------|------|------|---------|--------|
| httpx | Yes | Yes | Yes | Yes |
| pydantic | Yes | Yes | Yes | Yes |
| pyautogui | Yes | No | Yes | No |
| pillow | Yes | No | Yes | No |
| fastapi | Yes | No | No | Yes |
| socketio | Yes | No | No | Yes |

## Configuration

### Environment Variables

```bash
# Required
export OAGI_API_KEY="your_api_key_here"

# Optional (with defaults)
export OAGI_BASE_URL="https://api.agiopen.org"
export OAGI_TIMEOUT="30"
```

### Python Configuration

```python
from oagi import Config

# Configure via environment (recommended)
# Reads OAGI_API_KEY automatically

# Or configure explicitly
config = Config(
    api_key="your_api_key",
    base_url="https://api.agiopen.org",
    timeout=30
)
```

## Core Components

### AsyncDefaultAgent

High-level agent that handles the screenshot-action loop automatically.

```python
from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

# Initialize agent with max steps
agent = AsyncDefaultAgent(max_steps=10)

# Execute a task
completed = await agent.execute(
    "Search for weather on Google",
    action_handler=AsyncPyautoguiActionHandler(),
    image_provider=AsyncScreenshotMaker(),
)

# Check completion status
if completed:
    print("Task completed successfully")
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_steps` | int | 10 | Maximum number of steps to execute |
| `model` | str | "lux-actor-1" | Model to use (lux-actor-1, lux-thinker-1, lux-tasker-1) |
| `verbose` | bool | False | Enable verbose logging |

### AsyncActor

Low-level control for manual step-by-step execution.

```python
from oagi import AsyncActor

actor = AsyncActor()

# Manual step execution
async for step in actor.run("Navigate to google.com"):
    print(f"Step: {step.action}")
    print(f"Coordinates: {step.x}, {step.y}")

    # You can intervene between steps
    if step.requires_confirmation:
        user_confirmed = await get_user_confirmation()
        if not user_confirmed:
            break
```

### AsyncPyautoguiActionHandler

Handles UI action execution via PyAutoGUI.

```python
from oagi import AsyncPyautoguiActionHandler

handler = AsyncPyautoguiActionHandler(
    move_duration=0.5,  # Mouse movement duration
    click_delay=0.1,    # Delay between clicks
    type_interval=0.05  # Interval between keystrokes
)

# Supported actions
await handler.click(x=100, y=200)
await handler.double_click(x=100, y=200)
await handler.right_click(x=100, y=200)
await handler.type_text("Hello, World!")
await handler.press_key("enter")
await handler.scroll(clicks=3, direction="down")
await handler.drag(start_x=100, start_y=100, end_x=200, end_y=200)
```

### AsyncScreenshotMaker

Captures screenshots for the model to interpret.

```python
from oagi import AsyncScreenshotMaker, ImageConfig

# Default screenshot maker
screenshot_maker = AsyncScreenshotMaker()

# With custom configuration
config = ImageConfig(
    max_width=1920,
    max_height=1080,
    quality=85,  # JPEG quality
    format="png"
)
screenshot_maker = AsyncScreenshotMaker(config=config)

# Capture screenshot
image = await screenshot_maker.capture()
```

### PILImage and ImageConfig

Image processing utilities for optimization.

```python
from oagi import PILImage, ImageConfig

# Configure image processing
config = ImageConfig(
    max_width=1920,
    max_height=1080,
    quality=85,
    format="png"
)

# Process an image
image = PILImage.from_file("screenshot.png")
optimized = image.optimize(config)
base64_data = optimized.to_base64()
```

## TaskerAgent Framework

The `TaskerAgent` is a specialized framework for executing multi-step workflows with explicit control over each step.

### TaskerAgent Overview

```python
from oagi import TaskerAgent

# Initialize TaskerAgent with configuration
tasker = TaskerAgent(
    max_steps=50,
    model="lux-tasker-1",
    retry_on_failure=True,
    max_retries=3
)
```

### Defining Task Steps

```python
# Define explicit task steps
task_steps = [
    "Navigate to https://www.cvs.com/immunizations/flu",
    "Click 'Schedule an appointment'",
    "Enter zip code '10001' in the location field",
    "Click 'Search'",
    "Select the first available location",
    "Choose the earliest available time slot",
    "Fill in personal information",
    "Click 'Confirm appointment'"
]

# Execute the task
result = await tasker.execute(steps=task_steps)
```

### TaskerAgent Features

| Feature | Description |
|---------|-------------|
| **Step-by-step execution** | Execute each step sequentially with verification |
| **Retry logic** | Automatic retry on failure with configurable attempts |
| **State tracking** | Track progress through multi-step workflows |
| **Error recovery** | Graceful handling of failures with rollback options |
| **Execution logging** | Detailed logs of each action performed |
| **Report generation** | Generate execution reports (HTML, Markdown, JSON) |

### TaskerAgent Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_steps` | int | 50 | Maximum steps per execution |
| `model` | str | "lux-tasker-1" | Model to use |
| `retry_on_failure` | bool | True | Auto-retry failed steps |
| `max_retries` | int | 3 | Maximum retry attempts |
| `timeout_per_step` | int | 30 | Seconds per step |
| `verbose` | bool | False | Enable detailed logging |

### Example: Web Scraping Workflow

```python
from oagi import TaskerAgent

async def scrape_amazon_products(product_name: str):
    tasker = TaskerAgent(max_steps=30, model="lux-tasker-1")

    steps = [
        f"Navigate to https://www.amazon.com",
        f"Type '{product_name}' in the search box",
        "Click the search button",
        "Click 'Sort by: Best Sellers'",
        "For each of the top 5 products, extract: name, price, rating",
        "Copy the extracted data to clipboard"
    ]

    result = await tasker.execute(steps=steps)
    return result
```

### Example: QA Testing Workflow

```python
from oagi import TaskerAgent

async def test_nuclear_player_ui():
    tasker = TaskerAgent(
        max_steps=100,
        model="lux-tasker-1",
        retry_on_failure=True
    )

    # Define all sidebar buttons to test
    sidebar_buttons = [
        "Library", "Playlists", "Favorites",
        "Downloads", "Settings", "About"
    ]

    steps = []
    for button in sidebar_buttons:
        steps.extend([
            f"Click the '{button}' button in the sidebar",
            f"Verify the {button} page loads correctly",
            "Take a screenshot for verification"
        ])

    result = await tasker.execute(steps=steps)
    return result
```

---

## CLI Reference

### Running Agents

```bash
# Basic usage with Actor mode
oagi agent run "Go to google.com and search for AI news" --model lux-actor-1

# Complex task with Thinker mode
oagi agent run "Research the top 5 AI companies and summarize their products" --model lux-thinker-1

# Scripted execution with Tasker mode
oagi agent run --tasker-file tasks.json --model lux-tasker-1
```

### CLI Options

| Option | Description |
|--------|-------------|
| `--model` | Model to use (lux-actor-1, lux-thinker-1, lux-tasker-1) |
| `--max-steps` | Maximum steps to execute |
| `--verbose` | Enable verbose output |
| `--output` | Output format (json, html, markdown) |
| `--export` | Export execution history to file |
| `--dry-run` | Preview actions without executing |

### Inspecting Modes

```bash
# List available modes
oagi modes list

# Get mode details
oagi modes info lux-actor-1
```

### Managing Permissions

```bash
# List current permissions
oagi permissions list

# Grant screen capture permission
oagi permissions grant screen-capture

# Revoke permission
oagi permissions revoke keyboard-control
```

### Exporting History

```bash
# Export to HTML
oagi export --format html --output execution-report.html

# Export to Markdown
oagi export --format markdown --output execution-report.md

# Export to JSON
oagi export --format json --output execution-report.json
```

## Server Mode

### FastAPI Server

```python
from oagi.server import create_app

# Create FastAPI application
app = create_app(
    api_key="your_api_key",
    cors_origins=["http://localhost:3000"]
)

# Run with uvicorn
# uvicorn main:app --host 0.0.0.0 --port 8000
```

### Socket.IO Integration

```python
from oagi.server import SocketIOServer

server = SocketIOServer(
    api_key="your_api_key",
    namespace="/lux"
)

# Client can connect and send tasks
# server.on("execute_task", handle_task)
```

## Error Handling

```python
from oagi import OAGIError, AuthenticationError, RateLimitError, ExecutionError

try:
    result = await agent.execute("Some task")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except ExecutionError as e:
    print(f"Execution failed at step {e.step}: {e.message}")
except OAGIError as e:
    print(f"General error: {e}")
```

## Best Practices

### 1. Use Appropriate Mode

```python
# Actor for simple, clear tasks
await agent.execute("Click the submit button", model="lux-actor-1")

# Thinker for complex, multi-step goals
await agent.execute("Create a monthly report from the dashboard", model="lux-thinker-1")

# Tasker for maximum control
await tasker.execute(steps=[...], model="lux-tasker-1")
```

### 2. Optimize Images

```python
# Reduce image size for faster API calls
config = ImageConfig(max_width=1280, max_height=720, quality=75)
```

### 3. Handle Failures Gracefully

```python
# Use retry logic
for attempt in range(3):
    try:
        result = await agent.execute(task)
        break
    except ExecutionError:
        if attempt == 2:
            raise
        await asyncio.sleep(1)
```

### 4. Monitor Execution

```python
# Enable verbose mode for debugging
agent = AsyncDefaultAgent(max_steps=10, verbose=True)

# Or use callbacks
async def on_step(step):
    print(f"Executing: {step.action}")

agent.on_step = on_step
```
