# Client Engagement & Subscription Retention Analytics

> An end-to-end business analytics project investigating how customer engagement, product usage, and client interactions relate to subscription renewal.

**Tools:** SQL | Python | Pandas | Excel | Power BI | Statistics

---

## Project Overview

This project demonstrates a complete analytics workflow built to answer a realistic business question. It uses a publicly available fictional customer churn dataset combined with clearly labeled synthetic operational data to simulate a real-world analytics environment.


---

## Business Problem

A fictional B2B subscription company wants to understand what engagement patterns are associated with subscription renewal. Management knows who renewed and who did not, but lacks an analytical view of:

- What engagement patterns are associated with renewal?
- Which client segments have different retention levels?
- Does recent activity matter differently from lifetime activity?
- Which clients show declining engagement near their renewal period?

**Primary Question:** What patterns in client engagement, product usage, and client interactions are associated with subscription renewal?

---

## Data Sources

### Public Data
- **IBM Telco Customer Churn** — public sample dataset providing customer demographics, subscription details, contract values, and churn labels.

### Synthetic Data (Educational)
The following tables were programmatically generated to simulate operational activity:

- `interactions` — client meetings, webinars, support tickets
- `content_usage` — reports viewed, downloads, time spent
- `event_participation` — webinar/conference attendance
- `account_activity` — logins, sessions, feature usage

All synthetic data uses a fixed random seed (`RANDOM_SEED = 42`) for reproducibility.

---

## Project Structure

```
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   ├── public/         # IBM Telco dataset
│   │   └── synthetic/      # Generated operational data
│   ├── staging/
│   └── processed/
│
├── docs/
│   ├── PROJECT_PLAN.md
│   ├── DATA_DICTIONARY.md
│   ├── DATA_LINEAGE.md
│   ├── ASSUMPTIONS.md
│   └── ANALYTICAL_METHODS.md
│
├── sql/
│   ├── 01_schema.sql
│   ├── 02_staging.sql
│   ├── 03_cleaning.sql
│   ├── 04_kpis.sql
│   ├── 05_retention_analysis.sql
│   └── 06_advanced_analysis.sql
│
├── src/
│   ├── generate_synthetic_data.py
│   ├── ingest_data.py
│   ├── clean_data.py
│   ├── validate_data.py
│   └── build_features.py
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_quality.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_retention_analysis.ipynb
│   └── 05_statistical_analysis.ipynb
│
├── excel/
│   └── executive_reporting.xlsx
│
├── powerbi/
│   ├── dashboard.pbix
│   └── screenshots/
│
└── reports/
    ├── executive_summary.md
    └── data_quality_report.md
```

---

## Analytical Approach

The project follows a structured 10-phase workflow:

1. **Business Understanding** — define questions, KPIs, and scope
2. **Data Acquisition** — obtain and document public data
3. **Synthetic Data Generation** — create realistic operational tables
4. **Data Quality** — validate, clean, and document data issues
5. **SQL Analytics** — 15+ queries from basic to advanced (CTEs, window functions)
6. **Python Analytics** — EDA, statistical testing, feature engineering
7. **Excel Layer** — pivot tables, KPI reconciliation, management reporting
8. **Power BI Dashboard** — 4-page interactive dashboard
9. **Final Analysis** — findings, limitations, business interpretation
10. **Portfolio Polish** — documentation, README, screenshots

---

## Key Analytical Principles

- **Descriptive + Diagnostic focus** — what happened and what patterns might explain it
- **No false causation claims** — correlation is documented, causation is not assumed
- **Honest limitations** — data boundaries, synthetic data caveats, and sample constraints are stated clearly
- **Reproducible** — fixed random seeds, documented generation process, clean code

---

## Tools & Technologies

| Tool | Purpose |
|------|---------|
| **SQL** | Data modeling, KPI queries, advanced analytics |
| **Python (Pandas)** | Data cleaning, EDA, statistical analysis |
| **Excel** | Pivot tables, KPI reconciliation, reporting |
| **Power BI** | Interactive dashboard, stakeholder communication |
| **Statistics** | Correlation, chi-square, t-tests, confidence intervals |

---

## Key Findings

**Data Scale:** 7,043 customers | 25,000 interactions | 30,000 content records | 5,950 events | 799,220 activity records

**Core Metrics:**
- Renewal Rate: **84.6%** (5,956 renewed, 1,087 churned)
- Total Monthly Revenue: **$448,305.85**
- Average Contract Value: **$1,336.03**
- Average Engagement Score: **0.294** (0–1 scale)

**Key Insights:**

1. **Contract type is the strongest predictor of renewal:**
   - Two year contracts: 98.5% renewal
   - One year contracts: 89.4% renewal
   - Month-to-month contracts: 77.6% renewal
   - Chi-square test: p < 0.001 (highly significant)

2. **Tenure strongly correlates with retention:**
   - 0–12 months: 76.4% renewal
   - 13–24 months: 84.6% renewal
   - 25–48 months: 92.3% renewal
   - 49+ months: 97.9% renewal

3. **Engagement score is NOT significantly different between renewed and churned clients:**
   - Renewed avg: 0.2935 | Churned avg: 0.2950
   - Difference: −0.5%
   - t-test: p = 0.62 (not significant at α = 0.05)
   - This is a critical finding — engagement alone is not a reliable churn signal

4. **At-risk clients (bottom 25% interactions + logins):**
   - 221 clients (3.1% of base)
   - At-risk renewal rate: 86.0% (slightly above average)

**Business Implications:**
- Contract type and tenure are actionable levers for retention strategy
- Engagement metrics alone should not be used as a churn prediction model
- Focus retention interventions on contract renewal windows and early-tenure clients

---

## What I Learned

This project spanned the full analytics lifecycle — from raw data ingestion to business-ready deliverables.

**Technical:**
- Building a star schema in SQLite with proper dimensional modeling
- Writing SQL at three complexity levels: basic aggregation, intermediate joins, advanced CTEs with window functions
- Generating reproducible synthetic data with controlled correlations using Python
- Engineering a composite engagement score with sensitivity analysis across three weighting schemes
- Using scipy for hypothesis testing (t-tests, chi-square, confidence intervals)
- Reconciling KPIs across SQL, Python, and Excel to ensure data consistency

**Analytical:**
- The most counterintuitive finding was that engagement score did NOT significantly predict renewal (p = 0.62) — contract type and tenure were far stronger signals
- Synthetic data generation requires deliberate design: too-perfect correlations are unrealistic, too-weak correlations are uninformative
- Data quality is not a one-time step — it requires validation, documentation, and honest disclosure of remaining issues
- A project portfolio should show end-to-end thinking, not just isolated analyses

**Portfolio:**
- Documenting assumptions and limitations is as important as the analysis itself
- Writing for a hiring manager means explaining the "so what" for every finding
- Version control (git) keeps the project history clean and shows professional workflow

---

## Future Improvements

- Logistic regression for churn prediction
- K-Means customer segmentation
- Cohort analysis by plan and segment
- Automated data pipeline
- Sensitivity analysis on engagement weights

---

## License

This project is released under the MIT License.

---

*Built as a self-learning portfolio project targeting an Associate Data Analyst role. All synthetic data is educational and does not represent real customers.*
