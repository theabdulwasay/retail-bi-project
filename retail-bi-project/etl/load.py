"""Load: write cleaned star-schema tables into the SQLite data warehouse."""
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "retail_dw.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "schema.sql")


def load_to_warehouse(tables: dict):
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())

    for name, df in tables.items():
        df.to_sql(name, conn, if_exists="append", index=False)
        print(f"[load] wrote {len(df)} rows -> {name}")

    conn.commit()
    conn.close()
    print(f"[load] warehouse ready at {DB_PATH}")
