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

*(To be added after analysis completion)*

---

## What I Learned

*(To be added after project completion)*

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
