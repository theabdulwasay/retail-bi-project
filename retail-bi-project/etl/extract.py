"""Extract: load raw CSV files into pandas DataFrames."""
import pandas as pd
import os

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def extract_all():
    """Read all raw source files and return them as a dict of DataFrames."""
    stores = pd.read_csv(os.path.join(RAW_DIR, "stores.csv"))
    products = pd.read_csv(os.path.join(RAW_DIR, "products.csv"))
    customers = pd.read_csv(os.path.join(RAW_DIR, "customers.csv"))
    sales = pd.read_csv(os.path.join(RAW_DIR, "sales_raw.csv"))

    print(f"[extract] stores={len(stores)} products={len(products)} "
          f"customers={len(customers)} sales_lines={len(sales)}")

    return {
        "stores": stores,
        "products": products,
        "customers": customers,
        "sales": sales,
    }


if __name__ == "__main__":
    extract_all()
