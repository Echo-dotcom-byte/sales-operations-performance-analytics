# Olist Data Model and Analytical Grain

## 1. Purpose

The Olist dataset is relational and contains information at multiple levels, including orders, order items, customers, products, payments, sellers, and reviews.

Because different tables operate at different levels of detail, the analysis must account for data grain before joining tables.

## 2. Primary Analytical Grain

The primary research dataset will use:

> One row = one order

This order-level dataset is appropriate for analyzing delivery performance, order characteristics, payment behavior, and customer satisfaction.

## 3. Secondary Analytical Grain

A secondary order-item-level dataset will be retained for:

- Product analysis
- Product-category analysis
- Item-level price analysis
- Freight analysis
- Seller analysis

For this dataset:

> One row = one product item within an order.

## 4. Major Relationships

### Orders → Order Items

One order can contain multiple order items.

Therefore, order-level attributes must not be summed after joining directly to order-item records.

### Orders → Payments

An order may contain multiple payment records.

Payment records will therefore be aggregated to order level before being joined to the primary analytical dataset.

Planned order-level payment measures include:

- Total payment value
- Number of payment records
- Payment method information
- Installment information where appropriate

### Orders → Reviews

An order may contain multiple review records.

The review data will therefore be aggregated to order level before being joined to the primary analytical dataset.

Planned order-level review measures include:

- Review count
- Average review score

Where multiple review scores exist for an order, the underlying review records will be retained and the aggregation method will be documented.

### Orders → Customers

Orders are connected to customers through `customer_id`.

`customer_unique_id` will be used when identifying unique customers and repeat purchasing behavior.

### Order Items → Products

Order items are connected to products through `product_id`.

Product category information will be obtained from the product table and translated into English where required using the category translation table.

### Order Items → Sellers

Order items are connected to sellers through `seller_id`.

Seller information may be used for seller-level or geographic analysis.

## 5. Orders Without Order Items

The initial data-quality assessment identified 775 orders without corresponding order-item records.

Their order statuses were:

- unavailable: 603
- canceled: 164
- created: 5
- invoiced: 2
- shipped: 1

These orders will remain in the order-level dataset for order-status and operational analysis but will not contribute item-derived sales metrics where no order-item records exist.

## 6. Review Data Considerations

The raw review dataset contains duplicate review identifiers and multiple reviews associated with some orders.

The initial investigation identified:

- 814 duplicated review IDs
- 551 orders with multiple review records
- 202 orders with multiple different review scores
- 0 exact duplicate review rows

Therefore, duplicate review records will not be removed solely on the basis of `review_id`. Review information will instead be aggregated at order level for the primary research dataset.

## 7. Data Integration Principle

One-to-many relationships will be aggregated before joining to the order-level analytical dataset to prevent unintended duplication and inflation of order-level metrics.
