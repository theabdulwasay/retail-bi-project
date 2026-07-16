# 🛍️ RetailPulse BI

### End-to-End Retail Sales Analytics · ETL · Star Schema · Interactive Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Warehouse-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-ETL-150458?style=for-the-badge&logo=pandas&logoColor=white)

---

## 📖 Table of Contents

1. [🌟 Project Overview](#-project-overview)
2. [✨ Key Features](#-key-features)
3. [🏗️ Architecture](#️-architecture)
4. [📊 Data Scale](#-data-scale)
5. [⭐ Star Schema Design](#-star-schema-design)
6. [🧹 ETL Pipeline](#-etl-pipeline)
7. [📁 Project Structure](#-project-structure)
8. [🚀 Getting Started](#-getting-started)
9. [📈 Dashboard Guide](#-dashboard-guide)
10. [🧮 Analytics / KPI Queries](#-analytics--kpi-queries)
11. [🧰 Tech Stack](#-tech-stack)
12. [🔮 Future Enhancements](#-future-enhancements)
13. [📝 License & Credits](#-license--credits)

---

## 🌟 Project Overview

**RetailPulse BI** is a complete, portfolio-ready **Business Intelligence** project that mirrors how real retail analytics systems work.

It takes you through the full data journey:

```
📦 Messy raw CSVs
        ↓
🔄 Python ETL (clean, transform, enrich)
        ↓
🗄️ SQLite star-schema data warehouse
        ↓
🧮 Reusable SQL KPI queries
        ↓
🎨 Colorful interactive Streamlit dashboard
```

### 🎯 Why this project exists

Most “BI demos” only show charts. This one demonstrates the **full analytics lifecycle**:

| Layer | What you learn |
|-------|----------------|
| 🧪 **Data generation** | How source systems produce imperfect data |
| 🧹 **ETL** | Cleaning, validation, and auditable transforms |
| 🗄️ **Warehousing** | Dimensional modeling (star schema) |
| 🧮 **Analytics SQL** | Reusable KPI logic for reporting |
| 📊 **Visualization** | Interactive filters, KPIs, and multi-tab insights |

Perfect for portfolios, interviews, and learning modern analytics engineering.

---

## ✨ Key Features

### 📦 Data & Warehouse
- ✅ **~135,000** sales line items across **2 years**
- ✅ **12 stores** in **4 US regions**
- ✅ **80 products** across **8 categories** (with brands & subcategories)
- ✅ **1,200 customers** with loyalty segments
- ✅ Intentionally **messy raw data** (duplicates, mixed dates, nulls, returns)
- ✅ Star schema with **fact + 4 dimension tables**
- ✅ Revenue, cost, **gross profit**, discounts, and payment methods

### 🔄 ETL
- ✅ Extract → Transform → Load orchestration
- ✅ Date normalization (3 formats → one)
- ✅ Payment method cleaning
- ✅ Return flagging (negative quantities kept, not deleted)
- ✅ Cost & profit calculation per line
- ✅ Before/after row-count logging for auditability

### 📊 Dashboard
- ✅ Beautiful **teal / coral / amber** themed UI
- ✅ **6 KPI cards** with prior-period comparison deltas
- ✅ **6 analysis tabs** (Overview → Returns & payments)
- ✅ Filters: date, region, store, category, segment
- ✅ Charts: area, bar, pie, sunburst, treemap, heatmap, scatter, YoY

### 🧮 Analytics
- ✅ **14 ready-to-run SQL KPI queries**
- ✅ Revenue, margin, returns, payment mix, brands, YoY, and more

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                        RetailPulse BI                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   📂 data/raw/*.csv                                             │
│        stores · products · customers · sales_raw                │
│                           │                                     │
│                           ▼                                     │
│   🔄 etl/                                                       │
│        extract.py  →  transform.py  →  load.py                  │
│                           │                                     │
│                           ▼                                     │
│   🗄️ database/retail_dw.db                                      │
│        dim_date · dim_store · dim_product · dim_customer        │
│        fact_sales                                               │
│              │                          │                       │
│              ▼                          ▼                       │
│   🧮 analytics/kpi_queries.sql     🎨 dashboard/app.py         │
│        (14 SQL KPIs)                 (Streamlit + Plotly)       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🔁 Data flow (step by step)

1. **Generate** synthetic retail CSVs (`generate_raw_data.py`)
2. **Extract** CSVs into pandas DataFrames
3. **Transform** dirty data into clean star-schema tables
4. **Load** into SQLite warehouse (`retail_dw.db`)
5. **Analyze** with SQL KPIs and/or the Streamlit dashboard

---

## 📊 Data Scale

Approximate volumes after regenerating data and running ETL:

| 🏷️ Entity | 📏 Size | 📝 Notes |
|-----------|---------|----------|
| 🏪 Stores | **12** | Across Northeast, West, Midwest, South |
| 📦 Products | **80 SKUs** | 8 categories · brands · subcategories |
| 👥 Customers | **1,200** | Retail, Loyalty, VIP, Wholesale |
| 📅 Time span | **~730 days** | Jan 2024 → Dec 2025 (2 years) |
| 🧾 Raw sales lines | **~135,249** | Includes duplicates & messy rows |
| 🧼 Clean fact rows | **~134,624** | After ETL cleaning |
| 🗓️ Date dimension | **730** | One row per calendar day |

### 🌦️ Built-in seasonality

Sales volume is **not flat**. The generator includes:

- 📈 Higher traffic on **weekends**
- 🎄 Peak season in **November–December**
- ☀️ Summer bump in **June–July**

This makes trends, YoY charts, and heatmaps look realistic.

---

## ⭐ Star Schema Design

A classic **dimensional model** optimized for analytics:

```text
                    ┌──────────────┐
                    │   dim_date   │
                    └──────┬───────┘
                           │
┌──────────────┐    ┌──────┴───────┐    ┌──────────────┐
│  dim_store   │────┤  fact_sales  ├────│ dim_product  │
└──────────────┘    └──────┬───────┘    └──────────────┘
                           │
                    ┌──────┴───────┐
                    │ dim_customer │
                    └──────────────┘
```

### 🧾 `fact_sales` (grain = one order line)

| Column | Description |
|--------|-------------|
| `order_id` | Order identifier |
| `date_key` | FK → `dim_date` (YYYYMMDD) |
| `store_id` | FK → `dim_store` |
| `customer_id` | FK → `dim_customer` |
| `product_id` | FK → `dim_product` |
| `quantity` | Units sold (negative = return) |
| `unit_price` | Selling price per unit |
| `discount_pct` | Discount applied (0–0.25+) |
| `net_revenue` | `qty × price × (1 − discount)` |
| `cost_amount` | Product cost × quantity |
| `gross_profit` | `net_revenue − cost_amount` |
| `payment_method` | Credit / Debit / Cash / Mobile / Gift Card / Other |
| `is_return` | `1` if return, else `0` |

### 📅 `dim_date`

`date_key`, `full_date`, `year`, `quarter`, `month`, `month_name`, `day_of_week`, `week_of_year`, `is_weekend`

### 🏪 `dim_store`

`store_id`, `store_name`, `city`, `state`, `region`

### 📦 `dim_product`

`product_id`, `product_name`, `category`, `subcategory`, `brand`, `unit_price`, `unit_cost`, `margin_pct`

### 👤 `dim_customer`

`customer_id`, `customer_name`, `email`, `signup_date`, `segment`

---

## 🧹 ETL Pipeline

### ▶️ How to run

```bash
python etl/run_etl.py
```

### 🧩 Modules

| File | Role |
|------|------|
| `etl/extract.py` | 📥 Reads raw CSVs into DataFrames |
| `etl/transform.py` | 🧼 Cleans, enriches, builds star schema |
| `etl/load.py` | 🗄️ Creates SQLite DB from `schema.sql` and loads tables |
| `etl/run_etl.py` | 🎛️ Orchestrates extract → transform → load |

### 🧪 What the raw data mess includes

The generator intentionally creates real-world problems:

| ⚠️ Issue | 🛠️ How ETL handles it |
|----------|------------------------|
| Duplicate line items | Drop exact duplicates |
| Mixed date formats (`YYYY-MM-DD`, `MM/DD/YYYY`, `DD-Mon-YYYY`) | Parse with mixed-format datetime |
| Missing `customer_id` | Drop unattributable sales |
| Negative quantities | Flag as returns (`is_return = 1`) |
| Blank / inconsistent segments | Default to `Retail` |
| Messy payment labels (`credit card`, `DEBIT`, `cash `) | Normalize to clean categories |

### 💰 Business enrichments during transform

- ✅ Compute **net revenue** after discount  
- ✅ Join product cost → compute **cost_amount**  
- ✅ Compute **gross_profit** per line  
- ✅ Build a complete **date dimension** from observed range  

Console output shows before/after counts so cleaning impact is auditable:

```text
[extract] stores=12 products=80 customers=1200 sales_lines=135249
[transform] sales rows 135249 -> 134624 after cleaning (625 removed...)
[load] wrote 134624 rows -> fact_sales
=== ETL complete ===
```

---

## 📁 Project Structure

```text
retail-bi-project/
│
├── 📂 data/
│   ├── 🐍 generate_raw_data.py      # Create synthetic messy CSVs
│   └── 📂 raw/
│       ├── stores.csv
│       ├── products.csv
│       ├── customers.csv
│       └── sales_raw.csv
│
├── 📂 etl/
│   ├── extract.py                   # Load CSVs
│   ├── transform.py                 # Clean + star schema
│   ├── load.py                      # Write SQLite warehouse
│   └── run_etl.py                   # Pipeline entrypoint
│
├── 📂 database/
│   ├── schema.sql                   # DDL for star schema
│   └── retail_dw.db                 # Generated warehouse (after ETL)
│
├── 📂 analytics/
│   └── kpi_queries.sql              # 14 reusable KPI queries
│
├── 📂 dashboard/
│   └── app.py                       # Streamlit + Plotly UI
│
├── 📄 requirements.txt              # Python dependencies
└── 📘 README.md                     # You are here
```

---

## 🚀 Getting Started

### ✅ Prerequisites

- 🐍 **Python 3.10+**
- 📦 `pip`
- (Optional) 🗄️ `sqlite3` CLI for running SQL files in the terminal

### 1️⃣ Install dependencies

```bash
cd retail-bi-project
pip install -r requirements.txt
```

**Dependencies:**

| Package | Purpose |
|---------|---------|
| `pandas` | Data wrangling / ETL |
| `numpy` | Numeric transforms |
| `streamlit` | Interactive dashboard |
| `plotly` | Charts & visuals |

### 2️⃣ Generate raw data (optional if CSVs already exist)

```bash
python data/generate_raw_data.py
```

This rebuilds all files under `data/raw/`.

### 3️⃣ Run the ETL pipeline

```bash
python etl/run_etl.py
```

Creates / refreshes `database/retail_dw.db`.

### 4️⃣ (Optional) Run KPI SQL

```bash
sqlite3 database/retail_dw.db < analytics/kpi_queries.sql
```

### 5️⃣ Launch the dashboard

```bash
python -m streamlit run dashboard/app.py
```

Then open your browser:

### 🌐 http://localhost:8501

> 💡 Tip (Windows): if `streamlit` is not recognized as a command, always use  
> `python -m streamlit run dashboard/app.py`

---

## 📈 Dashboard Guide

The dashboard is named **RetailPulse BI** and uses a colorful retail theme (teal / coral / amber), custom typography, and multi-tab analytics.

### 🎛️ Sidebar filters

| Filter | What it controls |
|--------|------------------|
| 📅 Date range | Analysis window |
| 🗺️ Region | Northeast / West / Midwest / South |
| 🏪 Stores | Individual store selection |
| 🏷️ Categories | Product category filter |
| 👥 Customer segment | Retail / Loyalty / VIP / Wholesale |

### 🃏 KPI cards (top of page)

| KPI | Meaning |
|-----|---------|
| 💵 **Total revenue** | Sum of net revenue (+ vs prior period) |
| 🧾 **Orders** | Distinct order count (+ vs prior period) |
| 🧺 **Avg order value** | Revenue ÷ orders |
| 📦 **Units sold** | Total quantity |
| 💚 **Gross profit** | Revenue − cost (with margin %) |
| ↩️ **Return lines** | Return volume & rate |

### 🗂️ Tabs explained

| Tab | What’s inside |
|-----|----------------|
| 🏠 **Overview** | Daily revenue area chart, category mix donut, top stores, segment bars |
| 📈 **Trends** | Monthly revenue vs profit, weekday performance, heatmap, YoY lines |
| 🏷️ **Products & brands** | Top 15 SKUs, brand scatter, category→subcategory sunburst, margin table |
| 🏪 **Stores & regions** | Regional revenue, store treemap, full store leaderboard |
| 👥 **Customers** | Revenue per customer, top buyers, discount-band impact |
| 💳 **Returns & payments** | Payment mix pie, return rate by category, transaction sample table |

---

## 🧮 Analytics / KPI Queries

File: `analytics/kpi_queries.sql` — **14 queries** ready for reporting or notebooks.

| # | Query | Insight |
|---|-------|---------|
| 1️⃣ | Total revenue / orders / AOV / profit | Executive headline KPIs |
| 2️⃣ | Monthly revenue & profit trend | Seasonality & growth |
| 3️⃣ | Revenue & margin by category | Category profitability |
| 4️⃣ | Store performance ranking | Location leaders/laggards |
| 5️⃣ | Top 15 products | Best sellers |
| 6️⃣ | Customer segment breakdown | Who spends the most |
| 7️⃣ | Return rate by category | Quality / fit issues |
| 8️⃣ | Weekday vs weekend | Traffic patterns |
| 9️⃣ | Revenue by region | Geo performance |
| 🔟 | Payment method mix | Checkout behavior |
| 1️⃣1️⃣ | Brand performance | Brand contribution |
| 1️⃣2️⃣ | Top customers (LTV) | High-value buyers |
| 1️⃣3️⃣ | YoY monthly comparison | Year-over-year growth |
| 1️⃣4️⃣ | Discount impact bands | Promo effectiveness |

---

## 🧰 Tech Stack

| Layer | Tools |
|-------|-------|
| 🐍 Language | Python 3 |
| 📊 Data | pandas, numpy |
| 🗄️ Warehouse | SQLite |
| 🧮 Analytics | SQL |
| 🎨 Dashboard | Streamlit |
| 📉 Charts | Plotly Express + Graph Objects |
| 📁 Sources | CSV |

---

## 🔮 Future Enhancements

Ideas to grow this into a production-style portfolio piece:

| Idea | Why it’s valuable |
|------|-------------------|
| 🐘 Move warehouse to **PostgreSQL** | Closer to real enterprise stacks |
| ⏰ Orchestrate with **Airflow / Dagster** | Scheduled, reliable pipelines |
| 🧱 Add a **dbt** modeling layer | Tests, docs, versioned SQL models |
| ☁️ Deploy dashboard to **Streamlit Community Cloud** | Live demo link for resumes |
| 👥 Add **RFM / cohort retention** | Deeper customer analytics |
| 🐳 **Docker Compose** the stack | One-command local/prod-like setup |
| 🔐 Add role-based dashboard views | Manager vs analyst experiences |
| 📧 Email / Slack KPI alerts | Operational BI |

---

## 🧑‍💻 Typical workflow cheatsheet

```bash
# Refresh everything from scratch
python data/generate_raw_data.py
python etl/run_etl.py
python -m streamlit run dashboard/app.py
```

```bash
# Only refresh warehouse (raw CSVs already exist)
python etl/run_etl.py
```

```bash
# Only open dashboard (warehouse already built)
python -m streamlit run dashboard/app.py
```

---

## 📝 License & Credits

Built as a **portfolio / learning project** for end-to-end retail analytics.

- 🎨 Dashboard theme: teal · coral · amber  
- 🏗️ Modeling style: Kimball-style star schema  
- 📦 Data: fully synthetic (no real customer PII)

---

### ⭐ If this project helped you

Use it in your portfolio, extend it, and show the full pipeline story — not just the charts.

**Happy analyzing!** 📊🛍️✨
