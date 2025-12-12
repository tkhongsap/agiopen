# TalentMatch AI - UI Testing with OAGI TaskerAgent

## Overview

This document describes UI testing for the TalentMatch AI web application using the **OAGI TaskerAgent** framework. The tests use the Lux model to perform real browser automation through natural language instructions.

- **Application URL**: https://talentum.tkhongsap.io/
- **Testing Framework**: OAGI TaskerAgent (pip install oagi)
- **Model**: lux-tasker-1

## How It Works

The OAGI TaskerAgent uses the Lux computer-use model to:

1. **Capture screenshots** of your desktop/browser
2. **Interpret natural language steps** describing what to do
3. **Execute actions** (click, type, scroll) via PyAutoGUI
4. **Verify results** by analyzing the screen

```python
from oagi import TaskerAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

tasker = TaskerAgent(
    max_steps=50,
    model="lux-tasker-1",
    retry_on_failure=True,
    max_retries=3
)

result = await tasker.execute(
    steps=[
        "Navigate to https://talentum.tkhongsap.io/",
        "Click on the 'Shortlists' link in the sidebar",
        "Verify 'My Shortlists' heading appears",
    ],
    action_handler=AsyncPyautoguiActionHandler(),
    image_provider=AsyncScreenshotMaker(),
)
```

---

## Application Structure

TalentMatch AI has 5 main pages:

| Page | URL | Description |
|------|-----|-------------|
| Search | `/` | AI-powered candidate search with filters |
| Shortlists | `/shortlists` | Manage candidate shortlists |
| Summaries | `/summaries` | Post-interview candidate briefs |
| History | `/history` | View and reuse previous searches |
| Admin | `/admin` | System settings and AI embeddings |

---

## Test Suites

### 1. Navigation Tests (`--test-navigation`)

Tests sidebar navigation and header elements:

| Test | Description |
|------|-------------|
| `navigation_all_pages` | Navigate to all 5 main pages via sidebar |
| `sidebar_toggle` | Test sidebar collapse/expand button |
| `header_elements` | Test language selector and theme toggle |

**Steps Example:**
```
- Navigate to https://talentum.tkhongsap.io/
- Click on 'Shortlists' in sidebar navigation
- Verify URL changes to /shortlists
- Verify 'My Shortlists' heading appears
```

### 2. Search Tests (`--test-search`)

Tests the main search functionality:

| Test | Description |
|------|-------------|
| `search_basic` | Type query and execute search |
| `search_filters_experience` | Drag experience slider |
| `search_filters_location` | Select/deselect location checkboxes |
| `search_filters_skills` | Select skills and add custom skill |
| `search_options` | Test Scoring Profile and Results dropdowns |
| `upload_jd` | Open and close Upload JD modal |

**Steps Example:**
```
- Click on the search input field
- Type 'Python developer in Bangkok'
- Click the 'Search' button
- Verify search results appear
```

### 3. Shortlists Tests (`--test-shortlists`)

Tests shortlist management:

| Test | Description |
|------|-------------|
| `shortlists_page` | Verify page elements and Create button |
| `shortlist_interaction` | Click on shortlist cards |

### 4. Summaries Tests (`--test-summaries`)

Tests candidate summaries table:

| Test | Description |
|------|-------------|
| `summaries_page` | Verify table columns and layout |
| `summaries_interaction` | Test search and filter interactions |

### 5. History Tests (`--test-history`)

Tests search history:

| Test | Description |
|------|-------------|
| `history_page` | Verify history items display |
| `history_reuse` | Click to reuse a search |

### 6. Admin Tests (`--test-admin`)

Tests admin settings:

| Test | Description |
|------|-------------|
| `admin_page` | Verify AI Embeddings stats and Regenerate button |

---

## Running Tests

### Prerequisites

1. Install the OAGI SDK:
```bash
pip install oagi
```

2. Set your API key:
```bash
# Linux/Mac
export OAGI_API_KEY='sk-your-key-here'

# Windows PowerShell
$env:OAGI_API_KEY='sk-your-key-here'
```

