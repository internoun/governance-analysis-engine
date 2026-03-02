"""Tests for custom exceptions."""

from governance_analysis_engine.exceptions import ExternalAPIError


def test_external_api_error_basic() -> None:
    """Test ExternalAPIError with just a message."""
    error = ExternalAPIError("API request failed")
    assert str(error) == "API request failed"
    assert error.original_error is None


def test_external_api_error_with_original_error() -> None:
    """Test ExternalAPIError with an original exception."""
    original = ValueError("invalid input")
    error = ExternalAPIError("API request failed", original)

    assert error.original_error is original
    assert "API request failed" in str(error)
    assert "ValueError" in str(error)
