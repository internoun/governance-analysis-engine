"""Configuration management for the application.

This module provides a centralized settings class using pydantic-settings
for environment-based configuration management.
"""

import logging
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["Settings", "configure_logging", "settings"]


class Settings(BaseSettings):
    """Application configuration settings.

    Settings can be overridden via environment variables or a .env file.
    """

    app_name: str = "governance-analysis-engine"
    log_level: str = "INFO"

    model_config: SettingsConfigDict = SettingsConfigDict(  # type: ignore[misc]
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def configure_logging(log_level: str = "INFO") -> None:
    """Configure the root logger with the specified level.

    Args:
        log_level: The logging level (e.g., "DEBUG", "INFO", "WARNING").

    Raises:
        ValueError: If an invalid log level is provided.
    """
    level: int | str = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


# Global settings instance
settings: Final[Settings] = Settings()
