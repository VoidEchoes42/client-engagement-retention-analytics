-- ============================================================================
-- ADVANCED ANALYSIS: CTEs, Window Functions, Cohort Logic
-- ============================================================================

-- ============================================================================
-- 1. Client Activity in 90 Days Before Renewal
-- ============================================================================
WITH renewal_window AS (
    SELECT
        sc.customer_id,
        sc.churn,
        sc.tenure,
        DATE(sc.tenure * 30, '-90 days') AS window_start,
        DATE(sc.tenure * 30) AS window_end,
        COUNT(DISTINCT faa.activity_id) AS activity_days,
        SUM(faa.login_count) AS total_logins,
        SUM(faa.session_count) AS total_sessions,
        SUM(faa.features_used) AS total_features,
        SUM(fcu.time_spent_minutes) AS total_time_spent,
        COUNT(DISTINCT fi.interaction_id) AS interaction_count,
        COUNT(DISTINCT fep.event_participation_id) AS event_count
    FROM stg_customer sc
    LEFT JOIN fact_account_activity faa
        ON sc.customer_id = faa.customer_id
        AND faa.date BETWEEN DATE(sc.tenure * 30, '-90 days') AND DATE(sc.tenure * 30)
    LEFT JOIN fact_content_usage fcu
        ON sc.customer_id = fcu.customer_id
        AND fcu.date BETWEEN DATE(sc.tenure * 30, '-90 days') AND DATE(sc.tenure * 30)
    LEFT JOIN fact_interaction fi
        ON sc.customer_id = fi.customer_id
        AND fi.date BETWEEN DATE(sc.tenure * 30, '-90 days') AND DATE(sc.tenure * 30)
    LEFT JOIN fact_event_participation fep
        ON sc.customer_id = fep.customer_id
        AND fep.date BETWEEN DATE(sc.tenure * 30, '-90 days') AND DATE(sc.tenure * 30)
    GROUP BY sc.customer_id, sc.churn, sc.tenure
)
SELECT
    churn AS renewal_status,
    COUNT(*) AS customer_count,
    ROUND(AVG(activity_days), 2) AS avg_active_days,
    ROUND(AVG(total_logins), 2) AS avg_logins,
    ROUND(AVG(total_sessions), 2) AS avg_sessions,
    ROUND(AVG(total_features), 2) AS avg_features,
    ROUND(AVG(total_time_spent), 2) AS avg_time_spent,
    ROUND(AVG(interaction_count), 2) AS avg_interactions,
    ROUND(AVG(event_count), 2) AS avg_events
FROM renewal_window
GROUP BY churn;

-- ============================================================================
-- 2. Clients with Declining Recent Activity (using LAG)
-- ============================================================================
WITH monthly_activity AS (
    SELECT
        customer_id,
        dd.year,
        dd.month,
        SUM(login_count) AS monthly_logins,
        SUM(session_count) AS monthly_sessions
    FROM fact_account_activity faa
    JOIN dim_date dd ON faa.date = dd.date
    GROUP BY customer_id, dd.year, dd.month
),
activity_trend AS (
    SELECT
        customer_id,
        year,
        month,
        monthly_logins,
        LAG(monthly_logins) OVER (PARTITION BY customer_id ORDER BY year, month) AS prev_logins,
        monthly_logins - LAG(monthly_logins) OVER (PARTITION BY customer_id ORDER BY year, month) AS login_change
    FROM monthly_activity
)
SELECT
    customer_id,
    year,
    month,
    monthly_logins,
    prev_logins,
    login_change,
    CASE
        WHEN login_change < -5 THEN 'Significant Decline'
        WHEN login_change < 0 THEN 'Slight Decline'
        WHEN login_change = 0 THEN 'Stable'
        WHEN login_change <= 5 THEN 'Slight Increase'
        ELSE 'Significant Increase'
    END AS activity_trend
FROM activity_trend
WHERE prev_logins IS NOT NULL
ORDER BY customer_id, year, month;

