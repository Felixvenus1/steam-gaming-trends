# Feature Engineering Log

Documents all derived features added to the Steam dataset.

---

## `review_positivity_ratio`

**Source columns**: `positive`, `negative`  
**Formula**: `positive / (positive + negative)`  
**Rationale**: Raw counts are not comparable across games with different total review volumes. The ratio normalises this, giving a [0, 1] sentiment proxy comparable across the catalogue. Games with `positive + negative == 0` receive `NaN`.  
**Added in**: `02_eda_trends.ipynb` → cell "Feature Engineering"

---

## `price_per_playtime_hour`

**Source columns**: `price` (USD), `median_playtime_forever` (minutes)  
**Formula**: `price / (median_playtime_forever / 60)`  
**Rationale**: Measures value-for-money. A $60 game with 60 h median playtime costs $1/h, while a $10 game with 2 h costs $5/h. Games with zero median playtime receive `NaN` (infinite cost is undefined).  
**Added in**: `02_eda_trends.ipynb` → cell "Feature Engineering"

---

## `release_year_lag`

**Source columns**: `release_date`  
**Formula**: `CURRENT_YEAR - release_year` where `CURRENT_YEAR = 2024`  
**Rationale**: Captures how long ago a game was released. Useful for analysing whether older games accumulate reviews over time versus newer titles. Games with missing or unparseable release dates receive `NaN`.  
**Added in**: `02_eda_trends.ipynb` → cell "Feature Engineering"

---

## VADER Sentiment Labels

**Source columns**: `review_text` (raw review body from `recommendations.csv`)  
**Method**: VADER `SentimentIntensityAnalyzer` compound score  
**Thresholds**:
- `compound >= 0.05` → `"positive"`
- `compound <= -0.05` → `"negative"`
- otherwise → `"neutral"`

**Rationale**: VADER is a lexicon-based method tuned for informal/social-media text. Gaming reviews are short, informal, and emotionally expressive — a good fit without requiring training data.  
**Added in**: `03_baseline_sentiment.ipynb`

---

## Notes

- All feature computation is implemented in `src/features.py` and called from the notebooks.
- The processed dataset (with all features + VADER labels) is serialised to `outputs/processed_reviews.parquet` for use by **P17 steam-review-classifier**.
