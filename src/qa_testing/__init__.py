"""
QA Testing Module

Provides tools for automated UI testing:
- Test runner for UI test sequences
- UI validator for element verification
"""

from .test_runner import TestRunner, TestCase, TestResult
from .ui_validator import UIValidator, ValidationResult

__all__ = ["TestRunner", "TestCase", "TestResult", "UIValidator", "ValidationResult"]
