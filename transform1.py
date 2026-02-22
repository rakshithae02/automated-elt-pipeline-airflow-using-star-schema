import psycopg2

DWH_CONN = {
    "host": "postgres_dwh",
    "port": 5432,
    "dbname": "ecommerce_dwh",
    "user": "dwh_user",
    "password": "dwh_pass"
}

def transform_to_star_schema():
    print("=== TRANSFORM TASK STARTED ===")

    conn = psycopg2.connect(**DWH_CONN)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO dwh.dim_date (
            full_date, day, month, month_name, quarter, year, weekday
        )
        SELECT DISTINCT
            order_date,
            EXTRACT(DAY FROM order_date)::INT,
            EXTRACT(MONTH FROM order_date)::INT,
            TO_CHAR(order_date, 'Month'),
            EXTRACT(QUARTER FROM order_date)::INT,
            EXTRACT(YEAR FROM order_date)::INT,
            TO_CHAR(order_date, 'Day')
        FROM staging.raw_orders
        ON CONFLICT (full_date) DO NOTHING;
    """)

    cur.execute("""
        INSERT INTO dwh.dim_customers (customer_id, customer_name, customer_email)
        SELECT DISTINCT customer_id, customer_name, customer_email
        FROM staging.raw_orders
        ON CONFLICT (customer_id) DO NOTHING;
    """)

    cur.execute("""
        INSERT INTO dwh.dim_products (product_id, product_name, category, unit_price)
        SELECT DISTINCT product_id, product_name, category, unit_price
        FROM staging.raw_orders
        ON CONFLICT (product_id) DO NOTHING;
    """)

    cur.execute("""
        INSERT INTO dwh.dim_location (city, country)
        SELECT DISTINCT city, country
        FROM staging.raw_orders
        ON CONFLICT (city, country) DO NOTHING;
    """)

    cur.execute("""
        INSERT INTO dwh.fact_orders (
            order_id, date_key, customer_key, product_key, location_key,
            quantity, unit_price, discount, total_amount, payment_method
        )
        SELECT
            r.order_id,
            d.date_id,
            c.customer_key,
            p.product_key,
            l.location_key,
            r.quantity,
            r.unit_price,
            r.discount,
            ROUND((r.unit_price * r.quantity * (1 - r.discount))::NUMERIC, 2),
            r.payment_method
        FROM staging.raw_orders r
        JOIN dwh.dim_date d      ON d.full_date   = r.order_date
        JOIN dwh.dim_customers c ON c.customer_id  = r.customer_id
        JOIN dwh.dim_products p  ON p.product_id   = r.product_id
        JOIN dwh.dim_location l  ON l.city = r.city AND l.country = r.country;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("=== TRANSFORM DONE ===")
