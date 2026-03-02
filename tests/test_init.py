"""Tests for the governance_analysis_engine package initialization."""

from governance_analysis_engine import __version__, settings


def test_package_version() -> None:
    """Test that the package has a valid version string."""
    assert __version__ is not None
    assert isinstance(__version__, str)


def test_settings_is_exported() -> None:
    """Test that settings is exported from the package."""
    assert settings is not None
