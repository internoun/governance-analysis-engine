"""FastAPI application for the governance analysis engine."""

from fastapi import FastAPI
from pydantic import BaseModel

from governance_analysis_engine.config import configure_logging, settings
from governance_analysis_engine.middleware.error_handler import (
    error_handling_middleware,
)
from governance_analysis_engine.repositories import InMemoryProposalRepository
from governance_analysis_engine.schemas import SummarizeRequest, SummarizeResponse
from governance_analysis_engine.services.proposal_service import (
    Proposal,
    ProposalService,
)


__all__ = [
    "app",
    "HealthResponse",
    "MessageResponse",
    "SummarizeRequest",
    "SummarizeResponse",
    "health_check",
    "get_info",
    "summarize",
]


configure_logging(settings.log_level)

app: FastAPI = FastAPI()
app.middleware("http")(error_handling_middleware)

# Instantiate repository and service
_repository = InMemoryProposalRepository()
_proposal_service = ProposalService(_repository)


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


@app.post("/proposal/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest) -> SummarizeResponse:
    """Summarize a governance proposal.

    Args:
        request: The proposal data to summarize.

    Returns:
        A summary of the proposal.
    """
    proposal = Proposal(
        proposal_id=request.proposal_id,
        title=request.title,
        body=request.body,
    )

    # Store proposal for retrieval
    _proposal_service.add_proposal(proposal)

    # Generate summary using the service
    result = _proposal_service.summarize(proposal.proposal_id)

    return SummarizeResponse(
        proposal_id=result.proposal_id,
        summary=result.summary,
    )
