AUTOMATED ELT PIPELINE AIRFLOW USING STAR SCHEMA 
 
An Automated ELT pipeline using Apache Airflow streamlines the process of extracting, loading, and transforming e-commerce data efficiently. This project comes under Data Engineering domain using python programming language. Here we are using the E-commerce dataset.
Apache Airflow is used to schedule and monitor workflows, ensuring reliable data processing. The data is modeled using a Star Schema, which organizes fact and dimension tables for better analytical performance. Docker is used to containerize and deploy Airflow, making setup and scalability easier. This pipeline enables automated downloading, loading, and transformation of e-commerce datasets into a structured data warehouse for business intelligence and reporting.

DEVELOPING PHASE
•	Download docker in your laptop, Docker runs Airflow and PostgreSQL inside isolated containers instead of installing them directly on your system.
•	Here we use the Apache Airflow where it schedules and manges the task in specific order.

•	ELT Pipeline Steps
Step 1 — Extract
The extract.py script reads the orders.csv file using pandas.
It pulls raw e-commerce data without modifying it.
Step 2 — Load
The raw data is loaded into staging.raw_orders inside PostgreSQL.
This staging table stores the flat, unorganized copy of the CSV.
Step 3 — Transform
The transform.py script restructures the flat table into a Star Schema.
Data is split into dimension tables and a fact table for efficient analysis.

CREATING THE PYCHARM ENVIRONMENT
•	Keep the docker running in the laptop or PC where in left down of the docker it shows the engine starting .
•	Open pycharm create new project of pycharm version 3.11.
•	Name the project as elt.
•	Create new file in the elt file named dags, data, scripts, sql, .env, 
docker-compose.yml, requirement.txt
•	Inside the dags file create new file named as ecommerce_elt_dag.py.
•	Inside the data file create new file named as orders.csv.
•	Inside the scripts file create new file named as extract.py , transform.py .
•	Inside the sql file create new file named as create_star_schema.sql.
•	Add the codes inside the files created. 
├── dags/
│   ├── extract_dag.py
│   ├── load_dag.py
│   └── transform_dag.py
│
├── scripts/
│   ├── extract.py
│   ├── load.py
│   └── transform.py
│
├── sql/
│   ├── create_staging.sql
│   ├── create_star_schema.sql
│   └── transform_queries.sql
│
├── data/
│   └── sample_ecommerce.csv        ← raw data goes here
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env
•	The pycharm files need to look like this

RUN THE PROGRAM 
Go to the local host created that is the airflow turn on the dataset in DAG and run the graphs if there is any failure click on the box of failure and select clear to get success of the boxes in green colour. http://localhost:8080 this is the dashboard for this project.
You'll see: init_schema → extract_and_load_staging → transform_to_star_schema.
•	Open terminal check the docker is running by docker –version
•	Open terminal and run 
docker-compose up airflow-init
docker-compose up -d
docker-compose ps
run the DAG 
Stopping the Pipeline
            docker-compose down
            docker-compose up -d
after everything is success
            docker exec airflow_scheduler cat /opt/airflow/scripts/extract.py
            docker-compose up -d
            docker-compose ps
            docker exec airflow_scheduler head -1 /opt/airflow/data/orders.csv
after running all this in pychram it has to shoe UTF-8 if not change it to UTF-8.
             docker exec airflow_scheduler python3 -c "import pandas as pd; df=pd.read_csv('/opt/airflow/data/orders.csv'); print('COLUMNS:',list(df.columns)); print('ROWS:',len(df))"
COLUMNS: ['order_id', 'order_date', 'customer_id', 'customer_name', 
          'customer_email', 'city', 'country', 'product_id', 
          'product_name', 'category', 'unit_price', 'quantity', 
          'discount', 'payment_method']
docker exec postgres_dwh psql -U dwh_user -d ecommerce_dwh -c "SELECT * FROM dwh.fact_orders;"
docker exec postgres_dwh psql -U dwh_user -d ecommerce_dwh -c "SELECT p.category, COUNT(*) AS orders, SUM(f.total_amount) AS revenue FROM dwh.fact_orders f JOIN dwh.dim_products p ON f.product_key = p.product_key GROUP BY p.category ORDER BY revenue DESC;"






