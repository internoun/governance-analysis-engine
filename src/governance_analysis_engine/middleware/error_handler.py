"""Error handling middleware for FastAPI."""

from typing import Final

from fastapi import Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import RequestResponseEndpoint


__all__ = ["error_handling_middleware"]

DEFAULT_ERROR_MESSAGE: Final = "Internal server error"
DEFAULT_ERROR_STATUS_CODE: Final = 500


async def error_handling_middleware(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    """Middleware that catches exceptions and returns standardized error responses.

    This middleware wraps all requests and catches any unhandled exceptions,
    returning a consistent JSON error response to the client.

    Args:
        request: The incoming HTTP request.
        call_next: The next middleware or route handler in the chain.

    Returns:
        The response from the next handler, or a standardized error response
        if an exception occurs.
    """
    try:
        return await call_next(request)
    except Exception:
        return JSONResponse(
            status_code=DEFAULT_ERROR_STATUS_CODE,
            content={"detail": DEFAULT_ERROR_MESSAGE},
        )
