from typing import Any

import httpx
import pytest

from governance_analysis_engine.clients.data_client import (
    DataClient,
    ExternalAPIError,
)

BASE_URL = "https://example.com"


class MockResponse:
    """Simple mock HTTP response object for testing."""

    def __init__(
        self,
        json_data: dict[str, Any] | None = None,
        raise_error: bool = False,
    ) -> None:
        self._json_data = json_data
        self._raise_error = raise_error

    def raise_for_status(self) -> None:
        if self._raise_error:
            raise httpx.HTTPError("HTTP error")

    def json(self) -> dict[str, Any]:
        if self._json_data is None:
            raise ValueError("Invalid JSON")
        return self._json_data


@pytest.fixture
def client() -> DataClient:
    """Return a DataClient instance for testing."""
    return DataClient(BASE_URL)


def test_fetch_data_success(
    monkeypatch: pytest.MonkeyPatch,
    client: DataClient,
) -> None:
    def mock_get(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse(json_data={"key": "value"})

    monkeypatch.setattr(httpx, "get", mock_get)

    result = client.fetch_data("test")

    assert result == {"key": "value"}


def test_fetch_data_http_error(
    monkeypatch: pytest.MonkeyPatch,
    client: DataClient,
) -> None:
    def mock_get(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse(raise_error=True)

    monkeypatch.setattr(httpx, "get", mock_get)

    with pytest.raises(ExternalAPIError):
        client.fetch_data("test")


def test_fetch_data_invalid_json(
    monkeypatch: pytest.MonkeyPatch,
    client: DataClient,
) -> None:
    def mock_get(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse(json_data=None)

    monkeypatch.setattr(httpx, "get", mock_get)

    with pytest.raises(ExternalAPIError):
        client.fetch_data("test")


def test_empty_endpoint_raises_value_error(
    client: DataClient,
) -> None:
    with pytest.raises(ValueError):
        client.fetch_data("")
