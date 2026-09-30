"""
test_data_quality.py

Unit tests for data quality validation.
Run with: pytest tests/test_data_quality.py -v
"""

import pandas as pd
import numpy as np
import os
import pytest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")


def load_processed(filename: str) -> pd.DataFrame:
    path = os.path.join(PROCESSED_DIR, filename)
    if not os.path.exists(path):
        pytest.skip(f"Processed file not found: {path}. Run src/clean_data.py first.")
    return pd.read_csv(path)


class TestCustomerData:
    def test_customer_data_exists(self):
        df = load_processed("processed_customer.csv")
        assert len(df) > 0, "Customer data is empty"

    def test_customer_id_unique(self):
        df = load_processed("processed_customer.csv")
        assert df["customer_id"].is_unique, "Duplicate customer IDs found"

    def test_no_negative_tenure(self):
        df = load_processed("processed_customer.csv")
        assert (df["tenure"] >= 0).all(), "Negative tenure values found"

    def test_no_negative_charges(self):
        df = load_processed("processed_customer.csv")
        assert (df["monthly_charges"] >= 0).all(), "Negative monthly charges found"
        assert (df["total_charges"] >= 0).all(), "Negative total charges found"

    def test_churn_values_valid(self):
        df = load_processed("processed_customer.csv")
        valid_values = {"Yes", "No"}
        assert set(df["churn"].unique()).issubset(valid_values), "Invalid churn values"

    def test_total_charges_not_null(self):
        df = load_processed("processed_customer.csv")
        null_count = df["total_charges"].isnull().sum()
        assert null_count == 0, f"{null_count} null values in total_charges"


class TestInteractionData:
    def test_interaction_data_exists(self):
        df = load_processed("processed_interactions.csv")
        assert len(df) > 0, "Interaction data is empty"

    def test_interaction_id_unique(self):
        df = load_processed("processed_interactions.csv")
        assert df["interaction_id"].is_unique, "Duplicate interaction IDs found"

    def test_no_negative_duration(self):
        df = load_processed("processed_interactions.csv")
        assert (df["duration_minutes"] >= 0).all(), "Negative duration found"

    def test_interaction_types_capitalized(self):
        df = load_processed("processed_interactions.csv")
        types = df["interaction_type"].dropna().unique()
        for t in types:
            assert t == t.title(), f"Interaction type not title-cased: {t}"


class TestContentUsageData:
    def test_content_usage_exists(self):
        df = load_processed("processed_content_usage.csv")
        assert len(df) > 0, "Content usage data is empty"

    def test_usage_id_unique(self):
        df = load_processed("processed_content_usage.csv")
        assert df["usage_id"].is_unique, "Duplicate usage IDs found"

    def test_no_negative_values(self):
        df = load_processed("processed_content_usage.csv")
        for col in ["reports_viewed", "downloads", "time_spent_minutes"]:
            assert (df[col] >= 0).all(), f"Negative values in {col}"


class TestEventParticipationData:
    def test_participation_exists(self):
        df = load_processed("processed_event_participation.csv")
        assert len(df) > 0, "Event participation data is empty"

    def test_participation_id_unique(self):
        df = load_processed("processed_event_participation.csv")
        assert df["event_participation_id"].is_unique, "Duplicate participation IDs"


class TestAccountActivityData:
    def test_activity_exists(self):
        df = load_processed("processed_account_activity.csv")
        assert len(df) > 0, "Account activity data is empty"

    def test_activity_id_unique(self):
        df = load_processed("processed_account_activity.csv")
        assert df["activity_id"].is_unique, "Duplicate activity IDs found"

    def test_no_negative_counts(self):
        df = load_processed("processed_account_activity.csv")
        for col in ["active_users", "login_count", "features_used", "session_count"]:
            assert (df[col] >= 0).all(), f"Negative values in {col}"


class TestReferentialIntegrity:
    def test_fact_customer_ids_exist(self):
        try:
            customers = set(load_processed("processed_customer.csv")["customer_id"].astype(str))
        except FileNotFoundError:
            pytest.skip("Customer data not found")

        fact_tables = {
            "processed_interactions.csv": "customer_id",
            "processed_content_usage.csv": "customer_id",
            "processed_event_participation.csv": "customer_id",
            "processed_account_activity.csv": "customer_id",
        }

        for filename, id_col in fact_tables.items():
            try:
                df = load_processed(filename)
                orphan_ids = set(df[id_col].astype(str)) - customers
                assert len(orphan_ids) == 0, f"{len(orphan_ids)} orphan customer IDs in {filename}"
            except FileNotFoundError:
                pytest.skip(f"{filename} not found")
