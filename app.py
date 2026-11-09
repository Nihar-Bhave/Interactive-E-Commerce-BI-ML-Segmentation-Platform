import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from ml_clustering import run_customer_segmentation

# --- Page Setup ---
st.set_page_config(page_title="E-Commerce Analytics & ML Dashboard", layout="wide")
st.title("📊 E-Commerce Analytics & ML Executive Portal")
st.markdown("Interactive business intelligence and customer segmentation engine.")

# --- Database Connection Helper ---
def get_data(query):
    conn = sqlite3.connect("ecommerce.db")
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- Sidebar Filters ---
st.sidebar.header("Filter Analytics")
status_filter = st.sidebar.multiselect(
    "Select Order Status:",
    options=["Delivered", "Returned", "Cancelled"],
    default=["Delivered", "Returned", "Cancelled"]
)

# --- Data Queries ---
status_str = "', '".join(status_filter)
orders_df = get_data(f"""
    SELECT 
        o.order_id, o.order_date, o.status, o.quantity,
        p.product_name, p.category, p.Selling_price, p.Cost_price,
        (o.quantity * p.Selling_price) AS gross_revenue,
        (o.quantity * (p.Selling_price - p.Cost_price)) AS net_profit
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    WHERE o.status IN ('{status_str}')
""")

# --- Section 1: Executive KPI Metrics ---
total_rev = orders_df[orders_df["status"] == "Delivered"]["gross_revenue"].sum()
total_profit = orders_df[orders_df["status"] == "Delivered"]["net_profit"].sum()
total_orders_count = len(orders_df)

col1, col2, col3 = st.columns(3)
col1.metric("Delivered Gross Revenue", f"${total_rev:,.2f}")
col2.metric("Total Net Profit", f"${total_profit:,.2f}")
col3.metric("Total Filtered Orders", f"{total_orders_count}")

st.divider()

# --- Section 2: Visual Charts ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Profit by Product Category")
    cat_profit = orders_df.groupby("category")["net_profit"].sum().reset_index()
    
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.bar(cat_profit["category"], cat_profit["net_profit"], color="#2b5c8f")
    ax1.set_ylabel("Net Profit ($)")
    ax1.grid(axis="y", linestyle="--", alpha=0.6)
    st.pyplot(fig1)

with chart_col2:
    st.subheader("Order Fulfillment Breakdown")
    status_counts = orders_df["status"].value_counts()
    
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=90, colors=["#4CAF50", "#FF9800", "#E91E63"])
    st.pyplot(fig2)

st.divider()

# --- Section 3: Machine Learning Segmentation Tab ---
st.header("🤖 Machine Learning: Customer Segmentation (K-Means)")
st.markdown("Customers grouped automatically using unsupervised K-Means clustering based on purchasing frequency and lifetime expenditure.")

df_segmented = run_customer_segmentation()

# Dynamic Segment Filter
selected_segment = st.selectbox("Filter by Segment Tier:", options=["All"] + list(df_segmented["customer_segment"].unique()))

if selected_segment != "All":
    display_df = df_segmented[df_segmented["customer_segment"] == selected_segment]
else:
    display_df = df_segmented

st.dataframe(
    display_df[["customer_name", "city", "total_orders", "total_spent", "avg_order_value", "customer_segment"]],
    use_container_width=True
)