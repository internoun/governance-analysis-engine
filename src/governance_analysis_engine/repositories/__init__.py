"""Repository layer for data access."""

from governance_analysis_engine.repositories.proposal_repository import (
    InMemoryProposalRepository,
    ProposalRepository,
)

__all__ = ["ProposalRepository", "InMemoryProposalRepository"]
