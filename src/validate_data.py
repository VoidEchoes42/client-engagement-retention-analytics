"""
validate_data.py

Validates data quality in the processed layer:
  - Completeness checks
  - Duplicate detection
  - Range validation
  - Referential integrity
  - Category consistency
"""

import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "..", "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)


def load_processed(filename: str) -> pd.DataFrame:
    """Load a processed CSV file."""
    path = os.path.join(PROCESSED_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Processed file not found: {path}")
    return pd.read_csv(path)


def check_missing_values(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """Check for missing values in each column."""
    missing = df.isnull().sum()
    pct = (missing / len(df) * 100).round(2)
    result = pd.DataFrame({"missing_count": missing, "missing_pct": pct})
    result = result[result["missing_count"] > 0].sort_values("missing_count", ascending=False)
    if len(result) > 0:
        print(f"\n{table_name} - Missing Values:")
        print(result)
    else:
        print(f"\n{table_name}: No missing values.")
    return result


def check_duplicates(df: pd.DataFrame, table_name: str, id_column: str) -> int:
    """Check for duplicate IDs."""
    duplicates = df[id_column].duplicated().sum()
    print(f"{table_name}: {duplicates} duplicate {id_column} values")
    return duplicates


def check_ranges(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """Check for invalid ranges in numeric columns."""
    issues = []

    for col in df.select_dtypes(include=[np.number]).columns:
        neg_count = (df[col] < 0).sum()
        if neg_count > 0:
            issues.append({"column": col, "issue": "negative_values", "count": int(neg_count)})

    if issues:
        result = pd.DataFrame(issues)
        print(f"\n{table_name} - Range Issues:")
        print(result)
    else:
        print(f"\n{table_name}: No range issues.")

    return pd.DataFrame(issues)


def check_referential_integrity() -> dict:
    """Check that all foreign keys reference existing primary keys."""
    results = {}

    try:
        customers = set(load_processed("processed_customer.csv")["customer_id"].astype(str))
    except FileNotFoundError:
        print("Warning: processed_customer.csv not found. Skipping referential integrity checks.")
        return results

    fact_tables = {
        "fact_interaction": "processed_interactions.csv",
        "fact_content_usage": "processed_content_usage.csv",
        "fact_event_participation": "processed_event_participation.csv",
        "fact_account_activity": "processed_account_activity.csv",
    }

    for table_name, filename in fact_tables.items():
        try:
            df = load_processed(filename)
            if "customer_id" in df.columns:
                orphan_count = (~df["customer_id"].isin(customers)).sum()
                results[table_name] = int(orphan_count)
                if orphan_count > 0:
                    print(f"WARNING: {orphan_count} orphan customer_ids in {table_name}")
                else:
                    print(f"{table_name}: All customer_ids valid.")
        except FileNotFoundError:
            print(f"Warning: {filename} not found. Skipping.")

    return results


def check_category_consistency(df: pd.DataFrame, table_name: str, columns: list) -> dict:
    """Check for inconsistent category values."""
    results = {}
    for col in columns:
        if col in df.columns:
            values = df[col].dropna().unique()
            # Check for case variations
            lower_values = [str(v).lower() for v in values]
            unique_lower = set(lower_values)
            if len(unique_lower) != len(values):
                results[col] = {
                    "issue": "case_inconsistency",
                    "values": list(values),
                }
                print(f"WARNING: Case inconsistency in {table_name}.{col}: {list(values)}")
            else:
                print(f"{table_name}.{col}: Category values consistent.")
    return results


def validate_all():
    """Run all validation checks."""
    print("=" * 60)
    print("DATA VALIDATION")
    print("=" * 60)

    # Check missing values
    tables = {
        "Customer": "processed_customer.csv",
        "Interactions": "processed_interactions.csv",
        "Content Usage": "processed_content_usage.csv",
        "Event Participation": "processed_event_participation.csv",
        "Account Activity": "processed_account_activity.csv",
    }

    missing_summary = {}
    for table_name, filename in tables.items():
        try:
            df = load_processed(filename)
            missing = check_missing_values(df, table_name)
            missing_summary[table_name] = missing
        except FileNotFoundError:
            print(f"Warning: {filename} not found.")

    # Check duplicates
    print("\n--- Duplicate Checks ---")
    try:
        customer_df = load_processed("processed_customer.csv")
        check_duplicates(customer_df, "Customer", "customer_id")
    except FileNotFoundError:
        pass

    # Check ranges
    print("\n--- Range Checks ---")
    for table_name, filename in tables.items():
        try:
            df = load_processed(filename)
            check_ranges(df, table_name)
        except FileNotFoundError:
            pass

    # Referential integrity
    print("\n--- Referential Integrity ---")
    ref_results = check_referential_integrity()

    # Category consistency
    print("\n--- Category Consistency ---")
    try:
        interactions_df = load_processed("processed_interactions.csv")
        check_category_consistency(
            interactions_df, "Interactions", ["interaction_type", "channel", "outcome"]
        )
    except FileNotFoundError:
        pass

    try:
        participation_df = load_processed("processed_event_participation.csv")
        check_category_consistency(
            participation_df, "Event Participation", ["event_type", "registered", "attended"]
        )
    except FileNotFoundError:
        pass

    print("\n" + "=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    validate_all()
