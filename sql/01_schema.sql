-- ============================================================================
-- CLIENT ENGAGEMENT & RETENTION ANALYTICS
-- Database Schema (Star Schema Design)
-- ============================================================================

-- ============================================================================
-- DIMENSION TABLES
-- ============================================================================

CREATE TABLE dim_customer (
    customer_id TEXT PRIMARY KEY,
    gender TEXT,
    age_group TEXT,
    senior_citizen TEXT,
    partner TEXT,
    dependents TEXT,
    region TEXT,
    industry TEXT,
    company_size TEXT
);

CREATE TABLE dim_subscription (
    subscription_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    plan_type TEXT,
    contract_type TEXT,
    start_date TEXT,
    renewal_date TEXT,
    contract_value REAL,
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id)
);

CREATE TABLE dim_date (
    date TEXT PRIMARY KEY,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name TEXT,
    week INTEGER,
    day_of_week TEXT
);

CREATE TABLE dim_content (
    content_id TEXT PRIMARY KEY,
    content_category TEXT,
    content_type TEXT
);

CREATE TABLE dim_event (
    event_id TEXT PRIMARY KEY,
    event_type TEXT,
    event_topic TEXT
);

-- ============================================================================
-- FACT TABLES
-- ============================================================================

CREATE TABLE fact_interaction (
    interaction_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    date TEXT NOT NULL,
    interaction_type TEXT,
    channel TEXT,
    duration_minutes INTEGER,
    outcome TEXT,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (date) REFERENCES dim_date(date)
);

CREATE TABLE fact_content_usage (
    usage_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    date TEXT NOT NULL,
    content_id TEXT,
    reports_viewed INTEGER,
    downloads INTEGER,
    time_spent_minutes INTEGER,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (date) REFERENCES dim_date(date),
    FOREIGN KEY (content_id) REFERENCES dim_content(content_id)
);

CREATE TABLE fact_event_participation (
    event_participation_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    event_id TEXT,
    date TEXT NOT NULL,
    registered TEXT,
    attended TEXT,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (event_id) REFERENCES dim_event(event_id),
    FOREIGN KEY (date) REFERENCES dim_date(date)
);

CREATE TABLE fact_account_activity (
    activity_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    date TEXT NOT NULL,
    active_users INTEGER,
    login_count INTEGER,
    features_used INTEGER,
    session_count INTEGER,
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (date) REFERENCES dim_date(date)
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

CREATE INDEX idx_subscription_customer ON dim_subscription(customer_id);
CREATE INDEX idx_interaction_customer ON fact_interaction(customer_id);
CREATE INDEX idx_interaction_date ON fact_interaction(date);
CREATE INDEX idx_content_customer ON fact_content_usage(customer_id);
CREATE INDEX idx_content_date ON fact_content_usage(date);
CREATE INDEX idx_event_customer ON fact_event_participation(customer_id);
CREATE INDEX idx_event_date ON fact_event_participation(date);
CREATE INDEX idx_activity_customer ON fact_account_activity(customer_id);
CREATE INDEX idx_activity_date ON fact_account_activity(date);
