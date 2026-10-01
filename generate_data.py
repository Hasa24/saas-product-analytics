"""
Generates a synthetic SaaS product usage dataset for analysis.
Simulates 6 months of signups, feature usage events, and churn outcomes
for a B2B SaaS product with 5 core features.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N_USERS = 1200
FEATURES = ["Dashboard", "Reports", "Integrations", "Automation", "Team Collab"]
COHORT_MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]

# --- Users & signup cohort ---
users = pd.DataFrame({
    "user_id": range(1, N_USERS + 1),
    "signup_cohort": np.random.choice(COHORT_MONTHS, N_USERS, p=[0.22, 0.20, 0.18, 0.16, 0.14, 0.10]),
    "plan": np.random.choice(["Free", "Pro", "Business"], N_USERS, p=[0.55, 0.32, 0.13]),
})

# --- Feature adoption: each user adopts a subset of features, weighted by plan ---
plan_adoption_boost = {"Free": 0.0, "Pro": 0.15, "Business": 0.30}

rows = []
for _, u in users.iterrows():
    boost = plan_adoption_boost[u["plan"]]
    engagement_score = np.clip(np.random.beta(2, 3) + boost, 0, 1)  # 0-1 engagement proxy
    adopted = []
    for f in FEATURES:
        base_rate = {"Dashboard": 0.85, "Reports": 0.55, "Integrations": 0.35,
                     "Automation": 0.28, "Team Collab": 0.40}[f]
        if np.random.rand() < np.clip(base_rate + boost - 0.1 + engagement_score * 0.2, 0, 1):
            adopted.append(f)
    n_features_used = len(adopted)

    # Churn probability driven by engagement + feature depth (fewer features -> higher churn)
    churn_base = 0.42 - 0.09 * n_features_used - 0.20 * engagement_score
    churn_prob = np.clip(churn_base, 0.03, 0.65)
    churned = np.random.rand() < churn_prob

    rows.append({
        "user_id": u["user_id"],
        "signup_cohort": u["signup_cohort"],
        "plan": u["plan"],
        "engagement_score": round(engagement_score, 3),
        "n_features_used": n_features_used,
        "features_used": ";".join(adopted),
        "churned": churned,
    })

df = pd.DataFrame(rows)
df.to_csv("saas_users.csv", index=False)
print(f"Generated {len(df)} synthetic users -> saas_users.csv")
print(df.head())
