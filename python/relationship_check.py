import pandas as pd
from pathlib import Path

DATA_PATH = Path.home() / "Documents" / "Olist_Temp"

orders = pd.read_csv(DATA_PATH / "olist_orders_dataset.csv")
order_items = pd.read_csv(DATA_PATH / "olist_order_items_dataset.csv")
payments = pd.read_csv(DATA_PATH / "olist_order_payments_dataset.csv")
reviews = pd.read_csv(DATA_PATH / "olist_order_reviews_dataset.csv")
customers = pd.read_csv(DATA_PATH / "olist_customers_dataset.csv")
products = pd.read_csv(DATA_PATH / "olist_products_dataset.csv")
sellers = pd.read_csv(DATA_PATH / "olist_sellers_dataset.csv")

print("=" * 70)
print("RELATIONSHIP CHECK")
print("=" * 70)

# Orders → Order Items
print("\nOrders missing from Order Items:")
print(
    len(
        set(orders["order_id"])
        - set(order_items["order_id"])
    )
)

# Order Items → Orders
print("\nOrder Items with no matching Order:")
print(
    len(
        set(order_items["order_id"])
        - set(orders["order_id"])
    )
)

# Orders → Customers
print("\nOrders with no matching Customer:")
print(
    len(
        set(orders["customer_id"])
        - set(customers["customer_id"])
    )
)

# Order Items → Products
print("\nOrder Items with no matching Product:")
print(
    len(
        set(order_items["product_id"])
        - set(products["product_id"])
    )
)

# Order Items → Sellers
print("\nOrder Items with no matching Seller:")
print(
    len(
        set(order_items["seller_id"])
        - set(sellers["seller_id"])
    )
)

# Multiple payments per order
payment_counts = payments.groupby("order_id").size()

print("\nOrders with multiple payment records:")
print((payment_counts > 1).sum())

# Multiple reviews per order
review_counts = reviews.groupby("order_id").size()

print("\nOrders with multiple review records:")
print((review_counts > 1).sum())

print("\n" + "=" * 70)
print("RELATIONSHIP CHECK COMPLETE")
print("=" * 70)

# --------------------------------------------------
# ORDERS WITHOUT ORDER ITEMS
# --------------------------------------------------

orders_without_items = orders[
    ~orders["order_id"].isin(order_items["order_id"])
]

print("\n" + "=" * 70)
print("ORDERS WITHOUT ORDER ITEMS - STATUS")
print("=" * 70)

print(
    orders_without_items["order_status"]
    .value_counts()
)

print("\nNumber of orders without items:")
print(len(orders_without_items))

# --------------------------------------------------
# MULTIPLE PAYMENT RECORDS
# --------------------------------------------------

print("\n" + "=" * 70)
print("PAYMENT RECORD ANALYSIS")
print("=" * 70)

print(
    payment_counts.value_counts()
    .sort_index()
    .head(10)
)

# --------------------------------------------------
# MULTIPLE REVIEW RECORDS
# --------------------------------------------------

print("\n" + "=" * 70)
print("REVIEW RECORD ANALYSIS")
print("=" * 70)

print(
    review_counts.value_counts()
    .sort_index()
    .head(10)
)

# --------------------------------------------------
# REVIEW ID DUPLICATES
# --------------------------------------------------

print("\nDuplicate review IDs:")
print(
    reviews["review_id"].duplicated().sum()
)

print("\nDuplicate order IDs in reviews:")
print(
    reviews["order_id"].duplicated().sum()
)
# --------------------------------------------------
# REVIEW DUPLICATE INVESTIGATION
# --------------------------------------------------

print("\n" + "=" * 70)
print("REVIEW DUPLICATE INVESTIGATION")
print("=" * 70)

# Rows where review_id is duplicated
duplicate_review_rows = reviews[
    reviews["review_id"].duplicated(keep=False)
].sort_values("review_id")

print("\nRows with duplicated review IDs:")
print(len(duplicate_review_rows))

print("\nSample duplicated review IDs:")
print(
    duplicate_review_rows[
        [
            "review_id",
            "order_id",
            "review_score",
            "review_creation_date",
            "review_answer_timestamp"
        ]
    ].head(20).to_string(index=False)
)

# Check whether duplicate review IDs have different order IDs
review_id_order_counts = (
    reviews.groupby("review_id")["order_id"]
    .nunique()
)

print("\nDuplicated review IDs linked to multiple orders:")
print(
    (review_id_order_counts > 1).sum()
)

# Check whether duplicate order IDs have different review scores
order_review_score_counts = (
    reviews.groupby("order_id")["review_score"]
    .nunique()
)

print("\nOrders with multiple different review scores:")
print(
    (order_review_score_counts > 1).sum()
)

# Exact duplicate rows
print("\nExact duplicate review rows:")
print(
    reviews.duplicated().sum()
)
