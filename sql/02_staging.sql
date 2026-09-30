-- ============================================================================
-- STAGING: Load raw data into staging tables
-- ============================================================================

-- Staging customer table (from public IBM Telco dataset)
CREATE TABLE stg_customer (
    customer_id TEXT,
    gender TEXT,
    senior_citizen TEXT,
    partner TEXT,
    dependents TEXT,
    tenure REAL,
    phone_service TEXT,
    multiple_lines TEXT,
    internet_service TEXT,
    online_security TEXT,
    online_backup TEXT,
    device_protection TEXT,
    tech_support TEXT,
    streaming_tv TEXT,
    streaming_movies TEXT,
    contract TEXT,
    paperless_billing TEXT,
    payment_method TEXT,
    monthly_charges REAL,
    total_charges REAL,
    churn TEXT
);

-- Staging synthetic tables
CREATE TABLE stg_interactions (
    interaction_id TEXT,
    customer_id TEXT,
    interaction_date TEXT,
    interaction_type TEXT,
    channel TEXT,
    duration_minutes REAL,
    outcome TEXT
);

CREATE TABLE stg_content_usage (
    usage_id TEXT,
    customer_id TEXT,
    usage_date TEXT,
    content_category TEXT,
    reports_viewed REAL,
    downloads REAL,
    time_spent_minutes REAL
);

CREATE TABLE stg_event_participation (
    event_participation_id TEXT,
    customer_id TEXT,
    event_id TEXT,
    event_date TEXT,
    event_type TEXT,
    registered TEXT,
    attended TEXT
);

CREATE TABLE stg_account_activity (
    activity_id TEXT,
    customer_id TEXT,
    activity_date TEXT,
    active_users REAL,
    login_count REAL,
    features_used REAL,
    session_count REAL
);

CREATE TABLE stg_events (
    event_id TEXT,
    event_type TEXT,
    event_topic TEXT
);
