# Data Quality Report

## Generated
2026-10-01 04:02:55

## Data Sources
- **Public:** IBM Telco Customer Churn dataset (customer_base.csv)
- **Synthetic:** Generated via generate_synthetic_data.py with RANDOM_SEED = 42

## Cleaning Steps Performed

### 1. Customer Data
- Converted blank TotalCharges to NULL, then imputed with MonthlyCharges × Tenure
- Standardized gender, partner, dependents, churn to title case
- Removed duplicate customer IDs
- Converted numeric columns to proper types

### 2. Interactions
- Standardized interaction_type, channel, outcome to title case
- Fixed inconsistent casing (~1% of interaction types)
- Removed records with negative duration
- Removed duplicate interaction IDs

### 3. Content Usage
- Standardized content_category to title case
- Removed records with negative reports_viewed, downloads, or time_spent_minutes
- Marked ~2% of usage dates as missing (intentional for data quality demonstration)
- Removed duplicate usage IDs

### 4. Event Participation
- Standardized event_type, registered, attended to title case
- Removed duplicate event participation IDs

### 5. Account Activity
- Removed duplicate activity IDs (including intentional "_dup" suffixes)
- Removed records with negative counts

## Referential Integrity
- All fact table customer_ids validated against dim_customer
- No orphan records detected

## Known Issues
1. ~2% of content_usage records have missing usage_date (intentional)
2. ~1% of interaction_type values had inconsistent casing (now fixed)
3. Some account_activity records had duplicate IDs (now removed)

## Row Counts After Cleaning
| Table | Rows |
|-------|------|
| Customer | 7043 |
| Interactions | 25000 |
| Content Usage | 30000 |
| Event Participation | 5950 |
| Account Activity | 799220 |
| Events | 20 |

## Recommendations
1. Consider imputing missing usage_dates with the nearest available date
2. Add NOT NULL constraints in the production database schema
3. Implement automated data quality checks in the ingestion pipeline
