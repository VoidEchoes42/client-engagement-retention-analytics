# Client Engagement & Subscription Retention Analytics

> **Project type:** Self-learning business/data analytics portfolio project  
> **Primary goal:** Learn and demonstrate an end-to-end analytics workflow using Excel, SQL, Python, statistics, and Power BI.  
> **Important:** This is an independent educational project. It does **not** use Gartner proprietary data and must not be presented as a Gartner project.

---

## 1. Project Overview

### Project title

**Client Engagement & Subscription Retention Analytics**

### Suggested GitHub repository name

`client-engagement-retention-analytics`

### One-line description

> An end-to-end business analytics project investigating how customer engagement, product usage, and client interactions relate to subscription renewal.

### Core learning objective

The project is designed to show how a beginner/intermediate analyst can move from a real-world business question to:

1. understanding the business problem,
2. obtaining and documenting data,
3. designing a relational data model,
4. cleaning and validating data,
5. querying data with SQL,
6. exploring and analyzing data with Python,
7. applying basic statistical reasoning,
8. building KPI reporting in Excel,
9. communicating findings through Power BI,
10. converting findings into business recommendations.

The project should look like a **student learning analytics by solving a structured business problem**, not like a fabricated claim of having worked on an enterprise client's confidential data.

---

# 2. Business Problem

A fictional B2B subscription company provides research/content/services to business clients.

The company has information about:

- client characteristics,
- subscription plans,
- product/service usage,
- content consumption,
- client interactions,
- event participation,
- account activity,
- renewals/churn.

Management knows **who renewed and who did not**, but does not have a clear analytical view of:

- what engagement patterns are associated with renewal,
- which client segments have different retention levels,
- whether engagement changes before renewal,
- which clients show declining activity,
- which business metrics are useful for monitoring retention.

### Primary business question

> **What patterns in client engagement, product usage, and client interactions are associated with subscription renewal?**

### Secondary questions

1. Which client segments have different renewal rates?
2. What does a highly engaged client look like?
3. Are usage and interaction levels different between renewed and non-renewed clients?
4. Does recent activity matter differently from lifetime activity?
5. Are certain subscription types associated with higher/lower renewal?
6. Do high-value clients behave differently from lower-value clients?
7. Which clients show declining engagement near their renewal period?
8. Which metrics should management monitor regularly?
9. Which findings are strong enough to act on, and which require further investigation?

---

# 3. Important Scope & Honesty Rules

This section is mandatory.

## 3.1 No Gartner proprietary data

Do not use:

- Gartner customer data,
- Gartner internal systems,
- Gartner proprietary metrics,
- scraped Gartner customer information,
- confidential or restricted datasets.

Do not imply that the project was commissioned by, inspired by confidential Gartner work, or built from Gartner data.

## 3.2 Public + synthetic data

The project uses:

### Public source data

A publicly available **fictional customer churn dataset** can be used as the base customer/subscription dataset.

Recommended starting point:

**IBM Telco Customer Churn sample dataset**

Use the public dataset only for the fields that are actually present in it.

### Synthetic extension data

Create clearly labelled synthetic operational tables for:

- client interactions,
- content usage,
- event participation,
- account activity,
- product usage,
- monthly engagement/activity.

The README must clearly distinguish:

> **Public source data** vs **synthetically generated educational data**

## 3.3 Do not manufacture a fake business impact

Never write:

- "Increased revenue by 25%"
- "Reduced churn by 15%"
- "Saved the company ₹5 lakh"

unless such impact genuinely happened and is documented.

Instead use language such as:

- "The analysis identified..."
- "The results suggest..."
- "The pattern was associated with..."
- "The findings could help prioritize..."
- "Further testing would be required to establish causality."

---

# 4. Data Provenance

The project should have an explicit data lineage.

