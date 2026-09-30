"""
generate_synthetic_data.py

Generates synthetic operational data for the Client Engagement &
Subscription Retention Analytics project.

Data is based on public IBM Telco Customer Churn dataset fields and
extends them with:
  - interactions
  - content_usage
  - event_participation
  - account_activity

All data uses RANDOM_SEED = 42 for reproducibility.
"""

import pandas as pd
import numpy as np
import os

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "raw", "synthetic")
os.makedirs(DATA_DIR, exist_ok=True)


def generate_customer_base(n_customers: int = 7043) -> pd.DataFrame:
    """
    Generate a customer base table based on IBM Telco field structure.
    This is a simplified version focused on key fields.
    """
    np.random.seed(RANDOM_SEED)

    genders = np.random.choice(["Male", "Female"], size=n_customers, p=[0.505, 0.495])
    senior = np.random.choice([0, 1], size=n_customers, p=[0.836, 0.164])
    partner = np.random.choice(["Yes", "No"], size=n_customers, p=[0.48, 0.52])
    dependents = np.random.choice(["Yes", "No"], size=n_customers, p=[0.30, 0.70])

    internet = np.random.choice(
        ["Fiber optic", "DSL", "No"], size=n_customers, p=[0.44, 0.35, 0.21]
    )

    contract = np.random.choice(
        ["Month-to-month", "One year", "Two year"],
        size=n_customers,
        p=[0.55, 0.27, 0.18],
    )

    # tenure correlated with contract type
    tenure = []
    for c in contract:
        if c == "Month-to-month":
            tenure.append(max(1, int(np.random.exponential(12))))
        elif c == "One year":
            tenure.append(max(1, int(np.random.normal(24, 10))))
        else:
            tenure.append(max(1, int(np.random.normal(48, 15))))

    tenure = np.clip(tenure, 1, 72)

    # monthly charges correlated with internet service
    monthly_charges = []
    for i_service in internet:
        if i_service == "Fiber optic":
            monthly_charges.append(round(np.random.normal(90, 15), 2))
        elif i_service == "DSL":
            monthly_charges.append(round(np.random.normal(55, 10), 2))
        else:
            monthly_charges.append(round(np.random.normal(20, 5), 2))

    monthly_charges = np.clip(monthly_charges, 10, 150)

    # churn: inversely correlated with tenure and contract length
    churn_prob = []
    for t, c in zip(tenure, contract):
        base = 0.26
        if c == "Two year":
            base -= 0.15
        elif c == "One year":
            base -= 0.08
        base -= t * 0.003
        base = np.clip(base, 0.02, 0.60)
        churn_prob.append(base)

    churn = [np.random.choice(["No", "Yes"], p=[1 - p, p]) for p in churn_prob]

    # total charges = monthly * tenure (with some noise)
    total_charges = [round(m * t * np.random.uniform(0.9, 1.1), 2) for m, t in zip(monthly_charges, tenure)]

    # Payment method
    payment = np.random.choice(
        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
        size=n_customers,
        p=[0.34, 0.15, 0.27, 0.24],
    )

    df = pd.DataFrame(
        {
            "customerID": [f"CUST-{i:05d}" for i in range(1, n_customers + 1)],
            "gender": genders,
            "SeniorCitizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": np.random.choice(["Yes", "No"], size=n_customers, p=[0.90, 0.10]),
            "InternetService": internet,
            "Contract": contract,
            "PaperlessBilling": np.random.choice(["Yes", "No"], size=n_customers, p=[0.59, 0.41]),
            "PaymentMethod": payment,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
            "Churn": churn,
        }
    )

    return df


