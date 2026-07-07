"""
Tests for the bundled demo fixture. No API key or network required.

These guard the one-command demo: if the sample transcript goes missing or
shrinks below the pipeline's minimum, `python -m src.demo` would fail for
anyone trying the repo, so catch it here instead.
"""

from src.demo import SAMPLE_TRANSCRIPT

# Mirror main.MIN_TRANSCRIPT_WORDS. Not imported directly because src.main pulls
# in the CrewAI stack, which these no-network tests shouldn't require.
MIN_TRANSCRIPT_WORDS = 50


def test_sample_transcript_is_bundled():
    assert SAMPLE_TRANSCRIPT.exists(), f"missing demo fixture: {SAMPLE_TRANSCRIPT}"


def test_sample_transcript_is_long_enough():
    words = len(SAMPLE_TRANSCRIPT.read_text(encoding="utf-8").split())
    assert words >= MIN_TRANSCRIPT_WORDS
