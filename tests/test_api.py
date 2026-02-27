from fastapi.testclient import TestClient
from governance_analysis_engine.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_info_endpoint_returns_expected_message() -> None:
    response = client.get("/info")

    assert response.status_code == 200
    assert response.json() == {"message": "governance-analysis-engine running"}


def test_info_endpoint_content_type_is_json() -> None:
    response = client.get("/info")

    assert response.headers["content-type"].startswith("application/json")


def test_invalid_route_returns_404() -> None:
    response = client.get("/non-existent-route")

    assert response.status_code == 404


def test_openapi_schema_contains_info_endpoint() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/info" in response.json()["paths"]


def test_health_response_structure() -> None:
    response = client.get("/health")

    assert isinstance(response.json()["status"], str)
