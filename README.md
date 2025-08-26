# WealthGPT Starter (India-first)

A minimal, **compliance-aware**, goal- and risk-based portfolio recommendation prototype.

## What it does
- Captures user profile & risk tolerance.
- Suggests a strategic asset allocation (Equity, Intl Equity, Debt, Gold).
- Compares **current vs recommended** and shows a simple **rebalance plan**.
- Generates a downloadable CSV report.

> ⚠️ **Disclaimer**: This tool is for **educational use only** and does **not** constitute investment advice. Consult a SEBI-registered Investment Adviser for personalised advice.

## Quickstart
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files
- `app.py` – Streamlit UI + orchestration
- `engine/allocation.py` – allocation logic and rebalancing
- `engine/risk.py` – 6-question risk profiler
- `engine/compliance.py` – disclaimers & guardrails
- `engine/data_sources.py` – stubs for AMFI/NSE/AlphaVantage connectors
- `example_data/holdings_sample.csv` – sample holdings
- `actions_specs/pricequote_openapi.json` – optional Action spec for a price quote microservice (if you wire this into ChatGPT GPTs Actions)

## Notes
- Asset classes mapped for India: **Equity (India)**, **Equity (International)**, **Debt (short/medium)**, **Gold**.
- Keep distribution-only vs advisory segregation per SEBI norms. This starter **does not** execute orders or provide product recommendations; only categories.
- Extend with: goal buckets, SIP planning, XIRR, drawdown, VaR, tax planning, and SEBI audit trails.
