import sqlite3
import pandas as pd
import numpy as np

#1
df_products=pd.read_csv("products_data.csv")
df_customers=pd.read_csv("customers.csv")
df_orders=pd.read_csv("orders.csv")
#2.
df_customers["signup_date"]=pd.to_datetime(df_customers["signup_date"])
df_orders["order_date"]=pd.to_datetime(df_orders["order_date"])

#3.
df_products["restock_needed"]=np.where(df_products["Stock_quantity"]<10,"YES","NO")
df_products["profit_margin"]=df_products["Selling_price"]-df_products["Cost_price"]
#4.
conn=sqlite3.connect("ecommerce.db")
df_products.to_sql("products",conn,if_exists='replace',index=False)
df_customers.to_sql("customers",conn,if_exists='replace',index=False)
df_orders.to_sql("orders",conn,if_exists='replace',index=False)
conn.close()
print('Multitable database "ecommerce.db" constructed and populated successfully')