"""Transform: clean raw data and build the star-schema dimension/fact tables."""
import pandas as pd
import numpy as np


PAYMENT_MAP = {
    "credit card": "Credit Card",
    "creditcard": "Credit Card",
    "debit": "Debit Card",
    "debit card": "Debit Card",
    "cash": "Cash",
    "mobile": "Mobile Pay",
    "mobile pay": "Mobile Pay",
    "gift card": "Gift Card",
    "giftcard": "Gift Card",
}


def _parse_mixed_dates(series: pd.Series) -> pd.Series:
    """Raw dates arrive in 3 different formats — normalize them all to datetime."""
    return pd.to_datetime(series, format="mixed", dayfirst=False, errors="coerce")


def _normalize_payment(series: pd.Series) -> pd.Series:
    cleaned = series.fillna("").astype(str).str.strip().str.lower()
    mapped = cleaned.map(PAYMENT_MAP)
    return mapped.fillna("Other")


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    df = customers.copy()
    df["signup_date"] = _parse_mixed_dates(df["signup_date"])
    df["segment"] = df["segment"].fillna("Retail").replace("", "Retail")
    df["customer_name"] = df["customer_name"].str.strip()
    df = df.drop_duplicates(subset="customer_id")
    return df


def clean_products(products: pd.DataFrame) -> pd.DataFrame:
    df = products.copy()
    if "subcategory" not in df.columns:
        df["subcategory"] = "General"
    if "brand" not in df.columns:
        df["brand"] = "Unknown"
    df["margin_pct"] = ((df["unit_price"] - df["unit_cost"]) / df["unit_price"] * 100).round(1)
    return df


def clean_stores(stores: pd.DataFrame) -> pd.DataFrame:
    df = stores.copy()
    if "region" not in df.columns:
        df["region"] = "Unknown"
    return df


def clean_sales(sales: pd.DataFrame, products: pd.DataFrame, valid_customer_ids: set) -> pd.DataFrame:
    """
    Cleaning steps applied, in order:
    1. Drop exact duplicate line items (accidental double-loads)
    2. Normalize the 3 mixed date formats into one
    3. Drop rows with missing/invalid customer_id (can't attribute the sale)
    4. Flag negative-quantity rows as returns instead of dropping them
    5. Normalize payment method labels
    6. Recompute line revenue, cost, and gross profit
    """
    df = sales.copy()
    before = len(df)

    df = df.drop_duplicates()

    df["order_date"] = _parse_mixed_dates(df["order_date"])

    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce")
    df = df[df["customer_id"].notna()]
    df["customer_id"] = df["customer_id"].astype(int)
    df = df[df["customer_id"].isin(valid_customer_ids)]

    if "payment_method" not in df.columns:
        df["payment_method"] = "Other"
    df["payment_method"] = _normalize_payment(df["payment_method"])

    df["is_return"] = (df["quantity"] < 0).astype(int)
    df["net_revenue"] = (df["quantity"] * df["unit_price"] * (1 - df["discount_pct"])).round(2)

    cost_lookup = products.set_index("product_id")["unit_cost"]
    df["unit_cost"] = df["product_id"].map(cost_lookup).fillna(0)
    df["cost_amount"] = (df["quantity"].abs() * df["unit_cost"] * np.sign(df["quantity"])).round(2)
    df["gross_profit"] = (df["net_revenue"] - df["cost_amount"]).round(2)

    df = df.dropna(subset=["order_date"])

    after = len(df)
    print(f"[transform] sales rows {before} -> {after} after cleaning "
          f"({before - after} removed as unattributable/duplicate)")
    return df


def build_star_schema(raw: dict) -> dict:
    dim_store = clean_stores(raw["stores"])
    dim_product = clean_products(raw["products"])
    dim_customer = clean_customers(raw["customers"])

    fact_sales = clean_sales(
        raw["sales"],
        dim_product,
        valid_customer_ids=set(dim_customer["customer_id"]),
    )

    date_range = pd.date_range(fact_sales["order_date"].min(), fact_sales["order_date"].max())
    dim_date = pd.DataFrame({
        "date_key": date_range.strftime("%Y%m%d").astype(int),
        "full_date": date_range.strftime("%Y-%m-%d"),
        "year": date_range.year,
        "quarter": date_range.quarter,
        "month": date_range.month,
        "month_name": date_range.strftime("%B"),
        "day_of_week": date_range.strftime("%A"),
        "week_of_year": date_range.isocalendar().week.astype(int),
        "is_weekend": (date_range.dayofweek >= 5).astype(int),
    })

    fact_sales["date_key"] = fact_sales["order_date"].dt.strftime("%Y%m%d").astype(int)
    fact_sales = fact_sales[[
        "order_id", "date_key", "store_id", "customer_id", "product_id",
        "quantity", "unit_price", "discount_pct", "net_revenue",
        "cost_amount", "gross_profit", "payment_method", "is_return",
    ]]

    return {
        "dim_date": dim_date,
        "dim_store": dim_store,
        "dim_product": dim_product,
        "dim_customer": dim_customer,
        "fact_sales": fact_sales,
    }