def generate_interactions(customer_ids: list, n_interactions: int = 25000) -> pd.DataFrame:
    """Generate synthetic client interaction records."""
    np.random.seed(RANDOM_SEED)

    interaction_types = [
        "Analyst Meeting",
        "Webinar",
        "Support",
        "Email",
        "Product Demo",
        "Account Review",
    ]
    channels = ["Online", "Email", "Phone", "Video", "In-Person"]
    outcomes = ["Resolved", "Pending", "Escalated", "No Response"]

    interaction_weights = [0.20, 0.25, 0.30, 0.15, 0.05, 0.05]
    channel_weights = [0.30, 0.25, 0.25, 0.15, 0.05]
    outcome_weights = [0.60, 0.15, 0.10, 0.15]

    df = pd.DataFrame(
        {
            "interaction_id": [f"INT-{i:06d}" for i in range(1, n_interactions + 1)],
            "customer_id": np.random.choice(customer_ids, size=n_interactions),
            "interaction_date": pd.date_range("2023-01-01", "2024-06-30", freq="h")
            .to_series()
            .sample(n_interactions, replace=True, random_state=RANDOM_SEED)
            .dt.date,
            "interaction_type": np.random.choice(interaction_types, size=n_interactions, p=interaction_weights),
            "channel": np.random.choice(channels, size=n_interactions, p=channel_weights),
            "duration_minutes": np.clip(
                np.random.exponential(25, n_interactions).astype(int), 1, 300
            ),
            "outcome": np.random.choice(outcomes, size=n_interactions, p=outcome_weights),
        }
    )

    # Introduce some data quality issues intentionally
    # ~1% of interaction types have inconsistent casing
    mask = np.random.choice([True, False], size=n_interactions, p=[0.01, 0.99])
    df.loc[mask, "interaction_type"] = df.loc[mask, "interaction_type"].str.lower()

    return df


def generate_content_usage(customer_ids: list, n_records: int = 30000) -> pd.DataFrame:
    """Generate synthetic content usage records."""
    np.random.seed(RANDOM_SEED)

    categories = ["Technology", "Strategy", "Operations", "Finance", "Marketing", "Industry Research"]

    df = pd.DataFrame(
        {
            "usage_id": [f"USE-{i:07d}" for i in range(1, n_records + 1)],
            "customer_id": np.random.choice(customer_ids, size=n_records),
            "usage_date": pd.date_range("2023-01-01", "2024-06-30", freq="h")
            .to_series()
            .sample(n_records, replace=True, random_state=RANDOM_SEED + 1)
            .dt.date,
            "content_category": np.random.choice(categories, size=n_records),
            "reports_viewed": np.clip(
                np.random.poisson(3, n_records), 0, 20
            ),
            "downloads": np.clip(
                np.random.poisson(1, n_records), 0, 10
            ),
            "time_spent_minutes": np.clip(
                np.random.exponential(30, n_records).astype(int), 1, 500
            ),
        }
    )

    # Some missing dates (~2%)
    mask = np.random.choice([True, False], size=n_records, p=[0.02, 0.98])
    df.loc[mask, "usage_date"] = pd.NaT

    return df


def generate_event_participation(customer_ids: list, n_events: int = 20) -> pd.DataFrame:
    """Generate synthetic event participation records."""
    np.random.seed(RANDOM_SEED)

    event_types = ["Webinar", "Conference", "Roundtable", "Executive Session", "Workshop"]
    topics = [
        "Digital Transformation",
        "Market Trends",
        "Leadership",
        "Innovation",
        "Cost Optimization",
        "Data Strategy",
    ]

    events = []
    for i in range(n_events):
        events.append(
            {
                "event_id": f"EVT-{i+1:03d}",
                "event_type": np.random.choice(event_types),
                "event_topic": np.random.choice(topics),
            }
        )
    events_df = pd.DataFrame(events)

    # Generate participation records
    records = []
    for _, event in events_df.iterrows():
        n_registered = np.random.randint(50, 500)
        registered_customers = np.random.choice(customer_ids, size=n_registered, replace=False)
        for customer_id in registered_customers:
            attended = np.random.choice(["Yes", "No"], p=[0.60, 0.40])
            records.append(
                {
                    "event_participation_id": f"EP-{len(records)+1:06d}",
                    "customer_id": customer_id,
                    "event_id": event["event_id"],
                    "event_date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=np.random.randint(0, 180)),
                    "event_type": event["event_type"],
                    "registered": "Yes",
                    "attended": attended,
                }
            )

    participation_df = pd.DataFrame(records)
    return participation_df, events_df


