"""
Configuration management for Lux automation.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration for Lux API and automation settings."""

    api_key: str
    base_url: str = "https://api.agiopen.org"
    timeout: int = 30
    max_retries: int = 3
    verbose: bool = False

    # Image settings
    max_image_width: int = 1920
    max_image_height: int = 1080
    image_quality: int = 85
    image_format: str = "png"

    # Action settings
    mouse_move_duration: float = 0.3
    click_delay: float = 0.1
    type_interval: float = 0.05

    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        api_key = os.getenv("OAGI_API_KEY")
        if not api_key:
            raise ValueError(
                "OAGI_API_KEY environment variable is required. "
                "Get your API key from https://developer.agiopen.org"
            )

        return cls(
            api_key=api_key,
            base_url=os.getenv("OAGI_BASE_URL", "https://api.agiopen.org"),
            timeout=int(os.getenv("OAGI_TIMEOUT", "30")),
            max_retries=int(os.getenv("OAGI_MAX_RETRIES", "3")),
            verbose=os.getenv("OAGI_VERBOSE", "false").lower() == "true",
        )


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config.from_env()
    return _config


def set_config(config: Config) -> None:
    """Set the global configuration instance."""
    global _config
    _config = config
