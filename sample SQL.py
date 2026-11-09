import sqlite3
import pandas as pd
import numpy as np

conn=sqlite3.connect("ecommerce.db")

#1.
query_profitability="""
SELECT 
p.product_name,
p.category,
ROUND(SUM(o.quantity * p.Selling_price) ,2) as total_revenue,
ROUND(SUM(o.quantity * (p.Selling_price - p.Cost_price)), 2) as total_profit
FROM orders o
JOIN products p ON o.product_id=p.product_id
GROUP BY p.product_id
ORDER BY total_profit DESC;
"""

print("==Product Profitability and Revenue==")
print(pd.read_sql(query_profitability,conn).to_string(index=False))

#2.
query_CLV="""
SELECT
c.customer_name,
c.customer_id,
c.city,
COUNT(o.order_id) as total_orders,
ROUND(SUM(CASE WHEN status="Delivered" THEN o.quantity * p.Selling_price ELSE 0 END),2) as total_spent
FROM customers c
JOIN orders o ON c.customer_id=o.customer_id
JOIN products p ON o.product_id=p.product_id
GROUP BY c.customer_id
ORDER BY total_profit DESC;
"""

print("==Customer Lifetime Value (CLV)==")
print(pd.read_sql(query_CLV,conn).to_string(index=False))

#3.
query_inventory="""
SELECT
 product_name,
 Stock_quantity,
 Selling_price
 FROM products
 WHERE restock_needed="YES"
 ORDER BY Stock_quantity ASC;
 """
 print("==Inventory Restock Warnings==")
 print(pd.read_sql(query_inventory,conn).to_string(index=False))
 conn.close()
 
