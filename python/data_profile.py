import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PATH TO RAW OLIST DATA
# --------------------------------------------------

DATA_PATH = Path.home() / "Documents" / "Olist_Temp"


# --------------------------------------------------
# DATASET FILES
# --------------------------------------------------

files = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}


# --------------------------------------------------
# LOAD DATASETS
# --------------------------------------------------

data = {}

for name, filename in files.items():
    print(f"Loading {filename}...")
    data[name] = pd.read_csv(DATA_PATH / filename)


# --------------------------------------------------
# MISSING VALUES
# --------------------------------------------------

print("\n" + "=" * 70)
print("DATA QUALITY PROFILE - MISSING VALUES")
print("=" * 70)

for name, df in data.items():

    print(f"\n{name.upper()}")
    print("-" * 50)

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if len(missing) == 0:
        print("No missing values")
    else:
        print(missing.sort_values(ascending=False))


# --------------------------------------------------
# KEY COUNTS
# --------------------------------------------------

print("\n" + "=" * 70)
print("KEY COUNTS")
print("=" * 70)

orders = data["orders"]
order_items = data["order_items"]
customers = data["customers"]
products = data["products"]

print(f"\nOrders: {len(orders):,}")
print(f"Unique order IDs: {orders['order_id'].nunique():,}")

print(f"\nOrder items: {len(order_items):,}")
print(
    f"Unique order IDs in order items: "
    f"{order_items['order_id'].nunique():,}"
)

print(f"\nCustomers: {len(customers):,}")
print(
    f"Unique customer IDs: "
    f"{customers['customer_id'].nunique():,}"
)

print(
    f"Unique customer IDs (unique customer): "
    f"{customers['customer_unique_id'].nunique():,}"
)

print(f"\nProducts: {len(products):,}")
print(
    f"Unique product IDs: "
    f"{products['product_id'].nunique():,}"
)


# --------------------------------------------------
# ORDER STATUS
# --------------------------------------------------

print("\n" + "=" * 70)
print("ORDER STATUS")
print("=" * 70)

print(orders["order_status"].value_counts())


# --------------------------------------------------
# ORDER DATE RANGE
# --------------------------------------------------

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

print("\n" + "=" * 70)
print("ORDER DATE RANGE")
print("=" * 70)

print("Earliest:", orders["order_purchase_timestamp"].min())
print("Latest:", orders["order_purchase_timestamp"].max())


# --------------------------------------------------
# REVIEW SCORES
# --------------------------------------------------

reviews = data["reviews"]

print("\n" + "=" * 70)
print("REVIEW SCORES")
print("=" * 70)

print(
    reviews["review_score"]
    .value_counts()
    .sort_index()
)


# --------------------------------------------------
# PAYMENT TYPES
# --------------------------------------------------

payments = data["payments"]

print("\n" + "=" * 70)
print("PAYMENT TYPES")
print("=" * 70)

print(
    payments["payment_type"]
    .value_counts()
)


# --------------------------------------------------
# PRODUCT CATEGORIES
# --------------------------------------------------

print("\n" + "=" * 70)
print("TOP PRODUCT CATEGORIES")
print("=" * 70)

print(
    products["product_category_name"]
    .value_counts(dropna=False)
    .head(20)
)


# --------------------------------------------------
# ORDER ITEM NUMERICAL SUMMARY
# --------------------------------------------------

print("\n" + "=" * 70)
print("ORDER ITEM NUMERICAL SUMMARY")
print("=" * 70)

print(
    order_items[
        ["price", "freight_value"]
    ].describe()
)


# --------------------------------------------------
# COMPLETE
# --------------------------------------------------

print("\n" + "=" * 70)
print("PROFILE COMPLETE")
print("=" * 70)
