"""FastAPI application for the governance analysis engine."""

from fastapi import FastAPI
from pydantic import BaseModel

from governance_analysis_engine.config import configure_logging, settings
from governance_analysis_engine.middleware.error_handler import (
    error_handling_middleware,
)
from governance_analysis_engine.services.proposal_service import (
    Proposal,
    summarize_proposal,
)


__all__ = ["app", "HealthResponse", "MessageResponse", "health_check", "get_info", "summarize"]


configure_logging(settings.log_level)

app: FastAPI = FastAPI()
app.middleware("http")(error_handling_middleware)


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str


class MessageResponse(BaseModel):
    """Generic message response model."""

    message: str


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Health check endpoint.

    Returns:
        A response indicating the service is healthy.
    """
    return HealthResponse(status="ok")


@app.get("/info", response_model=MessageResponse)
def get_info() -> MessageResponse:
    """Get application information.

    Returns:
        A response with the application name and status.
    """
    return MessageResponse(message=f"{settings.app_name} running")


@app.post("/proposal/summarize")
def summarize(input_data: MessageResponse) -> MessageResponse:
    """Summarize a governance proposal.

    Args:
        input_data: The proposal text to summarize.

    Returns:
        A summary of the proposal.
    """
    proposal: Proposal = Proposal(
        proposal_id="static-id",
        title="",
        body=input_data.message,
    )

    result = summarize_proposal(proposal)

    return MessageResponse(message=result.summary)
