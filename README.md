# SaaS Product Analytics Dashboard

Analysis of a 1,200-user SaaS usage dataset to find what drives churn, with an interactive dashboard to present the findings.

## Key finding
Feature-adoption depth is the strongest churn driver:
- 0 features used: **40% churn**
- 4+ features used: **2.7% churn**

## Recommendation
Prioritize onboarding flows that get users to a third feature within their first week.

## What's inside
- `generate_data.py`: generates the synthetic SaaS usage dataset
- `analyze.py`: cohort retention, feature-adoption rates, churn by engagement segment (pandas)
- `summary.json`: computed metrics
- `dashboard.html`: dashboard presenting the results

## Run it
    python generate_data.py
    python analyze.py
    # then open dashboard.html in a browser

## Stack
Python, Pandas, NumPy, HTML/JS

*Note: the dataset is synthetic, so findings demonstrate the analysis approach rather than real product data.*
