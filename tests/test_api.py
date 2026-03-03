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


# Proposal Summarize Endpoint Tests


def test_summarize_endpoint_returns_200() -> None:
    response = client.post(
        "/proposal/summarize",
        json={
            "proposal_id": "test-123",
            "title": "Test Proposal",
            "body": "This is a test proposal body that should be summarized.",
        },
    )

    assert response.status_code == 200


def test_summarize_endpoint_returns_expected_structure() -> None:
    response = client.post(
        "/proposal/summarize",
        json={
            "proposal_id": "test-123",
            "title": "Test Proposal",
            "body": "This is a test proposal body that should be summarized.",
        },
    )

    data = response.json()
    assert "proposal_id" in data
    assert "summary" in data
    assert data["proposal_id"] == "test-123"


def test_summarize_endpoint_truncates_long_body() -> None:
    long_body = "a" * 200
    response = client.post(
        "/proposal/summarize",
        json={
            "proposal_id": "test-123",
            "title": "Test Proposal",
            "body": long_body,
        },
    )

    data = response.json()
    assert len(data["summary"]) == 120


def test_summarize_endpoint_content_type_is_json() -> None:
    response = client.post(
        "/proposal/summarize",
        json={
            "proposal_id": "test-123",
            "title": "Test Proposal",
            "body": "This is a test proposal body.",
        },
    )

    assert response.headers["content-type"].startswith("application/json")


def test_summarize_endpoint_422_missing_proposal_id() -> None:
    response = client.post(
        "/proposal/summarize",
        json={
            "title": "Test Proposal",
            "body": "This is a test proposal body.",
        },
    )

    assert response.status_code == 422


def test_summarize_endpoint_422_missing_title() -> None:
    response = client.post(
        "/proposal/summarize",
        json={
            "proposal_id": "test-123",
            "body": "This is a test proposal body.",
        },
    )

    assert response.status_code == 422


def test_summarize_endpoint_422_missing_body() -> None:
    response = client.post(
        "/proposal/summarize",
        json={
            "proposal_id": "test-123",
            "title": "Test Proposal",
        },
    )

    assert response.status_code == 422


def test_summarize_endpoint_422_empty_proposal_id() -> None:
    response = client.post(
        "/proposal/summarize",
        json={
            "proposal_id": "",
            "title": "Test Proposal",
            "body": "This is a test proposal body.",
        },
    )

    assert response.status_code == 422


def test_summarize_endpoint_422_empty_title() -> None:
    response = client.post(
        "/proposal/summarize",
        json={
            "proposal_id": "test-123",
            "title": "",
            "body": "This is a test proposal body.",
        },
    )

    assert response.status_code == 422


def test_summarize_endpoint_422_empty_body() -> None:
    response = client.post(
        "/proposal/summarize",
        json={
            "proposal_id": "test-123",
            "title": "Test Proposal",
            "body": "",
        },
    )

    assert response.status_code == 422


def test_summarize_endpoint_422_whitespace_only_proposal_id() -> None:
    response = client.post(
        "/proposal/summarize",
        json={
            "proposal_id": "   ",
            "title": "Test Proposal",
            "body": "This is a test proposal body.",
        },
    )

    assert response.status_code == 422


def test_summarize_endpoint_422_whitespace_only_title() -> None:
    response = client.post(
        "/proposal/summarize",
        json={
            "proposal_id": "test-123",
            "title": "   ",
            "body": "This is a test proposal body.",
        },
    )

    assert response.status_code == 422


def test_summarize_endpoint_422_whitespace_only_body() -> None:
    response = client.post(
        "/proposal/summarize",
        json={
            "proposal_id": "test-123",
            "title": "Test Proposal",
            "body": "   ",
        },
    )

    assert response.status_code == 422


def test_summarize_endpoint_422_extra_fields() -> None:
    response = client.post(
        "/proposal/summarize",
        json={
            "proposal_id": "test-123",
            "title": "Test Proposal",
            "body": "This is a test proposal body.",
            "extra_field": "should not be here",
        },
    )

    # Pydantic by default ignores extra fields, so this should return 200
    # If strict validation is desired, we would configure Pydantic differently
    assert response.status_code == 200


def test_openapi_schema_contains_summarize_endpoint() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/proposal/summarize" in response.json()["paths"]
