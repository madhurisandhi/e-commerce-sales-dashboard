-- ────────────────────────────────────────────────────
-- E-Commerce Sales Performance — SQL Queries
-- Author: Madhuri Sandhi
-- ────────────────────────────────────────────────────


-- 1. Total revenue, profit and orders by category
SELECT
    category,
    COUNT(DISTINCT order_id)                          AS total_orders,
    SUM(sales)                                        AS total_revenue,
    SUM(profit)                                       AS total_profit,
    ROUND(SUM(profit) / SUM(sales) * 100, 2)          AS profit_margin_pct,
    ROUND(AVG(sales), 2)                              AS avg_order_value
FROM sales
GROUP BY category
ORDER BY total_revenue DESC;


-- 2. Monthly revenue trend
SELECT
    YEAR(order_date)                                  AS year,
    MONTH(order_date)                                 AS month,
    DATENAME(MONTH, order_date)                       AS month_name,
    SUM(sales)                                        AS monthly_revenue,
    SUM(profit)                                       AS monthly_profit,
    COUNT(DISTINCT order_id)                          AS order_count
FROM sales
GROUP BY YEAR(order_date), MONTH(order_date), DATENAME(MONTH, order_date)
ORDER BY year, month;


-- 3. Top 10 products by revenue
SELECT TOP 10
    product_name,
    category,
    SUM(sales)                                        AS total_revenue,
    SUM(quantity)                                     AS units_sold,
    ROUND(AVG(profit / NULLIF(sales, 0)) * 100, 2)   AS avg_margin_pct
FROM sales
GROUP BY product_name, category
ORDER BY total_revenue DESC;


-- 4. Regional performance by quarter
SELECT
    region,
    CONCAT(YEAR(order_date), ' Q', DATEPART(QUARTER, order_date))  AS quarter,
    SUM(sales)                                                      AS revenue,
    SUM(profit)                                                     AS profit,
    COUNT(DISTINCT customer_id)                                     AS unique_customers
FROM sales
GROUP BY region, YEAR(order_date), DATEPART(QUARTER, order_date)
ORDER BY region, quarter;


-- 5. Customer lifetime value (CLV) ranking
SELECT
    customer_id,
    customer_name,
    segment,
    COUNT(DISTINCT order_id)        AS total_orders,
    SUM(sales)                      AS total_spend,
    ROUND(AVG(sales), 2)            AS avg_order_value,
    MIN(order_date)                 AS first_order,
    MAX(order_date)                 AS last_order,
    DATEDIFF(DAY, MIN(order_date), MAX(order_date))  AS customer_tenure_days
FROM sales
GROUP BY customer_id, customer_name, segment
ORDER BY total_spend DESC;


-- 6. Cohort retention — customers who ordered in month 1 and returned in later months
WITH first_order AS (
    SELECT
        customer_id,
        MIN(DATEFROMPARTS(YEAR(order_date), MONTH(order_date), 1))  AS cohort_month
    FROM sales
    GROUP BY customer_id
),
monthly_activity AS (
    SELECT
        s.customer_id,
        f.cohort_month,
        DATEFROMPARTS(YEAR(s.order_date), MONTH(s.order_date), 1)   AS activity_month,
        DATEDIFF(MONTH, f.cohort_month,
            DATEFROMPARTS(YEAR(s.order_date), MONTH(s.order_date), 1))  AS months_since_first
    FROM sales s
    JOIN first_order f ON s.customer_id = f.customer_id
)
SELECT
    cohort_month,
    months_since_first,
    COUNT(DISTINCT customer_id)   AS active_customers
FROM monthly_activity
GROUP BY cohort_month, months_since_first
ORDER BY cohort_month, months_since_first;


-- 7. Discount impact on profit margin
SELECT
    CASE
        WHEN discount = 0       THEN 'No Discount'
        WHEN discount <= 0.1    THEN '1–10%'
        WHEN discount <= 0.2    THEN '11–20%'
        ELSE '21%+'
    END                                            AS discount_bucket,
    COUNT(*)                                       AS order_count,
    ROUND(AVG(sales), 2)                           AS avg_sales,
    ROUND(AVG(profit), 2)                          AS avg_profit,
    ROUND(AVG(profit / NULLIF(sales, 0)) * 100, 2) AS avg_margin_pct
FROM sales
GROUP BY
    CASE
        WHEN discount = 0       THEN 'No Discount'
        WHEN discount <= 0.1    THEN '1–10%'
        WHEN discount <= 0.2    THEN '11–20%'
        ELSE '21%+'
    END
ORDER BY avg_margin_pct DESC;
