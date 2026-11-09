import pandas as pd
import numpy as np
#1.Products_dataset
products_Data={
    'Product_ID': [101,102,103,104,105,106],
    'Product_name':['Wireless earbuds','Mechanical keyboard','Gaming Mouse','USB-C Hub','Monitor Stand','Desk Mat'],
    'category':['Accessories','Peripherals','Peripherals','Accessories','Furniture','Accessories'],
    'Cost_price':[25.0, 45.0, 18.0, 12.0, 15.0, 8.0],
    'Selling_price':[59.99, 99.99, 39.99, 29.99, 24.99, 8.99],
    'Stock_quantity':[14,5,22,3,18,45]
}
pd.DataFrame(products_Data).to_csv('products_data.csv',index=False)

# 2. Customers Dataset
customers_data = {
    "customer_id": [1, 2, 3, 4, 5],
    "customer_name": ["Alex Reed", "Jordan Smith", "Rohan Mehta", "Emily Chen", "David Kim"],
    "city": ["Mumbai", "Bengaluru", "Delhi", "Pune", "Hyderabad"],
    "signup_date": ["2026-01-10", "2026-02-15", "2026-03-01", "2026-03-12", "2026-04-05"]
}
pd.DataFrame(customers_data).to_csv("customers.csv", index=False)

# 3. Orders Dataset (with foreign keys product_id and customer_id)
orders_data = {
    "order_id": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010],
    "customer_id": [1, 2, 1, 3, 4, 2, 5, 3, 1, 4],
    "product_id": [101, 102, 103, 101, 104, 105, 106, 102, 105, 104],
    "quantity": [2, 1, 1, 3, 2, 1, 4, 1, 2, 1],
    "order_date": [
        "2026-05-01", "2026-05-03", "2026-05-10", "2026-05-12", "2026-05-18",
        "2026-05-22", "2026-06-01", "2026-06-05", "2026-06-11", "2026-06-15"
    ],
    "status": ["Delivered", "Delivered", "Delivered", "Returned", "Delivered", "Delivered", "Delivered", "Cancelled", "Delivered", "Delivered"]
}
pd.DataFrame(orders_data).to_csv("orders.csv", index=False)

print("Generated products.csv, customers.csv, and orders.csv successfully!")

