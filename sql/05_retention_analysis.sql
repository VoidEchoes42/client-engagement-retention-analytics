-- ============================================================================
-- RETENTION ANALYSIS: Renewal patterns by segment
-- ============================================================================

-- ============================================================================
-- 1. Renewal Rate by Tenure Band
-- ============================================================================
SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 24 THEN '13-24 months'
        WHEN tenure <= 48 THEN '25-48 months'
        ELSE '49+ months'
    END AS tenure_band,
    COUNT(*) AS customer_count,
    COUNT(CASE WHEN churn = 'No' THEN 1 END) AS renewed,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned,
    ROUND(COUNT(CASE WHEN churn = 'No' THEN 1 END) * 100.0 / COUNT(*), 2) AS renewal_rate
FROM stg_customer
GROUP BY tenure_band
ORDER BY renewal_rate DESC;

-- ============================================================================
-- 2. Renewal Rate by Contract Type
-- ============================================================================
SELECT
    contract AS contract_type,
    COUNT(*) AS customer_count,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    ROUND(AVG(total_charges), 2) AS avg_total_charges,
    ROUND(COUNT(CASE WHEN churn = 'No' THEN 1 END) * 100.0 / COUNT(*), 2) AS renewal_rate
FROM stg_customer
GROUP BY contract
ORDER BY renewal_rate DESC;

-- ============================================================================
-- 3. Renewal Rate by Internet Service Type
-- ============================================================================
SELECT
    internet_service,
    COUNT(*) AS customer_count,
    ROUND(COUNT(CASE WHEN churn = 'No' THEN 1 END) * 100.0 / COUNT(*), 2) AS renewal_rate,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
FROM stg_customer
GROUP BY internet_service
ORDER BY renewal_rate DESC;

-- ============================================================================
-- 4. Engagement Comparison: Renewed vs Non-Renewed
-- ============================================================================
WITH engagement_summary AS (
    SELECT
        sc.customer_id,
        sc.churn,
        COUNT(DISTINCT fi.interaction_id) AS interaction_count,
        AVG(fi.duration_minutes) AS avg_interaction_duration,
        COUNT(DISTINCT fcu.usage_id) AS content_views,
        SUM(fcu.time_spent_minutes) AS total_time_spent,
        SUM(fcu.reports_viewed) AS total_reports,
        COUNT(DISTINCT fep.event_participation_id) AS events_participated,
        AVG(faa.login_count) AS avg_logins,
        AVG(faa.session_count) AS avg_sessions,
        AVG(faa.features_used) AS avg_features_used
    FROM stg_customer sc
    LEFT JOIN fact_interaction fi ON sc.customer_id = fi.customer_id
    LEFT JOIN fact_content_usage fcu ON sc.customer_id = fcu.customer_id
    LEFT JOIN fact_event_participation fep ON sc.customer_id = fep.customer_id
    LEFT JOIN fact_account_activity faa ON sc.customer_id = faa.customer_id
    GROUP BY sc.customer_id, sc.churn
)
SELECT
    churn AS renewal_status,
    COUNT(*) AS customer_count,
    ROUND(AVG(interaction_count), 2) AS avg_interactions,
    ROUND(AVG(avg_interaction_duration), 2) AS avg_duration,
    ROUND(AVG(content_views), 2) AS avg_content_views,
    ROUND(AVG(total_time_spent), 2) AS avg_time_spent,
    ROUND(AVG(total_reports), 2) AS avg_reports,
    ROUND(AVG(events_participated), 2) AS avg_events,
    ROUND(AVG(avg_logins), 2) AS avg_logins,
    ROUND(AVG(avg_sessions), 2) AS avg_sessions,
    ROUND(AVG(avg_features_used), 2) AS avg_features
FROM engagement_summary
GROUP BY churn;

-- ============================================================================
-- 5. High-Value Client Retention
-- ============================================================================
SELECT
    CASE
        WHEN monthly_charges >= 100 THEN 'High Value'
        WHEN monthly_charges >= 60 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS value_segment,
    COUNT(*) AS customer_count,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    ROUND(SUM(monthly_charges), 2) AS total_monthly_revenue,
    COUNT(CASE WHEN churn = 'No' THEN 1 END) AS renewed,
    COUNT(CASE WHEN churn = 'Yes' THEN 1 END) AS churned,
    ROUND(COUNT(CASE WHEN churn = 'No' THEN 1 END) * 100.0 / COUNT(*), 2) AS renewal_rate
FROM stg_customer
GROUP BY value_segment
ORDER BY renewal_rate DESC;

-- ============================================================================
-- 6. Repeat Event Attendance
-- ============================================================================
SELECT
    sc.customer_id,
    sc.churn,
    COUNT(DISTINCT fep.event_participation_id) AS total_events,
    SUM(CASE WHEN fep.attended = 'Yes' THEN 1 ELSE 0 END) AS events_attended,
    ROUND(SUM(CASE WHEN fep.attended = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT fep.event_participation_id), 2) AS attendance_rate
FROM stg_customer sc
LEFT JOIN fact_event_participation fep ON sc.customer_id = fep.customer_id
GROUP BY sc.customer_id, sc.churn;
