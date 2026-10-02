# Sales & Operations Performance Analytics

An end-to-end data analytics project using the **Olist Brazilian E-Commerce Public Dataset** to analyze sales performance, product categories, customer behavior, payment patterns, delivery operations, freight, geography, and customer satisfaction.

The project demonstrates a complete analytics workflow covering **data quality assessment, data preparation, analytical data modeling, Python EDA, SQL analysis, Excel analysis, statistical analysis, and Tableau visualization**.

The project also provides the analytical foundation for an MSc IT research study examining associations between operational factors and customer satisfaction.

---

## 📌 Project Overview

E-commerce operations generate data across multiple areas such as orders, products, customers, payments, sellers, delivery, and reviews. These datasets operate at different levels of detail, making data modeling and careful aggregation important before performing analysis.

This project brings these datasets together into structured analytical datasets and examines the resulting information from both **sales and operational perspectives**.

The analysis focuses on questions such as:

- How do sales and order volumes change over time?
- Which product categories contribute the most product value?
- How does freight vary across product categories?
- What does the order fulfillment and delivery performance look like?
- How are delivery performance and customer review scores associated?
- What payment methods and payment patterns are observed?
- How frequently do customers place orders?
- How are customers distributed geographically?
- What operational patterns can be identified from the data?

---

## 🎯 Project Objectives

The project aims to:

1. Analyze sales and order patterns across the available observation period.
2. Examine product and product-category performance using price and freight information.
3. Evaluate order fulfillment and delivery performance using order status and delivery timestamps.
4. Analyze customer satisfaction using review scores.
5. Examine payment methods, installments, and payment values.
6. Investigate customer purchasing behavior and order frequency.
7. Examine geographic patterns in customer activity.
8. Identify useful sales and operational patterns for e-commerce analysis.

---

## 📊 Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**.

The dataset contains multiple related datasets covering:

- Orders
- Order items
- Customers
- Products
- Payments
- Reviews
- Sellers
- Geolocation
- Product category translations

### Dataset Coverage

| Dataset Component | Records |
|---|---:|
| Orders | 99,441 |
| Order Items | 112,650 |
| Customer Records | 99,441 |
| Unique Customers | 96,096 |
| Products | 32,951 |
| Payments | 103,886 |
| Reviews | 99,224 |
| Sellers | 3,095 |
| Geolocation Records | 1,000,163 |

The order purchase dates range from **September 2016 to October 2018**.

The original raw Olist dataset is **not redistributed in this repository**. The processed analytical datasets used by the project are included under `data/processed/`.

---

# 🔄 Project Workflow

```text
Olist Public Dataset
        │
        ▼
Data Quality Assessment
        │
        ▼
Data Preparation & Cleaning
        │
        ▼
Analytical Data Modeling
        │
        ├───────────────┐
        ▼               ▼
Order-Level        Order-Item-Level
Dataset             Dataset
        │               │
        ├───────┬───────┴───────┐
        ▼       ▼               ▼
     Python    SQL            Excel
        │       │               │
        └───────┴───────┬───────┘
                        ▼
                    Tableau
                        │
                        ▼
              Insights & Findings
                        │
                        ▼
               Research Application

