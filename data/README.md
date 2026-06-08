# Dataset Provenance

## Primary source — Steam public web API (no account required)

`data/fetch_steam_public.py` builds the dataset live from Steam's public endpoints:

- `store.steampowered.com/api/appdetails` — price, genres, release date
- `store.steampowered.com/appreviews/<appid>` — review text + recommended flag + global counts

For a curated set of ~40 popular titles it writes:

| File | Rows (approx.) | Description |
|---|---|---|
| `games.csv` | ~40 | One row per game: price, genres, global review counts, median playtime |
| `recommendations.csv` | ~4 800 | One row per English review: review text, recommended flag, playtime |

Data is © Valve, retrieved via the public Steam Web API for non-commercial,
educational analysis. Raw CSVs are git-ignored.

## Optional source — Kaggle (larger sample)

**Source**: Kaggle — fronkongames/steam-games-dataset (CC0 Public Domain)
**URL**: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset

Run `python data/download_data.py` (requires `~/.kaggle/kaggle.json`) for a much
larger games table.

## Setup Kaggle CLI

```bash
pip install kaggle
# Place API token at ~/.kaggle/kaggle.json
# Download from: https://www.kaggle.com/settings → API → Create New Token
```
