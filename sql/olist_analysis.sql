-- REF 01 — Monthly Sales and Order Trend
-- Table: order_level

SELECT
    purchase_year_month AS month,
    COUNT(order_id) AS order_count,
    ROUND(SUM(total_product_value), 2) AS product_value,
    ROUND(SUM(total_freight_value), 2) AS freight_value,
    ROUND(SUM(total_order_value), 2) AS total_order_value
FROM order_level
GROUP BY purchase_year_month
ORDER BY purchase_year_month;


-- REF 02 — Top Product Categories by Product Value
-- Table: order_item_level

SELECT
    product_category_name_english AS product_category,
    COUNT(order_item_id) AS item_count,
    ROUND(SUM(price), 2) AS product_value,
    ROUND(SUM(freight_value), 2) AS freight_value
FROM order_item_level
WHERE product_category_name_english IS NOT NULL
GROUP BY product_category_name_english
ORDER BY product_value DESC
LIMIT 10;


-- REF 03 — Delivery Performance Analysis
-- Table: order_level

SELECT
    delivery_performance,
    COUNT(order_id) AS order_count,
    ROUND(AVG(delivery_days), 2) AS average_delivery_days,
    ROUND(AVG(delivery_delay_days), 2) AS average_delivery_delay_days
FROM order_level
GROUP BY delivery_performance
ORDER BY order_count DESC;


-- REF 04 — Delivery Performance vs Customer Review Score
-- Table: order_level

SELECT
    delivery_performance,
    COUNT(order_id) AS order_count,
    ROUND(AVG(average_review_score), 2) AS average_review_score
FROM order_level
WHERE average_review_score IS NOT NULL
GROUP BY delivery_performance
ORDER BY average_review_score DESC;


-- REF 05 — Order Status Distribution
-- Table: order_level

SELECT
    order_status,
    COUNT(order_id) AS order_count,
    ROUND(
        COUNT(order_id) * 100.0 /
        (SELECT COUNT(*) FROM order_level),
        2
    ) AS percentage_of_orders
FROM order_level
GROUP BY order_status
ORDER BY order_count DESC;


-- REF 06 — Payment Value by Payment Type/Group
-- Table: order_level

SELECT
    payment_types AS payment_type_group,
    ROUND(SUM(payment_value), 2) AS total_payment_value,
    SUM(payment_record_count) AS payment_record_count
FROM order_level
WHERE payment_types IS NOT NULL
GROUP BY payment_types
ORDER BY total_payment_value DESC;


-- REF 07 — Customer Orders by State
-- Table: order_level

SELECT
    customer_state,
    COUNT(order_id) AS order_count,
    ROUND(
        COUNT(order_id) * 100.0 /
        (SELECT COUNT(*) FROM order_level),
        2
    ) AS percentage_of_orders
FROM order_level
WHERE customer_state IS NOT NULL
GROUP BY customer_state
ORDER BY order_count DESC;


-- REF 08 — Customer Order Frequency
-- Table: order_level

WITH customer_orders AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS orders_per_customer
    FROM order_level
    WHERE customer_unique_id IS NOT NULL
    GROUP BY customer_unique_id
)

SELECT
    orders_per_customer,
    COUNT(*) AS customer_count
FROM customer_orders
GROUP BY orders_per_customer
ORDER BY orders_per_customer;


-- REF 09 — Freight Cost by Product Category
-- Table: order_item_level

SELECT
    product_category_name_english AS product_category,
    COUNT(order_item_id) AS item_count,
    ROUND(AVG(price), 2) AS average_product_price,
    ROUND(AVG(freight_value), 2) AS average_freight_value,
    ROUND(
        AVG(
            CASE
                WHEN price > 0
                THEN freight_value * 100.0 / price
            END
        ),
        2
    ) AS average_freight_percentage
FROM order_item_level
WHERE product_category_name_english IS NOT NULL
GROUP BY product_category_name_english
HAVING COUNT(order_item_id) >= 100
ORDER BY average_freight_percentage DESC;


-- REF 10 — Order Characteristics vs Customer Review Score
-- Table: order_level

SELECT
    average_review_score AS review_score,
    COUNT(order_id) AS order_count,
    ROUND(AVG(total_product_value), 2) AS average_product_value,
    ROUND(AVG(total_freight_value), 2) AS average_freight_value,
    ROUND(AVG(total_order_value), 2) AS average_order_value,
    ROUND(AVG(item_count), 2) AS average_item_count,
    ROUND(AVG(product_count), 2) AS average_product_count
FROM order_level
WHERE average_review_score IS NOT NULL
GROUP BY average_review_score
ORDER BY review_score;