```text
PUBLIC DATA
    |
    v
Customer / Subscription Base
    |
    | customer_id
    |
    +--------------------+--------------------+--------------------+
    |                    |                    |                    |
    v                    v                    v                    v
Synthetic            Synthetic            Synthetic            Synthetic
Interactions         Usage Logs           Events               Activity
    |                    |                    |                    |
    +--------------------+--------------------+--------------------+
                         |
                         v
                    Data Warehouse
                         |
                         v
                    SQL Analytics
                         |
              +----------+----------+
              |                     |
              v                     v
           Python                Excel
              |                     |
              +----------+----------+
                         |
                         v
                  Analytical Model
                         |
                         v
                    Power BI
                         |
                         v
                  Business Insights
```

---

# 5. Proposed Data Sources

## 5.1 Base customer table

Source:

- Public sample dataset
- Customer/subscription/churn fields

Possible fields may include:

```text
customer_id
gender
senior_citizen
partner
dependents
tenure
phone_service
multiple_lines
internet_service
online_security
online_backup
device_protection
tech_support
streaming_tv
streaming_movies
contract
paperless_billing
payment_method
monthly_charges
total_charges
churn
```

Only retain fields actually present in the chosen source/version.

---

## 5.2 Synthetic client interaction table

Create this table for educational purposes.

Suggested columns:

```text
interaction_id
customer_id
interaction_date
interaction_type
channel
duration_minutes
outcome
```

Example interaction types:

```text
Analyst Meeting
Webinar
Support
Email
Product Demo
Account Review
```

Example channels:

```text
Online
Email
Phone
Video
In-Person
```

---

## 5.3 Synthetic content usage table

Suggested columns:

```text
usage_id
customer_id
usage_date
content_category
reports_viewed
downloads
time_spent_minutes
```

Possible content categories:

```text
Technology
Strategy
Operations
Finance
Marketing
Industry Research
```

---

## 5.4 Synthetic event participation table

Suggested columns:

```text
event_participation_id
customer_id
event_id
event_date
event_type
registered
attended
```

Possible event types:

```text
Webinar
Conference
Roundtable
Executive Session
Workshop
```

---

## 5.5 Synthetic account activity table

Suggested columns:

```text
activity_id
customer_id
activity_date
active_users
login_count
features_used
session_count
```

---

## 5.6 Subscription table

If the public dataset already contains subscription-level information, use it where appropriate.

If a separate subscription history table is needed, create a synthetic extension only where the public dataset does not provide the required history.

Suggested schema:

```text
subscription_id
customer_id
plan_type
start_date
renewal_date
contract_value
subscription_status
renewed
```

---

# 6. Data Model

The analytical model should use a simple relational/star-schema design.

## Dimension tables

### `dim_customer`

```text
customer_id PK
gender
age_group
senior_citizen
partner
dependents
region
industry
company_size
```

Some fields may be synthetic if they do not exist in the public source.

### `dim_subscription`

```text
subscription_id PK
customer_id FK
plan_type
contract_type
start_date
renewal_date
contract_value
status
```

### `dim_date`

```text
date PK
year
quarter
month
month_name
week
day_of_week
```

### `dim_content`

```text
content_id PK
content_category
content_type
```

### `dim_event`

```text
event_id PK
event_type
event_topic
```

## Fact tables

### `fact_interaction`

```text
interaction_id PK
customer_id FK
date FK
interaction_type
channel
duration_minutes
outcome
```

### `fact_content_usage`

```text
usage_id PK
customer_id FK
date FK
content_id FK
reports_viewed
downloads
time_spent_minutes
```

### `fact_event_participation`

```text
event_participation_id PK
customer_id FK
event_id FK
date FK
registered
attended
```

### `fact_account_activity`

```text
activity_id PK
customer_id FK
date FK
active_users
login_count
features_used
session_count
```

---

# 7. Key Relationships

Primary relationship:

```text
customer_id
```

Core structure:

