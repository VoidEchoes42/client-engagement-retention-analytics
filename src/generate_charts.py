"""
generate_charts.py

Creates all dashboard-ready visualizations from the analyzed data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "..", "powerbi", "screenshots")
REPORTS_DIR = os.path.join(BASE_DIR, "..", "reports")

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

features_df = pd.read_csv(os.path.join(PROCESSED_DIR, "customer_features_vB.csv"))

# ============================================================================
# CHART 1: Distribution Overview
# ============================================================================
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Client Engagement & Retention Analytics — Data Overview', fontsize=14, fontweight='bold')

axes[0, 0].hist(features_df['tenure'], bins=30, edgecolor='black', alpha=0.7, color='steelblue')
axes[0, 0].set_title('Tenure Distribution'); axes[0, 0].set_xlabel('Months')

axes[0, 1].hist(features_df['monthly_charges'], bins=30, edgecolor='black', alpha=0.7, color='coral')
axes[0, 1].set_title('Monthly Charges Distribution'); axes[0, 1].set_xlabel('$')

axes[0, 2].hist(features_df['total_charges'], bins=30, edgecolor='black', alpha=0.7, color='seagreen')
axes[0, 2].set_title('Total Charges Distribution'); axes[0, 2].set_xlabel('$')

axes[1, 0].hist(features_df['engagement_score'], bins=30, edgecolor='black', alpha=0.7, color='gold')
axes[1, 0].set_title('Engagement Score Distribution'); axes[1, 0].set_xlabel('Score')

axes[1, 1].hist(features_df['total_logins'], bins=30, edgecolor='black', alpha=0.7, color='mediumpurple')
axes[1, 1].set_title('Total Logins Distribution'); axes[1, 1].set_xlabel('Logins')

churn_counts = features_df['churn'].value_counts()
axes[1, 2].bar(churn_counts.index, churn_counts.values, color=['steelblue', 'coral'], edgecolor='black')
axes[1, 2].set_title('Renewal Status'); axes[1, 2].set_ylabel('Count')
for i, v in enumerate(churn_counts.values):
    axes[1, 2].text(i, v + 100, str(v), ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(SCREENSHOTS_DIR, '01_data_overview.png'), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: 01_data_overview.png")

# ============================================================================
# CHART 2: Engagement vs Renewal
# ============================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

renewed = features_df[features_df['churn'] == 'No']['engagement_score']
churned = features_df[features_df['churn'] == 'Yes']['engagement_score']
axes[0].hist([renewed, churned], bins=25, label=['Renewed', 'Churned'], alpha=0.7, color=['steelblue', 'coral'], edgecolor='black')
axes[0].set_title('Engagement Score by Renewal Status'); axes[0].set_xlabel('Engagement Score'); axes[0].legend()

# Box plot
box_data = [renewed, churned]
bp = axes[1].boxplot(box_data, patch_artist=True)
axes[1].set_xticklabels(['Renewed', 'Churned'])
bp['boxes'][0].set_facecolor('steelblue'); bp['boxes'][0].set_alpha(0.7)
bp['boxes'][1].set_facecolor('coral'); bp['boxes'][1].set_alpha(0.7)
axes[1].set_title('Engagement Score: Box Plot Comparison'); axes[1].set_ylabel('Engagement Score')

plt.tight_layout()
plt.savefig(os.path.join(SCREENSHOTS_DIR, '02_engagement_vs_renewal.png'), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: 02_engagement_vs_renewal.png")

# ============================================================================
# CHART 3: Renewal Rate by Contract Type
# ============================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

contract_data = features_df.groupby('Contract').apply(
    lambda x: (x['churn'] == 'No').mean() * 100
).sort_values(ascending=False)

colors = ['seagreen', 'gold', 'coral']
bars = axes[0].bar(contract_data.index, contract_data.values, color=colors, edgecolor='black', alpha=0.85)
axes[0].set_title('Renewal Rate by Contract Type', fontweight='bold')
axes[0].set_ylabel('Renewal Rate (%)')
axes[0].set_ylim(0, 105)
for bar, val in zip(bars, contract_data.values):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5, f'{val:.1f}%', ha='center', fontweight='bold')

# Contract type customer distribution
contract_counts = features_df['Contract'].value_counts()
axes[1].pie(contract_counts.values, labels=contract_counts.index, autopct='%1.1f%%', colors=colors, startangle=90)
axes[1].set_title('Customer Distribution by Contract Type')

plt.tight_layout()
plt.savefig(os.path.join(SCREENSHOTS_DIR, '03_renewal_by_contract.png'), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: 03_renewal_by_contract.png")

# ============================================================================
# CHART 4: Renewal Rate by Tenure Band
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

tenure_data = features_df.groupby('tenure_band').apply(
    lambda x: pd.Series({
        'renewal_rate': (x['churn'] == 'No').mean() * 100,
        'customers': len(x)
    })
).reindex(['0-12 months', '13-24 months', '25-48 months', '49+ months'])

x = np.arange(len(tenure_data))
bars = ax.bar(x, tenure_data['renewal_rate'], color='teal', edgecolor='black', alpha=0.85)
ax.set_xticks(x); ax.set_xticklabels(tenure_data.index)
ax.set_title('Renewal Rate by Tenure Band', fontweight='bold')
ax.set_ylabel('Renewal Rate (%)')
ax.set_ylim(0, 105)
for i, (idx, row) in enumerate(tenure_data.iterrows()):
    ax.text(i, row['renewal_rate'] + 1.5, f'{row["renewal_rate"]:.1f}%', ha='center', fontweight='bold')
    ax.text(i, 3, f'n={int(row["customers"])}', ha='center', fontsize=10, color='white', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(SCREENSHOTS_DIR, '04_renewal_by_tenure.png'), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: 04_renewal_by_tenure.png")

# ============================================================================
# CHART 5: Correlation Heatmap
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 10))

numeric_cols = [
    'tenure', 'monthly_charges', 'total_charges',
    'engagement_score', 'total_interactions', 'total_content_views',
    'total_events', 'total_logins', 'total_sessions', 'total_features',
    'total_active_days',
]
corr_matrix = features_df[numeric_cols].corr()

sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlBu_r', center=0,
            square=True, linewidths=0.5, annot_kws={'size': 8}, ax=ax)
ax.set_title('Correlation Matrix: Engagement & Subscription Metrics', fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(SCREENSHOTS_DIR, '05_correlation_matrix.png'), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: 05_correlation_matrix.png")

# ============================================================================
# CHART 6: Engagement Metrics Comparison (Renewed vs Churned)
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 6))

comparison_cols = [
    'engagement_score', 'total_interactions', 'avg_duration',
    'total_time_spent', 'total_reports', 'events_attended',
    'total_logins', 'total_sessions', 'total_features',
]
comparison = features_df.groupby('churn')[comparison_cols].mean().T
comparison.columns = ['Renewed', 'Churned']

x = np.arange(len(comparison))
width = 0.35
bars1 = ax.bar(x - width/2, comparison['Renewed'], width, label='Renewed', color='steelblue', alpha=0.8, edgecolor='black')
bars2 = ax.bar(x + width/2, comparison['Churned'], width, label='Churned', color='coral', alpha=0.8, edgecolor='black')

ax.set_xticks(x)
ax.set_xticklabels([c.replace('_', ' ').title() for c in comparison.index], rotation=45, ha='right')
ax.set_title('Engagement Metrics: Renewed vs Churned Clients', fontweight='bold')
ax.set_ylabel('Average Value')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(SCREENSHOTS_DIR, '06_engagement_comparison.png'), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: 06_engagement_comparison.png")

# ============================================================================
# CHART 7: Engagement Score Distribution by Contract Type
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

contracts = features_df['Contract'].unique()
data_by_contract = [features_df[features_df['Contract'] == c]['engagement_score'].values for c in contracts]
bp = ax.boxplot(data_by_contract, patch_artist=True)
ax.set_xticklabels(contracts)
colors = ['coral', 'gold', 'seagreen']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color); patch.set_alpha(0.7)
ax.set_title('Engagement Score by Contract Type', fontweight='bold')
ax.set_ylabel('Engagement Score')
plt.tight_layout()
plt.savefig(os.path.join(SCREENSHOTS_DIR, '07_engagement_by_contract.png'), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: 07_engagement_by_contract.png")

# ============================================================================
# CHART 8: Renewal Rate by Engagement Band and Contract Type
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

segment_data = features_df.groupby(['Contract', 'engagement_band']).apply(
    lambda x: (x['churn'] == 'No').mean() * 100
).unstack()

segment_data.plot(kind='bar', ax=ax, width=0.8)
ax.set_title('Renewal Rate by Contract Type & Engagement Band', fontweight='bold')
ax.set_ylabel('Renewal Rate (%)')
ax.set_xlabel('Contract Type')
ax.legend(title='Engagement Band', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.tick_params(axis='x', rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(SCREENSHOTS_DIR, '08_renewal_by_segment.png'), dpi=200, bbox_inches='tight')
plt.close()
print("Saved: 08_renewal_by_segment.png")

print("\nAll charts generated successfully!")
