"""Service for processing governance proposals."""

from dataclasses import dataclass
from typing import Protocol


__all__ = ["Proposal", "ProposalSummary", "summarize_proposal", "ProposalService"]


DEFAULT_SUMMARY_LENGTH: int = 120


@dataclass(frozen=True)
class Proposal:
    """A governance proposal.

    Attributes:
        proposal_id: Unique identifier for the proposal.
        title: The title of the proposal.
        body: The full text content of the proposal.
    """

    proposal_id: str
    title: str
    body: str


@dataclass(frozen=True)
class ProposalSummary:
    """A summary of a governance proposal.

    Attributes:
        proposal_id: Unique identifier for the proposal.
        summary: The summarized text of the proposal.
    """

    proposal_id: str
    summary: str


class ProposalRepository(Protocol):
    """Repository abstraction for proposal data access."""

    def get(self, proposal_id: str) -> Proposal | None: ...
    def add(self, proposal: Proposal) -> None: ...


def summarize_proposal(
    proposal: Proposal, max_length: int = DEFAULT_SUMMARY_LENGTH
) -> ProposalSummary:
    """Generate a deterministic summary of a proposal.

    The current implementation truncates the proposal body to the specified
    maximum length. In production, this would integrate with an LLM or other
    summarization service.

    Args:
        proposal: The proposal to summarize.
        max_length: Maximum length of the summary in characters.

    Returns:
        A ProposalSummary containing the truncated proposal body.
    """
    summary: str = proposal.body[:max_length]

    return ProposalSummary(
        proposal_id=proposal.proposal_id,
        summary=summary,
    )


class ProposalService:
    """Service for managing and summarizing proposals."""

    def __init__(self, repository: ProposalRepository) -> None:
        """Initialize the service with a repository.

        Args:
            repository: The repository for proposal data access.
        """
        self._repository = repository

    def summarize(
        self, proposal_id: str, max_length: int = DEFAULT_SUMMARY_LENGTH
    ) -> ProposalSummary:
        """Summarize a proposal by ID.

        Args:
            proposal_id: Unique identifier for the proposal.
            max_length: Maximum length of the summary in characters.

        Returns:
            A ProposalSummary containing the summarized proposal.

        Raises:
            ValueError: If the proposal is not found.
        """
        proposal = self._repository.get(proposal_id)
        if proposal is None:
            raise ValueError("Proposal not found")
        return summarize_proposal(proposal, max_length)

    def add_proposal(self, proposal: Proposal) -> None:
        """Add a proposal to the repository.

        Args:
            proposal: The proposal to add.
        """
        self._repository.add(proposal)
