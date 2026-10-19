-- E-commerce Sales Analytics SQL practice
-- Dialect: SQLite-compatible SQL

-- 1. Overall KPIs
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2) AS profit_margin_pct
FROM sales_data;

-- 2. Monthly revenue and profit
SELECT
    substr(order_date, 1, 7) AS sales_month,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit
FROM sales_data
GROUP BY substr(order_date, 1, 7)
ORDER BY sales_month;

-- 3. Category performance
SELECT
    category,
    COUNT(DISTINCT order_id) AS orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(revenue), 0), 2) AS profit_margin_pct
FROM sales_data
GROUP BY category
ORDER BY revenue DESC;

-- 4. Region-wise profit
SELECT region, ROUND(SUM(profit), 2) AS total_profit
FROM sales_data
GROUP BY region
ORDER BY total_profit DESC;

-- 5. Sales channel contribution
SELECT
    sales_channel,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(100.0 * SUM(revenue) / (SELECT SUM(revenue) FROM sales_data), 2) AS revenue_share_pct
FROM sales_data
GROUP BY sales_channel
ORDER BY revenue DESC;

-- 6. Products with high revenue but below-average profit margin
WITH product_metrics AS (
    SELECT
        product,
        category,
        SUM(revenue) AS revenue,
        SUM(profit) AS profit,
        100.0 * SUM(profit) / NULLIF(SUM(revenue), 0) AS margin_pct
    FROM sales_data
    GROUP BY product, category
),
overall_margin AS (
    SELECT 100.0 * SUM(profit) / NULLIF(SUM(revenue), 0) AS avg_margin_pct
    FROM sales_data
)
SELECT p.product, p.category, ROUND(p.revenue, 2) AS revenue,
       ROUND(p.profit, 2) AS profit, ROUND(p.margin_pct, 2) AS margin_pct
FROM product_metrics p
CROSS JOIN overall_margin o
WHERE p.margin_pct < o.avg_margin_pct
ORDER BY p.revenue DESC;

-- 7. Rank categories by revenue within each region (window function)
WITH region_category AS (
    SELECT region, category, SUM(revenue) AS revenue
    FROM sales_data
    GROUP BY region, category
)
SELECT region, category, ROUND(revenue, 2) AS revenue,
       DENSE_RANK() OVER (PARTITION BY region ORDER BY revenue DESC) AS revenue_rank
FROM region_category
ORDER BY region, revenue_rank;

-- 8. Month-over-month revenue change using LAG
WITH monthly AS (
    SELECT substr(order_date, 1, 7) AS sales_month, SUM(revenue) AS revenue
    FROM sales_data
    GROUP BY substr(order_date, 1, 7)
),
with_previous AS (
    SELECT sales_month, revenue,
           LAG(revenue) OVER (ORDER BY sales_month) AS previous_month_revenue
    FROM monthly
)
SELECT sales_month,
       ROUND(revenue, 2) AS revenue,
       ROUND(previous_month_revenue, 2) AS previous_month_revenue,
       ROUND(100.0 * (revenue - previous_month_revenue) /
             NULLIF(previous_month_revenue, 0), 2) AS mom_growth_pct
FROM with_previous
ORDER BY sales_month;
