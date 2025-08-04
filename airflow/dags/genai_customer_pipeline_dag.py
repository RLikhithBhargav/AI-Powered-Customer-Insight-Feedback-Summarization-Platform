from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os
import pendulum
from datetime import timedelta

# Add your project path to system path
sys.path.append('L:/Data Engineering & Analytics Projects/AI Powered Customer Insights Platform/airflow/dags')

# Import each function from the script
from dag_data_pipeline_combined_final import (
    upload_to_snowflake,
    run_dbt_transforms,
    export_customer_features,
    generate_gpt_summaries,
    notify_dashboard_ready,
)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1, tzinfo=pendulum.timezone("UTC")),
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
}

with DAG(
    dag_id='genai_customer_pipeline_dag',
    default_args=default_args,
    schedule_interval=None,  # manual trigger for now
    catchup=False,
    tags=['genai', 'customer-insights'],
) as dag:

    task_upload = PythonOperator(
        task_id='upload_to_snowflake',
        python_callable=upload_to_snowflake
    )

    task_dbt = PythonOperator(
        task_id='run_dbt_transforms',
        python_callable=run_dbt_transforms
    )

    task_export = PythonOperator(
        task_id='export_customer_features',
        python_callable=export_customer_features
    )

    task_gpt = PythonOperator(
        task_id='generate_gpt_summaries',
        python_callable=generate_gpt_summaries
    )

    task_notify = PythonOperator(
        task_id='notify_dashboard_ready',
        python_callable=notify_dashboard_ready
    )

    # Define dependencies
    task_upload >> task_dbt >> task_export >> [task_gpt, task_notify]
