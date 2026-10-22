
from pathlib import Path

import numpy as np
import pandas as pd

# Use a fixed random seed so results stay consistent.
rng = np.random.default_rng(42)

# Find the project folder and create the data folder.
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

regions = {
    "Northeast": ["New York", "Boston", "Philadelphia"],
    "South": ["Houston", "Dallas", "Atlanta"],
    "Midwest": ["Chicago", "Detroit", "Minneapolis"],
    "West": ["Los Angeles", "Seattle", "Denver"],
}

products = [
    ("Laptop", "Technology", 850, 1250),
    ("Monitor", "Technology", 150, 350),
    ("Keyboard", "Accessories", 25, 90),
    ("Mouse", "Accessories", 15, 60),
    ("Office Chair", "Furniture", 120, 320),
    ("Desk", "Furniture", 180, 500),
    ("Headphones", "Accessories", 40, 180),
    ("Printer", "Technology", 100, 300),
]

segments = ["Consumer", "Corporate", "Small Business"]
channels = ["Online", "Retail Store", "Partner"]
payment_methods = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer"]

n_orders = 2000

dates = pd.to_datetime(
    rng.choice(
        pd.date_range("2024-01-01", "2025-12-31", freq="D"),
        size=n_orders,
    )
)

rows = []

for i in range(n_orders):
    region = rng.choice(list(regions.keys()))
    city = rng.choice(regions[region])

    product, category, min_price, max_price = products[
        int(rng.integers(0, len(products)))
    ]

    quantity = int(rng.integers(1, 9))
    unit_price = round(float(rng.uniform(min_price, max_price)), 2)

    discount = float(
        rng.choice(
            [0, 0.05, 0.10, 0.15, 0.20],
            p=[0.30, 0.20, 0.25, 0.15, 0.10],
        )
    )

    gross_sales = quantity * unit_price
    revenue = round(gross_sales * (1 - discount), 2)

    cost_rate = float(rng.uniform(0.55, 0.78))
    cost = round(gross_sales * cost_rate, 2)
    profit = round(revenue - cost, 2)

    rows.append({
        "OrderID": f"ORD-{i + 1:05d}",
        "OrderDate": dates[i],
        "CustomerID": f"CUST-{int(rng.integers(1, 401)):04d}",
        "Region": region,
        "City": city,
        "Segment": rng.choice(
            segments, p=[0.55, 0.25, 0.20]
        ),
        "Product": product,
        "Category": category,
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "Discount": discount,
        "Revenue": revenue,
        "Cost": cost,
        "Profit": profit,
        "Channel": rng.choice(channels),
        "PaymentMethod": rng.choice(payment_methods),
    })

df = pd.DataFrame(rows)
df = df.sort_values("OrderDate").reset_index(drop=True)

output_file = DATA_DIR / "sales_data.csv"
df.to_csv(output_file, index=False, date_format="%Y-%m-%d")

print("\nDATASET CREATED SUCCESSFULLY")
print("-" * 40)
print(f"File: {output_file}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Date range: {df['OrderDate'].min().date()} to "
      f"{df['OrderDate'].max().date()}")
print(f"Total revenue: ${df['Revenue'].sum():,.2f}")
print(f"Total cost: ${df['Cost'].sum():,.2f}")
print(f"Total profit: ${df['Profit'].sum():,.2f}")

print("\nFirst five orders:")
print(df.head().to_string(index=False))

print("\nMissing values:")
print(df.isnull().sum().to_string())
