-- ============================================================================
-- KPI QUERIES: Core business metrics
-- ============================================================================

-- ============================================================================
-- KPI 1: Total Customers
-- ============================================================================
SELECT
    COUNT(*) AS total_customers,
    COUNT(CASE WHEN churn = 'No' THEN 1 END) AS renewed,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned,
    ROUND(COUNT(CASE WHEN churn = 'No' THEN 1 END) * 100.0 / COUNT(*), 2) AS renewal_rate,
    ROUND(COUNT(CASE WHEN churn = 'Yes' THEN 1 END) * 100.0 / COUNT(*), 2) AS churn_rate
FROM stg_customer;

-- ============================================================================
-- KPI 2: Revenue Metrics
-- ============================================================================
SELECT
    COUNT(*) AS total_customers,
    ROUND(SUM(monthly_charges), 2) AS total_monthly_revenue,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_revenue_per_customer,
    ROUND(SUM(total_charges), 2) AS total_contract_value,
    ROUND(AVG(total_charges), 2) AS avg_contract_value,
    ROUND(SUM(CASE WHEN churn = 'No' THEN monthly_charges ELSE 0 END), 2) AS retained_revenue,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN monthly_charges ELSE 0 END), 2) AS lost_revenue
FROM stg_customer;

-- ============================================================================
-- KPI 3: Customers by Plan Type
-- ============================================================================
SELECT
    contract AS plan_type,
    COUNT(*) AS customer_count,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    ROUND(AVG(total_charges), 2) AS avg_total_charges,
    COUNT(CASE WHEN churn = 'No' THEN 1 END) AS renewed,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned,
    ROUND(COUNT(CASE WHEN churn = 'No' THEN 1 END) * 100.0 / COUNT(*), 2) AS renewal_rate
FROM stg_customer
GROUP BY contract
ORDER BY renewal_rate DESC;

-- ============================================================================
-- KPI 4: Customers by Region (requires dim_customer)
-- ============================================================================
SELECT
    dc.region,
    COUNT(DISTINCT dc.customer_id) AS customer_count,
    ROUND(AVG(sc.monthly_charges), 2) AS avg_monthly_charges,
    COUNT(CASE WHEN sc.churn = 'No' THEN 1 END) AS renewed,
    COUNT(CASE WHEN sc.churn = 'Yes' THEN 1 END) AS churned,
    ROUND(COUNT(CASE WHEN sc.churn = 'No' THEN 1 END) * 100.0 / COUNT(*), 2) AS renewal_rate
FROM dim_customer dc
JOIN stg_customer sc ON dc.customer_id = sc.customer_id
GROUP BY dc.region
ORDER BY renewal_rate DESC;

-- ============================================================================
-- KPI 5: Average Engagement by Renewal Status (requires fact tables)
-- ============================================================================
SELECT
    sc.churn AS renewal_status,
    COUNT(DISTINCT sc.customer_id) AS customer_count,
    ROUND(AVG(faa.login_count), 2) AS avg_logins,
    ROUND(AVG(faa.session_count), 2) AS avg_sessions,
    ROUND(AVG(faa.features_used), 2) AS avg_features_used,
    ROUND(AVG(faa.active_users), 2) AS avg_active_users,
    ROUND(AVG(fcu.time_spent_minutes), 2) AS avg_time_spent,
    COUNT(DISTINCT fi.interaction_id) AS total_interactions,
    COUNT(DISTINCT fep.event_participation_id) AS total_events
FROM stg_customer sc
LEFT JOIN fact_account_activity faa ON sc.customer_id = faa.customer_id
LEFT JOIN fact_content_usage fcu ON sc.customer_id = fcu.customer_id
LEFT JOIN fact_interaction fi ON sc.customer_id = fi.customer_id
LEFT JOIN fact_event_participation fep ON sc.customer_id = fep.customer_id
GROUP BY sc.churn;

-- ============================================================================
-- KPI 6: Monthly Trend (requires dim_date)
-- ============================================================================
SELECT
    dd.year,
    dd.month,
    dd.month_name,
    COUNT(DISTINCT faa.customer_id) AS active_customers,
    ROUND(AVG(faa.login_count), 2) AS avg_logins,
    ROUND(AVG(faa.session_count), 2) AS avg_sessions
FROM fact_account_activity faa
JOIN dim_date dd ON faa.date = dd.date
GROUP BY dd.year, dd.month, dd.month_name
ORDER BY dd.year, dd.month;
