
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------
# 1. Page configuration
# -----------------------------
st.set_page_config(
    page_title="Northstar BI + AI Assistant",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Northstar BI + AI Data Assistant")
st.caption(
    "Explore sales performance with interactive analytics "
    "and a data-grounded business assistant."
)

# -----------------------------
# 2. Load the shared dataset
# -----------------------------
DATA_FILE = Path(__file__).resolve().parent / "data" / "sales_data.csv"


@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path, parse_dates=["OrderDate"])

    required_columns = {
        "OrderID", "OrderDate", "Region", "Product",
        "Category", "Revenue", "Cost", "Profit", "Quantity",
    }

    missing = required_columns - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    return data


try:
    df = load_data(DATA_FILE)
except FileNotFoundError:
    st.error(f"Dataset not found: {DATA_FILE}")
    st.info("Make sure data/sales_data.csv exists in your project folder.")
    st.stop()
except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()

# -----------------------------
# 3. Sidebar filters
# -----------------------------
st.sidebar.header("Dashboard Filters")

regions = sorted(df["Region"].dropna().unique())
selected_regions = st.sidebar.multiselect(
    "Region",
    options=regions,
    default=regions,
)

categories = sorted(df["Category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Category",
    options=categories,
    default=categories,
)

min_date = df["OrderDate"].min().date()
max_date = df["OrderDate"].max().date()

selected_dates = st.sidebar.date_input(
    "Order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

filtered = df[
    df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
].copy()

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered = filtered[
        filtered["OrderDate"].dt.date.between(start_date, end_date)
    ]

if filtered.empty:
    st.warning("No orders match these filters. Please change the selections.")
    st.stop()

# -----------------------------
# 4. Dashboard KPIs
# -----------------------------
total_revenue = filtered["Revenue"].sum()
total_profit = filtered["Profit"].sum()
total_orders = filtered["OrderID"].nunique()
profit_margin = total_profit / total_revenue if total_revenue else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${total_revenue:,.2f}")
c2.metric("Total Profit", f"${total_profit:,.2f}")
c3.metric("Total Orders", f"{total_orders:,}")
c4.metric("Profit Margin", f"{profit_margin:.1%}")

# -----------------------------
# 5. Tabs
# -----------------------------
dashboard_tab, assistant_tab, data_tab = st.tabs(
    ["📈 Dashboard", "🤖 Business Assistant", "📋 Data Explorer"]
)

with dashboard_tab:
    left, right = st.columns(2)

    monthly = (
        filtered.assign(Month=filtered["OrderDate"].dt.to_period("M").dt.to_timestamp())
        .groupby("Month", as_index=False)
        .agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"))
        .sort_values("Month")
    )

    with left:
        fig = px.line(
            monthly,
            x="Month",
            y="Revenue",
            markers=True,
            title="Monthly Revenue",
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        region_sales = (
            filtered.groupby("Region", as_index=False)["Revenue"]
            .sum()
            .sort_values("Revenue", ascending=False)
        )
        fig = px.bar(
            region_sales,
            x="Region",
            y="Revenue",
            title="Revenue by Region",
        )
        st.plotly_chart(fig, use_container_width=True)

    product_sales = (
        filtered.groupby("Product", as_index=False)
        .agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"))
        .sort_values("Revenue", ascending=False)
    )
    fig = px.bar(
        product_sales,
        x="Product",
        y="Revenue",
        color="Profit",
        title="Product Performance",
    )
    st.plotly_chart(fig, use_container_width=True)

with assistant_tab:
    st.subheader("Ask a business question")
    st.write(
        "Try: Which region generated the most revenue? "
        "Which product is most profitable? "
        "Show monthly revenue. "
        "Find unusual orders."
    )

    def answer_question(question, data):
        q = question.lower().strip()

        if not q:
            return "Please enter a question.", None

        if any(word in q for word in ["anomal", "unusual", "outlier", "abnormal"]):
            q1 = data["Revenue"].quantile(0.25)
            q3 = data["Revenue"].quantile(0.75)
            iqr = q3 - q1
            unusual = data[
                (data["Revenue"] < q1 - 1.5 * iqr)
                | (data["Revenue"] > q3 + 1.5 * iqr)
            ].sort_values("Revenue", ascending=False)

            if unusual.empty:
                return "No revenue outliers were detected using the IQR rule.", None

            return (
                f"Detected {len(unusual)} unusual orders using the "
                "interquartile-range (IQR) rule. These are candidates "
                "for review, not confirmed business problems.",
                unusual[
                    ["OrderID", "OrderDate", "Region", "Product", "Revenue", "Profit"]
                ],
            )

        if "region" in q and any(
            word in q for word in ["revenue", "sales", "highest", "top", "best"]
        ):
            result = (
                data.groupby("Region", as_index=False)["Revenue"]
                .sum()
                .sort_values("Revenue", ascending=False)
            )
            best = result.iloc[0]
            return (
                f"{best['Region']} has the highest revenue in the selected data: "
                f"${best['Revenue']:,.2f}.",
                result,
            )

        if "product" in q and any(
            word in q for word in ["profit", "profitable", "highest", "top", "best"]
        ):
            result = (
                data.groupby("Product", as_index=False)["Profit"]
                .sum()
                .sort_values("Profit", ascending=False)
            )
            best = result.iloc[0]
            return (
                f"{best['Product']} has the highest total profit: "
                f"${best['Profit']:,.2f}.",
                result,
            )

        if any(word in q for word in ["monthly", "month", "trend", "over time"]):
            result = (
                data.assign(
                    Month=data["OrderDate"].dt.to_period("M").dt.to_timestamp()
                )
                .groupby("Month", as_index=False)["Revenue"]
                .sum()
                .sort_values("Month")
            )
            return "Here is the monthly revenue trend for the selected data.", result

        if "margin" in q:
            revenue = data["Revenue"].sum()
            profit = data["Profit"].sum()
            margin = profit / revenue if revenue else 0
            return f"Profit margin for the selected data is {margin:.1%}.", None

        if "order" in q and any(
            word in q for word in ["count", "number", "total", "how many"]
        ):
            count = data["OrderID"].nunique()
            return f"There are {count:,} unique orders in the selected data.", None

        if "profit" in q:
            return f"Total profit in the selected data is ${data['Profit'].sum():,.2f}.", None

        if any(word in q for word in ["revenue", "sales", "total"]):
            return f"Total revenue in the selected data is ${data['Revenue'].sum():,.2f}.", None

        return (
            "I can't answer that question yet. Try asking about total revenue, "
            "profit, profit margin, order count, revenue by region, product profit, "
            "monthly revenue, or unusual orders.",
            None,
        )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask about your sales data...")

    if question:
        st.session_state.chat_history.append(
            {"role": "user", "content": question}
        )

        answer, result_table = answer_question(question, filtered)

        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            st.markdown(answer)

            if result_table is not None:
                st.dataframe(result_table, use_container_width=True)

                if "Month" in result_table.columns:
                    fig = px.line(
                        result_table, x="Month", y="Revenue",
                        markers=True, title="Monthly Revenue",
                    )
                    st.plotly_chart(fig, use_container_width=True)
                elif "Region" in result_table.columns and "Revenue" in result_table.columns:
                    fig = px.bar(
                        result_table, x="Region", y="Revenue",
                        title="Revenue by Region",
                    )
                    st.plotly_chart(fig, use_container_width=True)
                elif "Product" in result_table.columns and "Profit" in result_table.columns:
                    fig = px.bar(
                        result_table, x="Product", y="Profit",
                        title="Profit by Product",
                    )
                    st.plotly_chart(fig, use_container_width=True)

    if st.button("Clear chat history"):
        st.session_state.chat_history = []
        st.rerun()

with data_tab:
    st.subheader("Filtered Sales Records")
    st.dataframe(filtered, use_container_width=True)

    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered data as CSV",
        data=csv_data,
        file_name="northstar_filtered_sales.csv",
        mime="text/csv",
    )

st.sidebar.caption(f"Loaded {len(df):,} orders")
st.sidebar.caption(f"Showing {len(filtered):,} orders after filters")
