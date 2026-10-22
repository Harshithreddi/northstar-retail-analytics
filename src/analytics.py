
import pandas as pd


def calculate_kpis(df):
    """
    Calculate the main business KPIs from the sales dataset.
    """
    total_revenue = df["Revenue"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["OrderID"].nunique()

    if total_revenue != 0:
        profit_margin = (total_profit / total_revenue) * 100
    else:
        profit_margin = 0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "total_orders": int(total_orders),
        "profit_margin": round(profit_margin, 2),
    }


def revenue_by_region(df):
    """
    Summarize revenue, profit, and order count by region.
    """
    result = (
        df.groupby("Region", as_index=False)
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("OrderID", "nunique"),
        )
        .sort_values("Revenue", ascending=False)
        .reset_index(drop=True)
    )

    result["Revenue"] = result["Revenue"].round(2)
    result["Profit"] = result["Profit"].round(2)

    return result


def profit_by_product(df):
    """
    Summarize revenue and profit by product.
    """
    result = (
        df.groupby("Product", as_index=False)
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("OrderID", "nunique"),
        )
        .sort_values("Profit", ascending=False)
        .reset_index(drop=True)
    )

    result["Revenue"] = result["Revenue"].round(2)
    result["Profit"] = result["Profit"].round(2)

    return result


def monthly_revenue(df):
    """
    Calculate total revenue and profit for each month.
    """
    work = df.copy()

    work["OrderDate"] = pd.to_datetime(
        work["OrderDate"], errors="coerce"
    )

    work = work.dropna(subset=["OrderDate"])

    work["Month"] = (
        work["OrderDate"]
        .dt.to_period("M")
        .astype(str)
    )

    result = (
        work.groupby("Month", as_index=False)
        .agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("OrderID", "nunique"),
        )
        .sort_values("Month")
        .reset_index(drop=True)
    )

    result["Revenue"] = result["Revenue"].round(2)
    result["Profit"] = result["Profit"].round(2)

    return result


def detect_revenue_anomalies(df, multiplier=1.5):
    """
    Flag unusually low or high revenue within each product group.

    Uses the interquartile range (IQR) method separately for each
    product so that products with different price ranges are compared
    more fairly.

    Statistical flags require business review; they do not prove errors.
    """
    work = df.copy()

    work["Revenue"] = pd.to_numeric(
        work["Revenue"], errors="coerce"
    )

    work["AnomalyReason"] = ""

    if "Product" not in work.columns:
        work["Product"] = "All products"

    for product, indexes in work.groupby(
        "Product", dropna=False
    ).groups.items():

        values = work.loc[indexes, "Revenue"].dropna()

        # Avoid calculating thresholds from very small groups.
        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - multiplier * iqr
        upper_bound = q3 + multiplier * iqr

        low = work.loc[indexes, "Revenue"] < lower_bound
        high = work.loc[indexes, "Revenue"] > upper_bound

        low_indexes = low[low].index
        high_indexes = high[high].index

        work.loc[low_indexes, "AnomalyReason"] = (
            "Unusually low revenue for this product"
        )

        work.loc[high_indexes, "AnomalyReason"] = (
            "Unusually high revenue for this product"
        )

    anomalies = work[
        work["AnomalyReason"] != ""
    ].copy()

    return (
        anomalies
        .sort_values("Revenue", ascending=False)
        .reset_index(drop=True)
    )
