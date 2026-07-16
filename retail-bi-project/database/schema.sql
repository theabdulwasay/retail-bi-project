-- Star schema for the retail sales data warehouse

CREATE TABLE dim_date (
    date_key    INTEGER PRIMARY KEY,   -- YYYYMMDD
    full_date   TEXT NOT NULL,
    year        INTEGER NOT NULL,
    quarter     INTEGER NOT NULL,
    month       INTEGER NOT NULL,
    month_name  TEXT NOT NULL,
    day_of_week TEXT NOT NULL,
    week_of_year INTEGER NOT NULL,
    is_weekend  INTEGER NOT NULL
);

CREATE TABLE dim_store (
    store_id    INTEGER PRIMARY KEY,
    store_name  TEXT NOT NULL,
    city        TEXT NOT NULL,
    state       TEXT NOT NULL,
    region      TEXT NOT NULL
);

CREATE TABLE dim_product (
    product_id   INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category     TEXT NOT NULL,
    subcategory  TEXT NOT NULL,
    brand        TEXT NOT NULL,
    unit_price   REAL NOT NULL,
    unit_cost    REAL NOT NULL,
    margin_pct   REAL NOT NULL
);

CREATE TABLE dim_customer (
    customer_id   INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    email         TEXT,
    signup_date   TEXT,
    segment       TEXT NOT NULL
);

CREATE TABLE fact_sales (
    order_id        INTEGER NOT NULL,
    date_key        INTEGER NOT NULL REFERENCES dim_date(date_key),
    store_id        INTEGER NOT NULL REFERENCES dim_store(store_id),
    customer_id     INTEGER NOT NULL REFERENCES dim_customer(customer_id),
    product_id      INTEGER NOT NULL REFERENCES dim_product(product_id),
    quantity        INTEGER NOT NULL,
    unit_price      REAL NOT NULL,
    discount_pct    REAL NOT NULL,
    net_revenue     REAL NOT NULL,
    cost_amount     REAL NOT NULL,
    gross_profit    REAL NOT NULL,
    payment_method  TEXT NOT NULL,
    is_return       INTEGER NOT NULL
);

CREATE INDEX idx_fact_date     ON fact_sales(date_key);
CREATE INDEX idx_fact_store    ON fact_sales(store_id);
CREATE INDEX idx_fact_product  ON fact_sales(product_id);
CREATE INDEX idx_fact_customer ON fact_sales(customer_id);
CREATE INDEX idx_fact_payment  ON fact_sales(payment_method);
