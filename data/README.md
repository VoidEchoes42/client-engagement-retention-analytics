# Data Directory

This directory contains all data used in the project.

## Structure

```
data/
├── raw/
│   ├── public/       # Publicly available datasets (not in git due to size)
│   └── synthetic/    # Synthetically generated educational data
├── staging/          # Cleaned and validated data ready for analysis
└── processed/        # Final datasets used for SQL, Python, and Power BI
```

## Data Provenance

### Public Data
- **IBM Telco Customer Churn** — used as the base customer/subscription dataset
- Source: publicly available sample dataset
- Contains: customer demographics, subscription details, contract values, churn labels

### Synthetic Data
The following tables are synthetically generated for educational purposes:
- `interactions.csv` — client meeting and support interactions
- `content_usage.csv` — report views, downloads, time spent
- `event_participation.csv` — event registration and attendance
- `account_activity.csv` — login counts, sessions, feature usage

**All synthetic data uses `RANDOM_SEED = 42` for reproducibility.**

## Generating Synthetic Data

```bash
python src/generate_synthetic_data.py
```

This will create all synthetic tables in `data/raw/synthetic/`.

## Data Quality

See `docs/DATA_QUALITY_REPORT.md` for validation results and known issues.
