import sqlite3
import pandas as pd

conn = sqlite3.connect("ecommerce.db")

# Query 1: Product Profitability & Revenue Breakdown (JOIN orders + products)
query_profitability = """
SELECT 
    p.product_name,
    p.category,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.quantity * p.selling_price), 2) AS gross_revenue,
    ROUND(SUM(o.quantity * (p.selling_price - p.cost_price)), 2) AS total_profit
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY p.product_id
ORDER BY total_profit DESC;
"""

print("=== PRODUCT PROFITABILITY & REVENUE ===")
print(pd.read_sql(query_profitability, conn).to_string(index=False))

# Query 2: Customer Lifetime Value (CLV) & Order Frequency (JOIN orders + customers + products)
query_clv = """
SELECT 
    c.customer_name,
    c.city,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(CASE WHEN o.status = 'Delivered' THEN o.quantity * p.selling_price ELSE 0 END), 2) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN products p ON o.product_id = p.product_id
GROUP BY c.customer_id
ORDER BY total_spent DESC;
"""

print("\n=== CUSTOMER LIFETIME VALUE (CLV) ===")
print(pd.read_sql(query_clv, conn).to_string(index=False))

# Query 3: Low-Stock Restock Warning List
query_inventory = """
SELECT 
    product_name, 
    stock_quantity, 
    selling_price
FROM products
WHERE restock_needed = 'YES'
ORDER BY stock_quantity ASC;
"""

print("\n=== INVENTORY RESTOCK WARNINGS ===")
print(pd.read_sql(query_inventory, conn).to_string(index=False))

conn.close()