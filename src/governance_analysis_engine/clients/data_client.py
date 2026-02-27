from typing import Any, cast
import httpx
from governance_analysis_engine.exceptions import ExternalAPIError


class DataClient:
    """HTTP client wrapper for external governance data sources."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def fetch_data(self, endpoint: str) -> dict[str, Any]:
        if not endpoint:
            raise ValueError("endpoint must not be empty")

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = httpx.get(url, timeout=5.0)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ExternalAPIError(str(exc)) from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise ExternalAPIError("Invalid JSON response") from exc

        return cast(dict[str, Any], data)
