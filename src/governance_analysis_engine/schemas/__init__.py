"""Request and response schemas for the governance analysis API."""

from governance_analysis_engine.schemas.proposal import (
    ProposalRequest,
    ProposalResponse,
    SummarizeRequest,
    SummarizeResponse,
)

__all__ = [
    "ProposalRequest",
    "ProposalResponse",
    "SummarizeRequest",
    "SummarizeResponse",
]
