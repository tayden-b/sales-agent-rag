"""
Tests for the extraction eval. No API key or network required.

These score the recorded prediction fixture against the gold labels so the
matching logic and metrics are checked deterministically, and bracket the range
with a full-coverage prediction (perfect recall) and an empty one (zero recall).
"""

from src.eval import (
    ACTION_RECALL_MIN,
    CONCERN_RECALL_MIN,
    load_fixture_prediction,
    load_gold,
    score,
)
from src.schemas import TranscriptAnalysis


def _prediction_covering(gold: dict) -> TranscriptAnalysis:
    """A prediction whose text contains every synonym of every gold rubric, so
    each label is guaranteed to match — an upper bound on recall."""
    concerns = []
    for c in gold["technical_concerns"]:
        text = " ".join(syn for group in c["keywords"] for syn in group)
        concerns.append({"concern": text, "context_quote": "", "severity": "medium"})
    actions = []
    for a in gold["action_items"]:
        text = " ".join(syn for group in a["keywords"] for syn in group)
        actions.append({"action": text, "priority": "medium"})
    return TranscriptAnalysis(
        account_name="X",
        account_stage="Discovery",
        sentiment=gold["sentiment"],
        technical_concerns=concerns,
        action_items=actions,
    )


def test_gold_labels_present():
    gold = load_gold()
    assert gold["technical_concerns"]
    assert gold["action_items"]
    assert gold["sentiment"]


def test_recorded_prediction_passes_thresholds():
    report = score(load_fixture_prediction(), load_gold())
    assert report.sentiment_correct
    assert report.concerns.recall >= CONCERN_RECALL_MIN
    assert report.action_items.recall >= ACTION_RECALL_MIN
    assert report.passed


def test_recorded_prediction_metrics_are_stable():
    report = score(load_fixture_prediction(), load_gold())
    # The fixture deliberately misses the cost concern and the Terraform action
    # item, so recall is high but not perfect and every prediction is on-target.
    assert report.concerns.labels_found == report.concerns.label_total - 1
    assert report.action_items.labels_found == report.action_items.label_total - 1
    assert report.concerns.precision == 1.0
    assert report.action_items.precision == 1.0
    assert "cost" in " ".join(report.missed_concerns).lower()
    assert "terraform" in " ".join(report.missed_actions).lower()


def test_full_coverage_scores_perfect_recall():
    gold = load_gold()
    report = score(_prediction_covering(gold), gold)
    assert report.concerns.recall == 1.0
    assert report.action_items.recall == 1.0
    assert report.sentiment_correct


def test_empty_prediction_scores_zero_recall():
    gold = load_gold()
    empty = TranscriptAnalysis(
        account_name="X", account_stage="Discovery", sentiment="Neutral"
    )
    report = score(empty, gold)
    assert report.concerns.recall == 0.0
    assert report.action_items.recall == 0.0
    assert not report.passed
