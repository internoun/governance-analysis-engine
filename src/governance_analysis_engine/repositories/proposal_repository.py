"""Repository for proposal data access."""

from typing import Protocol

from governance_analysis_engine.services.proposal_service import Proposal


class ProposalRepository(Protocol):
    """Repository abstraction for proposal data access."""

    def get(self, proposal_id: str) -> Proposal | None:
        """Retrieve a proposal by ID.

        Args:
            proposal_id: Unique identifier for the proposal.

        Returns:
            The proposal if found, None otherwise.
        """
        ...

    def add(self, proposal: Proposal) -> None:
        """Store a proposal.

        Args:
            proposal: The proposal to store.
        """
        ...


class InMemoryProposalRepository:
    """In-memory implementation of ProposalRepository."""

    def __init__(self) -> None:
        """Initialize an empty in-memory store."""
        self._store: dict[str, Proposal] = {}

    def get(self, proposal_id: str) -> Proposal | None:
        """Retrieve a proposal by ID.

        Args:
            proposal_id: Unique identifier for the proposal.

        Returns:
            The proposal if found, None otherwise.
        """
        return self._store.get(proposal_id)

    def add(self, proposal: Proposal) -> None:
        """Store a proposal.

        Args:
            proposal: The proposal to store.
        """
        self._store[proposal.proposal_id] = proposal