-- ============================================================================
-- 3. Engagement Ranking by Segment
-- ============================================================================
WITH engagement_scores AS (
    SELECT
        sc.customer_id,
        dc.region,
        dc.industry,
        ds.plan_type,
        sc.churn,
        sc.tenure,
        COUNT(DISTINCT fi.interaction_id) AS interaction_count,
        SUM(fcu.time_spent_minutes) AS total_content_time,
        COUNT(DISTINCT fep.event_participation_id) AS events_attended,
        AVG(faa.login_count) AS avg_logins,
        AVG(faa.features_used) AS avg_features,
        RANK() OVER (PARTITION BY dc.region ORDER BY
            COUNT(DISTINCT fi.interaction_id) + SUM(fcu.time_spent_minutes) + COUNT(DISTINCT fep.event_participation_id) DESC
        ) AS engagement_rank_in_region,
        RANK() OVER (PARTITION BY ds.plan_type ORDER BY
            COUNT(DISTINCT fi.interaction_id) + SUM(fcu.time_spent_minutes) + COUNT(DISTINCT fep.event_participation_id) DESC
        ) AS engagement_rank_in_plan
    FROM stg_customer sc
    LEFT JOIN dim_customer dc ON sc.customer_id = dc.customer_id
    LEFT JOIN dim_subscription ds ON sc.customer_id = ds.customer_id
    LEFT JOIN fact_interaction fi ON sc.customer_id = fi.customer_id
    LEFT JOIN fact_content_usage fcu ON sc.customer_id = fcu.customer_id
    LEFT JOIN fact_event_participation fep ON sc.customer_id = fep.customer_id
    LEFT JOIN fact_account_activity faa ON sc.customer_id = faa.customer_id
    GROUP BY sc.customer_id, dc.region, dc.industry, ds.plan_type, sc.churn, sc.tenure
)
SELECT
    customer_id,
    region,
    industry,
    plan_type,
    churn,
    tenure,
    interaction_count,
    total_content_time,
    events_attended,
    avg_logins,
    avg_features,
    engagement_rank_in_region,
    engagement_rank_in_plan,
    CASE
        WHEN engagement_rank_in_region <= 10 THEN 'Top 10 in Region'
        WHEN engagement_rank_in_region <= 50 THEN 'Top 50 in Region'
        ELSE 'Lower Engagement'
    END AS engagement_tier
FROM engagement_scores
ORDER BY engagement_rank_in_region;

-- ============================================================================
-- 4. Cohort Analysis by Contract Start Month
-- ============================================================================
WITH cohorts AS (
    SELECT
        sc.customer_id,
        sc.churn,
        ds.start_date,
        ds.contract_type,
        STRFTIME('%Y-%m', ds.start_date) AS cohort_month
    FROM stg_customer sc
    JOIN dim_subscription ds ON sc.customer_id = ds.customer_id
),
cohort_retention AS (
    SELECT
        cohort_month,
        contract_type,
        COUNT(*) AS cohort_size,
        COUNT(CASE WHEN churn = 'No' THEN 1 END) AS retained,
        ROUND(COUNT(CASE WHEN churn = 'No' THEN 1 END) * 100.0 / COUNT(*), 2) AS retention_rate
    FROM cohorts
    GROUP BY cohort_month, contract_type
)
SELECT
    cohort_month,
    contract_type,
    cohort_size,
    retained,
    retention_rate
FROM cohort_retention
ORDER BY cohort_month, contract_type;

-- ============================================================================
-- 5. At-Risk Client Identification (Investigation List)
-- ============================================================================
WITH risk_assessment AS (
    SELECT
        sc.customer_id,
        sc.churn,
        ds.contract_value,
        ds.renewal_date,
        COUNT(DISTINCT fi.interaction_id) AS interaction_count,
        AVG(faa.login_count) AS avg_logins,
        SUM(fcu.time_spent_minutes) AS total_time_spent,
        CASE
            WHEN COUNT(DISTINCT fi.interaction_id) < 3 THEN 'Low'
            WHEN COUNT(DISTINCT fi.interaction_id) < 6 THEN 'Medium'
            ELSE 'High'
        END AS interaction_level,
        CASE
            WHEN AVG(faa.login_count) < 5 THEN 'Low'
            WHEN AVG(faa.login_count) < 10 THEN 'Medium'
            ELSE 'High'
        END AS activity_level
    FROM stg_customer sc
    LEFT JOIN dim_subscription ds ON sc.customer_id = ds.customer_id
    LEFT JOIN fact_interaction fi ON sc.customer_id = fi.customer_id
    LEFT JOIN fact_account_activity faa ON sc.customer_id = faa.customer_id
    LEFT JOIN fact_content_usage fcu ON sc.customer_id = fcu.customer_id
    GROUP BY sc.customer_id, sc.churn, ds.contract_value, ds.renewal_date
)
SELECT
    customer_id,
    contract_value,
    renewal_date,
    interaction_count,
    avg_logins,
    total_time_spent,
    interaction_level,
    activity_level,
    CASE
        WHEN interaction_level = 'Low' AND activity_level = 'Low' THEN 'High Risk'
        WHEN interaction_level = 'Medium' OR activity_level = 'Medium' THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS risk_category
FROM risk_assessment
WHERE interaction_level = 'Low' OR activity_level = 'Low'
ORDER BY contract_value DESC;
