"""Tests for repository layer and service integration."""

import pytest

from governance_analysis_engine.repositories import InMemoryProposalRepository
from governance_analysis_engine.services.proposal_service import (
    Proposal,
    ProposalService,
)


def test_add_then_get_returns_proposal() -> None:
    """Test that add() followed by get() returns the stored proposal."""
    repository = InMemoryProposalRepository()
    proposal = Proposal(
        proposal_id="test-123",
        title="Test Proposal",
        body="Test body",
    )

    repository.add(proposal)
    result = repository.get("test-123")

    assert result is not None
    assert result.proposal_id == "test-123"
    assert result.title == "Test Proposal"
    assert result.body == "Test body"


def test_get_returns_none_for_missing_id() -> None:
    """Test that get() returns None when proposal ID does not exist."""
    repository = InMemoryProposalRepository()
    result = repository.get("non-existent-id")

    assert result is None


def test_service_returns_summary_when_proposal_exists() -> None:
    """Test that service returns summary when proposal exists in repository."""
    repository = InMemoryProposalRepository()
    service = ProposalService(repository)
    proposal = Proposal(
        proposal_id="test-123",
        title="Test Proposal",
        body="a" * 200,
    )

    repository.add(proposal)
    result = service.summarize("test-123")

    assert result.proposal_id == "test-123"
    assert len(result.summary) == 120


def test_service_raises_value_error_when_proposal_missing() -> None:
    """Test that service raises ValueError when proposal is not found."""
    repository = InMemoryProposalRepository()
    service = ProposalService(repository)

    with pytest.raises(ValueError, match="Proposal not found"):
        service.summarize("non-existent-id")
