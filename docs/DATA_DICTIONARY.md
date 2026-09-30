# Data Dictionary

This document describes all tables and fields used in the project.

---

## Public Data: IBM Telco Customer Churn

### Source
- Publicly available fictional customer churn dataset
- Used as the base customer and subscription table

### Fields

| Field | Type | Description |
|-------|------|-------------|
| customerID | string | Unique customer identifier |
| gender | string | Male / Female |
| SeniorCitizen | int | 0 = No, 1 = Yes |
| Partner | string | Yes / No |
| Dependents | string | Yes / No |
| tenure | int | Months as a customer |
| PhoneService | string | Yes / No |
| MultipleLines | string | Yes / No / No phone service |
| InternetService | string | DSL / Fiber optic / No |
| OnlineSecurity | string | Yes / No / No internet service |
| OnlineBackup | string | Yes / No / No internet service |
| DeviceProtection | string | Yes / No / No internet service |
| TechSupport | string | Yes / No / No internet service |
| StreamingTV | string | Yes / No / No internet service |
| StreamingMovies | string | Yes / No / No internet service |
| Contract | string | Month-to-month / One year / Two year |
| PaperlessBilling | string | Yes / No |
| PaymentMethod | string | Electronic check / Mailed check / Bank transfer / Credit card |
| MonthlyCharges | float | Monthly subscription amount |
| TotalCharges | float | Total amount charged to date |
| Churn | string | Yes / No |

---

## Synthetic Tables

### interactions

Client interaction records.

| Field | Type | Description |
|-------|------|-------------|
| interaction_id | string | Unique identifier |
| customer_id | string | FK to customer |
| interaction_date | date | Date of interaction |
| interaction_type | string | Analyst Meeting / Webinar / Support / Email / Product Demo / Account Review |
| channel | string | Online / Email / Phone / Video / In-Person |
| duration_minutes | int | Duration of interaction |
| outcome | string | Resolved / Pending / Escalated / No Response |

### content_usage

Content consumption records.

| Field | Type | Description |
|-------|------|-------------|
| usage_id | string | Unique identifier |
| customer_id | string | FK to customer |
| usage_date | date | Date of usage |
| content_category | string | Technology / Strategy / Operations / Finance / Marketing / Industry Research |
| reports_viewed | int | Number of reports viewed |
| downloads | int | Number of downloads |
| time_spent_minutes | int | Time spent on content |

### event_participation

Event registration and attendance.

| Field | Type | Description |
|-------|------|-------------|
| event_participation_id | string | Unique identifier |
| customer_id | string | FK to customer |
| event_id | string | FK to event |
| event_date | date | Date of event |
| event_type | string | Webinar / Conference / Roundtable / Executive Session / Workshop |
| registered | string | Yes / No |
| attended | string | Yes / No |

### account_activity

Daily account activity metrics.

| Field | Type | Description |
|-------|------|-------------|
| activity_id | string | Unique identifier |
| customer_id | string | FK to customer |
| activity_date | date | Date of activity record |
| active_users | int | Number of active users on account |
| login_count | int | Number of logins |
| features_used | int | Number of features used |
| session_count | int | Number of sessions |

---

## Dimension Tables (Star Schema)

### dim_customer

| Field | Type | Description |
|-------|------|-------------|
| customer_id | PK | Unique customer identifier |
| gender | string | Gender |
| age_group | string | Age band |
| senior_citizen | string | Yes / No |
| partner | string | Yes / No |
| dependents | string | Yes / No |
| region | string | Geographic region |
| industry | string | Client industry |
| company_size | string | Company size band |

### dim_subscription

| Field | Type | Description |
|-------|------|-------------|
| subscription_id | PK | Unique subscription identifier |
| customer_id | FK | FK to dim_customer |
| plan_type | string | Basic / Standard / Premium / Enterprise |
| contract_type | string | Month-to-month / One year / Two year |
| start_date | date | Subscription start date |
| renewal_date | date | Next renewal date |
| contract_value | float | Annual contract value |
| status | string | Active / Cancelled / Expired |

### dim_date

| Field | Type | Description |
|-------|------|-------------|
| date | PK | Full date |
| year | int | Year |
| quarter | int | Quarter |
| month | int | Month number |
| month_name | string | Month name |
| week | int | Week number |
| day_of_week | string | Day name |

### dim_content

| Field | Type | Description |
|-------|------|-------------|
| content_id | PK | Unique content identifier |
| content_category | string | Content category |
| content_type | string | Report / Whitepaper / Webinar Recording / Case Study |

### dim_event

| Field | Type | Description |
|-------|------|-------------|
| event_id | PK | Unique event identifier |
| event_type | string | Event type |
| event_topic | string | Event topic/category |

---

## Fact Tables

### fact_interaction

| Field | Type | Description |
|-------|------|-------------|
| interaction_id | PK | Unique identifier |
| customer_id | FK | FK to dim_customer |
| date | FK | FK to dim_date |
| interaction_type | string | Interaction type |
| channel | string | Channel used |
| duration_minutes | int | Duration in minutes |
| outcome | string | Outcome of interaction |

### fact_content_usage

| Field | Type | Description |
|-------|------|-------------|
| usage_id | PK | Unique identifier |
| customer_id | FK | FK to dim_customer |
| date | FK | FK to dim_date |
| content_id | FK | FK to dim_content |
| reports_viewed | int | Reports viewed |
| downloads | int | Downloads |
| time_spent_minutes | int | Time spent |

### fact_event_participation

| Field | Type | Description |
|-------|------|-------------|
| event_participation_id | PK | Unique identifier |
| customer_id | FK | FK to dim_customer |
| event_id | FK | FK to dim_event |
| date | FK | FK to dim_date |
| registered | string | Yes / No |
| attended | string | Yes / No |

### fact_account_activity

| Field | Type | Description |
|-------|------|-------------|
| activity_id | PK | Unique identifier |
| customer_id | FK | FK to dim_customer |
| date | FK | FK to dim_date |
| active_users | int | Active users |
| login_count | int | Login count |
| features_used | int | Features used |
| session_count | int | Session count |

---

## Derived Fields

### engagement_score

Composite metric calculated in `src/build_features.py`.

| Component | Weight | Source |
|-----------|--------|--------|
| Product/Usage Activity | 30% | fact_account_activity, fact_content_usage |
| Client Interactions | 25% | fact_interaction |
| Content Consumption | 20% | fact_content_usage |
| Event Participation | 15% | fact_event_participation |
| Recent Activity | 10% | fact_account_activity (last 30 days) |
