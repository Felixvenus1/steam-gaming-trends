# Dataset Provenance

**Source**: Kaggle — fronkongames/steam-games-dataset  
**URL**: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset  
**Licence**: CC0 Public Domain  

## Files

| File | Rows (approx.) | Description |
|---|---|---|
| `games.csv` | 27 000+ | One row per game: price, genres, review counts, playtime, metacritic score |
| `recommendations.csv` | 41 M+ | One row per user review: review text, recommended flag, hours played |

Raw CSVs are git-ignored. Run `python data/download_data.py` to fetch them (requires `~/.kaggle/kaggle.json`).

## Setup Kaggle CLI

```bash
pip install kaggle
# Place API token at ~/.kaggle/kaggle.json
# Download from: https://www.kaggle.com/settings → API → Create New Token
```
