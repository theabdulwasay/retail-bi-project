-- Reusable KPI queries against retail_dw.db
-- Run with: sqlite3 database/retail_dw.db < analytics/kpi_queries.sql

-- 1. Total net revenue, orders, AOV, gross profit
SELECT
    ROUND(SUM(net_revenue), 2) AS total_net_revenue,
    COUNT(DISTINCT order_id)   AS total_orders,
    ROUND(SUM(net_revenue) * 1.0 / COUNT(DISTINCT order_id), 2) AS avg_order_value,
    ROUND(SUM(gross_profit), 2) AS total_gross_profit,
    ROUND(100.0 * SUM(gross_profit) / NULLIF(SUM(net_revenue), 0), 1) AS gross_margin_pct
FROM fact_sales
WHERE is_return = 0;

-- 2. Monthly revenue and profit trend
SELECT
    d.year, d.month, d.month_name,
    ROUND(SUM(f.net_revenue), 2) AS monthly_revenue,
    ROUND(SUM(f.gross_profit), 2) AS monthly_profit,
    COUNT(DISTINCT f.order_id) AS orders
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE f.is_return = 0
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 3. Revenue and margin by product category
SELECT
    p.category,
    ROUND(SUM(f.net_revenue), 2) AS revenue,
    ROUND(SUM(f.gross_profit), 2) AS gross_profit,
    ROUND(AVG(p.margin_pct), 1)  AS avg_list_margin_pct,
    SUM(f.quantity)              AS units_sold
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
WHERE f.is_return = 0
GROUP BY p.category
ORDER BY revenue DESC;

-- 4. Store performance ranking
SELECT
    s.store_name, s.city, s.region,
    ROUND(SUM(f.net_revenue), 2) AS revenue,
    ROUND(SUM(f.gross_profit), 2) AS gross_profit,
    COUNT(DISTINCT f.order_id)   AS orders
FROM fact_sales f
JOIN dim_store s ON f.store_id = s.store_id
WHERE f.is_return = 0
GROUP BY s.store_id
ORDER BY revenue DESC;

-- 5. Top 15 products by revenue
SELECT
    p.product_name, p.category, p.brand,
    ROUND(SUM(f.net_revenue), 2) AS revenue,
    SUM(f.quantity)              AS units_sold
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
WHERE f.is_return = 0
GROUP BY p.product_id
ORDER BY revenue DESC
LIMIT 15;

-- 6. Customer segment breakdown
SELECT
    c.segment,
    COUNT(DISTINCT c.customer_id) AS customers,
    ROUND(SUM(f.net_revenue), 2) AS revenue,
    ROUND(SUM(f.net_revenue) / COUNT(DISTINCT c.customer_id), 2) AS revenue_per_customer
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
WHERE f.is_return = 0
GROUP BY c.segment
ORDER BY revenue DESC;

-- 7. Return rate by category
SELECT
    p.category,
    SUM(CASE WHEN f.is_return = 1 THEN 1 ELSE 0 END) AS return_lines,
    COUNT(*) AS total_lines,
    ROUND(100.0 * SUM(CASE WHEN f.is_return = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS return_rate_pct
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.category
ORDER BY return_rate_pct DESC;

-- 8. Weekday vs weekend revenue
SELECT
    CASE WHEN d.is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS day_type,
    ROUND(SUM(f.net_revenue), 2) AS revenue,
    ROUND(AVG(f.net_revenue), 2) AS avg_line_revenue,
    COUNT(DISTINCT f.order_id) AS orders
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE f.is_return = 0
GROUP BY d.is_weekend;

-- 9. Revenue by region
SELECT
    s.region,
    ROUND(SUM(f.net_revenue), 2) AS revenue,
    COUNT(DISTINCT f.order_id) AS orders,
    COUNT(DISTINCT s.store_id) AS stores
FROM fact_sales f
JOIN dim_store s ON f.store_id = s.store_id
WHERE f.is_return = 0
GROUP BY s.region
ORDER BY revenue DESC;

-- 10. Payment method mix
SELECT
    payment_method,
    COUNT(*) AS line_items,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(net_revenue), 2) AS revenue,
    ROUND(100.0 * SUM(net_revenue) / (SELECT SUM(net_revenue) FROM fact_sales WHERE is_return = 0), 1) AS revenue_share_pct
FROM fact_sales
WHERE is_return = 0
GROUP BY payment_method
ORDER BY revenue DESC;

-- 11. Brand performance
SELECT
    p.brand, p.category,
    ROUND(SUM(f.net_revenue), 2) AS revenue,
    ROUND(SUM(f.gross_profit), 2) AS gross_profit,
    SUM(f.quantity) AS units_sold
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
WHERE f.is_return = 0
GROUP BY p.brand, p.category
ORDER BY revenue DESC
LIMIT 20;

-- 12. Top customers by lifetime revenue
SELECT
    c.customer_name, c.segment,
    COUNT(DISTINCT f.order_id) AS orders,
    ROUND(SUM(f.net_revenue), 2) AS lifetime_revenue
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
WHERE f.is_return = 0
GROUP BY c.customer_id
ORDER BY lifetime_revenue DESC
LIMIT 20;

-- 13. YoY monthly comparison (when 2+ years present)
SELECT
    d.month, d.month_name,
    d.year,
    ROUND(SUM(f.net_revenue), 2) AS revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE f.is_return = 0
GROUP BY d.year, d.month
ORDER BY d.month, d.year;

-- 14. Discount impact
SELECT
    CASE
        WHEN discount_pct = 0 THEN 'No discount'
        WHEN discount_pct <= 0.10 THEN '1-10%'
        WHEN discount_pct <= 0.20 THEN '11-20%'
        ELSE '21%+'
    END AS discount_band,
    COUNT(*) AS lines,
    ROUND(SUM(net_revenue), 2) AS revenue,
    ROUND(AVG(net_revenue), 2) AS avg_line_revenue
FROM fact_sales
WHERE is_return = 0
GROUP BY discount_band
ORDER BY MIN(discount_pct);
