from fastapi import FastAPI
from pydantic import BaseModel

from governance_analysis_engine.services.proposal_service import (
    Proposal,
    summarize_proposal,
)

app = FastAPI()


class HealthResponse(BaseModel):
    status: str


class MessageResponse(BaseModel):
    message: str


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/info", response_model=MessageResponse)
def get_info() -> MessageResponse:
    return MessageResponse(message="governance-analysis-engine running")


@app.post("/proposal/summarize")
def summarize(input_data: MessageResponse) -> MessageResponse:
    proposal = Proposal(
        proposal_id="static-id",
        title="",
        body=input_data.message,
    )

    result = summarize_proposal(proposal)

    return MessageResponse(message=result.summary)
