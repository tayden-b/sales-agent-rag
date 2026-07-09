"""
Configuration loader. Reads .env and exposes validated settings.
"""

import os
import logging
from dotenv import load_dotenv

load_dotenv()

# --- Required ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# --- Email ---
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "")
EMAIL_TO = os.getenv("EMAIL_TO", "")
EMAIL_PREVIEW_MODE = os.getenv("EMAIL_PREVIEW_MODE", "true").lower() == "true"

# --- ChromaDB ---
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

# --- Logging ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# --- LLM ---
LLM_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"

# --- Pipeline ---
# Shortest transcript the pipeline will process. Lives here (not in main) so
# the demo and its tests can reference it without importing the CrewAI stack.
MIN_TRANSCRIPT_WORDS = 50


def validate_config() -> list[str]:
    """Check that required config values are set. Returns list of missing keys."""
    missing = []
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    if not EMAIL_PREVIEW_MODE:
        if not SENDGRID_API_KEY:
            missing.append("SENDGRID_API_KEY")
        if not EMAIL_FROM:
            missing.append("EMAIL_FROM")
        if not EMAIL_TO:
            missing.append("EMAIL_TO")
    return missing


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
