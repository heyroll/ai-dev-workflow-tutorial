import streamlit as st

from sales_data import load_sales_data, total_sales, total_orders

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
