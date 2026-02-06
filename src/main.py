"""
CLI entry point for the Sales Call Intelligence System.

Usage:
    python -m src.main --file path/to/transcript.txt
    python -m src.main --paste
"""

import argparse
import logging
import sys
from pathlib import Path

from src.config import validate_config, setup_logging
from src.crew.pipeline import run_pipeline
from src.email.templates import build_html_email, build_email_subject
from src.email.sender import send_email

logger = logging.getLogger(__name__)

MIN_TRANSCRIPT_WORDS = 50


def read_transcript_from_file(file_path: str) -> str:
    """Read transcript text from a file."""
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    if not path.is_file():
        print(f"Error: Not a file: {file_path}")
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    return text


def read_transcript_from_stdin() -> str:
    """Read transcript text from interactive paste."""
    print("Paste your call transcript below. Press Ctrl+D (Unix) or Ctrl+Z (Windows) when done:\n")
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    return "\n".join(lines)


def validate_transcript(text: str) -> bool:
    """Check that the transcript has enough content to analyze."""
    word_count = len(text.split())
    if word_count < MIN_TRANSCRIPT_WORDS:
        print(f"Error: Transcript is too short ({word_count} words). Minimum is {MIN_TRANSCRIPT_WORDS} words.")
        return False
    if word_count > 50000:
        print(f"Warning: Transcript is very long ({word_count} words). Processing may take longer than usual.")
    return True


def main():
    """Main entry point."""
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Sales Call Intelligence System — Analyze call transcripts and generate email summaries."
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--file", "-f", help="Path to a transcript text file")
    input_group.add_argument("--paste", "-p", action="store_true", help="Paste transcript interactively")

    args = parser.parse_args()

    # Validate configuration
    missing = validate_config()
    if missing:
        print(f"Error: Missing required configuration: {', '.join(missing)}")
        print("Copy .env.example to .env and fill in the required values.")
        sys.exit(1)

    # Read transcript
    if args.file:
        transcript = read_transcript_from_file(args.file)
    else:
        transcript = read_transcript_from_stdin()

    # Validate transcript
    if not validate_transcript(transcript):
        sys.exit(1)

    word_count = len(transcript.split())
    print(f"\nProcessing transcript ({word_count} words)...")
    print("This typically takes 1-3 minutes.\n")

    # Run the pipeline
    try:
        result = run_pipeline(transcript)
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        print(f"\nError: Pipeline failed — {e}")
        print("Check logs for details. Common issues: invalid API key, rate limits, network errors.")
        sys.exit(1)

    if not result["success"]:
        print("\nPipeline completed with errors. Check logs for details.")
        sys.exit(1)

    # Build and send email
    email_body = result["email_body"]
    email_subject = result["email_subject"]

    # Extract account name and date from subject for template
    parts = email_subject.replace("Call Summary: ", "").split(" - ", 1)
    account_name = parts[0] if parts else "Customer"
    call_date = parts[1] if len(parts) > 1 else "Unknown"

    html_email = build_html_email(email_body, account_name, call_date)

    success = send_email(
        subject=email_subject,
        html_content=html_email,
        plain_text=email_body,
    )

    if success:
        print("\nDone! Email summary generated successfully.")
    else:
        print("\nWarning: Email sending failed. The analysis was still completed.")
        print("Check your SendGrid configuration or enable EMAIL_PREVIEW_MODE=true in .env")


if __name__ == "__main__":
    main()
