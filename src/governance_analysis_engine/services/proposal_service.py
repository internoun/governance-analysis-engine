from dataclasses import dataclass


@dataclass
class Proposal:
    proposal_id: str
    title: str
    body: str


@dataclass
class ProposalSummary:
    proposal_id: str
    summary: str


def summarize_proposal(proposal: Proposal) -> ProposalSummary:
    """
    Generate a deterministic summary of a proposal.
    """
    summary = proposal.body[:120]

    return ProposalSummary(
        proposal_id=proposal.proposal_id,
        summary=summary,
    )
