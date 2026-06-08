"""VADER baseline sentiment for Steam review text."""

from __future__ import annotations

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyser = SentimentIntensityAnalyzer()


def score(text: str) -> float:
    """Return VADER compound score for a single review string."""
    if not isinstance(text, str) or not text.strip():
        return 0.0
    return _analyser.polarity_scores(text)["compound"]


def label(compound: float) -> str:
    """Map a compound score to positive / neutral / negative."""
    if compound >= 0.05:
        return "positive"
    if compound <= -0.05:
        return "negative"
    return "neutral"


def add_vader(df: pd.DataFrame, text_col: str = "review_text") -> pd.DataFrame:
    """Add ``vader_compound`` and ``vader_polarity`` columns to *df*."""
    df = df.copy()
    df["vader_compound"] = df[text_col].map(score)
    df["vader_polarity"] = df["vader_compound"].map(label)
    return df
