"""
build_features.py

Builds derived features for analysis:
  - Engagement score (3 versions)
  - Activity trends
  - Segment labels
  - Engagement bands
"""

import pandas as pd
import numpy as np
import os

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "..", "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)


def load_processed(filename: str) -> pd.DataFrame:
    """Load a processed CSV file."""
    path = os.path.join(PROCESSED_DIR, filename)
    return pd.read_csv(path)


def aggregate_customer_metrics() -> pd.DataFrame:
    """
    Aggregate all fact table metrics to the customer level.
    Returns a single customer-level dataframe for analysis.
    """
    print("Aggregating customer metrics...")

    customer_df = load_processed("processed_customer.csv")
    interactions_df = load_processed("processed_interactions.csv")
    content_df = load_processed("processed_content_usage.csv")
    participation_df = load_processed("processed_event_participation.csv")
    activity_df = load_processed("processed_account_activity.csv")

    # Aggregate interactions
    interaction_agg = interactions_df.groupby("customer_id").agg(
        total_interactions=("interaction_id", "count"),
        avg_duration=("duration_minutes", "mean"),
        total_duration=("duration_minutes", "sum"),
    ).reset_index()

    # Aggregate content usage
    content_agg = content_df.groupby("customer_id").agg(
        total_content_views=("usage_id", "count"),
        total_time_spent=("time_spent_minutes", "sum"),
        total_reports=("reports_viewed", "sum"),
        total_downloads=("downloads", "sum"),
    ).reset_index()

    # Aggregate event participation
    participation_agg = participation_df.groupby("customer_id").agg(
        total_events=("event_participation_id", "count"),
        events_attended=("attended", lambda x: (x == "Yes").sum()),
        attendance_rate=("attended", lambda x: (x == "Yes").mean()),
    ).reset_index()

    # Aggregate account activity
    activity_agg = activity_df.groupby("customer_id").agg(
        total_active_days=("activity_id", "count"),
        total_logins=("login_count", "sum"),
        total_sessions=("session_count", "sum"),
        total_features=("features_used", "sum"),
        avg_active_users=("active_users", "mean"),
        avg_logins_per_day=("login_count", "mean"),
        avg_sessions_per_day=("session_count", "mean"),
    ).reset_index()

    # Merge all
    customer_metrics = customer_df.merge(interaction_agg, on="customer_id", how="left")
    customer_metrics = customer_metrics.merge(content_agg, on="customer_id", how="left")
    customer_metrics = customer_metrics.merge(participation_agg, on="customer_id", how="left")
    customer_metrics = customer_metrics.merge(activity_agg, on="customer_id", how="left")

    # Fill NaN with 0 for customers with no activity
    metric_cols = [
        "total_interactions", "avg_duration", "total_duration",
        "total_content_views", "total_time_spent", "total_reports", "total_downloads",
        "total_events", "events_attended", "attendance_rate",
        "total_active_days", "total_logins", "total_sessions", "total_features",
        "avg_active_users", "avg_logins_per_day", "avg_sessions_per_day",
    ]
    for col in metric_cols:
        if col in customer_metrics.columns:
            customer_metrics[col] = customer_metrics[col].fillna(0)

    return customer_metrics


