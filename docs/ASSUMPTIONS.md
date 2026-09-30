# Assumptions

This document records all assumptions made during the project.

## Data Assumptions

1. **IBM Telco dataset represents B2B clients.** The original dataset is consumer-focused. For this project, we treat customers as business clients without changing the underlying data fields.

2. **Churn = non-renewal.** We interpret the `Churn` field as "subscription not renewed" for analytical purposes.

3. **Synthetic data simulates operational activity.** The interactions, content usage, events, and account activity tables are fictional and designed to be realistic but not perfectly correlated with renewal.

4. **Analysis window is 90 days before renewal.** To avoid data leakage, all engagement metrics are calculated within a 90-day window before the renewal date (or churn date for non-renewed clients).

5. **Engagement score weights are analyst-defined.** The weighting scheme (30/25/20/15/10) is an educational construct, not an industry standard.

## Business Assumptions

6. **The fictional company offers research/content/services** similar to analyst firms like Gartner, Forrester, etc.

7. **Contract value reflects annual subscription value** for B2B clients.

8. **Interaction types cover the main client engagement channels** for a research subscription business.

9. **Content categories represent the main research domains** a client-focused analytics firm would provide.

## Technical Assumptions

10. **SQLite is used as the database engine** for simplicity and portability. The project can be adapted to PostgreSQL or MySQL with minor changes.

11. **Python 3.10+ is required** for all scripts and notebooks.

12. **Power BI Desktop is required** to open and edit the `.pbix` file.

## Analytical Assumptions

13. **Correlation does not imply causation.** All findings are descriptive/diagnostic unless explicitly tested for prediction.

14. **Sample size limitations.** With ~7,000 customers in the base dataset, findings may not generalize to very large or very small client bases.

15. **Synthetic data introduces noise deliberately.** Moderate (not perfect) relationships between engagement and renewal are intentional to demonstrate realistic analysis.