def generate_account_activity(customer_ids: list, n_days: int = 365) -> pd.DataFrame:
    """Generate synthetic daily account activity records."""
    np.random.seed(RANDOM_SEED)

    records = []
    start_date = pd.Timestamp("2023-07-01")
    all_dates = pd.date_range(start_date, periods=n_days, freq="D")

    for customer_id in customer_ids:
        # Not every customer is active every day
        active_days = np.random.choice(
            all_dates,
            size=np.random.randint(30, min(n_days, 200)),
            replace=False,
        )

        for date in active_days:
            # More active customers have higher counts
            activity_level = np.random.choice(["low", "medium", "high"], p=[0.40, 0.40, 0.20])

            if activity_level == "low":
                logins = np.random.randint(0, 3)
                sessions = np.random.randint(0, 2)
                features = np.random.randint(0, 3)
                active_users = np.random.randint(1, 2)
            elif activity_level == "medium":
                logins = np.random.randint(2, 8)
                sessions = np.random.randint(1, 5)
                features = np.random.randint(2, 8)
                active_users = np.random.randint(1, 4)
            else:
                logins = np.random.randint(5, 20)
                sessions = np.random.randint(3, 12)
                features = np.random.randint(5, 15)
                active_users = np.random.randint(2, 10)

            records.append(
                {
                    "activity_id": f"ACT-{len(records)+1:08d}",
                    "customer_id": customer_id,
                    "activity_date": date,
                    "active_users": active_users,
                    "login_count": logins,
                    "features_used": features,
                    "session_count": sessions,
                }
            )

    df = pd.DataFrame(records)

    # Introduce some duplicate activity IDs (~0.5%)
    if len(df) > 100:
        dup_indices = np.random.choice(df.index, size=int(len(df) * 0.005), replace=False)
        df.loc[dup_indices, "activity_id"] = df.loc[dup_indices, "activity_id"] + "_dup"

    return df


def generate_dim_date(start: str = "2023-01-01", end: str = "2024-12-31") -> pd.DataFrame:
    """Generate a date dimension table."""
    dates = pd.date_range(start, end, freq="D")
    df = pd.DataFrame({"date": dates})
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%B")
    df["week"] = df["date"].dt.isocalendar().week
    df["day_of_week"] = df["date"].dt.strftime("%A")
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    return df


def generate_dim_customer(customer_df: pd.DataFrame) -> pd.DataFrame:
    """Generate dim_customer from public customer data."""
    np.random.seed(RANDOM_SEED)
    n = len(customer_df)

    regions = ["North", "South", "East", "West", "Central"]
    industries = ["Technology", "Finance", "Healthcare", "Manufacturing", "Retail", "Education"]
    company_sizes = ["1-50", "51-200", "201-1000", "1001-5000", "5000+"]

    age_groups = ["18-30", "31-45", "46-60", "60+"]

    df = pd.DataFrame(
        {
            "customer_id": customer_df["customerID"],
            "gender": customer_df["gender"],
            "age_group": np.random.choice(age_groups, size=n),
            "senior_citizen": customer_df["SeniorCitizen"].map({0: "No", 1: "Yes"}),
            "partner": customer_df["Partner"],
            "dependents": customer_df["Dependents"],
            "region": np.random.choice(regions, size=n),
            "industry": np.random.choice(industries, size=n),
            "company_size": np.random.choice(company_sizes, size=n),
        }
    )

    return df


def generate_dim_subscription(customer_df: pd.DataFrame) -> pd.DataFrame:
    """Generate dim_subscription from public customer data."""
    np.random.seed(RANDOM_SEED)

    records = []
    for _, row in customer_df.iterrows():
        start_date = pd.Timestamp("2022-01-01") + pd.Timedelta(
            days=np.random.randint(0, 730)
        )
        contract_duration_months = {"Month-to-month": 1, "One year": 12, "Two year": 24}[
            row["Contract"]
        ]
        renewal_date = start_date + pd.Timedelta(days=contract_duration_months * 30)

        records.append(
            {
                "subscription_id": f"SUB-{row['customerID']}",
                "customer_id": row["customerID"],
                "plan_type": row["Contract"],
                "contract_type": row["Contract"],
                "start_date": start_date.strftime("%Y-%m-%d"),
                "renewal_date": renewal_date.strftime("%Y-%m-%d"),
                "contract_value": round(row["TotalCharges"], 2),
                "status": "Active" if row["Churn"] == "No" else "Cancelled",
            }
        )

    return pd.DataFrame(records)