```text
                    dim_customer
                         |
                         | customer_id
       +-----------------+-----------------+
       |                 |                 |
       v                 v                 v
fact_interaction  fact_content_usage  fact_event_participation
       |                 |                 |
       +-----------------+-----------------+
                         |
                         v
                fact_account_activity
                         |
                         v
                 dim_subscription
```

Use foreign-key validation to make sure there are no orphan records.

---

# 8. Synthetic Data Generation Rules

The synthetic data must be realistic enough for analysis but must not be presented as real-world observations.

## 8.1 General principle

Do not make synthetic data too perfect.

Include realistic:

- missing values,
- duplicate records,
- inconsistent category labels,
- date issues,
- varying activity levels,
- inactive clients,
- unusual values,
- uneven segment sizes.

These defects will allow the project to demonstrate data cleaning and quality checks.

## 8.2 Avoid artificial conclusions

Do not create the synthetic data so that:

```text
high engagement -> renewal
low engagement  -> churn
```

with near-perfect separation.

That would make the analysis look engineered.

Instead:

- allow substantial overlap,
- include exceptions,
- introduce noise,
- make relationships moderate rather than deterministic.

The final project should demonstrate that analytical findings were discovered rather than hard-coded.

## 8.3 Reproducibility

Use a fixed random seed.

Example:

```python
RANDOM_SEED = 42
```

Document how synthetic data was generated.

---

# 9. Data Generation Process

Suggested process:

```text
1. Obtain public base dataset
2. Inspect schema
3. Standardize customer IDs
4. Create a master customer table
5. Generate synthetic activity records
6. Generate synthetic interaction records
7. Generate synthetic content usage
8. Generate synthetic event participation
9. Generate synthetic subscription history where necessary
10. Introduce controlled data-quality issues
11. Save raw synthetic data
12. Clean into staging tables
13. Validate keys and ranges
14. Load clean data into SQL
```

---

# 10. Data Quality Layer

Data quality must be a visible part of the project.

Check for:

### Missing values

```text
customer_id
dates
contract value
categorical fields
```

### Duplicates

```text
duplicate customer IDs
duplicate interaction IDs
duplicate event records
```

### Invalid values

```text
negative duration
negative revenue
invalid dates
future dates
impossible activity counts
```

### Referential integrity

```text
Does every customer_id in fact tables exist in dim_customer?
```

### Category consistency

For example:

```text
"Webinar"
"webinar"
"WEBINAR"
```

should be standardized.

### Reconciliation

Compare:

```text
Raw rows
vs
Staged rows
vs
Clean rows
vs
SQL aggregation
vs
Power BI totals
```

---

# 11. SQL Analytics

SQL should be a major part of the project.

## Level 1 — Basic

- total customers
- total revenue
- renewal count
- churn count
- average contract value
- clients by plan
- clients by region

## Level 2 — Intermediate

- renewal rate by segment
- revenue by subscription type
- average engagement by renewal status
- interaction frequency by segment
- monthly activity trends
- repeat event attendance
- customer cohorts

## Level 3 — Advanced

Use:

- CTEs
- window functions
- conditional aggregation
- date functions
- ranking
- cohort logic

Examples:

```text
ROW_NUMBER()
RANK()
LAG()
LEAD()
SUM() OVER()
AVG() OVER()
```

Potential questions:

1. What was each client's activity in the 30/60/90 days before renewal?
2. Which client segments experienced the largest change in engagement?
3. Which clients have declining recent activity?
4. What is the average engagement by renewal status?
5. How does engagement vary by tenure?
6. Which plans have higher retention?
7. What share of high-value customers renewed?

---

# 12. Python Analytics

Use Python primarily for exploration and statistical analysis.

Recommended libraries:

```text
pandas
numpy
matplotlib
scipy
scikit-learn (optional)
```

## Python tasks

### Data cleaning

- type conversion
- missing values
- category normalization
- duplicate handling
- outlier inspection

### Exploratory analysis

Investigate:

