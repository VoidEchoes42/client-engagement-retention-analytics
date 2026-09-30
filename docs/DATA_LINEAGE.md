# Data Lineage

This document traces how data flows from source to final analysis.

```
PUBLIC DATA                          SYNTHETIC DATA
    |                                       |
    v                                       v
IBM Telco Churn Dataset           generate_synthetic_data.py
    |                                       |
    |  customer_id                          |  customer_id (same IDs)
    |                                       |
    v                                       v
    +-----------------+---------------------+
                      |
                      v
                ingest_data.py
              (standardize IDs,
               validate schema)
                      |
                      v
                clean_data.py
              (missing values,
               duplicates,
               type conversion,
               category normalization)
                      |
                      v
                staging tables
              (validated, cleaned)
                      |
                      v
                validate_data.py
              (FK checks, range checks,
               duplicate checks)
                      |
                      v
                processed tables
              (star schema)
                      |
            +---------+---------+
            |                   |
            v                   v
         SQL                  Python
    (KPIs, retention,       (EDA, statistics,
     advanced queries)       feature engineering)
            |                   |
            +---------+---------+
                      |
                      v
              Analytical Model
           (engagement scores,
            segment analysis,
            retention comparison)
                      |
                      v
                  Power BI
            (4-page dashboard)
                      |
                      v
              Business Insights
            (executive summary,
             recommendations)
```

## Layer-by-Layer Description

### Layer 1: Raw Data
- **Public:** IBM Telco dataset loaded as-is (no modification)
- **Synthetic:** Generated via `generate_synthetic_data.py` with `RANDOM_SEED = 42`

### Layer 2: Staging
- ID standardization across all tables
- Type conversions (dates, numbers, categories)
- Missing value documentation
- Duplicate identification

### Layer 3: Processed (Star Schema)
- Dimension tables populated
- Fact tables linked via foreign keys
- Referential integrity validated
- Data quality report generated

### Layer 4: Analytics
- SQL queries produce KPI tables and analytical views
- Python notebooks explore distributions, correlations, segment differences
- Engagement score computed

### Layer 5: Communication
- Excel workbook for management reporting
- Power BI dashboard for interactive exploration
- Executive summary for stakeholders
