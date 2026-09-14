# Freemium Gaming — Monetization & Player Retention Analysis

One-line summary
- Applied data science and product analytics project that identifies monetization drivers and retention risks in freemium mobile games using in-app purchase telemetry, user engagement signals, and cohort analysis.

Why this project (recruiter-friendly)
- Demonstrates end-to-end analytics: data ingestion, cleaning, exploratory analysis, KPI computation, actionable recommendations, and a small demo app.
- Produces business-oriented outputs: ARPU/ARPPU, revenue concentration by segment, conversion latency (install → first purchase), correlation analysis, and LLM-generated strategy recommendations.
- Shows practical impact: identifies high-leverage interventions (targeted live-ops offers, conversion-window nudges, and segment-specific experiments).

Highlights (quick results)
- Data snapshot: ~3,000 users (notebook sample).
- Revenue profile: highly skewed — a small cohort (whales) generates the majority of revenue.
- Conversion latency: measurable time-to-first-purchase window that suggests focusing early retention & conversion nudges.
- Predictive signals: modest correlations between single demographics and spend — behavioral features and early-session patterns are stronger levers.
- Business outcome: prioritized recommendations for live-ops, bundle tuning, and segment-specific experiments to increase conversion volume and ARPPU.

What I built (components & responsibilities)
- Exploratory notebook with charts, cohort tables, and written recommendations:
  - Freemium-Gaming-Monetization-And-Player-Retention.ipynb
- Reusable Python modules for production-ready metrics and filtering:
  - src/data_loader.py — robust data discovery, cleaning, and payers vs F2P split.
  - src/monetization.py — ARPU, segment revenue contribution, genre monetization depth.
  - src/player_analysis.py — correlation matrix and numeric diagnostics.
  - src/retention.py — conversion latency distribution.
  - src/llm_insights.py — compact LLM prompt to turn KPIs into strategic bullets (OpenAI key required).
- Lightweight Flask demo (app.py) that exposes analysis and visualizations locally.
- Outputs written to outputs/ for quick review (tables, charts, CSVs).
- Tests under tests/ that validate metric logic.

Business & product recommendations
- Focus the first-purchase conversion effort in the observed early days after install with time-limited or progression-based offers.
- Run separate experiments for whales vs. mid/low spenders: protect long-term retention while optimizing short-term revenue.
- Improve targeting signals by adding behavioral features (early session patterns, progression, feature usage) because demographics alone are weak predictors.
- Use genre-specific bundle tuning where mean spend by genre/segment indicates higher receptivity.

Technical stack & skills demonstrated
- Python (pandas, numpy)
- Data engineering: robust data discovery, cleaning, and feature engineering
- Analytics: cohort analysis, pivot tables, correlation matrices, conversion distribution
- Lightweight web (Flask) for demoing analysis
- LLM integration for narrative synthesis (OpenAI client)
- Reproducibility: notebook outputs saved, tests included, requirements/environment files
- Tools: Git, pytest, Jupyter

How to run (quick)
1. Install dependencies
   - pip:
     ```
     python -m pip install -r requirements.txt
     ```
   - or use the provided conda environment:
     ```
     conda env create -f environment.yml
     conda activate <env-name>
     ```
2. Add the dataset
   - Place `mobile_game_inapp_purchases.csv` in `data/raw/` (or `data/` or repo root). The loader searches common locations automatically.
3. Reproduce analysis
   - Open and run the notebook: Freemium-Gaming-Monetization-And-Player-Retention.ipynb
   - Or run the Flask demo:
     ```
     export FLASK_APP=app        # macOS / Linux
     set FLASK_APP=app           # Windows PowerShell
     python -m flask run
     ```
4. Run tests
   ```
   python -m pytest tests/
   ```

What to look for when evaluating the project (for recruiters / hiring managers)
- Business impact: check the notebook conclusions and the "Recommendations" section — are they actionable and prioritized?
- Code quality: inspect src/ for modularity, docstrings, and error handling (see data discovery and clean functions).
- Reproducibility: run the notebook and confirm outputs are generated under outputs/.
- Metrics correctness: run tests in tests/ to validate arithmetic and aggregations (ARPU, revenue shares).
- Communication: evaluate the notebook narrative, which links data findings to product recommendations.
- Optional: validate the LLM-generated recommendations by setting an OPENAI_API_KEY and running the LLM helper.

Files & structure (top-level)
- README.md
- Freemium-Gaming-Monetization-And-Player-Retention.ipynb
- app.py
- data/ (expected dataset location)
- outputs/ (notebook artifacts)
- src/
  - data_loader.py
  - monetization.py
  - player_analysis.py
  - retention.py
  - llm_insights.py
- tests/
- requirements.txt / environment.yml

Environment & secrets
- `OPENAI_API_KEY`: optional. Required only if you want LLM-generated strategy bullets from src/llm_insights.py or notebook cells that call it.
- No other secrets required to run the analysis locally.

Author / contact
- Author: Akash Kumar Singh (GitHub profile at https://github.com/razesoni)
- For recruiters: I’m available to discuss this project, walk through the code and analysis, or present the findings in a short technical/product demo.

Live Site
https://freemium-gaming-monetization-player.onrender.com/