def calculate_engagement_score(df: pd.DataFrame, version: str = "B") -> pd.DataFrame:
    """
    Calculate engagement score using different weighting schemes.

    Version A: Equal weighting (20% each component)
    Version B: Business-rule weighting (30/25/20/15/10)
    Version C: Standardized components (z-score then weighted)

    Components:
      - Activity (40% of total weight in raw metrics)
      - Interactions (25%)
      - Content (20%)
      - Events (10%)
      - Recent Activity (5%)
    """
    print(f"Calculating engagement score (Version {version})...")
    df = df.copy()

    # Raw component scores (normalized 0-1 using min-max)
    def min_max_normalize(series):
        min_val = series.min()
        max_val = series.max()
        if max_val == min_val:
            return pd.Series(0.5, index=series.index)
        return (series - min_val) / (max_val - min_val)

    # Activity component (based on account activity)
    df["activity_score"] = min_max_normalize(
        df["total_active_days"].fillna(0) * 0.3
        + df["total_logins"].fillna(0) * 0.3
        + df["total_sessions"].fillna(0) * 0.2
        + df["total_features"].fillna(0) * 0.2
    )

    # Interaction component
    df["interaction_score"] = min_max_normalize(
        df["total_interactions"].fillna(0) * 0.6
        + df["avg_duration"].fillna(0) * 0.4
    )

    # Content component
    df["content_score"] = min_max_normalize(
        df["total_time_spent"].fillna(0) * 0.5
        + df["total_reports"].fillna(0) * 0.3
        + df["total_downloads"].fillna(0) * 0.2
    )

    # Event component
    df["event_score"] = min_max_normalize(
        df["events_attended"].fillna(0) * 0.7
        + df["attendance_rate"].fillna(0) * 0.3
    )

    # Recent activity (approximated by average daily activity)
    df["recent_activity_score"] = min_max_normalize(
        df["avg_logins_per_day"].fillna(0) * 0.5
        + df["avg_sessions_per_day"].fillna(0) * 0.5
    )

    if version == "A":
        # Equal weighting
        df["engagement_score"] = (
            df["activity_score"] * 0.20
            + df["interaction_score"] * 0.20
            + df["content_score"] * 0.20
            + df["event_score"] * 0.20
            + df["recent_activity_score"] * 0.20
        )
    elif version == "B":
        # Business-rule weighting
        df["engagement_score"] = (
            df["activity_score"] * 0.30
            + df["interaction_score"] * 0.25
            + df["content_score"] * 0.20
            + df["event_score"] * 0.15
            + df["recent_activity_score"] * 0.10
        )
    elif version == "C":
        # Standardized components
        for col in ["activity_score", "interaction_score", "content_score", "event_score", "recent_activity_score"]:
            df[col + "_z"] = (df[col] - df[col].mean()) / df[col].std()

        df["engagement_score"] = (
            df["activity_score_z"] * 0.30
            + df["interaction_score_z"] * 0.25
            + df["content_score_z"] * 0.20
            + df["event_score_z"] * 0.15
            + df["recent_activity_score_z"] * 0.10
        )
        # Normalize to 0-1
        min_val = df["engagement_score"].min()
        max_val = df["engagement_score"].max()
        df["engagement_score"] = (df["engagement_score"] - min_val) / (max_val - min_val)
    else:
        raise ValueError(f"Unknown version: {version}")

    # Clean up intermediate z-score columns for version C
    if version == "C":
        z_cols = [c for c in df.columns if c.endswith("_z")]
        df = df.drop(columns=z_cols)

    # Assign engagement bands
    df["engagement_band"] = pd.cut(
        df["engagement_score"],
        bins=[0, 0.25, 0.50, 0.75, 1.0],
        labels=["Low", "Medium", "High", "Very High"],
    )

    return df


def add_segment_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Add business-relevant segment labels."""
    df = df.copy()

    # Tenure band
    df["tenure_band"] = pd.cut(
        df["tenure"],
        bins=[0, 12, 24, 48, 100],
        labels=["0-12 months", "13-24 months", "25-48 months", "49+ months"],
    )

    # Value segment
    df["value_segment"] = pd.cut(
        df["monthly_charges"],
        bins=[0, 40, 70, 100, 200],
        labels=["Low Value", "Medium Value", "High Value", "Premium"],
    )

    return df


def build_all_features(version: str = "B") -> pd.DataFrame:
    """Build all features and save the final feature table."""
    df = aggregate_customer_metrics()
    df = calculate_engagement_score(df, version=version)
    df = add_segment_labels(df)

    # Save
    output_path = os.path.join(PROCESSED_DIR, f"customer_features_v{version}.csv")
    df.to_csv(output_path, index=False)
    print(f"Feature table saved to {output_path}")
    print(f"Total customers: {len(df)}")
    print(f"Engagement score stats:\n{df['engagement_score'].describe()}")

    return df


def compare_engagement_versions():
    """Compare engagement scores across versions."""
    versions = {}
    for v in ["A", "B", "C"]:
        try:
            df = pd.read_csv(os.path.join(PROCESSED_DIR, f"customer_features_v{v}.csv"))
            versions[v] = df["engagement_score"]
        except FileNotFoundError:
            print(f"Version {v} not found. Run build_all_features() first.")

    if len(versions) == 3:
        comparison = pd.DataFrame(versions)
        print("\nEngagement Score Comparison by Version:")
        print(comparison.describe())

        # Check correlation
        corr = comparison.corr()
        print("\nCorrelation Matrix:")
        print(corr.round(3))

        # Save comparison
        comparison_path = os.path.join(REPORTS_DIR, "engagement_score_comparison.csv")
        comparison.to_csv(comparison_path, index=False)
        print(f"\nComparison saved to {comparison_path}")


if __name__ == "__main__":
    # Build features with business-rule weighting (Version B)
    features_df = build_all_features(version="B")

    # Also build versions A and C for comparison
    print("\n--- Building Version A (Equal Weighting) ---")
    build_all_features(version="A")

    print("\n--- Building Version C (Standardized) ---")
    build_all_features(version="C")

    print("\n--- Comparing Versions ---")
    compare_engagement_versions()
