"""HTTP client for fetching external governance data."""

from typing import Any, Final

import httpx

from governance_analysis_engine.exceptions import ExternalAPIError


__all__ = ["DataClient"]


DEFAULT_TIMEOUT: Final = 5.0


class DataClient:
    """HTTP client wrapper for external governance data sources.

    This client provides a simplified interface for fetching JSON data from
    REST APIs with consistent error handling.

    Example:
        >>> client = DataClient("https://api.example.com")
        >>> data = client.fetch_data("proposals/123")
    """

    def __init__(self, base_url: str) -> None:
        """Initialize the data client.

        Args:
            base_url: The base URL of the external API.
        """
        self.base_url: str = base_url.rstrip("/")

    def fetch_data(self, endpoint: str, timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
        """Fetch JSON data from an external API endpoint.

        Args:
            endpoint: Path segment of the API endpoint.
            timeout: Request timeout in seconds.

        Returns:
            Parsed JSON response as a dictionary.

        Raises:
            ValueError: If endpoint is empty.
            ExternalAPIError: If HTTP request or JSON parsing fails.
        """
        if not endpoint:
            raise ValueError("endpoint must not be empty")

        url: str = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response: httpx.Response = httpx.get(url, timeout=timeout)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ExternalAPIError(str(exc)) from exc

        try:
            data = response.json()
            if not isinstance(data, dict):
                raise ExternalAPIError("Expected JSON object response")
        except ValueError as exc:
            raise ExternalAPIError("Invalid JSON response") from exc

        return data
