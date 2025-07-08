import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv("cleaned_pizza_sales.csv")

# Page config
st.set_page_config(page_title="Pizza Sales Dashboard", layout="wide")
st.title("🍕 Pizza Sales Analysis Dashboard")

# Sidebar filters
st.sidebar.header("Filter Data")
date_range = st.sidebar.date_input("Select Date Range", [df['order_date'].min(), df['order_date'].max()])

# Filter data based on date range
if len(date_range) == 2:
    df['order_date'] = pd.to_datetime(df['order_date'])
    df = df[(df['order_date'] >= pd.to_datetime(date_range[0])) & (df['order_date'] <= pd.to_datetime(date_range[1]))]

# KPI Section
st.subheader("📊 Key Performance Indicators")
total_revenue = df['total_price'].sum()
total_orders = df['order_id'].nunique()
avg_order_value = total_revenue / total_orders if total_orders else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Average Order Value", f"${avg_order_value:,.2f}")

# Sales Over Time
st.subheader("📅 Sales Over Time")
sales_time = df.groupby('order_date')['total_price'].sum()
fig1, ax1 = plt.subplots(figsize=(12, 4))
sales_time.plot(ax=ax1)
ax1.set_title("Revenue by Date")
ax1.set_ylabel("Revenue ($)")
st.pyplot(fig1)

# Top 10 Pizzas by Revenue
st.subheader("🏆 Top 10 Pizzas by Revenue")
top_pizzas = df.groupby('pizza_name')['total_price'].sum().sort_values(ascending=False).head(10)
fig2, ax2 = plt.subplots(figsize=(10, 5))
top_pizzas.plot(kind='bar', ax=ax2, color='orange')
ax2.set_ylabel("Revenue ($)")
ax2.set_title("Top 10 Best-Selling Pizzas")
ax2.tick_params(axis='x', rotation=45)
st.pyplot(fig2)

# Order Volume by Hour
st.subheader("⏰ Order Volume by Hour")
fig3, ax3 = plt.subplots(figsize=(10, 4))
sns.histplot(df['hour'], bins=24, kde=False, ax=ax3)
ax3.set_title("Orders by Hour of Day")
ax3.set_xlabel("Hour")
ax3.set_ylabel("Number of Orders")
st.pyplot(fig3)

# Revenue by Pizza Size
st.subheader("🍕 Revenue by Pizza Size")
size_revenue = df.groupby('pizza_size')['total_price'].sum().sort_values(ascending=False)
fig4, ax4 = plt.subplots(figsize=(8, 4))
size_revenue.plot(kind='bar', ax=ax4, color='green')
ax4.set_ylabel("Revenue ($)")
ax4.set_title("Revenue by Pizza Size")
st.pyplot(fig4)

st.caption("Dashboard by Jacques Mono | Data Analysis with Streamlit")
