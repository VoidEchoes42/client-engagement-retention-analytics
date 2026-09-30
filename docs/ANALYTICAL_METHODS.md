# Analytical Methods

This document describes the analytical techniques used in each phase of the project.

---

## Data Quality Methods

### Completeness Checks
- Count NULL values per column
- Percentage of missing values per field
- Documented in `data_quality_report.md`

### Duplicate Detection
- `customer_id` uniqueness in dimension tables
- `interaction_id` uniqueness in fact_interaction
- `usage_id` uniqueness in fact_content_usage
- `event_participation_id` uniqueness in fact_event_participation
- `activity_id` uniqueness in fact_account_activity

### Range Validation
- No negative durations, charges, or counts
- Dates within expected range (not future-dated)
- Contract values within business-expected range

### Referential Integrity
- Every FK in fact tables must exist in the corresponding dimension table
- No orphan records

### Category Consistency
- Standardized casing and spelling
- Example: "Webinar", "webinar", "WEBINAR" → "Webinar"

---

## SQL Methods

### Level 1: Basic Aggregation
- `COUNT()`, `SUM()`, `AVG()` for totals and averages
- `GROUP BY` for segment breakdowns
- `WHERE` for filtering

### Level 2: Intermediate Analysis
- Conditional aggregation with `CASE WHEN`
- `JOIN` operations across fact and dimension tables
- Date functions for time-based analysis
- Subqueries for derived metrics

### Level 3: Advanced Techniques
- **CTEs (Common Table Expressions):** Break complex logic into readable steps
- **Window Functions:**
  - `ROW_NUMBER()` — rank clients within segments
  - `RANK()` — handle ties in ranking
  - `LAG()` — compare current vs. previous period activity
  - `LEAD()` — look ahead to renewal dates
  - `SUM() OVER()` — running totals
  - `AVG() OVER()` — moving averages
- **Cohort Logic:** Group clients by acquisition period and track retention

---

## Statistical Methods (Python)

### Descriptive Statistics
- Mean, median, mode, standard deviation
- Distribution shapes (histograms, box plots)
- Five-number summary

### Correlation Analysis
- Pearson correlation for continuous variables
- Spearman correlation for ranked variables
- Correlation matrix visualization

### Group Comparison
- **Chi-square test:** Association between categorical variables (e.g., plan type vs. renewal)
- **t-test / Mann-Whitney U:** Compare continuous metrics between renewed and non-renewed groups

### Confidence Intervals
- 95% CI for renewal rates by segment
- Bootstrap CI for engagement score distributions

### Feature Engineering
- Engagement score calculation (weighted composite)
- Activity trend calculation (recent vs. historical)
- Segment definitions (contract value, tenure, engagement bands)

---

## Engagement Score Methodology

### Version A: Equal Weighting
```
Engagement Score = (Activity + Interactions + Content + Events + Recent) / 5
```

### Version B: Business-Rule Weighting
```
Engagement Score =
  30% × normalized(activity metrics)
+ 25% × normalized(interaction frequency)
+ 20% × normalized(content consumption)
+ 15% × normalized(event participation)
+ 10% × normalized(recent activity)
```

### Version C: Standardized Components
```
Each component = (value - mean) / std_dev
Engagement Score = weighted sum of standardized components
```

**Normalization:** Min-max scaling to [0, 1] range within each component before weighting.

---

## Retention Analysis Methods

### Renewal Rate Calculation
```
Renewal Rate = COUNT(renewed = Yes) / COUNT(total) × 100
```

### Cohort Analysis
- Group by contract start month/quarter
- Track renewal rate by cohort over time
- Compare cohort trajectories

### Engagement Band Analysis
- Divide clients into quartiles or custom bands based on engagement score
- Compare renewal rate across bands
- Identify threshold effects

### Pre-Renewal Activity Analysis
- Calculate 30/60/90-day activity windows before renewal
- Compare activity levels between renewed and non-renewed clients
- Identify declining activity patterns using `LAG()`

---

## Visualization Methods

### Python (Matplotlib/Seaborn)
- Histograms for distributions
- Box plots for group comparisons
- Scatter plots for relationships
- Heatmaps for correlation matrices
- Bar charts for segment comparisons

### Power BI
- KPI cards for headline metrics
- Line charts for trends
- Bar/column charts for segment comparisons
- Scatter plots for engagement vs. renewal
- Tables for investigation lists
- Slicers for interactive filtering

---

## Limitations of Methods

1. **Synthetic data limits generalizability.** Findings are educational, not predictive.
2. **No causal inference.** Statistical associations do not prove causation.
3. **Engagement score is analyst-defined.** Weights are subjective and should be validated with business stakeholders.
4. **Sample size.** With ~7,000 records, some segments may have insufficient data for reliable estimates.
5. **Single time period.** The analysis covers one snapshot in time, not longitudinal trends.
