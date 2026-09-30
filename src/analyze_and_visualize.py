"""
analyze_and_visualize.py

Generates key findings, charts, and summary statistics from the processed data.
This script replaces the need to run Jupyter notebooks manually.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats

# Setup
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "..", "powerbi", "screenshots")
REPORTS_DIR = os.path.join(BASE_DIR, "..", "reports")

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# Load data
features_df = pd.read_csv(os.path.join(PROCESSED_DIR, "customer_features_vB.csv"))
print(f"Loaded {len(features_df)} customer records\n")

# ============================================================================
# KEY METRICS
# ============================================================================
print("=" * 60)
print("KEY BUSINESS METRICS")
print("=" * 60)

total_customers = len(features_df)
renewed = (features_df['churn'] == 'No').sum()
churned = (features_df['churn'] == 'Yes').sum()
renewal_rate = renewed / total_customers * 100
churn_rate = churned / total_customers * 100

total_revenue = features_df['monthly_charges'].sum()
avg_contract_value = features_df['total_charges'].mean()
avg_engagement = features_df['engagement_score'].mean()

print(f"Total Customers: {total_customers}")
print(f"Renewed: {renewed} ({renewal_rate:.1f}%)")
print(f"Churned: {churned} ({churn_rate:.1f}%)")
print(f"Total Monthly Revenue: ${total_revenue:,.2f}")
print(f"Average Contract Value: ${avg_contract_value:.2f}")
print(f"Average Engagement Score: {avg_engagement:.3f}")

# ============================================================================
# ENGAGEMENT COMPARISON: RENEWED VS NON-RENEWED
# ============================================================================
print("\n" + "=" * 60)
print("ENGAGEMENT COMPARISON: RENEWED VS NON-RENEWED")
print("=" * 60)

comparison_cols = [
    'engagement_score', 'total_interactions', 'avg_duration',
    'total_time_spent', 'total_reports', 'events_attended',
    'total_logins', 'total_sessions', 'total_features', 'total_active_days',
]

comparison = features_df.groupby('churn')[comparison_cols].mean().T
comparison.columns = ['Renewed', 'Non-Renewed']
comparison['Difference (%)'] = ((comparison['Renewed'] - comparison['Non-Renewed']) / comparison['Non-Renewed'] * 100).round(1)
print(comparison)

# ============================================================================
# RENEWAL RATE BY SEGMENT
# ============================================================================
print("\n" + "=" * 60)
print("RENEWAL RATE BY SEGMENT")
print("=" * 60)

# By contract type
print("\nBy Contract Type:")
contract_renewal = features_df.groupby('contract').apply(
    lambda x: pd.Series({
        'customers': len(x),
        'renewed': (x['churn'] == 'No').sum(),
        'renewal_rate': (x['churn'] == 'No').mean() * 100
    })
).round(2)
print(contract_renewal)

# By engagement band
print("\nBy Engagement Band:")
engagement_renewal = features_df.groupby('engagement_band').apply(
    lambda x: pd.Series({
        'customers': len(x),
        'renewed': (x['churn'] == 'No').sum(),
        'renewal_rate': (x['churn'] == 'No').mean() * 100
    })
).round(2)
print(engagement_renewal)

# By tenure band
print("\nBy Tenure Band:")
tenure_renewal = features_df.groupby('tenure_band').apply(
    lambda x: pd.Series({
        'customers': len(x),
        'renewed': (x['churn'] == 'No').sum(),
        'renewal_rate': (x['churn'] == 'No').mean() * 100
    })
).round(2)
print(tenure_renewal)

# By value segment
print("\nBy Value Segment:")
value_renewal = features_df.groupby('value_segment').apply(
    lambda x: pd.Series({
        'customers': len(x),
        'renewed': (x['churn'] == 'No').sum(),
        'renewal_rate': (x['churn'] == 'No').mean() * 100
    })
).round(2)
print(value_renewal)

# ============================================================================
# STATISTICAL TESTS
# ============================================================================
print("\n" + "=" * 60)
print("STATISTICAL TESTS")
print("=" * 60)

renewed_engagement = features_df[features_df['churn'] == 'No']['engagement_score']
churned_engagement = features_df[features_df['churn'] == 'Yes']['engagement_score']

t_stat, p_value = stats.ttest_ind(renewed_engagement, churned_engagement, equal_var=False)
print(f"\nt-Test (Engagement Score):")
print(f"  Renewed: mean={renewed_engagement.mean():.4f}, std={renewed_engagement.std():.4f}")
print(f"  Churned: mean={churned_engagement.mean():.4f}, std={churned_engagement.std():.4f}")
print(f"  t-statistic: {t_stat:.4f}")
print(f"  p-value: {p_value:.4e}")
print(f"  Significant: {'Yes' if p_value < 0.05 else 'No'} at alpha=0.05")

# Chi-square test: contract vs churn
contingency = pd.crosstab(features_df['contract'], features_df['churn'])
chi2, p_value_chi2, dof, expected = stats.chi2_contingency(contingency)
print(f"\nChi-Square Test (Contract Type vs Renewal):")
print(f"  Chi-square: {chi2:.4f}")
print(f"  p-value: {p_value_chi2:.4e}")
print(f"  Significant: {'Yes' if p_value_chi2 < 0.05 else 'No'} at alpha=0.05")

# ============================================================================
# AT-RISK CLIENTS
# ============================================================================
print("\n" + "=" * 60)
print("AT-RISK CLIENT ANALYSIS")
print("=" * 60)

q25_interactions = features_df['total_interactions'].quantile(0.25)
q25_logins = features_df['avg_logins_per_day'].quantile(0.25)

features_df['at_risk'] = (
    (features_df['total_interactions'] < q25_interactions) &
    (features_df['avg_logins_per_day'] < q25_logins)
)

at_risk_count = features_df['at_risk'].sum()
at_risk_pct = at_risk_count / total_customers * 100
at_risk_renewed = (features_df[features_df['at_risk']]['churn'] == 'No').mean() * 100

print(f"At-Risk Clients: {at_risk_count} ({at_risk_pct:.1f}%)")
print(f"At-Risk Renewal Rate: {at_risk_renewed:.1f}%")
print(f"Overall Renewal Rate: {renewal_rate:.1f}%")

# ============================================================================
# SAVE FINDINGS TO FILE
# ============================================================================
print("\n" + "=" * 60)
print("Generating visualizations and reports...")
print("=" * 60)

# Save key metrics to CSV
metrics_summary = pd.DataFrame({
    'Metric': [
        'Total Customers', 'Renewed', 'Churned', 'Renewal Rate (%)', 'Churn Rate (%)',
        'Total Monthly Revenue ($)', 'Avg Contract Value ($)', 'Avg Engagement Score',
        'At-Risk Clients', 'At-Risk Renewal Rate (%)'
    ],
    'Value': [
        total_customers, renewed, churned, round(renewal_rate, 2), round(churn_rate, 2),
        round(total_revenue, 2), round(avg_contract_value, 2), round(avg_engagement, 4),
        at_risk_count, round(at_risk_renewed, 2)
    ]
})
metrics_summary.to_csv(os.path.join(REPORTS_DIR, "key_metrics.csv"), index=False)
print(f"Saved key metrics to reports/key_metrics.csv")

# Save comparison table
comparison.to_csv(os.path.join(REPORTS_DIR, "engagement_comparison.csv"))
print(f"Saved engagement comparison to reports/engagement_comparison.csv")

# Save segment analysis
segment_analysis = features_df.groupby(['contract', 'engagement_band']).apply(
    lambda x: pd.Series({
        'customers': len(x),
        'renewal_rate': (x['churn'] == 'No').mean() * 100,
        'avg_monthly_charges': x['monthly_charges'].mean(),
        'avg_engagement': x['engagement_score'].mean(),
    })
).round(2)
segment_analysis.to_csv(os.path.join(REPORTS_DIR, "segment_analysis.csv"))
print(f"Saved segment analysis to reports/segment_analysis.csv")

print("\nAnalysis complete!")
