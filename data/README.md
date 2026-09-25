# Data

`python data/fetch_steam_public.py` builds two git-ignored files from Steam's public store endpoints (`api/appdetails` and `appreviews/<appid>`) for a fixed list of about 40 popular games:

- `games.csv`: one row per game with price, genres, release date, global review counts and median playtime
- `recommendations.csv`: about 120 recent English reviews per game, with the recommended flag and playtime

`python data/download_data.py` fetches the larger Kaggle dataset fronkongames/steam-games-dataset (CC0). It needs the `kaggle` CLI and `~/.kaggle/kaggle.json`. That dataset has no review text, so the notebooks still need `recommendations.csv` from the public-API fetcher.
