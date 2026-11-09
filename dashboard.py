import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("ecommerce.db")

# Data 1: Profit per Product
df_profit = pd.read_sql("""
    SELECT p.product_name, ROUND(SUM(o.quantity * (p.selling_price - p.cost_price)), 2) as profit
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    WHERE o.status = 'Delivered'
    GROUP BY p.product_name
    ORDER BY profit ASC;
""", conn)

# Data 2: Order Status Distribution
df_status = pd.read_sql("""
    SELECT status, COUNT(*) as count
    FROM orders
    GROUP BY status;
""", conn)

# Data 3: Stock vs Threshold
df_stock = pd.read_sql("""
    SELECT product_name, stock_quantity
    FROM products
    ORDER BY stock_quantity ASC;
""", conn)

conn.close()

# Create a 3-panel dashboard
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))

# Panel 1: Horizontal Bar Chart of Profits
ax1.barh(df_profit["Product_name"], df_profit["profit"], color="#2b5c8f")
ax1.set_title("Total Net Profit by Product ($)")
ax1.set_xlabel("Profit ($)")
ax1.grid(axis="x", linestyle="--", alpha=0.6)

# Panel 2: Pie Chart of Order Fulfillment
ax2.pie(
    df_status["count"], 
    labels=df_status["status"], 
    autopct="%1.1f%%", 
    colors=["#4CAF50", "#FFC107", "#F44336"],
    startangle=90
)
ax2.set_title("Order Fulfillment Status")

# Panel 3: Inventory Levels with Alert Line
bars = ax3.bar(df_stock["Product_name"], df_stock["Stock_quantity"], color="#5c6bc0")
ax3.axhline(y=10, color="red", linestyle="--", label="Restock Threshold (<10)")
ax3.set_title("Current Inventory Levels")
ax3.set_ylabel("Units in Stock")
ax3.tick_params(axis="x", rotation=45)
ax3.legend()
ax3.grid(axis="y", linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("ecommerce_dashboard.png", dpi=300)
print("Dashboard created and saved as 'ecommerce_dashboard.png'!")
plt.show()