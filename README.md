# Freemium Gaming Monetization Analytics

A Python analysis and Flask dashboard for exploring player spending, engagement, revenue segments, and time to first purchase.

**Scope:** descriptive analytics. Cohort D1/D7/D30 retention, churn prediction, and lifetime-value forecasting are future work; they are not implemented by the current modules.

## What is included

- `src/data_loader.py`: CSV loading, missing-value handling, paying/non-paying splits, filters
- `src/monetization.py`: revenue per supplied user population, segment contributions, genre comparisons
- `src/retention.py`: descriptive statistics for days until first purchase
- `src/player_analysis.py`: numeric correlations
- `app.py`, `templates/`, `static/`: Flask dashboard
- `Freemium-Gaming-Monetization-And-Player-Retention.ipynb`: original exploratory notebook
- `tests/`: automated checks for metric behavior
- `.github/workflows/tests.yml`: test workflow

## Run

From the repository root in a Python 3.11 virtual environment:

```bash
python -m pip install -r requirements.txt
python -m flask --app app run
```

Open [the local dashboard](http://127.0.0.1:5000). The included input is `data/raw/mobile_game_inapp_purchases.csv`.

```bash
python -m pytest tests/
```

## Interpretation

Revenue divided by **all** users is ARPU. The same function called with only paying users calculates ARPPU. The caller must specify the population; paying-only results must not be presented as population-wide ARPU.

Time until first purchase is conversion latency, not retention. Correlations are descriptive and do not establish causal effects of engagement on spending.

See [methodology](docs/methodology.md) and [data dictionary](docs/data_dictionary.md) for scope and assumptions. No validated business uplift or production deployment is claimed.

## Next steps

Verify dataset provenance and observation period; publish reproducible numeric findings with sample sizes; add session-level event data for cohort retention; evaluate any churn model using time-based validation.

Author: **Akash Kumar Singh** — [GitHub](https://github.com/razesoni)
