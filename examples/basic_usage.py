"""
Basic Usage Example for Lux Computer Use

This example demonstrates the fundamental usage of the Lux model
for simple computer automation tasks.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def simple_navigation():
    """Navigate to a website."""
    try:
        from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

        print("Starting simple navigation example...")

        agent = AsyncDefaultAgent(max_steps=5, model="lux-actor-1")

        completed = await agent.execute(
            "Open Chrome and navigate to google.com",
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker(),
        )

        print(f"Navigation completed: {completed}")
        return completed

    except ImportError:
        print("Error: oagi package not installed. Run: pip install oagi")
        return False


async def search_google(query: str):
    """Search for something on Google."""
    try:
        from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

        print(f"Searching Google for: {query}")

        agent = AsyncDefaultAgent(max_steps=10, model="lux-actor-1")

        completed = await agent.execute(
            f"Go to Google and search for '{query}'",
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker(),
        )

        print(f"Search completed: {completed}")
        return completed

    except ImportError:
        print("Error: oagi package not installed. Run: pip install oagi")
        return False


async def click_element(element_description: str):
    """Click on an element described in natural language."""
    try:
        from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

        print(f"Clicking: {element_description}")

        agent = AsyncDefaultAgent(max_steps=5, model="lux-actor-1")

        completed = await agent.execute(
            f"Click on the {element_description}",
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker(),
        )

        print(f"Click completed: {completed}")
        return completed

    except ImportError:
        print("Error: oagi package not installed. Run: pip install oagi")
        return False


async def type_text(field_description: str, text: str):
    """Type text into a field."""
    try:
        from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

        print(f"Typing into {field_description}: {text}")

        agent = AsyncDefaultAgent(max_steps=5, model="lux-actor-1")

        completed = await agent.execute(
            f"Click on the {field_description} and type '{text}'",
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker(),
        )

        print(f"Typing completed: {completed}")
        return completed

    except ImportError:
        print("Error: oagi package not installed. Run: pip install oagi")
        return False


async def main():
    """Run basic usage examples."""
    print("=" * 50)
    print("Lux Basic Usage Examples")
    print("=" * 50)

    # Check for API key
    if not os.getenv("OAGI_API_KEY"):
        print("\nWarning: OAGI_API_KEY not set in environment.")
        print("Please set your API key: export OAGI_API_KEY='your_key_here'")
        print("Get your key at: https://developer.agiopen.org\n")

    # Example 1: Simple navigation
    print("\n--- Example 1: Simple Navigation ---")
    await simple_navigation()

    # Example 2: Google search
    print("\n--- Example 2: Google Search ---")
    await search_google("OpenAGI Lux computer use model")

    # Example 3: Click element
    print("\n--- Example 3: Click Element ---")
    await click_element("first search result")

    print("\n" + "=" * 50)
    print("Examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