- distributions
- trends
- segment differences
- engagement patterns
- renewal differences

### Statistical analysis

Possible techniques:

- descriptive statistics
- correlation analysis
- confidence intervals
- chi-square test for categorical relationships
- t-test or Mann-Whitney U where appropriate

Do not run tests just for decoration.

Every statistical method must answer a specific question.

---

# 13. Important Analytical Principle

The project should explicitly distinguish:

### Descriptive

> What happened?

### Diagnostic

> What patterns might explain what happened?

### Predictive

> Can we estimate what may happen?

### Prescriptive

> What could the business investigate or do next?

The main project should focus on:

**Descriptive + Diagnostic analytics**

Predictive analytics can be a small optional extension.

This keeps the project aligned with an Associate Data Analyst role rather than turning it into a machine-learning project.

---

# 14. Engagement Score

A simple composite score can be created for educational purposes.

Example:

```text
Engagement Score =
30% Product/Usage Activity
25% Client Interactions
20% Content Consumption
15% Event Participation
10% Recent Activity
```

Important:

- Document the weighting logic.
- Explain that it is an analyst-created educational framework.
- Do not claim that this is an industry-standard formula.
- Test whether different weighting schemes materially change conclusions.

A better version is to compare:

```text
Version A: equal weighting
Version B: business-rule weighting
Version C: standardized/normalized components
```

This creates a useful discussion around metric design.

---

# 15. Retention Analysis

Primary comparison:

```text
Renewed clients
vs
Non-renewed clients
```

Compare:

- average engagement,
- interaction frequency,
- reports viewed,
- time spent,
- event participation,
- active users,
- feature usage,
- tenure,
- contract value.

### Important caution

If the source churn/renewal outcome is historical, do not accidentally use information that occurred after the renewal/churn event to explain the outcome.

Define a clear **analysis window**.

For example:

```text
Observation window:
90 days before renewal date

Outcome:
Renewed / Not Renewed
```

This prevents leakage.

---

# 16. Client Risk Analysis

Create an **analytical investigation list**, not a claim of a production churn model.

Example rule:

```text
At-risk investigation candidate if:

- renewal within next 90 days
AND
- recent activity is declining
AND
- engagement is below historical average
```

This should be described as:

> "An analyst-defined prioritization rule for investigation."

Do not call it a validated churn prediction model unless you actually build and evaluate one.

---

# 17. Power BI Dashboard

Create 4 pages.

## Page 1 — Executive Overview

KPIs:

```text
Total Clients
Renewal Rate
Churn Rate
Subscription Revenue
Average Contract Value
Average Engagement Score
Clients Requiring Investigation
```

Visuals:

- renewal trend
- revenue trend
- renewal by segment
- engagement distribution

---

## Page 2 — Client Engagement

Visuals:

- usage over time
- interactions by type
- content consumption
- event participation
- engagement by plan
- engagement by client segment

---

## Page 3 — Retention Analysis

Visuals:

- renewal rate by plan
- renewal rate by tenure
- renewal rate by engagement band
- renewal rate by contract value
- renewed vs non-renewed engagement comparison

---

## Page 4 — Investigation View

Table:

```text
Customer
Renewal Date
Contract Value
Engagement Score
Recent Activity
Activity Change
Interaction Count
Investigation Flag
```

Add slicers:

```text
Region
Plan
Industry
Contract Type
Engagement Band
Renewal Window
```

---

# 18. Excel Layer

Excel should have a genuine purpose.

Use Excel for:

- initial validation,
- pivot tables,
- KPI reconciliation,
- simple management reporting,
- formula-based checks.

Suggested workbook:

```text
executive_reporting.xlsx

Sheets:
1. README
2. Raw_Checks
3. KPI_Summary
4. Segment_Analysis
5. Retention_Analysis
6. Reconciliation
```

Potential formulas:

```text
SUMIFS
COUNTIFS
XLOOKUP
IFERROR
AVERAGEIFS
```

