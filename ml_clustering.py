import sqlite3
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def run_customer_segmentation():
    conn = sqlite3.connect("ecommerce.db")
    
    # 1. Feature Engineering: Extract customer behavioral metrics via SQL
    query = """
    SELECT 
        c.customer_id,
        c.customer_name,
        c.city,
        COUNT(o.order_id) AS total_orders,
        COALESCE(SUM(CASE WHEN o.status = 'Delivered' THEN o.quantity * p.Selling_price ELSE 0 END), 0) AS total_spent,
        COALESCE(AVG(CASE WHEN o.status = 'Delivered' THEN o.quantity * p.Selling_price ELSE NULL END), 0) AS avg_order_value
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN products p ON o.product_id = p.product_id
    GROUP BY c.customer_id;
    """
    df_customers = pd.read_sql(query, conn)
    conn.close()

    # 2. Select numerical features for the ML model
    features = ["total_orders", "total_spent", "avg_order_value"]
    X = df_customers[features]

    # 3. Standardize features (ensures dollar values don't overpower order counts)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 4. Train K-Means Clustering Model (3 distinct customer tiers)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df_customers["cluster_id"] = kmeans.fit_predict(X_scaled)

    # 5. Map cluster numbers to meaningful business labels based on spending
    cluster_spending = df_customers.groupby("cluster_id")["total_spent"].mean()
    high_cluster = cluster_spending.idxmax()
    low_cluster = cluster_spending.idxmin()

    def label_cluster(cid):
        if cid == high_cluster:
            return "High-Value VIP"
        elif cid == low_cluster:
            return "Occasional Buyer"
        else:
            return "Regular Shopper"

    df_customers["customer_segment"] = df_customers["cluster_id"].apply(label_cluster)
    
    return df_customers

if __name__ == "__main__":
    segmented_df = run_customer_segmentation()
    print("=== ML CUSTOMER SEGMENTATION RESULTS ===")
    print(segmented_df[["customer_name", "total_orders", "total_spent", "customer_segment"]])