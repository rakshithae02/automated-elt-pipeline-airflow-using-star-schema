import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

DWH_CONN = {
    "host": "postgres_dwh",
    "port": 5432,
    "dbname": "ecommerce_dwh",
    "user": "dwh_user",
    "password": "dwh_pass"
}

def extract_and_load_staging():
    print("=== EXTRACT TASK STARTED ===")

    df = pd.read_csv('/opt/airflow/data/orders.csv')
    df.columns = df.columns.str.strip()

    print(f"Columns found: {list(df.columns)}")
    print(f"Found {len(df)} rows")

    df = pd.read_csv('/opt/airflow/data/student dataset.csv')

    conn = psycopg2.connect(**DWH_CONN)
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE staging.raw_orders;")

    rows = [
        (
            row.order_id, row.order_date, row.customer_id,
            row.customer_name, row.customer_email, row.city,
            row.country, row.product_id, row.product_name,
            row.category, row.unit_price, row.quantity,
            row.discount, row.payment_method
        )
        for row in df.itertuples(index=False)
    ]

    execute_values(cur, """
        INSERT INTO staging.raw_orders (
            order_id, order_date, customer_id, customer_name,
            customer_email, city, country, product_id, product_name,
            category, unit_price, quantity, discount, payment_method
        ) VALUES %s
    """, rows)

    conn.commit()
    cur.close()
    conn.close()
    print(f"=== EXTRACT DONE: {len(df)} rows loaded ===")
