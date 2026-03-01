"""Service for processing governance proposals."""

from dataclasses import dataclass


__all__ = ["Proposal", "ProposalSummary", "summarize_proposal"]


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
