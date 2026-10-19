import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="E-commerce Sales Analytics", page_icon="📊", layout="wide")

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "sales_data.csv"

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    data["month"] = data["order_date"].dt.to_period("M").astype(str)
    data["profit_margin_pct"] = (data["profit"] / data["revenue"].replace(0, pd.NA) * 100).fillna(0)
    return data

df = load_data()

st.title("📊 E-commerce Sales & Profitability Analytics")
st.caption("Portfolio project | SQL + Python + Pandas + Streamlit + Plotly")
st.info("This portfolio uses a generated sample dataset. Figures are illustrative, not real company results.")

with st.sidebar:
    st.header("Filters")
    min_date, max_date = df["order_date"].min().date(), df["order_date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    regions = st.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
    categories = st.multiselect("Category", sorted(df["category"].unique()), default=sorted(df["category"].unique()))
    channels = st.multiselect("Sales channel", sorted(df["sales_channel"].unique()), default=sorted(df["sales_channel"].unique()))

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    filtered = df[
        (df["order_date"] >= start_date) & (df["order_date"] <= end_date) &
        (df["region"].isin(regions)) & (df["category"].isin(categories)) &
        (df["sales_channel"].isin(channels))
    ]
else:
    filtered = df.iloc[0:0]

if filtered.empty:
    st.warning("No records match the selected filters. Try expanding your filters.")
    st.stop()

total_revenue = filtered["revenue"].sum()
total_profit = filtered["profit"].sum()
orders = filtered["order_id"].nunique()
aov = total_revenue / orders if orders else 0
margin = total_profit / total_revenue * 100 if total_revenue else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
c2.metric("Total Profit", f"₹{total_profit:,.0f}")
c3.metric("Orders", f"{orders:,}")
c4.metric("Average Order Value", f"₹{aov:,.0f}")
c5.metric("Profit Margin", f"{margin:.1f}%")

st.divider()
left, right = st.columns(2)
monthly = filtered.groupby("month", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
with left:
    st.subheader("Monthly Revenue Trend")
    fig = px.line(monthly, x="month", y="revenue", markers=True, labels={"month":"Month", "revenue":"Revenue (₹)"})
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Revenue by Category")
    by_cat = filtered.groupby("category", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    fig = px.bar(by_cat.sort_values("revenue", ascending=False), x="category", y="revenue", color="category",
                 labels={"category":"Category", "revenue":"Revenue (₹)"})
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Profit by Region")
    by_region = filtered.groupby("region", as_index=False)["profit"].sum().sort_values("profit", ascending=False)
    fig = px.bar(by_region, x="region", y="profit", labels={"region":"Region", "profit":"Profit (₹)"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Sales Channel Mix")
    by_channel = filtered.groupby("sales_channel", as_index=False)["revenue"].sum()
    fig = px.pie(by_channel, names="sales_channel", values="revenue", hole=0.45)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Category Performance")
cat_table = filtered.groupby("category", as_index=False).agg(
    orders=("order_id", "nunique"),
    units_sold=("quantity", "sum"),
    revenue=("revenue", "sum"),
    profit=("profit", "sum")
)
cat_table["profit_margin_pct"] = (cat_table["profit"] / cat_table["revenue"] * 100).round(2)
cat_table = cat_table.sort_values("revenue", ascending=False)
st.dataframe(cat_table, use_container_width=True, hide_index=True)

st.subheader("Data Explorer")
st.dataframe(filtered.sort_values("order_date", ascending=False), use_container_width=True, hide_index=True)
st.download_button("Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_sales_data.csv", mime="text/csv")

with st.expander("Business insights (example talking points)"):
    best_cat = by_cat.sort_values("revenue", ascending=False).iloc[0]
    best_region = by_region.iloc[0]
    st.markdown(
        f"- **Top revenue category in the selected filters:** {best_cat['category']} (₹{best_cat['revenue']:,.0f}).\n"
        f"- **Highest-profit region in the selected filters:** {best_region['region']} (₹{best_region['profit']:,.0f}).\n"
        f"- **Overall filtered profit margin:** {margin:.1f}%.\n"
        "- Use the filters to test whether these patterns remain consistent across months, regions, and channels."
    )

st.caption("Built for learning and portfolio demonstration. Validate insights from the currently selected filters before presenting them.")
