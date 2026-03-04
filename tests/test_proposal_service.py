from governance_analysis_engine.services.proposal_service import (
    Proposal,
    summarize_proposal,
)


def test_summary_truncates_body() -> None:
    proposal = Proposal(
        proposal_id="1",
        title="Test",
        body="a" * 200,
    )

    result = summarize_proposal(proposal)

    assert len(result.summary) == 120


def test_summary_with_empty_body() -> None:
    """Test summarization with empty body."""
    proposal = Proposal(
        proposal_id="empty",
        title="Empty Proposal",
        body="",
    )

    result = summarize_proposal(proposal)

    assert result.summary == ""
    assert result.proposal_id == "empty"
