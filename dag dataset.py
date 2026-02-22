from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys

sys.path.insert(0, '/opt/airflow/scripts')

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='ecommerce_elt_pipeline',
    default_args=default_args,
    description='E-Commerce ELT Pipeline',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['ecommerce', 'elt', 'star-schema'],
) as dag:

    def run_extract():
        from extract import extract_and_load_staging
        extract_and_load_staging()

    def run_transform():
        from transform import transform_to_star_schema
        transform_to_star_schema()

    init_schema = BashOperator(
        task_id='init_schema',
        bash_command=(
            'PGPASSWORD=dwh_pass psql '
            '-h postgres_dwh -U dwh_user -d ecommerce_dwh '
            '-f /opt/airflow/sql/create_star_schema.sql'
        )
    )

    extract_load = PythonOperator(
        task_id='extract_and_load_staging',
        python_callable=run_extract,
    )

    transform = PythonOperator(
        task_id='transform_to_star_schema',
        python_callable=run_transform,
    )

    init_schema >> extract_load >> transform