Use Pivot Tables where useful.

---

# 19. Recommended Repository Structure

```text
client-engagement-retention-analytics/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── README.md
│   ├── raw/
│   │   ├── public/
│   │   └── synthetic/
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
├── reports/
│   ├── executive_summary.pdf
│   └── data_quality_report.md
│
└── tests/
    ├── test_data_quality.py
    └── test_transformations.py
```

---

# 20. GitHub README Structure

The root `README.md` should contain:

```text
1. Project Overview
2. Business Problem
3. Why I Built This Project
4. Data Sources & Provenance
5. Data Lineage
6. Data Model
7. Analytical Questions
8. Tools
9. Data Quality
10. SQL Analysis
11. Python Analysis
12. Power BI Dashboard
13. Key Findings
14. Business Interpretation
15. Limitations
16. Reproducibility
17. Project Structure
18. What I Learned
19. Future Improvements
```

---

# 21. Why I Built This Project

Write this section honestly.

Suggested direction:

> I built this project as a self-learning exercise to understand how business analysts work with customer and operational data. I wanted to move beyond simply creating charts and learn how to define business questions, structure data, validate metrics, analyze customer behavior, and communicate findings to a non-technical audience.

Do not claim professional work experience from this project.

---

# 22. Expected Learning Outcomes

By the end of the project, demonstrate knowledge of:

### Excel

- formulas
- pivots
- reconciliation
- business reporting

### SQL

- joins
- aggregation
- CTEs
- window functions
- date analysis

### Python

- pandas
- data cleaning
- EDA
- statistical analysis
- reproducible scripts

### Power BI

- data model
- calculated measures
- filtering
- dashboard design
- stakeholder-oriented reporting

### Business analytics

- KPI definition
- segmentation
- trend analysis
- root-cause investigation
- metric design
- interpretation
- recommendation framing

---

# 23. Key Findings: How to Write Them

Do not dump screenshots and say:

> "The dashboard shows..."

Instead format findings like:

### Finding 1

**Observation**

Renewal rates differ across client segments.

**Evidence**

Show the relevant metric and population.

**Interpretation**

The difference indicates a segment-level pattern worth investigating.

**Caution**

The analysis does not establish that the segment itself causes renewal differences.

**Business implication**

Management could investigate whether service adoption, pricing, contract structure, or engagement differs across segments.

---

# 24. Example Interview Questions This Project Should Prepare You For

Be prepared to explain:

### Business

- Why did you choose retention?
- What does retention mean?
- Which KPI matters most?
- What would management actually do with the dashboard?

### Data

- Where did the data come from?
- What is public vs synthetic?
- Why did you generate synthetic tables?
- How did you choose the fields?
- How did you ensure reproducibility?

### SQL

- Why did you use CTEs?
- Explain one complex query.
- How did you avoid double-counting?
- How did you calculate renewal rate?

### Python

- Why Python after SQL?
- What cleaning did you perform?
- Which relationships did you investigate?
- Which statistical test did you use and why?

### Power BI

- Why those KPIs?
- Why those visualizations?
- How did you validate dashboard numbers?

### Analytical reasoning

- Does correlation imply causation?
- How would you validate the engagement score?
- What are the limitations?
- What additional data would you request?

---

# 25. Potential Resume Description

Do not write the final bullets until the project is actually completed.

Possible structure:

> **Client Engagement & Subscription Retention Analytics | SQL, Python, Excel, Power BI**
>
> - Built an end-to-end analytics workflow integrating public customer churn data with clearly labelled synthetic interaction, usage, and event datasets.
> - Developed SQL-based KPI and retention analyses and used Python for data quality checks, exploratory analysis, segmentation, and statistical testing.
> - Created an interactive Power BI dashboard to analyze engagement, renewal patterns, customer segments, and accounts requiring further investigation.

Replace generic wording with real numbers only after the project is complete.

---

# 26. Recommended Build Phases

