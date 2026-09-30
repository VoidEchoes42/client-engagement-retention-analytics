# Power BI Dashboard Specification
## Client Engagement & Subscription Retention Analytics

---

## Dashboard Overview

This dashboard provides an executive view of client engagement and subscription retention metrics, built from the client-engagement-retention-analytics dataset. It is designed for Gartner associate data analytics use cases.

---

## Data Source

**File:** `customer_features_vB.csv` (7,043 customers, 35 columns)

**Primary Tables:**
- Customer base (demographics, subscription, churn labels)
- Engagement features (interactions, logins, sessions, content, events)
- Derived segments (engagement_band, tenure_band, value_segment)

---

## Page 1: Executive Summary

### KPIs (Top Row — 5 Cards)

| KPI | Value | Trend |
|-----|-------|-------|
| Total Customers | 7,043 | — |
| Renewal Rate | 84.6% | Green |
| Churn Rate | 15.4% | Red |
| Total Monthly Revenue | $448,305.85 | — |
| Avg Contract Value | $1,336.03 | — |

**Visual:** Large number cards with conditional coloring (green for good, red for concern)

### Renewal Status Breakdown

**Visual:** Donut chart
- Renewed: 5,956 (84.6%) — Blue
- Churned: 1,087 (15.4%) — Red

---

## Page 2: Engagement & Retention Analysis

### Engagement Score Distribution

**Visual:** Histogram with overlaid renewal status
- Shows distribution of engagement_score (0-1)
- Color-coded by churn (Yes/No)
- Insight: Engagement score is nearly identical between renewed and churned

### Engagement Metrics Comparison

**Visual:** Grouped bar chart
- Metrics: engagement_score, total_interactions, avg_duration, total_time_spent, total_reports, events_attended, total_logins, total_sessions, total_features
- Grouped by: Renewed vs Churned
- Key insight: No metric shows a large difference between groups

---

## Page 3: Segment Deep Dive

### Renewal Rate by Contract Type

**Visual:** Bar chart (sorted descending)
- Two year: 98.5%
- One year: 89.4%
- Month-to-month: 77.6%
- Insight: Contract type is the strongest predictor

### Renewal Rate by Tenure Band

**Visual:** Bar chart
- 49+ months: 97.9%
- 25-48 months: 92.3%
- 13-24 months: 84.6%
- 0-12 months: 76.4%
- Insight: Tenure strongly correlates with retention

### Renewal Rate by Engagement Band

**Visual:** Bar chart
- High: 85.0%
- Medium: 84.5%
- Low: 84.7%
- Insight: Engagement band does NOT differentiate renewal rates

### Renewal Rate by Value Segment

**Visual:** Bar chart
- High Value: 85.0%
- Medium Value: 84.7%
- Low Value: 84.5%
- Premium: 83.3%
- Insight: Value segment has minimal impact on renewal

---

## Page 4: Correlation Matrix

**Visual:** Heatmap
- Variables: tenure, monthly_charges, total_charges, engagement_score, total_interactions, total_content_views, total_events, total_logins, total_sessions, total_features, total_active_days
- Color scale: Red (negative) to Blue (positive)
- Key insight: Tenure and total_charges are strongly positively correlated

---

## Page 5: Contract × Engagement Analysis

**Visual:** Grouped bar chart
- X-axis: Contract Type (Month-to-month, One year, Two year)
- Color: Engagement Band (Low, Medium, High)
- Y-axis: Renewal Rate (%)
- Insight: Contract type drives renewal more than engagement

---

## Page 6: At-Risk Clients

### At-Risk Definition
- Bottom 25% on total_interactions AND bottom 25% on avg_logins_per_day

### Metrics
- At-Risk Clients: 221 (3.1%)
- At-Risk Renewal Rate: 86.0%
- Overall Renewal Rate: 84.6%
- Insight: At-risk clients actually have a slightly higher renewal rate than average

### Visual: Slicer
- Filter by: Contract Type, Tenure Band, Value Segment, Engagement Band

---

## Data Refresh Instructions

1. Open the Power BI Desktop file
2. Go to Data source settings
3. Point to `data/processed/customer_features_vB.csv`
4. Click Refresh
5. All visuals will update automatically

---

## Color Scheme

- Primary Blue: #2E75B6 (headers, primary data)
- Green: #70AD47 (positive metrics, renewal)
- Red: #C5504B (churn, negative metrics)
- Yellow: #FFC000 (caution, medium)
- Gray: #E7E6E6 (backgrounds)

---

## Interactivity

- Slicers: Contract Type, Tenure Band, Engagement Band, Value Segment, Churn
- Drill-through: From any chart to detailed customer list
- Tooltips: Hover for exact values and percentages
- Cross-filtering: Click any segment to filter all visuals

---

## Files Referenced

| File | Purpose |
|------|---------|
| `powerbi/screenshots/01_data_overview.png` | Data distributions |
| `powerbi/screenshots/02_engagement_vs_renewal.png` | Engagement comparison |
| `powerbi/screenshots/03_renewal_by_contract.png` | Contract analysis |
| `powerbi/screenshots/04_renewal_by_tenure.png` | Tenure analysis |
| `powerbi/screenshots/05_correlation_matrix.png` | Correlation heatmap |
| `powerbi/screenshots/06_engagement_comparison.png` | Metrics comparison |
| `powerbi/screenshots/07_engagement_by_contract.png` | Engagement by contract |
| `powerbi/screenshots/08_renewal_by_segment.png` | Segment analysis |
| `excel/executive_reporting.xlsx` | Data source for Power BI |
| `data/processed/customer_features_vB.csv` | Primary data source |