3. Get your API key at: https://developer.agiopen.org

### Run All Tests

```bash
python examples/talentum_ui_tests.py --all
```

### Run Specific Test Suites

```bash
# Navigation tests only
python examples/talentum_ui_tests.py --test-navigation

# Search tests only
python examples/talentum_ui_tests.py --test-search

# Multiple suites
python examples/talentum_ui_tests.py --test-shortlists --test-summaries

# With verbose output
python examples/talentum_ui_tests.py --test-admin --verbose
```

### Available Options

| Option | Description |
|--------|-------------|
| `--test-navigation` | Run navigation tests |
| `--test-search` | Run search functionality tests |
| `--test-shortlists` | Run shortlists page tests |
| `--test-summaries` | Run summaries page tests |
| `--test-history` | Run history page tests |
| `--test-admin` | Run admin page tests |
| `--all` | Run all test suites |
| `--verbose` | Enable verbose output |

---

## Test Report Example

```
============================================================
         TALENTMATCH AI - UI TEST REPORT
============================================================

Application: https://talentum.tkhongsap.io/
Timestamp: 2025-12-11T10:30:00
Duration: 245.50 seconds

📊 SUMMARY:
   Total Tests: 14
   ✅ Passed:   12
   ❌ Failed:   1
   ⚠️  Errors:   1
   ⏭️  Skipped:  0

   Pass Rate: 85.7%

📋 RESULTS BY CATEGORY:
------------------------------------------------------------

NAVIGATION: 3/3 passed
  ✅ navigation_all_pages (45.20s)
  ✅ sidebar_toggle (12.30s)
  ✅ header_elements (18.50s)

SEARCH: 5/6 passed
  ✅ search_basic (22.10s)
  ✅ search_filters_experience (15.40s)
  ✅ search_filters_location (18.20s)
  ❌ search_filters_skills (25.30s)
     └─ Failed to find custom skill input...
  ✅ search_options (14.60s)
  ✅ upload_jd (10.80s)

============================================================
         END OF TEST REPORT
============================================================
```

---

## Desktop Setup Requirements

For best results with Lux computer-use:

### Good Setup
- Browser window maximized or large
- TalentMatch app open and logged in
- Minimal other windows/distractions
- Primary monitor used for browser

### Avoid
- Multiple overlapping windows
- Very small browser window
- Too many browser tabs
- Split screen with other apps

---

## Key Differences from Manual Testing

| Aspect | Manual Testing | TaskerAgent Testing |
|--------|---------------|---------------------|
| Execution | Human clicks/types | Lux AI interprets and acts |
| Speed | Variable | ~1-2 seconds per action |
| Consistency | May vary | Consistent interpretation |
| Language | Click here, type there | Natural language steps |
| Screenshots | Manual capture | Automatic on each step |

---

## Troubleshooting

### "oagi package not installed"
```bash
pip install oagi
```

### "OAGI_API_KEY not set"
```bash
export OAGI_API_KEY='sk-your-key-here'
```

### Tests failing to find elements
- Ensure browser window is large and visible
- Close other overlapping windows
- Make sure you're logged into TalentMatch
- Try running with `--verbose` for detailed logs

### Timeout errors
- The Lux model needs a clear view of the screen
- Reduce step complexity if needed
- Increase `timeout_per_step` in the code

---

## Related Files

| File | Description |
|------|-------------|
| `examples/talentum_ui_tests.py` | Main UI test suite |
| `examples/nuclear_player_qa.py` | Reference QA testing example |
| `examples/cvs_appointment_booking.py` | Reference TaskerAgent example |
| `docs/sdk-reference.md` | OAGI SDK documentation |

---

## Resources

- [OAGI Developer Platform](https://developer.agiopen.org)
- [TaskerAgent Documentation](https://developer.agiopen.org/docs/agent)
- [Lux Model Overview](https://developer.agiopen.org/docs/models)
- [Discord Community](https://discord.gg/PVAtX8PzxK)