## Phase 1 — Business Understanding

Deliver:

```text
business problem
analytical questions
KPIs
scope
assumptions
```

## Phase 2 — Data Acquisition

Deliver:

```text
public dataset
source documentation
data provenance
initial schema
```

## Phase 3 — Synthetic Data Generation

Deliver:

```text
generator script
fixed random seed
synthetic datasets
generation documentation
```

## Phase 4 — Data Quality

Deliver:

```text
quality checks
cleaned data
data-quality report
```

## Phase 5 — SQL

Deliver:

```text
database schema
SQL queries
analytical views
KPI outputs
```

## Phase 6 — Python

Deliver:

```text
EDA
statistical analysis
feature engineering
plots
```

## Phase 7 — Excel

Deliver:

```text
KPI workbook
pivot analysis
reconciliation
```

## Phase 8 — Power BI

Deliver:

```text
dashboard
data model
measures
screenshots
```

## Phase 9 — Final Analysis

Deliver:

```text
findings
limitations
business interpretation
executive summary
```

## Phase 10 — Portfolio Polish

Deliver:

```text
README
screenshots
data dictionary
lineage diagram
clean repository
```

---

# 27. Minimum Viable Version

Do not build everything at once.

MVP:

```text
1 public dataset
4 synthetic tables
SQL database
10-15 useful SQL queries
1 Python EDA notebook
1 Excel workbook
1 Power BI dashboard
data-quality checks
README
```

Then iterate.

---

# 28. Possible Advanced Extensions

Only add these after the core analytics project is working.

### A. Simple churn/renewal prediction

Use:

- logistic regression
- decision tree

Evaluate with:

- precision
- recall
- F1
- ROC-AUC

Do not make ML the headline.

### B. Customer segmentation

Use:

- K-Means

But first establish whether the segments are interpretable and useful.

### C. Cohort analysis

Track retention by:

- acquisition/starting period,
- plan,
- segment.

### D. Automated reporting

Create a reproducible pipeline:

```text
new data
  ↓
Python
  ↓
validation
  ↓
SQL
  ↓
Power BI refresh
```

### E. Sensitivity analysis

Check whether conclusions change when:

- engagement weights change,
- observation window changes,
- outliers are removed.

This is especially useful for demonstrating analytical maturity.

---

# 29. Major Risks to Avoid

## Risk 1 — Overengineering

Do not build:

- deep learning,
- complex cloud infrastructure,
- unnecessary APIs,
- advanced MLOps.

The goal is **data analytics**, not software engineering.

## Risk 2 — Synthetic data that looks fake

Avoid perfectly balanced data and perfect relationships.

## Risk 3 — Dashboard-first thinking

The dashboard is the final communication layer, not the project itself.

## Risk 4 — Confusing correlation with causation

Use careful wording.

## Risk 5 — Data leakage

Do not use post-outcome activity to predict/explain the outcome.

## Risk 6 — Too many KPIs

Use a small set of meaningful business metrics.

## Risk 7 — Unsupported business claims

Do not claim measurable business impact that did not happen.

---

# 30. Quality Bar Before Publishing

The project should not be published until all of these are true:

### Data

- [ ] Sources documented
- [ ] Public vs synthetic clearly labelled
- [ ] Data dictionary complete
- [ ] Foreign keys validated
- [ ] Duplicate checks performed
- [ ] Missing values documented
- [ ] Synthetic generator reproducible

### SQL

- [ ] Schema works
- [ ] Joins verified
- [ ] No accidental double counting
- [ ] KPIs reconcile with source data
- [ ] Intermediate/advanced queries included

### Python

- [ ] Notebook runs from a clean environment
- [ ] EDA has a purpose
- [ ] Statistical tests are justified
- [ ] Charts are readable
- [ ] No hard-coded conclusions

### Excel

- [ ] KPI calculations work
- [ ] Reconciliation works
- [ ] Pivot analyses work

