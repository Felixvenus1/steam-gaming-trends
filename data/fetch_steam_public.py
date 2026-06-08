"""Build the Steam dataset from Steam's free public web API (no Kaggle account).

For a curated list of popular app IDs this fetches:

* game-level metadata + review summary  -> data/games.csv
* individual English review text + the user's "recommended" flag -> data/reviews.csv

Endpoints used (public, no API key required):
  * https://store.steampowered.com/api/appdetails?appids=<id>
  * https://store.steampowered.com/appreviews/<id>?json=1

Usage:
    python data/fetch_steam_public.py                 # default ~40 apps
    python data/fetch_steam_public.py --reviews 200   # more reviews per app
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import pandas as pd
import requests

DATA_DIR = Path(__file__).parent

# A varied, stable selection of well-known Steam titles across genres.
APP_IDS = [
    730, 570, 578080, 1172470, 271590, 252490, 304930, 359550, 440, 230410,
    1245620, 292030, 413150, 105600, 218620, 322330, 4000, 250900, 620,
    1091500, 489830, 945360, 281990, 236850, 294100, 646570, 367520, 588650,
    268910, 275850, 1174180, 49520, 8930, 220, 400, 72850, 377160, 582010,
    1085660, 1086940,
]

HEADERS = {"User-Agent": "steam-gaming-trends-portfolio/1.0"}


def get_appdetails(appid: int) -> dict | None:
    url = "https://store.steampowered.com/api/appdetails"
    r = requests.get(url, params={"appids": appid, "cc": "us", "l": "en"},
                     headers=HEADERS, timeout=30)
    r.raise_for_status()
    payload = r.json().get(str(appid), {})
    if not payload.get("success"):
        return None
    return payload["data"]


def get_review_summary(appid: int) -> dict:
    """Global review totals (num_per_page=0 returns only the query_summary)."""
    url = f"https://store.steampowered.com/appreviews/{appid}"
    r = requests.get(
        url,
        params={"json": 1, "language": "all", "filter": "all", "num_per_page": 0},
        headers=HEADERS,
        timeout=30,
    )
    r.raise_for_status()
    return r.json().get("query_summary", {}) or {}


def get_reviews(appid: int, want: int) -> tuple[dict, list[dict]]:
    """Return (query_summary, list of review dicts)."""
    url = f"https://store.steampowered.com/appreviews/{appid}"
    collected: list[dict] = []
    cursor = "*"
    summary: dict = {}
    while len(collected) < want:
        r = requests.get(
            url,
            params={
                "json": 1,
                "filter": "recent",
                "language": "english",
                "num_per_page": 100,
                "purchase_type": "all",
                "cursor": cursor,
            },
            headers=HEADERS,
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        if data.get("success") != 1:
            break
        summary = data.get("query_summary", summary) or summary
        reviews = data.get("reviews", [])
        if not reviews:
            break
        collected.extend(reviews)
        cursor = data.get("cursor", "")
        if not cursor:
            break
        time.sleep(0.4)
    return summary, collected[:want]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviews", type=int, default=120,
                        help="Reviews to fetch per app (default 120).")
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    games_rows: list[dict] = []
    review_rows: list[dict] = []

    for appid in APP_IDS:
        try:
            details = get_appdetails(appid)
            time.sleep(0.4)
            summary = get_review_summary(appid)
            time.sleep(0.4)
            _, reviews = get_reviews(appid, args.reviews)
        except requests.RequestException as exc:
            print(f"  {appid}: skipped ({exc})")
            continue
        if details is None:
            print(f"  {appid}: no details, skipped")
            continue

        name = details.get("name", str(appid))
        price = 0.0
        if not details.get("is_free", False):
            price = (details.get("price_overview", {}) or {}).get("final", 0) / 100
        genres = ";".join(g["description"] for g in details.get("genres", []))
        release_date = (details.get("release_date", {}) or {}).get("date", "")

        playtimes = [
            r["author"]["playtime_forever"]
            for r in reviews
            if r.get("author", {}).get("playtime_forever")
        ]
        median_playtime = float(pd.Series(playtimes).median()) if playtimes else float("nan")

        games_rows.append({
            "app_id": appid,
            "name": name,
            "price": price,
            "positive": int(summary.get("total_positive", 0)),
            "negative": int(summary.get("total_negative", 0)),
            "total_reviews": int(summary.get("total_reviews", 0)),
            "review_score_desc": summary.get("review_score_desc", ""),
            "median_playtime_forever": median_playtime,
            "genres": genres,
            "release_date": release_date,
        })

        for r in reviews:
            review_rows.append({
                "app_id": appid,
                "review": r.get("review", ""),
                "is_recommended": bool(r.get("voted_up", False)),
                "playtime_forever": r.get("author", {}).get("playtime_forever", 0),
                "timestamp_created": r.get("timestamp_created", 0),
            })

        print(f"  {appid:>8}  {name[:30]:<30}  reviews={len(reviews)}")

    games = pd.DataFrame(games_rows)
    recs = pd.DataFrame(review_rows)
    games.to_csv(DATA_DIR / "games.csv", index=False)
    # Named to match the notebooks (review-level "recommendations" table).
    recs.to_csv(DATA_DIR / "recommendations.csv", index=False)
    print(f"\nWrote games.csv ({len(games)} games) and "
          f"recommendations.csv ({len(recs)} reviews).")


if __name__ == "__main__":
    main()
