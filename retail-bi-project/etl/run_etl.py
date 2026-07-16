"""Orchestrates the full ETL run: extract -> transform -> load.

Usage:
    python etl/run_etl.py
"""
import sys
import os

sys.path.append(os.path.dirname(__file__))

from extract import extract_all
from transform import build_star_schema
from load import load_to_warehouse


def main():
    print("=== Retail BI ETL pipeline ===")
    raw = extract_all()
    tables = build_star_schema(raw)
    load_to_warehouse(tables)
    print("=== ETL complete ===")


if __name__ == "__main__":
    main()
