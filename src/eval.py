"""
Extraction eval for the Transcript Analyzer.

Scores the analyzer's structured output for the bundled sample transcript
against hand-labeled gold data (``data/eval/gold_labels.json``): did it surface
the known technical concerns and action items, and did it read the sentiment
right.

Run it:

    python -m src.eval

With ``OPENAI_API_KEY`` set it runs the analyzer live on the sample transcript
and scores that. Without a key (CI, offline) it scores a recorded analyzer
output (``data/eval/sample_prediction.json``) so the harness and metrics stay
exercised without a network call. Exits non-zero when the score drops below the
thresholds, so it can gate CI.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

from src.schemas import TranscriptAnalysis

REPO_ROOT = Path(__file__).parent.parent
SAMPLE_TRANSCRIPT = REPO_ROOT / "data" / "sample_transcript.txt"
GOLD_PATH = REPO_ROOT / "data" / "eval" / "gold_labels.json"
PREDICTION_FIXTURE = REPO_ROOT / "data" / "eval" / "sample_prediction.json"

# Recall floors below which the eval fails. Precision on this transcript is
# expected to be high, but recall — did we catch the known concerns and
# actions — is the number that matters for extraction quality.
CONCERN_RECALL_MIN = 0.7
ACTION_RECALL_MIN = 0.6

Rubric = list[list[str]]


@dataclass
class FieldScore:
    label_total: int
    labels_found: int
    predicted_total: int
    predicted_matched: int

    @property
    def recall(self) -> float:
        return self.labels_found / self.label_total if self.label_total else 0.0

    @property
    def precision(self) -> float:
        return self.predicted_matched / self.predicted_total if self.predicted_total else 0.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if (p + r) else 0.0


@dataclass
class EvalReport:
    concerns: FieldScore
    action_items: FieldScore
    sentiment_expected: str
    sentiment_predicted: str
    source: str = ""
    missed_concerns: list[str] = field(default_factory=list)
    missed_actions: list[str] = field(default_factory=list)

    @property
    def sentiment_correct(self) -> bool:
        return self.sentiment_expected.lower() == self.sentiment_predicted.lower()

    @property
    def passed(self) -> bool:
        return (
            self.sentiment_correct
            and self.concerns.recall >= CONCERN_RECALL_MIN
            and self.action_items.recall >= ACTION_RECALL_MIN
        )


def _rubric_matches(rubric: Rubric, text: str) -> bool:
    """True when every keyword group has at least one synonym in ``text``."""
    text = text.lower()
    return all(any(syn.lower() in text for syn in group) for group in rubric)


def _score_field(gold_items: list[dict], predicted_texts: list[str]) -> tuple[FieldScore, list[str]]:
    labels_found = 0
    missed: list[str] = []
    for item in gold_items:
        if any(_rubric_matches(item["keywords"], text) for text in predicted_texts):
            labels_found += 1
        else:
            missed.append(item["label"])

    predicted_matched = sum(
        1
        for text in predicted_texts
        if any(_rubric_matches(item["keywords"], text) for item in gold_items)
    )

    score = FieldScore(
        label_total=len(gold_items),
        labels_found=labels_found,
        predicted_total=len(predicted_texts),
        predicted_matched=predicted_matched,
    )
    return score, missed


def score(prediction: TranscriptAnalysis, gold: dict) -> EvalReport:
    """Score one analyzer extraction against the gold labels."""
    concern_texts = [
        f"{c.concern} {c.context_quote}" for c in prediction.technical_concerns
    ]
    action_texts = [a.action for a in prediction.action_items]

    concerns, missed_concerns = _score_field(gold["technical_concerns"], concern_texts)
    actions, missed_actions = _score_field(gold["action_items"], action_texts)

    return EvalReport(
        concerns=concerns,
        action_items=actions,
        sentiment_expected=gold["sentiment"],
        sentiment_predicted=prediction.sentiment.value,
        missed_concerns=missed_concerns,
        missed_actions=missed_actions,
    )


def format_report(report: EvalReport) -> str:
    def pct(x: float) -> str:
        return f"{x * 100:5.1f}%"

    c, a = report.concerns, report.action_items
    lines = [
        "=" * 64,
        f"Transcript Analyzer — extraction eval ({report.source})",
        "=" * 64,
        f"Technical concerns  recall {pct(c.recall)}  precision {pct(c.precision)}  "
        f"f1 {pct(c.f1)}   ({c.labels_found}/{c.label_total} labels, {c.predicted_total} predicted)",
        f"Action items        recall {pct(a.recall)}  precision {pct(a.precision)}  "
        f"f1 {pct(a.f1)}   ({a.labels_found}/{a.label_total} labels, {a.predicted_total} predicted)",
        f"Sentiment           {report.sentiment_predicted} (expected {report.sentiment_expected}) — "
        f"{'correct' if report.sentiment_correct else 'WRONG'}",
    ]
    if report.missed_concerns:
        lines.append("Missed concerns:")
        lines.extend(f"  - {m}" for m in report.missed_concerns)
    if report.missed_actions:
        lines.append("Missed action items:")
        lines.extend(f"  - {m}" for m in report.missed_actions)
    lines.append("-" * 64)
    lines.append("RESULT: " + ("PASS" if report.passed else "FAIL"))
    lines.append("=" * 64)
    return "\n".join(lines)


def load_gold() -> dict:
    return json.loads(GOLD_PATH.read_text(encoding="utf-8"))


def load_fixture_prediction() -> TranscriptAnalysis:
    data = json.loads(PREDICTION_FIXTURE.read_text(encoding="utf-8"))
    data = {k: v for k, v in data.items() if not k.startswith("_")}
    return TranscriptAnalysis(**data)


def _live_prediction() -> TranscriptAnalysis:
    # Imported here so the offline path never pulls in the CrewAI stack.
    from src.crew.pipeline import run_analyzer

    transcript = SAMPLE_TRANSCRIPT.read_text(encoding="utf-8")
    return run_analyzer(transcript)


def main() -> int:
    gold = load_gold()
    if os.getenv("OPENAI_API_KEY"):
        prediction = _live_prediction()
        source = "live analyzer run"
    else:
        prediction = load_fixture_prediction()
        source = "recorded fixture — no OPENAI_API_KEY set"

    report = score(prediction, gold)
    report.source = source
    print(format_report(report))
    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
