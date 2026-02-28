from fastapi import Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import RequestResponseEndpoint


async def error_handling_middleware(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    try:
        return await call_next(request)
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )
