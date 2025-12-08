# Lux Model Overview

## Introduction

**Lux** is OpenAGI Foundation's frontier computer-use model, designed to automate interactions with desktop applications and web interfaces by interpreting screenshots and executing actions like a human user.

Released on December 1, 2025, Lux represents a new paradigm in AI automation - instead of relying solely on APIs, it operates computers natively through vision and actions.

## Key Statistics

| Metric | Value |
|--------|-------|
| **Online-Mind2Web Score** | 83.6 (300+ real-world tasks) |
| **Speed** | ~1 second per step |
| **Cost** | ~10x cheaper per token than competitors |
| **Team** | MIT, CMU, UIUC researchers |
| **Founder/CEO** | Zengyi Qin |

## Benchmark Comparison

| Model | Online-Mind2Web Score |
|-------|----------------------|
| **Lux (OpenAGI)** | **83.6** |
| Google Gemini CUA | 69.0 |
| OpenAI Operator | 61.3 |
| Anthropic Claude Sonnet 4 | 61.0 |

## Three Operating Modes

Lux provides three distinct modes optimized for different use cases:

### 1. Actor Mode (`lux-actor-1`)

**Best for:** Quick, clearly-specified tasks

- **Speed:** ~1 second per step (fastest)
- **Use Cases:** Form filling, data extraction, dashboard reports
- **Description:** Low-latency macro engine that understands natural language

```python
# Actor mode is ideal for straightforward tasks
oagi agent run "Click the submit button" --model lux-actor-1
```

### 2. Thinker Mode (`lux-thinker-1`)

**Best for:** Complex, multi-step goals

- **Speed:** Extended sessions (takes time to decompose)
- **Use Cases:** Complex research, multi-application workflows
- **Description:** Breaks high-level instructions into smaller sub-tasks

```python
# Thinker mode handles vague goals
oagi agent run "Research AI news and create a summary report" --model lux-thinker-1
```

### 3. Tasker Mode (`lux-tasker-1`)

**Best for:** Maximum user control with scripted sequences

- **Speed:** Varies by task complexity
- **Use Cases:** Scripted automation, guardrails, failure policies
- **Description:** Accepts Python list of steps, executes with retry logic

```python
# Tasker mode for explicit step control
steps = [
    "Open browser",
    "Navigate to google.com",
    "Search for 'OpenAGI Lux'"
]
```

## Training Methodology: Agentic Active Pre-training

Unlike traditional LLMs that passively absorb internet data, Lux was trained using **Agentic Active Pre-training**:

1. **Active Exploration** - Model learns by interacting with digital environments
2. **Skill Refinement** - Improves through scaled real-world interactions
3. **Trajectory Learning** - Trained on computer-use trajectories and action sequences

This methodology uses OSGym, a distributed data engine that runs 1,000+ OS replicas in parallel, generating 1,420 multi-turn trajectories per minute.

## Key Capabilities

### What Lux Can Do

- Navigate desktop applications (not browser-confined like competitors)
- Interpret screenshots and understand UI elements
- Execute mouse clicks, keyboard input, scrolling
- Handle multi-step task decomposition
- Retry failed operations automatically
- Work across any desktop application

### Key Differentiators

| Feature | Lux | Competitors |
|---------|-----|-------------|
| **Application Scope** | Any desktop app | Browser-only |
| **Speed** | 1 sec/step | 3 sec/step |
| **Cost** | 10x cheaper | Baseline |
| **Retry Logic** | Built-in (Tasker) | Manual |

## Supported Applications

Lux has been tested and trained on:

- **Browsers:** Chrome, Firefox
- **Office:** LibreOffice (Writer, Calc, Impress)
- **Development:** VS Code, terminals
- **Media:** VLC, GIMP
- **Communication:** ThunderBird email client
- **And more:** Any GUI-based application

## Official Example Scenarios

The `oagi-lux-samples` repository provides three primary demonstration scenarios:

### 1. Amazon Product Search (Tasker Mode)

**Purpose:** Web scraping workflow that navigates Amazon, sorts by best sellers, and collects product information.

```python
# Example: Search Amazon for a product
# Customizable arguments: product name, output directory, model, step limits
python tasker_examples/amazon_search.py --product "wireless headphones" --model lux-tasker-1
```

**Features:**
- Autonomous search and navigation
- Sorting results by criteria (best sellers, price, rating)
- Data extraction from product listings
- Command-line argument customization

### 2. CVS Appointment Scheduling (Tasker Mode)

**Purpose:** Automated workflow to schedule flu shot appointments on CVS.com.

```python
# Example: Schedule a CVS appointment
# Accepts personal information parameters
python tasker_examples/cvs_appointment.py \
    --name "John Doe" \
    --phone "555-1234" \
    --birthdate "1990-01-15" \
    --location "New York, NY"
```

**Features:**
- Form filling automation
- Option selection and navigation
- Personal information handling
- Multi-step booking process

### 3. Nuclear Player QA Testing (Tasker Mode)

**Purpose:** Automated UI testing of the Nuclear Player desktop application.

```python
# Example: Run QA tests on Nuclear Player
# Requires Nuclear Player to be pre-installed
python tasker_examples/nuclear_player_qa.py --verify-all-pages
```

**Features:**
- Clicks through all sidebar buttons
- Verifies each page loads correctly
- Desktop application testing (not browser-only)
- Execution logging and reporting

### TaskerAgent Framework

The examples use the `TaskerAgent` framework which provides:

| Feature | Description |
|---------|-------------|
| Multi-step execution | Execute complex workflows through task definitions |
| Visual analysis | Interpret UI state via screenshots |
| Automated interactions | Click, type, scroll, navigate |
| Documentation | Record execution steps and generate reports |

## Resources

| Resource | URL |
|----------|-----|
| Main Website | https://agiopen.org |
| Lux Platform | https://lux.agiopen.org |
| Developer Console | https://developer.agiopen.org |
| GitHub | https://github.com/agiopen-org |
| Samples Repository | https://github.com/agiopen-org/oagi-lux-samples |
| Discord | https://discord.gg/PVAtX8PzxK |
| OSGym Paper | https://arxiv.org/abs/2511.11672 |
