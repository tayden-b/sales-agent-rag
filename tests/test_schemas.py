"""
Tests for the Transcript Analyzer output schema. No API key or network required.

These guard the agent boundary: the analyzer's job is to hand downstream a
structurally valid extraction, and these check that valid payloads parse and
malformed ones raise instead of slipping through.
"""

import pytest
from pydantic import ValidationError

from src.schemas import (
    AccountStage,
    ActionItem,
    Priority,
    Sentiment,
    Severity,
    TechnicalConcern,
    TranscriptAnalysis,
)


def _valid_payload():
    return {
        "account_name": "Acme Corp",
        "call_date": "2026-02-06",
        "account_stage": "Evaluation",
        "products_discussed": ["Vault", "Terraform"],
        "technical_concerns": [
            {
                "concern": "Secret sprawl across teams",
                "context_quote": "We have API keys in a dozen places.",
                "severity": "high",
            }
        ],
        "pain_points": ["Manual rotation"],
        "competitors_mentioned": ["CyberArk"],
        "action_items": [
            {"action": "Send HA reference architecture", "owner": "SE", "priority": "high"}
        ],
        "sentiment": "Positive",
        "key_quotes": ["This could save us a lot of time."],
    }


class TestValidExtraction:
    def test_full_payload_parses(self):
        analysis = TranscriptAnalysis(**_valid_payload())
        assert analysis.account_name == "Acme Corp"
        assert analysis.account_stage is AccountStage.evaluation
        assert analysis.sentiment is Sentiment.positive
        assert analysis.technical_concerns[0].severity is Severity.high
        assert analysis.action_items[0].priority is Priority.high

    def test_optional_lists_default_empty(self):
        analysis = TranscriptAnalysis(
            account_name="Beta", account_stage="POC", sentiment="Neutral"
        )
        assert analysis.products_discussed == []
        assert analysis.technical_concerns == []
        assert analysis.call_date == "unknown"

    def test_poc_stage_preserved(self):
        analysis = TranscriptAnalysis(
            account_name="Beta", account_stage="POC", sentiment="Neutral"
        )
        assert analysis.account_stage is AccountStage.poc


class TestCaseInsensitiveEnums:
    def test_stage_and_sentiment_any_casing(self):
        analysis = TranscriptAnalysis(
            account_name="Gamma", account_stage="discovery", sentiment="POSITIVE"
        )
        assert analysis.account_stage is AccountStage.discovery
        assert analysis.sentiment is Sentiment.positive

    def test_severity_any_casing(self):
        concern = TechnicalConcern(concern="x", severity="HIGH")
        assert concern.severity is Severity.high


class TestMalformedExtractionRaises:
    def test_missing_required_field(self):
        payload = _valid_payload()
        del payload["account_name"]
        with pytest.raises(ValidationError):
            TranscriptAnalysis(**payload)

    def test_invalid_severity_value(self):
        with pytest.raises(ValidationError):
            TechnicalConcern(concern="x", severity="critical")

    def test_invalid_account_stage(self):
        payload = _valid_payload()
        payload["account_stage"] = "Closed Won"
        with pytest.raises(ValidationError):
            TranscriptAnalysis(**payload)

    def test_nested_concern_missing_field(self):
        payload = _valid_payload()
        payload["technical_concerns"] = [{"context_quote": "no concern or severity"}]
        with pytest.raises(ValidationError):
            TranscriptAnalysis(**payload)


class TestActionItemDefaults:
    def test_owner_defaults_when_absent(self):
        item = ActionItem(action="Follow up", priority="medium")
        assert item.owner == "unassigned"
        assert item.priority is Priority.medium
