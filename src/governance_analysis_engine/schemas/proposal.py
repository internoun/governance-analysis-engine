"""Pydantic schemas for proposal-related requests and responses."""

from pydantic import BaseModel, Field, field_validator


class ProposalRequest(BaseModel):
    """Request model for creating or processing a proposal.

    Attributes:
        proposal_id: Unique identifier for the proposal.
        title: The title of the proposal.
        body: The full text content of the proposal.
    """

    proposal_id: str = Field(..., min_length=1, description="Unique identifier for the proposal")
    title: str = Field(..., min_length=1, max_length=500, description="The title of the proposal")
    body: str = Field(..., min_length=1, description="The full text content of the proposal")

    @field_validator("proposal_id", "title", "body")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Strip leading and trailing whitespace from string fields."""
        return v.strip()


class ProposalResponse(BaseModel):
    """Response model for proposal data.

    Attributes:
        proposal_id: Unique identifier for the proposal.
        title: The title of the proposal.
        summary: A summary of the proposal content.
    """

    proposal_id: str
    title: str
    summary: str


class SummarizeRequest(BaseModel):
    """Request model for the proposal summarization endpoint.

    Attributes:
        proposal_id: Unique identifier for the proposal.
        title: The title of the proposal.
        body: The full text content of the proposal to summarize.
    """

    proposal_id: str = Field(..., min_length=1, description="Unique identifier for the proposal")
    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="The title of the proposal",
    )
    body: str = Field(..., min_length=1, description="The full text content to summarize")

    @field_validator("proposal_id", "title", "body")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Strip leading and trailing whitespace from string fields."""
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return v.strip()


class SummarizeResponse(BaseModel):
    """Response model for proposal summarization.

    Attributes:
        proposal_id: Unique identifier for the proposal.
        summary: The summarized text of the proposal.
    """

    proposal_id: str
    summary: str
