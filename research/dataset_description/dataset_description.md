# Dataset Description - Working Notes

## Dataset

Brazilian E-Commerce Public Dataset by Olist.

## Nature of Data

Real-world, anonymized e-commerce transaction data.

## Observation Period

September 2016 to October 2018 based on order purchase timestamps.

## Main Tables

The dataset contains information relating to:

- Orders
- Order items
- Customers
- Products
- Payments
- Reviews
- Sellers
- Geolocation
- Product category translations

## Scale

The orders dataset contains 99,441 records.

The order-items dataset contains 112,650 records.

The customer dataset contains 99,441 records representing 96,096 unique customers.

## Analytical Structure

The dataset is relational rather than a single flat table. Order-level, order-item-level, customer-level, product-level, payment-level, and review-level information must be distinguished during analysis.

## Initial Data Quality

The initial profile identified missing delivery timestamps, missing product attributes, missing product categories, and missing review text. These will be evaluated according to their analytical meaning rather than automatically treated as errors.

## Research Relevance

The dataset supports analysis of sales performance, product categories, customer behavior, payment characteristics, freight values, delivery performance, and customer satisfaction through review scores.
