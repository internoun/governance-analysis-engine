"""Business logic services."""

from governance_analysis_engine.services.proposal_service import (
    Proposal,
    ProposalSummary,
    summarize_proposal,
)

__all__ = ["Proposal", "ProposalSummary", "summarize_proposal"]
