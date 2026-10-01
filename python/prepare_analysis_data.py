import os
import pandas as pd

# ============================================================
# Olist E-Commerce Dataset
# Analysis-Ready Data Preparation
# ============================================================

RAW_DIR = os.path.expanduser("~/Documents/Olist_Temp")
OUTPUT_DIR = "data/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading Olist datasets...")

# ------------------------------------------------------------
# 1. Load raw datasets
# ------------------------------------------------------------

orders = pd.read_csv(
    os.path.join(RAW_DIR, "olist_orders_dataset.csv")
)

order_items = pd.read_csv(
    os.path.join(RAW_DIR, "olist_order_items_dataset.csv")
)

customers = pd.read_csv(
    os.path.join(RAW_DIR, "olist_customers_dataset.csv")
)

products = pd.read_csv(
    os.path.join(RAW_DIR, "olist_products_dataset.csv")
)

payments = pd.read_csv(
    os.path.join(RAW_DIR, "olist_order_payments_dataset.csv")
)

reviews = pd.read_csv(
    os.path.join(RAW_DIR, "olist_order_reviews_dataset.csv")
)

sellers = pd.read_csv(
    os.path.join(RAW_DIR, "olist_sellers_dataset.csv")
)

category_translation = pd.read_csv(
    os.path.join(RAW_DIR, "product_category_name_translation.csv")
)

print("All datasets loaded successfully.")


# ------------------------------------------------------------
# 2. Convert date columns
# ------------------------------------------------------------

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(orders[column], errors="coerce")


# ------------------------------------------------------------
# 3. Prepare order-item-level dataset
#    Grain: 1 row = 1 order item
# ------------------------------------------------------------

item_data = order_items.copy()

# Add product information
item_data = item_data.merge(
    products,
    on="product_id",
    how="left"
)

# Add English product category names
item_data = item_data.merge(
    category_translation,
    on="product_category_name",
    how="left"
)

# Add seller information
item_data = item_data.merge(
    sellers,
    on="seller_id",
    how="left"
)

