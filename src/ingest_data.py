"""
ingest_data.py

Loads and standardizes data from raw sources into staging tables.
Handles:
  - IBM Telco customer data loading
  - ID standardization across all tables
  - Schema validation
  - Initial type conversions
"""

import pandas as pd
import numpy as np
import os
import sqlite3
from datetime import datetime

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw", "synthetic")
STAGING_DIR = os.path.join(DATA_DIR, "staging")
DB_PATH = os.path.join(DATA_DIR, "analytics.db")

os.makedirs(STAGING_DIR, exist_ok=True)


def load_customer_data(path: str = None) -> pd.DataFrame:
    """Load and validate the public customer dataset."""
    if path is None:
        # Try public directory first, then synthetic
        public_path = os.path.join(DATA_DIR, "raw", "public", "customer_base.csv")
        synthetic_path = os.path.join(RAW_DIR, "customer_base.csv")

        if os.path.exists(public_path):
            path = public_path
        elif os.path.exists(synthetic_path):
            path = synthetic_path
            print("Warning: Using synthetic customer data instead of public dataset.")
        else:
            raise FileNotFoundError(
                "No customer data found. Run generate_synthetic_data.py first or place "
                "the public dataset in data/raw/public/"
            )

    print(f"Loading customer data from {path}...")
    df = pd.read_csv(path, dtype={"customer_id": str})

    # Standardize column names — handle both public dataset (customerID) and synthetic (customer_id)
    column_mapping = {}
    for old_col in df.columns:
        if old_col in ["customerID", "CustomerID", "customer_id"]:
            column_mapping[old_col] = "customer_id"
        elif old_col == "SeniorCitizen":
            column_mapping[old_col] = "senior_citizen"
        elif old_col == "PhoneService":
            column_mapping[old_col] = "phone_service"
        elif old_col == "MultipleLines":
            column_mapping[old_col] = "multiple_lines"
        elif old_col == "InternetService":
            column_mapping[old_col] = "internet_service"
        elif old_col == "OnlineSecurity":
            column_mapping[old_col] = "online_security"
        elif old_col == "OnlineBackup":
            column_mapping[old_col] = "online_backup"
        elif old_col == "DeviceProtection":
            column_mapping[old_col] = "device_protection"
        elif old_col == "TechSupport":
            column_mapping[old_col] = "tech_support"
        elif old_col == "StreamingTV":
            column_mapping[old_col] = "streaming_tv"
        elif old_col == "StreamingMovies":
            column_mapping[old_col] = "streaming_movies"
        elif old_col == "PaperlessBilling":
            column_mapping[old_col] = "paperless_billing"
        elif old_col == "PaymentMethod":
            column_mapping[old_col] = "payment_method"
        elif old_col == "MonthlyCharges":
            column_mapping[old_col] = "monthly_charges"
        elif old_col == "TotalCharges":
            column_mapping[old_col] = "total_charges"
        elif old_col == "Churn":
            column_mapping[old_col] = "churn"
    df = df.rename(columns=column_mapping)

    # Convert numeric columns
    df["monthly_charges"] = pd.to_numeric(df["monthly_charges"], errors="coerce")
    df["total_charges"] = pd.to_numeric(df["total_charges"], errors="coerce")
    df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce")
    df["senior_citizen"] = pd.to_numeric(df["senior_citizen"], errors="coerce").fillna(0).astype(int)

    # Standardize boolean columns
    bool_cols = ["partner", "dependents", "phone_service", "paperless_billing", "churn"]
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].str.title()

    print(f"Loaded {len(df)} customer records with {len(df.columns)} fields.")
    return df


def load_synthetic_table(filename: str, **dtype_kwargs) -> pd.DataFrame:
    """Load a synthetic CSV file from the raw/synthetic directory."""
    path = os.path.join(RAW_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Synthetic data file not found: {path}. Run generate_synthetic_data.py first.")

    df = pd.read_csv(path, dtype=dtype_kwargs)
    print(f"Loaded {len(df)} records from {filename}")
    return df


def standardize_ids(df: pd.DataFrame, id_column: str) -> pd.DataFrame:
    """Ensure all IDs are uppercase strings without leading/trailing whitespace."""
    df[id_column] = df[id_column].astype(str).str.strip().str.upper()
    return df


def validate_schema(df: pd.DataFrame, expected_columns: list) -> bool:
    """Check that required columns exist in the dataframe."""
    missing = set(expected_columns) - set(df.columns)
    if missing:
        print(f"Warning: Missing columns: {missing}")
        return False
    print(f"Schema validated: all {len(expected_columns)} expected columns present.")
    return True


def save_staging(df: pd.DataFrame, filename: str):
    """Save a dataframe to the staging directory."""
    output_path = os.path.join(STAGING_DIR, filename)
    df.to_csv(output_path, index=False)
    print(f"Saved staging data to {output_path}")


def ingest_all():
    """Run the full ingestion pipeline."""
    print("=" * 60)
    print("DATA INGESTION PIPELINE")
    print("=" * 60)

    # Load customer data
    customer_df = load_customer_data()
    customer_df = standardize_ids(customer_df, "customer_id")
    save_staging(customer_df, "stg_customer.csv")

    # Validate customer schema
    expected_customer_cols = [
        "customer_id", "gender", "senior_citizen", "partner",
        "dependents", "tenure", "phone_service", "internet_service",
        "contract", "paperless_billing", "payment_method",
        "monthly_charges", "total_charges", "churn"
    ]
    validate_schema(customer_df, expected_customer_cols)

    # Load synthetic tables
    interactions_df = load_synthetic_table("interactions.csv")
    interactions_df = standardize_ids(interactions_df, "customer_id")
    save_staging(interactions_df, "stg_interactions.csv")

    content_df = load_synthetic_table("content_usage.csv")
    content_df = standardize_ids(content_df, "customer_id")
    save_staging(content_df, "stg_content_usage.csv")

    participation_df = load_synthetic_table("event_participation.csv")
    participation_df = standardize_ids(participation_df, "customer_id")
    save_staging(participation_df, "stg_event_participation.csv")

    activity_df = load_synthetic_table("account_activity.csv")
    activity_df = standardize_ids(activity_df, "customer_id")
    save_staging(activity_df, "stg_account_activity.csv")

    events_df = load_synthetic_table("events.csv")
    save_staging(events_df, "stg_events.csv")

    # Load dimension tables
    dim_date_df = load_synthetic_table("dim_date.csv")
    save_staging(dim_date_df, "stg_dim_date.csv")

    dim_customer_df = load_synthetic_table("dim_customer.csv")
    dim_customer_df = standardize_ids(dim_customer_df, "customer_id")
    save_staging(dim_customer_df, "stg_dim_customer.csv")

    dim_subscription_df = load_synthetic_table("dim_subscription.csv")
    dim_subscription_df = standardize_ids(dim_subscription_df, "customer_id")
    save_staging(dim_subscription_df, "stg_dim_subscription.csv")

    dim_content_df = load_synthetic_table("dim_content.csv")
    save_staging(dim_content_df, "stg_dim_content.csv")

    dim_event_df = load_synthetic_table("dim_event.csv")
    save_staging(dim_event_df, "stg_dim_event.csv")

    print("\nIngestion complete!")
    print(f"Staging data saved to: {STAGING_DIR}")


if __name__ == "__main__":
    ingest_all()