def generate_all():
    """Generate all synthetic tables and save to CSV."""
    print("Generating customer base...")
    customer_df = generate_customer_base()
    customer_df.to_csv(
        os.path.join(DATA_DIR, "customer_base.csv"), index=False
    )
    print(f"  Saved {len(customer_df)} customer records.")

    customer_ids = customer_df["customerID"].tolist()

    print("Generating interactions...")
    interactions_df = generate_interactions(customer_ids)
    interactions_df.to_csv(
        os.path.join(DATA_DIR, "interactions.csv"), index=False
    )
    print(f"  Saved {len(interactions_df)} interaction records.")

    print("Generating content usage...")
    content_df = generate_content_usage(customer_ids)
    content_df.to_csv(
        os.path.join(DATA_DIR, "content_usage.csv"), index=False
    )
    print(f"  Saved {len(content_df)} content usage records.")

    print("Generating event participation...")
    participation_df, events_df = generate_event_participation(customer_ids)
    participation_df.to_csv(
        os.path.join(DATA_DIR, "event_participation.csv"), index=False
    )
    events_df.to_csv(
        os.path.join(DATA_DIR, "events.csv"), index=False
    )
    print(f"  Saved {len(participation_df)} participation records and {len(events_df)} events.")

    print("Generating account activity...")
    activity_df = generate_account_activity(customer_ids)
    activity_df.to_csv(
        os.path.join(DATA_DIR, "account_activity.csv"), index=False
    )
    print(f"  Saved {len(activity_df)} activity records.")

    print("Generating dimension tables...")
    dim_date_df = generate_dim_date()
    dim_date_df.to_csv(
        os.path.join(DATA_DIR, "dim_date.csv"), index=False
    )
    print(f"  Saved {len(dim_date_df)} date dimension records.")

    dim_customer_df = generate_dim_customer(customer_df)
    dim_customer_df.to_csv(
        os.path.join(DATA_DIR, "dim_customer.csv"), index=False
    )
    print(f"  Saved {len(dim_customer_df)} customer dimension records.")

    dim_subscription_df = generate_dim_subscription(customer_df)
    dim_subscription_df.to_csv(
        os.path.join(DATA_DIR, "dim_subscription.csv"), index=False
    )
    print(f"  Saved {len(dim_subscription_df)} subscription dimension records.")

    # dim_content and dim_event are derived from usage/participation
    dim_content_df = pd.DataFrame(
        {
            "content_id": [f"CNT-{i:03d}" for i in range(1, 19)],
            "content_category": ["Technology"] * 3 + ["Strategy"] * 3 + ["Operations"] * 3
            + ["Finance"] * 3 + ["Marketing"] * 3 + ["Industry Research"] * 2,
            "content_type": np.random.choice(
                ["Report", "Whitepaper", "Webinar Recording", "Case Study"],
                size=18,
            ),
        }
    )
    dim_content_df.to_csv(
        os.path.join(DATA_DIR, "dim_content.csv"), index=False
    )
    print(f"  Saved {len(dim_content_df)} content dimension records.")

    dim_event_df = events_df.rename(columns={"event_id": "event_id"}).copy()
    dim_event_df.to_csv(
        os.path.join(DATA_DIR, "dim_event.csv"), index=False
    )
    print(f"  Saved {len(dim_event_df)} event dimension records.")

    print("\nAll synthetic data generated successfully!")
    print(f"Random seed: {RANDOM_SEED}")
    print(f"Data directory: {DATA_DIR}")


if __name__ == "__main__":
    generate_all()
