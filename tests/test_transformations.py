"""
test_transformations.py

Unit tests for data transformations and feature engineering.
Run with: pytest tests/test_transformations.py -v
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
        pytest.skip(f"Processed file not found: {path}. Run src/clean_data.py and src/build_features.py first.")
    return pd.read_csv(path)


class TestEngagementScore:
    def test_engagement_score_exists(self):
        df = load_processed("customer_features_vB.csv")
        assert "engagement_score" in df.columns, "engagement_score column missing"

    def test_engagement_score_range(self):
        df = load_processed("customer_features_vB.csv")
        assert df["engagement_score"].min() >= 0, "Engagement score below 0"
        assert df["engagement_score"].max() <= 1, "Engagement score above 1"

    def test_engagement_score_not_all_null(self):
        df = load_processed("customer_features_vB.csv")
        assert df["engagement_score"].notna().sum() > 0, "All engagement scores are null"

    def test_engagement_bands_exist(self):
        df = load_processed("customer_features_vB.csv")
        assert "engagement_band" in df.columns, "engagement_band column missing"
        valid_bands = {"Low", "Medium", "High", "Very High"}
        actual_bands = set(df["engagement_band"].dropna().unique())
        assert actual_bands.issubset(valid_bands), f"Invalid engagement bands: {actual_bands - valid_bands}"


class TestSegmentLabels:
    def test_tenure_bands_exist(self):
        df = load_processed("customer_features_vB.csv")
        assert "tenure_band" in df.columns, "tenure_band column missing"
        valid_bands = {"0-12 months", "13-24 months", "25-48 months", "49+ months"}
        actual_bands = set(df["tenure_band"].dropna().unique())
        assert actual_bands.issubset(valid_bands), f"Invalid tenure bands: {actual_bands - valid_bands}"

    def test_value_segments_exist(self):
        df = load_processed("customer_features_vB.csv")
        assert "value_segment" in df.columns, "value_segment column missing"


class TestFeatureConsistency:
    def test_customer_count_matches(self):
        """Feature table should have same number of customers as source."""
        customer_df = load_processed("processed_customer.csv")
        features_df = load_processed("customer_features_vB.csv")
        assert len(features_df) == len(customer_df), "Feature table row count doesn't match customer table"

    def test_no_duplicate_customers_in_features(self):
        df = load_processed("customer_features_vB.csv")
        assert df["customer_id"].is_unique, "Duplicate customer IDs in feature table"

    def test_engagement_score_correlates_with_logins(self):
        """Engagement score should be positively correlated with login count."""
        df = load_processed("customer_features_vB.csv")
        corr = df["engagement_score"].corr(df["total_logins"])
        assert corr > 0, "Engagement score should correlate positively with logins"


class TestSyntheticDataReproducibility:
    def test_random_seed_documented(self):
        """Verify the random seed is documented in the generator script."""
        generator_path = os.path.join(BASE_DIR, "..", "src", "generate_synthetic_data.py")
        assert os.path.exists(generator_path), "Generator script not found"
        with open(generator_path) as f:
            content = f.read()
        assert "RANDOM_SEED = 42" in content, "Random seed not set to 42 in generator script"

    def test_synthetic_data_has_noise(self):
        """Synthetic data should not have perfect separation between churned and retained."""
        df = load_processed("customer_features_vB.csv")
        renewed_engagement = df[df["churn"] == "No"]["engagement_score"].mean()
        churned_engagement = df[df["churn"] == "Yes"]["engagement_score"].mean()
        gap = abs(renewed_engagement - churned_engagement)
        # Gap should be moderate, not near-perfect (which would indicate engineered data)
        assert gap < 0.5, f"Engagement gap too large ({gap:.3f}), suggests engineered data"
