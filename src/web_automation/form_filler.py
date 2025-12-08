"""
Form Filler - Automate form completion across websites.
"""

from dataclasses import dataclass
from typing import Any, Optional
import asyncio


@dataclass
class FormField:
    """Represents a form field to fill."""
    name: str
    value: Any
    field_type: str = "text"  # text, dropdown, checkbox, radio, textarea


@dataclass
class FormResult:
    """Result of a form fill operation."""
    success: bool
    fields_filled: int
    errors: list[str]
    screenshot_path: Optional[str] = None


class FormFiller:
    """
    Automate form filling using Lux.

    Example:
        filler = FormFiller()
        result = await filler.fill_form(
            url="https://example.com/contact",
            fields=[
                FormField("name", "John Doe"),
                FormField("email", "john@example.com"),
                FormField("message", "Hello!", field_type="textarea"),
            ]
        )
    """

    def __init__(
        self,
        max_steps: int = 20,
        model: str = "lux-actor-1",
        verbose: bool = False
    ):
        self.max_steps = max_steps
        self.model = model
        self.verbose = verbose

    async def fill_form(
        self,
        url: str,
        fields: list[FormField],
        submit: bool = True,
        submit_button_text: str = "Submit"
    ) -> FormResult:
        """
        Fill a form at the specified URL with provided field values.

        Args:
            url: The URL of the form page
            fields: List of FormField objects to fill
            submit: Whether to click submit after filling
            submit_button_text: Text of the submit button

        Returns:
            FormResult with success status and details
        """
        try:
            # Import here to avoid circular imports
            from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

            agent = AsyncDefaultAgent(max_steps=self.max_steps, model=self.model)

            # Build field instructions
            field_instructions = self._build_field_instructions(fields)

            instruction = f"""
            Navigate to {url} and fill out the form:

            {field_instructions}

            {"After filling all fields, click the '" + submit_button_text + "' button." if submit else ""}
            """

            completed = await agent.execute(
                instruction,
                action_handler=AsyncPyautoguiActionHandler(),
                image_provider=AsyncScreenshotMaker(),
            )

            return FormResult(
                success=completed,
                fields_filled=len(fields),
                errors=[]
            )

        except ImportError:
            return FormResult(
                success=False,
                fields_filled=0,
                errors=["oagi package not installed. Run: pip install oagi"]
            )
        except Exception as e:
            return FormResult(
                success=False,
                fields_filled=0,
                errors=[str(e)]
            )

    def _build_field_instructions(self, fields: list[FormField]) -> str:
        """Build instruction text for each field."""
        instructions = []
        for i, field in enumerate(fields, 1):
            if field.field_type == "checkbox":
                action = "check" if field.value else "uncheck"
                instructions.append(f"{i}. {action.capitalize()} the '{field.name}' checkbox")
            elif field.field_type == "dropdown":
                instructions.append(f"{i}. Select '{field.value}' from the '{field.name}' dropdown")
            elif field.field_type == "radio":
                instructions.append(f"{i}. Select the '{field.value}' radio option for '{field.name}'")
            else:
                instructions.append(f"{i}. Enter '{field.value}' in the '{field.name}' field")

        return "\n".join(instructions)

    async def fill_multiple_forms(
        self,
        form_configs: list[dict],
        delay_between: float = 1.0
    ) -> list[FormResult]:
        """
        Fill multiple forms sequentially.

        Args:
            form_configs: List of dicts with 'url' and 'fields' keys
            delay_between: Seconds to wait between forms

        Returns:
            List of FormResult for each form
        """
        results = []

        for config in form_configs:
            result = await self.fill_form(
                url=config["url"],
                fields=config["fields"],
                submit=config.get("submit", True)
            )
            results.append(result)
            await asyncio.sleep(delay_between)

        return results