### Power BI

- [ ] Data model is logical
- [ ] Measures are documented
- [ ] Filters work
- [ ] KPI totals reconcile with SQL

### README

- [ ] Business problem is clear
- [ ] Data lineage is visible
- [ ] Findings are explained
- [ ] Limitations are stated
- [ ] No false claims
- [ ] Screenshots included

---

# 31. Claude Review Instructions

Use the following prompt when asking Claude to review this project specification.

---

## Prompt for Claude

You are reviewing a proposed GitHub portfolio project for a student targeting an **Associate Data Analyst role at Gartner**.

The project is:

**Client Engagement & Subscription Retention Analytics**

The purpose is to demonstrate learning and practical ability in:

- Excel
- SQL
- Python/pandas
- basic statistics
- Power BI
- data cleaning
- data quality
- business problem solving
- communicating insights to non-technical stakeholders

The project uses:

1. a publicly available fictional customer-churn dataset as the base data,
2. clearly labelled synthetic operational tables for interactions, content usage, events, and account activity.

Please review this project specification as a **technical mentor + data analytics hiring manager**.

### Review criteria

#### 1. Business realism

Does the problem look like something a student could reasonably choose to learn analytics through?

Does it look realistic without pretending to have access to proprietary enterprise data?

#### 2. Gartner relevance

Assess whether the project demonstrates skills useful for an Associate Data Analyst role such as:

- SQL
- Excel
- Power BI
- Python
- statistics
- data validation
- root-cause analysis
- KPI definition
- business communication
- stakeholder thinking

Do not invent Gartner-specific requirements that are not supported by the project description.

#### 3. Data design

Review:

- table structure,
- primary keys,
- foreign keys,
- grain,
- relationships,
- synthetic-data generation,
- data lineage.

Identify any modeling mistakes or unnecessary tables.

#### 4. Analytical validity

Check:

- whether the questions are answerable,
- whether metrics are well-defined,
- whether the engagement score is defensible,
- whether there is risk of double counting,
- whether there is data leakage,
- whether correlation/causation is handled correctly.

#### 5. Synthetic data

Tell me whether the proposed synthetic data could accidentally manufacture the desired result.

Suggest a better way to generate realistic noise and moderate associations.

#### 6. Technical scope

Tell me what is:

- essential,
- optional,
- unnecessary.

The project should remain appropriate for a student rather than becoming overengineered.

#### 7. Portfolio quality

Review:

- repository structure,
- README,
- dashboard,
- notebooks,
- SQL scripts,
- documentation.

Tell me what would make this project look genuinely self-developed and educational rather than copied from a tutorial.

#### 8. Interview value

Give me the strongest technical and business questions an interviewer could ask from this project.

#### 9. Required changes

Identify:

- critical changes,
- recommended improvements,
- nice-to-have extensions.

Do not redesign the project completely unless there is a serious flaw.

#### 10. Final recommendation

Give:

- overall assessment,
- biggest strengths,
- biggest weaknesses,
- 5 highest-priority changes,
- suggested MVP scope.

Important constraints:

- Do not assume access to confidential Gartner data.
- Do not claim the project is equivalent to real Gartner internal work.
- Keep the project focused on analytics rather than ML.
- Keep public and synthetic data clearly separated.
- Prefer honest, reproducible, explainable analysis over impressive but unnecessary complexity.

---

# 32. Final Project Philosophy

The project should communicate this story:

```text
I had a business question
        ↓
I needed data
        ↓
I learned how to structure the data
        ↓
I learned SQL
        ↓
I learned Python
        ↓
I validated my data
        ↓
I investigated patterns statistically
        ↓
I built a dashboard
        ↓
I learned to communicate findings
        ↓
I understood the limitations of my analysis
```

The goal is not to look like a senior analyst.

The goal is to look like a **strong candidate who deliberately learned data analytics by solving a realistic business problem and can explain every step of the work.**
