"""
Pydantic schemas for what the Transcript Analyzer hands downstream.

The analyzer extracts intelligence from a call as JSON. Validating that JSON
against these models at the task boundary means a malformed extraction — a
missing field, a bad severity value, the wrong type — fails loudly right here
instead of silently poisoning the email four agents later.
"""

from enum import Enum

from pydantic import BaseModel, Field, field_validator


def _coerce_enum(enum_cls, value):
    """Match a string to an enum member case-insensitively by value.

    The LLM is asked for lowercase severities and title-case stages, but it
    doesn't always comply. We accept any casing here and let Pydantic raise if
    the value genuinely isn't one of the allowed options.
    """
    if isinstance(value, str):
        for member in enum_cls:
            if member.value.lower() == value.strip().lower():
                return member
    return value


class Severity(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class Priority(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class AccountStage(str, Enum):
    discovery = "Discovery"
    evaluation = "Evaluation"
    poc = "POC"
    negotiation = "Negotiation"
    renewal = "Renewal"
    expansion = "Expansion"


class Sentiment(str, Enum):
    positive = "Positive"
    neutral = "Neutral"
    cautious = "Cautious"
    negative = "Negative"


class TechnicalConcern(BaseModel):
    concern: str = Field(..., description="Brief description of the concern")
    context_quote: str = Field("", description="What the customer said")
    severity: Severity

    @field_validator("severity", mode="before")
    @classmethod
    def _normalize_severity(cls, v):
        return _coerce_enum(Severity, v)


class ActionItem(BaseModel):
    action: str = Field(..., description="What needs to be done")
    owner: str = Field("unassigned", description="Who should do it")
    priority: Priority

    @field_validator("priority", mode="before")
    @classmethod
    def _normalize_priority(cls, v):
        return _coerce_enum(Priority, v)


class TranscriptAnalysis(BaseModel):
    """The full structured extraction the analyzer produces for one call."""

    account_name: str
    call_date: str = "unknown"
    account_stage: AccountStage
    products_discussed: list[str] = Field(default_factory=list)
    technical_concerns: list[TechnicalConcern] = Field(default_factory=list)
    pain_points: list[str] = Field(default_factory=list)
    competitors_mentioned: list[str] = Field(default_factory=list)
    action_items: list[ActionItem] = Field(default_factory=list)
    sentiment: Sentiment
    key_quotes: list[str] = Field(default_factory=list)

    @field_validator("account_stage", mode="before")
    @classmethod
    def _normalize_stage(cls, v):
        return _coerce_enum(AccountStage, v)

    @field_validator("sentiment", mode="before")
    @classmethod
    def _normalize_sentiment(cls, v):
        return _coerce_enum(Sentiment, v)
