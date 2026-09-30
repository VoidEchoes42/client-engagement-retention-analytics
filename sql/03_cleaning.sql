-- ============================================================================
-- DATA CLEANING: Standardize and validate staging data
-- ============================================================================

-- ============================================================================
-- 1. Standardize customer data
-- ============================================================================

-- Fix gender casing
UPDATE stg_customer
SET gender = CASE
    WHEN LOWER(gender) = 'male' THEN 'Male'
    WHEN LOWER(gender) = 'female' THEN 'Female'
    ELSE gender
END;

-- Standardize yes/no fields
UPDATE stg_customer
SET partner = CASE WHEN LOWER(partner) = 'yes' THEN 'Yes' WHEN LOWER(partner) = 'no' THEN 'No' ELSE partner END,
    dependents = CASE WHEN LOWER(dependents) = 'yes' THEN 'Yes' WHEN LOWER(dependents) = 'no' THEN 'No' ELSE dependents END,
    phone_service = CASE WHEN LOWER(phone_service) = 'yes' THEN 'Yes' WHEN LOWER(phone_service) = 'no' THEN 'No' ELSE phone_service END,
    paperless_billing = CASE WHEN LOWER(paperless_billing) = 'yes' THEN 'Yes' WHEN LOWER(paperless_billing) = 'no' THEN 'No' ELSE paperless_billing END,
    churn = CASE WHEN LOWER(churn) = 'yes' THEN 'Yes' WHEN LOWER(churn) = 'no' THEN 'No' ELSE churn END;

-- Fix total_charges (some blank strings in original data)
UPDATE stg_customer
SET total_charges = NULL
WHERE TRIM(total_charges) = '';

-- Convert total_charges to numeric
UPDATE stg_customer
SET total_charges = CAST(total_charges AS REAL)
WHERE total_charges IS NOT NULL;

-- ============================================================================
-- 2. Clean interaction types and channels
-- ============================================================================

UPDATE stg_interactions
SET interaction_type = INITCAP(TRIM(interaction_type)),
    channel = INITCAP(TRIM(channel)),
    outcome = INITCAP(TRIM(outcome));

-- ============================================================================
-- 3. Clean content categories
-- ============================================================================

UPDATE stg_content_usage
SET content_category = INITCAP(TRIM(content_category));

-- ============================================================================
-- 4. Clean event types
-- ============================================================================

UPDATE stg_event_participation
SET event_type = INITCAP(TRIM(event_type)),
    registered = CASE WHEN LOWER(registered) = 'yes' THEN 'Yes' WHEN LOWER(registered) = 'no' THEN 'No' ELSE registered END,
    attended = CASE WHEN LOWER(attended) = 'yes' THEN 'Yes' WHEN LOWER(attended) = 'no' THEN 'No' ELSE attended END;

UPDATE stg_events
SET event_type = INITCAP(TRIM(event_type)),
    event_topic = INITCAP(TRIM(event_topic));

-- ============================================================================
-- 5. Remove duplicates
-- ============================================================================

-- Duplicate customer IDs
DELETE FROM stg_customer
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM stg_customer
    GROUP BY customer_id
);

-- Duplicate interaction IDs
DELETE FROM stg_interactions
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM stg_interactions
    GROUP BY interaction_id
);

-- ============================================================================
-- 6. Validate ranges
-- ============================================================================

-- Remove records with invalid values
DELETE FROM stg_interactions
WHERE duration_minutes < 0 OR duration_minutes > 480;

DELETE FROM stg_content_usage
WHERE reports_viewed < 0 OR downloads < 0 OR time_spent_minutes < 0;

DELETE FROM stg_account_activity
WHERE active_users < 0 OR login_count < 0 OR features_used < 0 OR session_count < 0;

-- ============================================================================
-- 7. Log cleaning results
-- ============================================================================

SELECT 'stg_customer' AS table_name, COUNT(*) AS row_count FROM stg_customer
UNION ALL
SELECT 'stg_interactions', COUNT(*) FROM stg_interactions
UNION ALL
SELECT 'stg_content_usage', COUNT(*) FROM stg_content_usage
UNION ALL
SELECT 'stg_event_participation', COUNT(*) FROM stg_event_participation
UNION ALL
SELECT 'stg_account_activity', COUNT(*) FROM stg_account_activity;
