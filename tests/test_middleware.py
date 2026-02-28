from fastapi import FastAPI
from fastapi.testclient import TestClient

from governance_analysis_engine.middleware.error_handler import (
    error_handling_middleware,
)


def create_test_app() -> FastAPI:
    app = FastAPI()
    app.middleware("http")(error_handling_middleware)

    @app.get("/force-error")
    def force_error() -> None:
        raise RuntimeError("unexpected")

    @app.get("/ok")
    def ok() -> dict[str, str]:
        return {"status": "ok"}

    return app


def test_middleware_handles_internal_error() -> None:
    app = create_test_app()
    client = TestClient(app)

    response = client.get("/force-error")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}


def test_middleware_allows_normal_requests() -> None:
    app = create_test_app()
    client = TestClient(app)

    response = client.get("/ok")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
