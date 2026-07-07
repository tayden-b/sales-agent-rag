"""
One-command demo.

Runs the full pipeline on a bundled sample transcript so the repo shows what it
does without you supplying your own call data. Email defaults to preview mode,
so the generated summary prints to the console and nothing is sent.

Usage:
    python -m src.demo
"""

import sys
from pathlib import Path

from src.config import validate_config, setup_logging

REPO_ROOT = Path(__file__).parent.parent
SAMPLE_TRANSCRIPT = REPO_ROOT / "data" / "sample_transcript.txt"


def main():
    setup_logging()

    if not SAMPLE_TRANSCRIPT.exists():
        print(f"Error: bundled sample transcript is missing at {SAMPLE_TRANSCRIPT}")
        sys.exit(1)

    print("=" * 70)
    print("Sales Call Intelligence — demo")
    print(f"Running the full pipeline on the bundled transcript:\n  {SAMPLE_TRANSCRIPT.relative_to(REPO_ROOT)}")
    print("=" * 70)

    missing = validate_config()
    if missing:
        print(f"\nThe demo runs the real pipeline, so it needs: {', '.join(missing)}")
        print("Copy .env.example to .env, add your OPENAI_API_KEY, and run it again.")
        print("Email stays in preview mode by default, so no SendGrid key is required.")
        sys.exit(1)

    transcript = SAMPLE_TRANSCRIPT.read_text(encoding="utf-8")

    # Imported here so the checks above can run without the heavier pipeline deps.
    from src.main import process_transcript

    if not process_transcript(transcript):
        sys.exit(1)


if __name__ == "__main__":
    main()
