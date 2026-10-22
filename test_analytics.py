
import pandas as pd

from src.analytics import (
    calculate_kpis,
    revenue_by_region,
    profit_by_product,
    monthly_revenue,
    detect_revenue_anomalies,
)

df = pd.read_csv("data/sales_data.csv")

print("\n--- DATASET ---")
print("Rows and columns:", df.shape)

print("\n--- KPIs ---")
print(calculate_kpis(df))

print("\n--- REVENUE BY REGION ---")
print(revenue_by_region(df).to_string(index=False))

print("\n--- TOP 5 PRODUCTS BY PROFIT ---")
print(profit_by_product(df).head(5).to_string(index=False))

print("\n--- MONTHLY REVENUE ---")
print(monthly_revenue(df).to_string(index=False))

print("\n--- REVENUE ANOMALIES ---")
anomalies = detect_revenue_anomalies(df)
print("Flagged orders:", len(anomalies))

columns = [
    col for col in [
        "OrderID",
        "OrderDate",
        "Region",
        "Product",
        "Revenue",
        "Profit",
        "AnomalyReason",
    ]
    if col in anomalies.columns
]

print(anomalies[columns].head(20).to_string(index=False))
print("\nAnalytics tests completed.")
