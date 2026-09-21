import plotly.express as px
import streamlit as st

from sales_data import (
    load_sales_data,
    total_sales,
    total_orders,
    monthly_sales_trend,
    sales_by_category,
    sales_by_region,
)

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")

try:
    df = load_sales_data("data/sales-data.csv")
except (FileNotFoundError, ValueError) as e:
    st.error(f"Could not load sales data: {e}")
    st.stop()

st.title("ShopSmart Sales Dashboard")

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(df):,.2f}")
col2.metric("Total Orders", f"{total_orders(df):,}")

trend = monthly_sales_trend(df)
fig_trend = px.line(
    trend, x="month", y="total_amount", markers=True,
    labels={"month": "Month", "total_amount": "Sales ($)"},
    title="Sales Trend Over Time",
)
fig_trend.update_yaxes(rangemode="tozero")
st.plotly_chart(fig_trend, use_container_width=True)

col3, col4 = st.columns(2)

category = sales_by_category(df)
fig_category = px.bar(
    category, x="total_amount", y="category", orientation="h",
    labels={"category": "Category", "total_amount": "Sales ($)"},
    title="Sales by Category",
)
fig_category.update_layout(yaxis=dict(autorange="reversed"))
fig_category.update_traces(hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.2f}<extra></extra>")
col3.plotly_chart(fig_category, use_container_width=True)

region = sales_by_region(df)
fig_region = px.bar(
    region, x="total_amount", y="region", orientation="h",
    labels={"region": "Region", "total_amount": "Sales ($)"},
    title="Sales by Region",
)
fig_region.update_layout(yaxis=dict(autorange="reversed"))
fig_region.update_traces(hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.2f}<extra></extra>")
col4.plotly_chart(fig_region, use_container_width=True)
