import pytest
import httpx
from governance_analysis_engine.clients.data_client import (
    DataClient,
    ExternalAPIError,
)


class MockResponse:
    def __init__(self, json_data=None, raise_error=False):
        self._json_data = json_data
        self._raise_error = raise_error

    def raise_for_status(self) -> None:
        if self._raise_error:
            raise httpx.HTTPError("HTTP error")

    def json(self):
        if self._json_data is None:
            raise ValueError("Invalid JSON")
        return self._json_data


def test_fetch_data_success(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_get(*args, **kwargs):
        return MockResponse(json_data={"key": "value"})

    monkeypatch.setattr(httpx, "get", mock_get)

    client = DataClient("https://example.com")
    result = client.fetch_data("test")

    assert result == {"key": "value"}


def test_fetch_data_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_get(*args, **kwargs):
        return MockResponse(raise_error=True)

    monkeypatch.setattr(httpx, "get", mock_get)

    client = DataClient("https://example.com")

    with pytest.raises(ExternalAPIError):
        client.fetch_data("test")


def test_fetch_data_invalid_json(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_get(*args, **kwargs):
        return MockResponse(json_data=None)

    monkeypatch.setattr(httpx, "get", mock_get)

    client = DataClient("https://example.com")

    with pytest.raises(ExternalAPIError):
        client.fetch_data("test")


def test_empty_endpoint_raises_value_error() -> None:
    client = DataClient("https://example.com")

    with pytest.raises(ValueError):
        client.fetch_data("")
