"""
Retail BI Dashboard — colorful multi-view analytics.
Run with: streamlit run dashboard/app.py
"""
import os
import sqlite3

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "retail_dw.db")

# Vibrant retail palette (teal / coral / amber / navy — not purple-default)
PALETTE = ["#0D9488", "#F97316", "#E11D48", "#2563EB", "#CA8A04", "#7C3AED", "#059669", "#DB2777"]
COLOR_SEQ = px.colors.qualitative.Bold

st.set_page_config(
    page_title="RetailPulse BI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: linear-gradient(165deg, #F0FDFA 0%, #FFF7ED 42%, #FEF2F2 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #134E4A 0%, #0F766E 55%, #115E59 100%);
    }
    [data-testid="stSidebar"] * {
        color: #ECFDF5 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label {
        color: #A7F3D0 !important;
        font-weight: 600;
    }

    .hero-title {
        font-family: 'Fraunces', Georgia, serif;
        font-size: 2.4rem;
        font-weight: 700;
        color: #134E4A;
        margin-bottom: 0.15rem;
        letter-spacing: -0.02em;
    }
    .hero-sub {
        color: #57534E;
        font-size: 1.05rem;
        margin-bottom: 1.25rem;
    }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1.25rem;
    }
    @media (max-width: 900px) {
        .kpi-grid { grid-template-columns: 1fr; }
    }
    .kpi-card {
        border-radius: 18px;
        padding: 1.1rem 1.25rem;
        color: white;
        box-shadow: 0 10px 28px rgba(15, 118, 110, 0.18);
        border: 1px solid rgba(255,255,255,0.25);
    }
    .kpi-card h3 {
        margin: 0;
        font-size: 0.82rem;
        font-weight: 600;
        opacity: 0.92;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .kpi-card p {
        margin: 0.35rem 0 0;
        font-family: 'Fraunces', Georgia, serif;
        font-size: 1.75rem;
        font-weight: 700;
    }
    .kpi-card span {
        display: block;
        margin-top: 0.25rem;
        font-size: 0.8rem;
        opacity: 0.88;
    }
    .kpi-teal { background: linear-gradient(135deg, #0D9488, #14B8A6); }
    .kpi-coral { background: linear-gradient(135deg, #E11D48, #FB7185); }
    .kpi-amber { background: linear-gradient(135deg, #D97706, #FBBF24); }
    .kpi-blue { background: linear-gradient(135deg, #2563EB, #60A5FA); }
    .kpi-violet { background: linear-gradient(135deg, #7C3AED, #A78BFA); }
    .kpi-green { background: linear-gradient(135deg, #059669, #34D399); }

    .section-label {
        font-family: 'Fraunces', Georgia, serif;
        color: #134E4A;
        font-size: 1.35rem;
        font-weight: 700;
        margin: 0.5rem 0 0.75rem;
    }

    div[data-testid="stTabs"] button {
        font-weight: 600;
        color: #0F766E;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def apply_chart_theme(fig, title=None):
    fig.update_layout(
        title=dict(text=title or fig.layout.title.text, font=dict(size=16, color="#134E4A", family="Fraunces")),
        paper_bgcolor="rgba(255,255,255,0.55)",
        plot_bgcolor="rgba(255,255,255,0.35)",
        font=dict(family="DM Sans", color="#44403C"),
        margin=dict(l=40, r=20, t=55, b=40),
        legend=dict(bgcolor="rgba(255,255,255,0.5)"),
    )
    fig.update_xaxes(gridcolor="rgba(20, 184, 166, 0.15)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(20, 184, 166, 0.15)", zeroline=False)
    return fig


@st.cache_data(show_spinner="Loading warehouse…")
def load_data():
    conn = sqlite3.connect(DB_PATH)
    fact = pd.read_sql("SELECT * FROM fact_sales", conn)
    dim_date = pd.read_sql("SELECT * FROM dim_date", conn)
    dim_product = pd.read_sql("SELECT * FROM dim_product", conn)
    dim_store = pd.read_sql("SELECT * FROM dim_store", conn)
    dim_customer = pd.read_sql("SELECT * FROM dim_customer", conn)
    conn.close()

    df = (
        fact.merge(dim_date, on="date_key")
        .merge(dim_product, on="product_id")
        .merge(dim_store, on="store_id")
        .merge(dim_customer, on="customer_id")
    )
    df["full_date"] = pd.to_datetime(df["full_date"])
    df["year_month"] = df["full_date"].dt.to_period("M").astype(str)
    return df


df_all = load_data()
df_sales = df_all[df_all["is_return"] == 0].copy()

st.markdown('<p class="hero-title">RetailPulse BI</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Interactive analytics on a star-schema warehouse — '
    f"{len(df_sales):,} sale lines · {df_sales['product_id'].nunique()} products · "
    f"{df_sales['store_id'].nunique()} stores · {df_sales['customer_id'].nunique():,} customers</p>",
    unsafe_allow_html=True,
)

# --- Sidebar filters ---
st.sidebar.markdown("### Filters")
date_min, date_max = df_sales["full_date"].min(), df_sales["full_date"].max()
date_range = st.sidebar.date_input(
    "Date range",
    (date_min.date(), date_max.date()),
    min_value=date_min.date(),
    max_value=date_max.date(),
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_d, end_d = date_range
else:
    start_d, end_d = date_min.date(), date_max.date()

regions = st.sidebar.multiselect(
    "Region", sorted(df_sales["region"].unique()), default=sorted(df_sales["region"].unique())
)
stores = st.sidebar.multiselect(
    "Stores", sorted(df_sales["store_name"].unique()), default=sorted(df_sales["store_name"].unique())
)
categories = st.sidebar.multiselect(
    "Categories", sorted(df_sales["category"].unique()), default=sorted(df_sales["category"].unique())
)
segments = st.sidebar.multiselect(
    "Customer segment", sorted(df_sales["segment"].unique()), default=sorted(df_sales["segment"].unique())
)

mask = (
    (df_sales["full_date"] >= pd.to_datetime(start_d))
    & (df_sales["full_date"] <= pd.to_datetime(end_d))
    & (df_sales["region"].isin(regions))
    & (df_sales["store_name"].isin(stores))
    & (df_sales["category"].isin(categories))
    & (df_sales["segment"].isin(segments))
)
fdf = df_sales[mask]

returns_mask = (
    (df_all["is_return"] == 1)
    & (df_all["full_date"] >= pd.to_datetime(start_d))
    & (df_all["full_date"] <= pd.to_datetime(end_d))
    & (df_all["region"].isin(regions))
    & (df_all["store_name"].isin(stores))
    & (df_all["category"].isin(categories))
)
rdf = df_all[returns_mask]

# Prior period for deltas
span_days = max((pd.to_datetime(end_d) - pd.to_datetime(start_d)).days, 1)
prev_end = pd.to_datetime(start_d) - pd.Timedelta(days=1)
prev_start = prev_end - pd.Timedelta(days=span_days)
prev = df_sales[
    (df_sales["full_date"] >= prev_start)
    & (df_sales["full_date"] <= prev_end)
    & (df_sales["region"].isin(regions))
    & (df_sales["store_name"].isin(stores))
    & (df_sales["category"].isin(categories))
    & (df_sales["segment"].isin(segments))
]

revenue = fdf["net_revenue"].sum()
orders = fdf["order_id"].nunique()
aov = revenue / max(orders, 1)
units = fdf["quantity"].sum()
profit = fdf["gross_profit"].sum()
margin = 100 * profit / revenue if revenue else 0
customers_n = fdf["customer_id"].nunique()

prev_rev = prev["net_revenue"].sum()
prev_orders = prev["order_id"].nunique()
rev_delta = ((revenue - prev_rev) / prev_rev * 100) if prev_rev else 0
ord_delta = ((orders - prev_orders) / prev_orders * 100) if prev_orders else 0


def delta_label(pct):
    arrow = "▲" if pct >= 0 else "▼"
    return f"{arrow} {abs(pct):.1f}% vs prior period"


st.markdown(
    f"""
    <div class="kpi-grid">
      <div class="kpi-card kpi-teal"><h3>Total revenue</h3><p>${revenue:,.0f}</p><span>{delta_label(rev_delta)}</span></div>
      <div class="kpi-card kpi-coral"><h3>Orders</h3><p>{orders:,}</p><span>{delta_label(ord_delta)}</span></div>
      <div class="kpi-card kpi-amber"><h3>Avg order value</h3><p>${aov:,.2f}</p><span>{customers_n:,} customers</span></div>
      <div class="kpi-card kpi-blue"><h3>Units sold</h3><p>{units:,}</p><span>{fdf['product_id'].nunique()} SKUs</span></div>
      <div class="kpi-card kpi-violet"><h3>Gross profit</h3><p>${profit:,.0f}</p><span>{margin:.1f}% margin</span></div>
      <div class="kpi-card kpi-green"><h3>Return lines</h3><p>{len(rdf):,}</p><span>{100 * len(rdf) / max(len(fdf) + len(rdf), 1):.2f}% of lines</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_overview, tab_trends, tab_products, tab_stores, tab_customers, tab_ops = st.tabs(
    ["Overview", "Trends", "Products & brands", "Stores & regions", "Customers", "Returns & payments"]
)

with tab_overview:
    st.markdown('<p class="section-label">Performance snapshot</p>', unsafe_allow_html=True)
    c1, c2 = st.columns([1.4, 1])

    with c1:
        daily = fdf.groupby("full_date", as_index=False)["net_revenue"].sum()
        fig = px.area(
            daily, x="full_date", y="net_revenue",
            color_discrete_sequence=["#0D9488"],
        )
        fig.update_traces(fill="tozeroy", line=dict(width=2.5))
        st.plotly_chart(apply_chart_theme(fig, "Daily revenue"), use_container_width=True)

    with c2:
        cat = (
            fdf.groupby("category", as_index=False)["net_revenue"]
            .sum()
            .sort_values("net_revenue", ascending=False)
        )
        fig = px.pie(
            cat, names="category", values="net_revenue",
            hole=0.55, color_discrete_sequence=PALETTE,
        )
        fig.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(apply_chart_theme(fig, "Revenue mix by category"), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        store = (
            fdf.groupby("store_name", as_index=False)["net_revenue"]
            .sum()
            .sort_values("net_revenue", ascending=True)
            .tail(10)
        )
        fig = px.bar(
            store, x="net_revenue", y="store_name", orientation="h",
            color="net_revenue", color_continuous_scale=["#99F6E4", "#0F766E"],
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(apply_chart_theme(fig, "Top stores by revenue"), use_container_width=True)

    with c4:
        seg = fdf.groupby("segment", as_index=False).agg(
            revenue=("net_revenue", "sum"),
            customers=("customer_id", "nunique"),
        )
        fig = px.bar(
            seg, x="segment", y="revenue", color="segment",
            color_discrete_sequence=PALETTE, text_auto=".2s",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(apply_chart_theme(fig, "Revenue by customer segment"), use_container_width=True)

with tab_trends:
    st.markdown('<p class="section-label">Time-series deep dive</p>', unsafe_allow_html=True)
    monthly = (
        fdf.groupby(["year", "month", "month_name", "year_month"], as_index=False)
        .agg(revenue=("net_revenue", "sum"), profit=("gross_profit", "sum"), orders=("order_id", "nunique"))
        .sort_values("year_month")
    )
    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly["year_month"], y=monthly["revenue"], name="Revenue", marker_color="#0D9488"))
    fig.add_trace(go.Scatter(
        x=monthly["year_month"], y=monthly["profit"], name="Gross profit",
        mode="lines+markers", line=dict(color="#E11D48", width=3),
    ))
    st.plotly_chart(apply_chart_theme(fig, "Monthly revenue vs gross profit"), use_container_width=True)

    t1, t2 = st.columns(2)
    with t1:
        dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow = fdf.groupby("day_of_week", as_index=False)["net_revenue"].sum()
        dow["day_of_week"] = pd.Categorical(dow["day_of_week"], categories=dow_order, ordered=True)
        dow = dow.sort_values("day_of_week")
        fig = px.bar(
            dow, x="day_of_week", y="net_revenue",
            color="net_revenue", color_continuous_scale=["#FED7AA", "#EA580C"],
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(apply_chart_theme(fig, "Revenue by day of week"), use_container_width=True)

    with t2:
        heat = (
            fdf.groupby(["month_name", "day_of_week"], as_index=False)["net_revenue"]
            .sum()
        )
        month_order = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ]
        pivot = heat.pivot(index="day_of_week", columns="month_name", values="net_revenue")
        pivot = pivot.reindex(index=dow_order, columns=[m for m in month_order if m in pivot.columns])
        fig = px.imshow(
            pivot, color_continuous_scale="Teal", aspect="auto",
            labels=dict(color="Revenue"),
        )
        st.plotly_chart(apply_chart_theme(fig, "Revenue heatmap (weekday × month)"), use_container_width=True)

    # YoY if multiple years
    years = sorted(fdf["year"].unique())
    if len(years) >= 2:
        yoy = fdf.groupby(["month", "month_name", "year"], as_index=False)["net_revenue"].sum()
        fig = px.line(
            yoy.sort_values(["year", "month"]),
            x="month_name", y="net_revenue", color="year",
            markers=True, color_discrete_sequence=PALETTE,
            category_orders={"month_name": month_order},
        )
        st.plotly_chart(apply_chart_theme(fig, "Year-over-year monthly revenue"), use_container_width=True)

with tab_products:
    st.markdown('<p class="section-label">Catalog performance</p>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)

    with p1:
        top = (
            fdf.groupby(["product_name", "category"], as_index=False)["net_revenue"]
            .sum()
            .sort_values("net_revenue", ascending=False)
            .head(15)
        )
        fig = px.bar(
            top.sort_values("net_revenue"),
            x="net_revenue", y="product_name", color="category",
            orientation="h", color_discrete_sequence=PALETTE,
        )
        st.plotly_chart(apply_chart_theme(fig, "Top 15 products"), use_container_width=True)

    with p2:
        brand = (
            fdf.groupby("brand", as_index=False)
            .agg(revenue=("net_revenue", "sum"), profit=("gross_profit", "sum"))
            .sort_values("revenue", ascending=False)
            .head(12)
        )
        fig = px.scatter(
            brand, x="revenue", y="profit", size="revenue", color="brand",
            color_discrete_sequence=PALETTE, hover_name="brand",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(apply_chart_theme(fig, "Brand: revenue vs profit"), use_container_width=True)

    sun = (
        fdf.groupby(["category", "subcategory"], as_index=False)["net_revenue"]
        .sum()
    )
    fig = px.sunburst(
        sun, path=["category", "subcategory"], values="net_revenue",
        color="net_revenue", color_continuous_scale="Tealgrn",
    )
    st.plotly_chart(apply_chart_theme(fig, "Category → subcategory sunburst"), use_container_width=True)

    margin_tbl = (
        fdf.groupby("category", as_index=False)
        .agg(
            revenue=("net_revenue", "sum"),
            profit=("gross_profit", "sum"),
            units=("quantity", "sum"),
            avg_discount=("discount_pct", "mean"),
        )
    )
    margin_tbl["margin_pct"] = (100 * margin_tbl["profit"] / margin_tbl["revenue"]).round(1)
    margin_tbl["avg_discount"] = (margin_tbl["avg_discount"] * 100).round(1)
    margin_tbl = margin_tbl.sort_values("revenue", ascending=False)
    st.dataframe(
        margin_tbl.rename(columns={
            "category": "Category", "revenue": "Revenue", "profit": "Gross profit",
            "units": "Units", "avg_discount": "Avg discount %", "margin_pct": "Margin %",
        }),
        use_container_width=True,
        hide_index=True,
    )

with tab_stores:
    st.markdown('<p class="section-label">Store & regional performance</p>', unsafe_allow_html=True)
    s1, s2 = st.columns(2)

    with s1:
        region = (
            fdf.groupby("region", as_index=False)
            .agg(revenue=("net_revenue", "sum"), orders=("order_id", "nunique"))
            .sort_values("revenue", ascending=False)
        )
        fig = px.bar(
            region, x="region", y="revenue", color="region",
            color_discrete_sequence=PALETTE, text_auto=".2s",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(apply_chart_theme(fig, "Revenue by region"), use_container_width=True)

    with s2:
        store_perf = (
            fdf.groupby(["store_name", "city", "region"], as_index=False)
            .agg(
                revenue=("net_revenue", "sum"),
                profit=("gross_profit", "sum"),
                orders=("order_id", "nunique"),
            )
        )
        fig = px.treemap(
            store_perf, path=["region", "store_name"], values="revenue",
            color="profit", color_continuous_scale="RdYlGn",
        )
        st.plotly_chart(apply_chart_theme(fig, "Store treemap (size=revenue, color=profit)"), use_container_width=True)

    store_tbl = store_perf.sort_values("revenue", ascending=False)
    store_tbl["aov"] = (store_tbl["revenue"] / store_tbl["orders"]).round(2)
    st.dataframe(
        store_tbl.rename(columns={
            "store_name": "Store", "city": "City", "region": "Region",
            "revenue": "Revenue", "profit": "Profit", "orders": "Orders", "aov": "AOV",
        }),
        use_container_width=True,
        hide_index=True,
    )

with tab_customers:
    st.markdown('<p class="section-label">Customer intelligence</p>', unsafe_allow_html=True)
    cu1, cu2 = st.columns(2)

    with cu1:
        seg_detail = (
            fdf.groupby("segment", as_index=False)
            .agg(
                customers=("customer_id", "nunique"),
                revenue=("net_revenue", "sum"),
                orders=("order_id", "nunique"),
            )
        )
        seg_detail["rev_per_customer"] = (seg_detail["revenue"] / seg_detail["customers"]).round(2)
        fig = px.bar(
            seg_detail, x="segment", y="rev_per_customer", color="segment",
            color_discrete_sequence=PALETTE, text_auto=".2s",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(apply_chart_theme(fig, "Revenue per customer by segment"), use_container_width=True)

    with cu2:
        top_cust = (
            fdf.groupby(["customer_name", "segment"], as_index=False)
            .agg(lifetime_revenue=("net_revenue", "sum"), orders=("order_id", "nunique"))
            .sort_values("lifetime_revenue", ascending=False)
            .head(12)
        )
        fig = px.bar(
            top_cust.sort_values("lifetime_revenue"),
            x="lifetime_revenue", y="customer_name", color="segment",
            orientation="h", color_discrete_sequence=PALETTE,
        )
        st.plotly_chart(apply_chart_theme(fig, "Top 12 customers"), use_container_width=True)

    disc = fdf.copy()
    disc["discount_band"] = pd.cut(
        disc["discount_pct"],
        bins=[-0.01, 0, 0.10, 0.20, 1],
        labels=["No discount", "1–10%", "11–20%", "21%+"],
    )
    disc_agg = disc.groupby("discount_band", observed=True, as_index=False).agg(
        lines=("order_id", "count"),
        revenue=("net_revenue", "sum"),
    )
    fig = px.bar(
        disc_agg, x="discount_band", y="revenue", color="discount_band",
        color_discrete_sequence=["#0D9488", "#2563EB", "#F97316", "#E11D48"],
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(apply_chart_theme(fig, "Revenue by discount band"), use_container_width=True)

with tab_ops:
    st.markdown('<p class="section-label">Returns & payment mix</p>', unsafe_allow_html=True)
    o1, o2 = st.columns(2)

    with o1:
        pay = (
            fdf.groupby("payment_method", as_index=False)["net_revenue"]
            .sum()
            .sort_values("net_revenue", ascending=False)
        )
        fig = px.pie(
            pay, names="payment_method", values="net_revenue",
            hole=0.45, color_discrete_sequence=PALETTE,
        )
        st.plotly_chart(apply_chart_theme(fig, "Payment method mix"), use_container_width=True)

    with o2:
        if len(rdf) and len(fdf):
            ret_cat = (
                pd.concat([
                    fdf.assign(_kind="sales"),
                    rdf.assign(_kind="returns"),
                ])
                .groupby(["category", "_kind"], as_index=False)
                .size()
            )
            # Return rate by category
            sales_lines = fdf.groupby("category").size()
            ret_lines = rdf.groupby("category").size()
            rate = pd.DataFrame({
                "category": sales_lines.index,
                "return_rate_pct": (100 * ret_lines.reindex(sales_lines.index).fillna(0) / (sales_lines + ret_lines.reindex(sales_lines.index).fillna(0))).values,
            }).sort_values("return_rate_pct", ascending=False)
            fig = px.bar(
                rate, x="category", y="return_rate_pct",
                color="return_rate_pct", color_continuous_scale=["#FEF3C7", "#DC2626"],
            )
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(apply_chart_theme(fig, "Return rate % by category"), use_container_width=True)
        else:
            st.info("No returns in the current filter selection.")

    st.markdown('<p class="section-label">Filtered transaction sample</p>', unsafe_allow_html=True)
    sample = (
        fdf[["full_date", "store_name", "region", "product_name", "category", "brand",
             "customer_name", "segment", "payment_method", "quantity", "discount_pct",
             "net_revenue", "gross_profit"]]
        .sort_values("full_date", ascending=False)
        .head(500)
    )
    sample["discount_pct"] = (sample["discount_pct"] * 100).round(0).astype(int)
    st.dataframe(sample, use_container_width=True, hide_index=True)

st.caption("RetailPulse BI · star-schema SQLite warehouse · Python ETL · Streamlit + Plotly")
