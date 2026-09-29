# Olist Dataset Dictionary

## Dataset Overview

The project uses the Brazilian E-Commerce Public Dataset by Olist, a real and anonymized e-commerce dataset containing approximately 100,000 orders from Olist's marketplace operations between 2016 and 2018.

The dataset consists of multiple relational tables covering orders, customers, products, sellers, payments, reviews, and geographic information.

## Dataset Inventory

| Dataset | Rows | Columns | Key Field | Purpose | Planned Use |
|---|---:|---:|---|---|---|
| olist_orders_dataset | 99,441 | 8 | order_id | Order lifecycle and timestamps | Core |
| olist_order_items_dataset | 112,650 | 7 | order_id + order_item_id | Products, sellers, price and freight | Core |
| olist_customers_dataset | 99,441 | 5 | customer_id | Customer identity and location | Core |
| olist_products_dataset | 32,951 | 9 | product_id | Product characteristics and category | Core |
| olist_order_payments_dataset | 103,886 | 5 | order_id + payment_sequential | Payment information | Core |
| olist_order_reviews_dataset | 99,224 | 7 | review_id / order_id | Customer review and satisfaction | Core |
| olist_sellers_dataset | 3,095 | 4 | seller_id | Seller identity and location | Supporting |
| olist_geolocation_dataset | 1,000,163 | 5 | geolocation_zip_code_prefix | Geographic coordinates | Supporting |
| product_category_name_translation | 71 | 2 | product_category_name | Portuguese-to-English category translation | Supporting |

## Important Data Structure Observations

- The dataset contains 99,441 orders and 112,650 order-item records.
- A single order can contain multiple order items.
- Order-level and order-item-level data must therefore be distinguished during analysis.
- `customer_id` identifies a customer record associated with an order, while `customer_unique_id` can be used to identify unique customers across orders.
- Payment data may contain multiple payment records for the same order.
- The geolocation dataset contains more than one million records and will not initially be loaded into Excel unless required for a specific analysis.

## Planned Analytical Areas

- Sales and order trends
- Product and category performance
- Customer purchasing behavior
- Payment methods and payment value
- Delivery performance
- Delivery delays
- Customer review scores
- Geographic patterns
- Freight cost analysis

## Analytical Grain

The primary analytical dataset will use one row per order.

A secondary order-item-level dataset will be retained for product, category, freight, and seller analysis.

One-to-many tables such as payments and reviews will be aggregated to order level before joining with the primary analytical dataset to prevent duplicate order records.
