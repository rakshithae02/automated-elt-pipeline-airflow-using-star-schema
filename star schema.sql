-- Create schemas
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS dwh;

-- ─────────────────────────────────────────
-- STAGING TABLE (raw data lands here first)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS staging.raw_orders (
    order_id        INTEGER,
    order_date      DATE,
    customer_id     VARCHAR(20),
    customer_name   VARCHAR(100),
    customer_email  VARCHAR(100),
    city            VARCHAR(100),
    country         VARCHAR(100),
    product_id      VARCHAR(20),
    product_name    VARCHAR(100),
    category        VARCHAR(50),
    unit_price      DECIMAL(10,2),
    quantity        INTEGER,
    discount        DECIMAL(5,2),
    payment_method  VARCHAR(50),
    loaded_at       TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────
-- DIMENSION TABLE: Date
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS dwh.dim_date (
    date_id     SERIAL PRIMARY KEY,
    full_date   DATE UNIQUE NOT NULL,
    day         INTEGER,
    month       INTEGER,
    month_name  VARCHAR(20),
    quarter     INTEGER,
    year        INTEGER,
    weekday     VARCHAR(20)
);

-- ─────────────────────────────────────────
-- DIMENSION TABLE: Customers
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS dwh.dim_customers (
    customer_key    SERIAL PRIMARY KEY,
    customer_id     VARCHAR(20) UNIQUE NOT NULL,
    customer_name   VARCHAR(100),
    customer_email  VARCHAR(100)
);

-- ─────────────────────────────────────────
-- DIMENSION TABLE: Products
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS dwh.dim_products (
    product_key     SERIAL PRIMARY KEY,
    product_id      VARCHAR(20) UNIQUE NOT NULL,
    product_name    VARCHAR(100),
    category        VARCHAR(50),
    unit_price      DECIMAL(10,2)
);

-- ─────────────────────────────────────────
-- DIMENSION TABLE: Location
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS dwh.dim_location (
    location_key    SERIAL PRIMARY KEY,
    city            VARCHAR(100),
    country         VARCHAR(100),
    UNIQUE(city, country)
);

-- ─────────────────────────────────────────
-- FACT TABLE: Orders (center of star schema)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS dwh.fact_orders (
    order_key       SERIAL PRIMARY KEY,
    order_id        INTEGER,
    date_key        INTEGER REFERENCES dwh.dim_date(date_id),
    customer_key    INTEGER REFERENCES dwh.dim_customers(customer_key),
    product_key     INTEGER REFERENCES dwh.dim_products(product_key),
    location_key    INTEGER REFERENCES dwh.dim_location(location_key),
    quantity        INTEGER,
    unit_price      DECIMAL(10,2),
    discount        DECIMAL(5,2),
    total_amount    DECIMAL(10,2),
    payment_method  VARCHAR(50),
    created_at      TIMESTAMP DEFAULT NOW()
);
