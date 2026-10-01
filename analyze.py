"""
Analyzes the synthetic SaaS dataset to answer core product questions:
1. What's the churn rate by feature-adoption depth?
2. Which features have the highest adoption?
3. How does engagement segment relate to churn?
4. Which cohort is retaining best?
Outputs a JSON summary consumed by the dashboard.
"""
import json
import pandas as pd

df = pd.read_csv("saas_users.csv")
FEATURES = ["Dashboard", "Reports", "Integrations", "Automation", "Team Collab"]

# 1. Churn rate by number of features adopted (the core insight)
churn_by_depth = (
    df.groupby("n_features_used")["churned"]
    .mean()
    .reindex(range(0, 6), fill_value=0)
    .round(3) * 100
)

# 2. Feature adoption rate (% of all users who used each feature at least once)
adoption = {}
for f in FEATURES:
    adoption[f] = round((df["features_used"].str.contains(f, na=False, regex=False)).mean() * 100, 1)

# 3. Engagement segment vs churn
df["segment"] = pd.cut(df["engagement_score"], bins=[-0.01, 0.33, 0.66, 1.0],
                        labels=["Low", "Medium", "High"])
churn_by_segment = (df.groupby("segment", observed=True)["churned"].mean() * 100).round(1)

# 4. Retention by cohort (non-churned %)
retention_by_cohort = (
    (1 - df.groupby("signup_cohort")["churned"].mean()) * 100
).round(1)

overall_churn = round(df["churned"].mean() * 100, 1)

summary = {
    "overall_churn_rate": overall_churn,
    "total_users": len(df),
    "churn_by_feature_depth": {str(k): round(v, 1) for k, v in churn_by_depth.items()},
    "feature_adoption_rate": adoption,
    "churn_by_engagement_segment": {str(k): v for k, v in churn_by_segment.items()},
    "retention_by_cohort": {str(k): v for k, v in retention_by_cohort.items()},
}

with open("summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
print("\nKey insight: churn drops from "
      f"{summary['churn_by_feature_depth']['0']}% (0 features used) to "
      f"{summary['churn_by_feature_depth']['4']}% (4 features used).")
