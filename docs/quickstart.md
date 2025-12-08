# Quickstart Guide

Get your first computer-use agent running in under 5 minutes.

## Prerequisites

- Python 3.10+ installed on your system

---

## Step 1: Install OpenAGI

Install the OAGI library with all features included:

```bash
pip install oagi
```

This installs the complete SDK including desktop automation, server capabilities, and all dependencies.

### Step 1b: Enable Permissions

Run the permission command:

```bash
oagi agent permission
```

**macOS Users:** You will likely see a permission request the first time you run this.

You must grant **Accessibility** and **Screen Recording** permissions to your terminal app (e.g., Terminal, iTerm2, VS Code):

1. Go to **System Settings > Privacy & Security**
2. Enable permissions for your terminal app
3. Restart your terminal

---

## Step 2: Set Up Authentication

### Get Your API Key

1. Visit the OpenAGI Developer Platform at [developer.agiopen.org](https://developer.agiopen.org)
2. Sign in with your developer account
3. Click **Create an API Key**, give it a descriptive name
4. Copy the generated value (keys start with `sk-`)
5. Store it securely—treat it like a password

**Free credits:** New users receive $10 in inference credits upon registration.

### Configure Your Environment

**Option A: Export in terminal**
```bash
export OAGI_API_KEY=sk-...
export OAGI_BASE_URL=https://api.agiopen.org
```

**Option B: Create a .env file**
```bash
# .env
OAGI_API_KEY=sk-your-api-key-here
OAGI_BASE_URL=https://api.agiopen.org
```

---

## Step 3: Prepare Your Desktop

For the best results, your desktop environment needs to be clean and simple. The agent "sees" your screen just like you do.

### Good Setup

- Single, large browser window on a blank page
- Clean desktop background
- Minimal distractions
- Key windows clearly visible

### Bad Setup (Avoid)

- **Too many tabs:** 20+ tabs make it hard to find the right one
- **Small window:** The agent needs to see page content clearly
- **Messy desktop:** Multiple overlapping apps confuse visual analysis

### Multi-Monitor Users

Keep your browser and any windows the agent needs to interact with on your **primary screen**. The agent may have difficulty detecting which monitor is active.

---

## Step 4: Run Your First Agent

Launch a Lux computer-use agent with a single command:

```bash
oagi agent run "Go to https://agiopen.org" --model "lux-actor-1"
```

### What Happens Next

1. The agent takes a screenshot of your current screen
2. Lux analyzes the visual interface and predicts keyboard/mouse actions
3. The agent executes actions (clicks, types, scrolls) to complete the goal
4. You'll see real-time feedback as the agent works

---

## More Examples

### Actor Mode (Fast, ~1 sec/step)

```bash
# Navigate to a website
oagi agent run "Go to google.com and search for AI news" --model lux-actor-1

# Fill a form
oagi agent run "Click the contact button and fill in name: John Doe" --model lux-actor-1
```

### Thinker Mode (Complex, multi-step)

```bash
# Research task
oagi agent run "Research the top 5 AI companies and summarize their products" --model lux-thinker-1
```

### Tasker Mode (Scripted control)

```bash
# Using a task file
oagi agent run --tasker-file tasks.json --model lux-tasker-1
```

---

## CLI Options

| Option | Description |
|--------|-------------|
| `--model` | Model to use: `lux-actor-1`, `lux-thinker-1`, `lux-tasker-1` |
| `--max-steps` | Maximum steps to execute (default: 10) |
| `--verbose` | Enable verbose output |
| `--export` | Export format: `html`, `markdown`, `json` |
| `--export-file` | Output file for export |
| `--dry-run` | Preview actions without executing |

---

## Troubleshooting

### Permission Issues (macOS)

If actions aren't working:
1. Check System Settings > Privacy & Security > Accessibility
2. Check System Settings > Privacy & Security > Screen Recording
3. Ensure your terminal app is listed and enabled
4. Restart your terminal after enabling permissions

### Agent Not Finding Elements

- Ensure the browser window is maximized or large enough
- Close unnecessary tabs and windows
- Move target window to primary monitor
- Avoid overlapping windows

### API Key Issues

- Verify your key starts with `sk-`
- Check that `OAGI_API_KEY` is exported in your environment
- Ensure you have available credits at [developer.agiopen.org](https://developer.agiopen.org)

---

## Next Steps

- Read the [SDK Reference](sdk-reference.md) for Python API usage
- Explore [Official Examples](official-examples.md) for common use cases
- Check [Use Cases](use-cases.md) for implementation guides
- Join the [Discord Community](https://discord.gg/PVAtX8PzxK) for support
