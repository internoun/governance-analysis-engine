"""Tests for CLI interface."""

import subprocess
import sys

from unittest.mock import patch

import pytest

from governance_analysis_engine.cli import main
from governance_analysis_engine.services.proposal_service import Proposal
from governance_analysis_engine.repositories.proposal_repository import (
    InMemoryProposalRepository,
)


class TestCLI:
    """Test suite for CLI functionality."""

    def test_cli_runs_with_valid_input(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that CLI runs successfully with valid proposal text."""
        test_args = ["cli.py", "This is a test proposal text"]
        with patch.object(sys, "argv", test_args):
            main()

        captured = capsys.readouterr()
        assert "This is a test proposal text" in captured.out

    def test_cli_handles_empty_input(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that CLI exits with error on empty input."""
        test_args = ["cli.py", "   "]
        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "cannot be empty" in captured.err

    def test_cli_respects_max_length_argument(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that --max-length argument truncates summary correctly."""
        long_text = "x" * 200
        test_args = ["cli.py", long_text, "--max-length", "50"]
        with patch.object(sys, "argv", test_args):
            main()

        captured = capsys.readouterr()
        assert len(captured.out.strip()) == 50

    def test_cli_custom_title_and_proposal_id(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test CLI with custom title and proposal ID."""
        test_args = [
            "cli.py",
            "Test body",
            "--title",
            "Custom Title",
            "--proposal-id",
            "custom-123",
        ]
        with patch.object(sys, "argv", test_args):
            main()

        captured = capsys.readouterr()
        assert "Test body" in captured.out

    def test_cli_repository_integration(self) -> None:
        """Test that CLI properly integrates with InMemoryProposalRepository."""
        repo = InMemoryProposalRepository()
        test_proposal = Proposal(
            proposal_id="test-id", title="Test Title", body="Test body content"
        )

        repo.add(test_proposal)
        retrieved = repo.get("test-id")

        assert retrieved is not None
        assert retrieved.proposal_id == "test-id"
        assert retrieved.title == "Test Title"
        assert retrieved.body == "Test body content"

    def test_cli_service_integration(self) -> None:
        """Test that CLI properly integrates with ProposalService."""
        from governance_analysis_engine.services.proposal_service import ProposalService

        repo = InMemoryProposalRepository()
        service = ProposalService(repo)

        proposal = Proposal(proposal_id="svc-test", title="Service", body="Test content")
        repo.add(proposal)

        summary = service.summarize("svc-test")

        assert summary.proposal_id == "svc-test"
        assert summary.summary == "Test content"

    def test_cli_as_module_subprocess(self) -> None:
        """Test CLI invocation via python -m module pattern."""
        import os

        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        src_path = os.path.join(repo_root, "src")

        result = subprocess.run(
            [sys.executable, "-m", "governance_analysis_engine", "subprocess test"],
            cwd=src_path,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "subprocess test" in result.stdout