# Add order dates/status
order_columns = [
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

item_data = item_data.merge(
    orders[order_columns],
    on="order_id",
    how="left"
)

# Add customer information
customer_columns = [
    "customer_id",
    "customer_unique_id",
    "customer_city",
    "customer_state"
]

item_data = item_data.merge(
    customers[customer_columns],
    on="customer_id",
    how="left"
)

# Save item-level dataset
item_output = os.path.join(
    OUTPUT_DIR,
    "olist_order_item_analysis.csv"
)

item_data.to_csv(
    item_output,
    index=False
)

print(
    f"Order-item dataset created: "
    f"{len(item_data):,} rows"
)


# ------------------------------------------------------------
# 4. Aggregate order items to order level
#    Grain: 1 row = 1 order
# ------------------------------------------------------------

item_summary = (
    order_items
    .groupby("order_id")
    .agg(
        total_product_value=("price", "sum"),
        total_freight_value=("freight_value", "sum"),
        item_count=("order_item_id", "count"),
        product_count=("product_id", "nunique"),
        seller_count=("seller_id", "nunique")
    )
    .reset_index()
)

item_summary["total_order_value"] = (
    item_summary["total_product_value"]
    + item_summary["total_freight_value"]
)


# ------------------------------------------------------------
# 5. Aggregate payment information
# ------------------------------------------------------------

payment_summary = (
    payments
    .groupby("order_id")
    .agg(
        payment_value=("payment_value", "sum"),
        payment_record_count=("payment_sequential", "count"),
        payment_type_count=("payment_type", "nunique"),
        max_installments=("payment_installments", "max")
    )
    .reset_index()
)

# Store payment types used in each order
payment_types = (
    payments
    .groupby("order_id")["payment_type"]
    .apply(lambda x: ", ".join(sorted(x.dropna().unique())))
    .reset_index(name="payment_types")
)

payment_summary = payment_summary.merge(
    payment_types,
    on="order_id",
    how="left"
)


# ------------------------------------------------------------
# 6. Aggregate review information
# ------------------------------------------------------------

review_summary = (
    reviews
    .groupby("order_id")
    .agg(
        review_count=("review_score", "count"),
        average_review_score=("review_score", "mean")
    )
    .reset_index()
)


# ------------------------------------------------------------
# 7. Add customer information to orders
# ------------------------------------------------------------

order_level = orders.merge(
    customers[
        [
            "customer_id",
            "customer_unique_id",
            "customer_city",
            "customer_state"
        ]
    ],
    on="customer_id",
    how="left"
)


# ------------------------------------------------------------
# 8. Add item, payment and review summaries
# ------------------------------------------------------------

order_level = order_level.merge(
    item_summary,
    on="order_id",
    how="left"
)

order_level = order_level.merge(
    payment_summary,
    on="order_id",
    how="left"
)

order_level = order_level.merge(
    review_summary,
    on="order_id",
    how="left"
)


# ------------------------------------------------------------
# 9. Calculate operational/delivery metrics
# ------------------------------------------------------------

order_level["delivery_days"] = (
    order_level["order_delivered_customer_date"]
    - order_level["order_purchase_timestamp"]
).dt.total_seconds() / (24 * 60 * 60)

order_level["estimated_delivery_days"] = (
    order_level["order_estimated_delivery_date"]
    - order_level["order_purchase_timestamp"]
).dt.total_seconds() / (24 * 60 * 60)

order_level["delivery_delay_days"] = (
    order_level["order_delivered_customer_date"]
    - order_level["order_estimated_delivery_date"]
).dt.total_seconds() / (24 * 60 * 60)

order_level["approval_delay_hours"] = (
    order_level["order_approved_at"]
    - order_level["order_purchase_timestamp"]
).dt.total_seconds() / (60 * 60)

order_level["carrier_delivery_days"] = (
    order_level["order_delivered_carrier_date"]
    - order_level["order_purchase_timestamp"]
).dt.total_seconds() / (24 * 60 * 60)


# ------------------------------------------------------------
# 10. Create delivery performance classification
# ------------------------------------------------------------

def classify_delivery(row):
    if pd.isna(row["order_delivered_customer_date"]):
        return "Not Delivered"

    delay = row["delivery_delay_days"]

    if delay < 0:
        return "Early"
    elif delay == 0:
        return "On Time"
    else:
        return "Late"


order_level["delivery_performance"] = order_level.apply(
    classify_delivery,
    axis=1
)


# ------------------------------------------------------------
# 11. Customer-level order frequency
# ------------------------------------------------------------

customer_order_count = (
    orders
    .groupby("customer_id")["order_id"]
    .nunique()
    .reset_index(name="customer_order_count")
)

order_level = order_level.merge(
    customer_order_count,
    on="customer_id",
    how="left"
)


# ------------------------------------------------------------
# 12. Final column organization
# ------------------------------------------------------------

order_columns_final = [
    "order_id",
    "customer_id",
    "customer_unique_id",
    "customer_city",
    "customer_state",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",

    "total_product_value",
    "total_freight_value",
    "total_order_value",
    "item_count",
    "product_count",
    "seller_count",

    "payment_value",
    "payment_record_count",
    "payment_type_count",
    "payment_types",
    "max_installments",

    "review_count",
    "average_review_score",

    "delivery_days",
    "estimated_delivery_days",
    "delivery_delay_days",
    "approval_delay_hours",
    "carrier_delivery_days",
    "delivery_performance",

    "customer_order_count"
]

# Keep only columns that exist
order_columns_final = [
    column
    for column in order_columns_final
    if column in order_level.columns
]

order_level = order_level[order_columns_final]


# ------------------------------------------------------------
# 13. Save order-level dataset
# ------------------------------------------------------------

order_output = os.path.join(
    OUTPUT_DIR,
    "olist_order_level_analysis.csv"
)

order_level.to_csv(
    order_output,
    index=False
)

print(
    f"Order-level dataset created: "
    f"{len(order_level):,} rows"
)


# ------------------------------------------------------------
# 14. Validation checks
# ------------------------------------------------------------

print("\n========== VALIDATION ==========")

print(
    "Original orders:",
    f"{len(orders):,}"
)

print(
    "Processed order-level rows:",
    f"{len(order_level):,}"
)

print(
    "Original order items:",
    f"{len(order_items):,}"
)

print(
    "Processed order-item rows:",
    f"{len(item_data):,}"
)

print(
    "Unique order IDs in order-level dataset:",
    f"{order_level['order_id'].nunique():,}"
)

print(
    "Unique order IDs in item-level dataset:",
    f"{item_data['order_id'].nunique():,}"
)

print(
    "Orders without item-level records:",
    f"{order_level['total_product_value'].isna().sum():,}"
)

print(
    "Orders with reviews:",
    f"{order_level['review_count'].notna().sum():,}"
)

print(
    "Orders with payment records:",
    f"{order_level['payment_value'].notna().sum():,}"
)

print("\nOutput files:")
print(item_output)
print(order_output)

print("\nAnalysis data preparation completed successfully.")
