"""CLI interface for governance analysis engine."""

import argparse
import sys

from governance_analysis_engine.services.proposal_service import (
    DEFAULT_SUMMARY_LENGTH,
    Proposal,
    ProposalService,
)
from governance_analysis_engine.repositories.proposal_repository import (
    InMemoryProposalRepository,
)


def main() -> None:
    """Run the CLI application.

    Parses command-line arguments, creates a proposal from the input,
    and prints a summary to stdout.
    """
    parser = argparse.ArgumentParser(
        description="Governance analysis CLI for proposal summarization"
    )
    parser.add_argument(
        "text",
        help="Proposal text to summarize",
    )
    parser.add_argument(
        "--title",
        default="CLI Proposal",
        help="Proposal title (default: CLI Proposal)",
    )
    parser.add_argument(
        "--proposal-id",
        default="cli",
        help="Proposal ID (default: cli)",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=DEFAULT_SUMMARY_LENGTH,
        help=f"Maximum summary length in characters (default: {DEFAULT_SUMMARY_LENGTH})",
    )

    args = parser.parse_args()

    # Validate text is not empty after stripping
    text = args.text.strip()
    if not text:
        print("Error: Proposal text cannot be empty", file=sys.stderr)
        sys.exit(1)

    repo = InMemoryProposalRepository()
    service = ProposalService(repo)

    proposal = Proposal(
        proposal_id=args.proposal_id,
        title=args.title,
        body=text,
    )

    repo.add(proposal)

    summary = service.summarize(args.proposal_id, max_length=args.max_length)

    print(summary.summary)


if __name__ == "__main__":
    main()
