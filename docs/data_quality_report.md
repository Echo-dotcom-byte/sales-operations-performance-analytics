# Olist Data Quality Report

## 1. Purpose

This report documents the initial quality assessment of the Brazilian E-Commerce Public Dataset by Olist before data cleaning and analytical transformation.

The assessment examines missing values, key uniqueness, categorical distributions, date ranges, and numerical characteristics.

## 2. Dataset Coverage

The dataset contains:

- 99,441 orders
- 112,650 order-item records
- 99,441 customer records
- 32,951 products
- 103,886 payment records
- 99,224 review records
- 3,095 sellers
- 1,000,163 geolocation records

The order purchase dates range from September 2016 to October 2018.

## 3. Missing Values

### Orders

| Variable | Missing Records |
|---|---:|
| order_delivered_customer_date | 2,965 |
| order_delivered_carrier_date | 1,783 |
| order_approved_at | 160 |

Missing delivery timestamps require contextual treatment because orders that were cancelled, unavailable, or not yet delivered may legitimately lack delivery dates.

### Products

| Variable | Missing Records |
|---|---:|
| product_category_name | 610 |
| product_name_lenght | 610 |
| product_description_lenght | 610 |
| product_photos_qty | 610 |
| product_weight_g | 2 |
| product_length_cm | 2 |
| product_height_cm | 2 |
| product_width_cm | 2 |

### Reviews

| Variable | Missing Records |
|---|---:|
| review_comment_title | 87,656 |
| review_comment_message | 58,247 |

Missing review text is not automatically treated as an error because customers may submit a numerical review score without providing written comments.

## 4. Key Uniqueness

- The orders dataset contains 99,441 records and 99,441 unique order IDs.
- The order-items dataset contains 112,650 records representing 98,666 unique orders.
- The customer dataset contains 99,441 customer records and 96,096 unique customer identifiers.
- The product dataset contains 32,951 records and 32,951 unique product IDs.

The difference between order-level and order-item-level record counts demonstrates that an order may contain multiple order items. Therefore, the analytical grain must be considered carefully when joining datasets.

## 5. Order Status

| Order Status | Records |
|---|---:|
| delivered | 96,478 |
| shipped | 1,107 |
| canceled | 625 |
| unavailable | 609 |
| invoiced | 314 |
| processing | 301 |
| created | 5 |
| approved | 2 |

## 6. Review Scores

| Review Score | Records |
|---:|---:|
| 1 | 11,424 |
| 2 | 3,151 |
| 3 | 8,179 |
| 4 | 19,142 |
| 5 | 57,328 |

## 7. Payment Types

| Payment Type | Records |
|---|---:|
| credit_card | 76,795 |
| boleto | 19,784 |
| voucher | 5,775 |
| debit_card | 1,529 |
| not_defined | 3 |

## 8. Numerical Characteristics

### Order Item Price

- Mean: 120.65
- Median: 74.99
- Minimum: 0.85
- Maximum: 6,735.00

### Freight Value

- Mean: 19.99
- Median: 16.26
- Minimum: 0.00
- Maximum: 409.68

The difference between mean and median suggests that price and freight distributions may be right-skewed. Further investigation will be performed during exploratory data analysis.

## 9. Initial Data Preparation Considerations

The following issues will be considered during data preparation:

1. Missing delivery timestamps will be handled according to order status and delivery eligibility.
2. Missing review comments will not automatically be treated as invalid observations.
3. Product category missing values will be investigated before deciding on treatment.
4. Multiple order items per order will be accounted for when calculating order-level metrics.
5. Multiple payment records per order will be aggregated appropriately when order-level payment metrics are required.
6. Customer analysis will distinguish customer records from unique customers using `customer_unique_id`.
7. Numerical variables such as price and freight value will be examined for extreme observations before analytical use.
## 10. Review Relationship Findings

Further investigation of the review dataset identified:

- 814 duplicated review IDs
- 789 duplicated review IDs associated with multiple orders
- 551 orders associated with multiple review records
- 202 orders containing multiple different review scores
- 0 exact duplicate review rows

Because the duplicated records are not exact duplicates, they will not be removed solely on the basis of the `review_id` field. Review records will instead be aggregated to order level for the primary analytical dataset.

The average review score and review count will be considered as order-level customer satisfaction measures.
