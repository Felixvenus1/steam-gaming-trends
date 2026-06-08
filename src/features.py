"""Feature engineering helpers for the Steam dataset."""

from __future__ import annotations

import pandas as pd

CURRENT_YEAR = 2024


def add_review_positivity_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """Add ``review_positivity_ratio`` = positive / (positive + negative)."""
    total = df["positive"] + df["negative"]
    df = df.copy()
    df["review_positivity_ratio"] = df["positive"] / total.where(total > 0)
    return df


def add_price_per_playtime_hour(df: pd.DataFrame) -> pd.DataFrame:
    """Add ``price_per_playtime_hour`` = price_usd / median_playtime_hours."""
    df = df.copy()
    hours = df["median_playtime_forever"] / 60
    df["price_per_playtime_hour"] = df["price"] / hours.where(hours > 0)
    return df


def add_release_year_lag(df: pd.DataFrame) -> pd.DataFrame:
    """Add ``release_year_lag`` = CURRENT_YEAR - release_year."""
    df = df.copy()
    release_dt = pd.to_datetime(df["release_date"], errors="coerce")
    df["release_year_lag"] = CURRENT_YEAR - release_dt.dt.year
    return df


def engineer_all(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all three derived features in one call."""
    df = add_review_positivity_ratio(df)
    df = add_price_per_playtime_hour(df)
    df = add_release_year_lag(df)
    return df
