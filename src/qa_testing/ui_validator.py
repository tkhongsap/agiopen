"""
UI Validator - Verify UI elements and states.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class ValidationType(Enum):
    """Types of UI validation."""
    ELEMENT_EXISTS = "element_exists"
    ELEMENT_VISIBLE = "element_visible"
    ELEMENT_ENABLED = "element_enabled"
    TEXT_CONTAINS = "text_contains"
    TEXT_EQUALS = "text_equals"
    ELEMENT_COUNT = "element_count"
    PAGE_TITLE = "page_title"
    URL_CONTAINS = "url_contains"


@dataclass
class ValidationRule:
    """A validation rule to check."""
    validation_type: ValidationType
    target: str  # Element description or selector
    expected_value: Optional[str] = None
    timeout: int = 10


@dataclass
class ValidationResult:
    """Result of a validation check."""
    rule: ValidationRule
    passed: bool
    actual_value: Optional[str] = None
    error_message: Optional[str] = None
    screenshot_path: Optional[str] = None


class UIValidator:
    """
    Validate UI elements and states using Lux.

    Example:
        validator = UIValidator()

        result = await validator.validate(
            url="https://example.com",
            rules=[
                ValidationRule(ValidationType.ELEMENT_EXISTS, "Login button"),
                ValidationRule(ValidationType.TEXT_CONTAINS, "Welcome header", "Welcome"),
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

    async def validate(
        self,
        url: str,
        rules: list[ValidationRule]
    ) -> list[ValidationResult]:
        """
        Validate multiple rules on a page.

        Args:
            url: The URL to validate
            rules: List of ValidationRule to check

        Returns:
            List of ValidationResult for each rule
        """
        results = []

        try:
            from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

            agent = AsyncDefaultAgent(max_steps=self.max_steps, model=self.model)

            # Build validation instruction
            instruction = self._build_validation_instruction(url, rules)

            completed = await agent.execute(
                instruction,
                action_handler=AsyncPyautoguiActionHandler(),
                image_provider=AsyncScreenshotMaker(),
            )

            # In a real implementation, you would parse the results
            # This is a simplified example
            for rule in rules:
                results.append(ValidationResult(
                    rule=rule,
                    passed=completed,
                    actual_value=None,
                    error_message=None if completed else "Validation could not be completed"
                ))

        except ImportError:
            for rule in rules:
                results.append(ValidationResult(
                    rule=rule,
                    passed=False,
                    error_message="oagi package not installed. Run: pip install oagi"
                ))
        except Exception as e:
            for rule in rules:
                results.append(ValidationResult(
                    rule=rule,
                    passed=False,
                    error_message=str(e)
                ))

        return results

    def _build_validation_instruction(
        self,
        url: str,
        rules: list[ValidationRule]
    ) -> str:
        """Build validation instruction from rules."""
        parts = [
            f"Navigate to {url}",
            "Wait for page to fully load.",
            "",
            "Perform the following validations and report results:",
            ""
        ]

        for i, rule in enumerate(rules, 1):
            validation_text = self._get_validation_text(rule)
            parts.append(f"{i}. {validation_text}")

        parts.append("")
        parts.append("Report which validations passed and which failed.")

        return "\n".join(parts)

    def _get_validation_text(self, rule: ValidationRule) -> str:
        """Convert a validation rule to instruction text."""
        if rule.validation_type == ValidationType.ELEMENT_EXISTS:
            return f"Verify that '{rule.target}' exists on the page"
        elif rule.validation_type == ValidationType.ELEMENT_VISIBLE:
            return f"Verify that '{rule.target}' is visible on the page"
        elif rule.validation_type == ValidationType.ELEMENT_ENABLED:
            return f"Verify that '{rule.target}' is enabled (not disabled)"
        elif rule.validation_type == ValidationType.TEXT_CONTAINS:
            return f"Verify that '{rule.target}' contains text '{rule.expected_value}'"
        elif rule.validation_type == ValidationType.TEXT_EQUALS:
            return f"Verify that '{rule.target}' has exact text '{rule.expected_value}'"
        elif rule.validation_type == ValidationType.ELEMENT_COUNT:
            return f"Verify that there are {rule.expected_value} instances of '{rule.target}'"
        elif rule.validation_type == ValidationType.PAGE_TITLE:
            return f"Verify that page title contains '{rule.expected_value}'"
        elif rule.validation_type == ValidationType.URL_CONTAINS:
            return f"Verify that URL contains '{rule.expected_value}'"
        else:
            return f"Validate {rule.target}"

    async def check_element_exists(
        self,
        url: str,
        element_description: str
    ) -> ValidationResult:
        """Quick check if an element exists."""
        rule = ValidationRule(ValidationType.ELEMENT_EXISTS, element_description)
        results = await self.validate(url, [rule])
        return results[0]

    async def check_text_content(
        self,
        url: str,
        element_description: str,
        expected_text: str,
        exact_match: bool = False
    ) -> ValidationResult:
        """Check if an element contains specific text."""
        validation_type = ValidationType.TEXT_EQUALS if exact_match else ValidationType.TEXT_CONTAINS
        rule = ValidationRule(validation_type, element_description, expected_text)
        results = await self.validate(url, [rule])
        return results[0]

    async def visual_regression_check(
        self,
        url: str,
        baseline_screenshot: str,
        threshold: float = 0.95
    ) -> ValidationResult:
        """
        Compare current page to a baseline screenshot.

        Args:
            url: The URL to check
            baseline_screenshot: Path to baseline image
            threshold: Similarity threshold (0-1)

        Returns:
            ValidationResult with comparison details
        """
        try:
            from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker

            agent = AsyncDefaultAgent(max_steps=10, model=self.model)

            instruction = f"""
            Navigate to {url}
            Wait for page to fully load.
            Take a screenshot of the page.
            Compare the current page visually to the baseline at {baseline_screenshot}.
            Report if they match within {threshold*100}% similarity.
            """

            completed = await agent.execute(
                instruction,
                action_handler=AsyncPyautoguiActionHandler(),
                image_provider=AsyncScreenshotMaker(),
            )

            return ValidationResult(
                rule=ValidationRule(ValidationType.ELEMENT_EXISTS, "visual_regression"),
                passed=completed,
                actual_value=f"Compared to {baseline_screenshot}"
            )

        except Exception as e:
            return ValidationResult(
                rule=ValidationRule(ValidationType.ELEMENT_EXISTS, "visual_regression"),
                passed=False,
                error_message=str(e)
            )
