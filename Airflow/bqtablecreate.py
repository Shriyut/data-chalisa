import datetime

from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator

default_args = {
    "owner": "Composer Example",
    "depends_on_past": False,
    "start_date": datetime.datetime.now(),  # Use current date
}

with DAG(
        "create_bigquery_table_dag",
        default_args=default_args,
        schedule_interval="0 */6 * * *",  # Run every 6 hours #starts the job at 6 hour multiple
) as dag:
    create_table_task = BigQueryCreateEmptyTableOperator(
        task_id="create_test_table",
        dataset_id="testdataset",
        table_id="test_table",
        schema_fields=[
            {"name": "column1", "type": "STRING", "mode": "NULLABLE"},
            {"name": "column2", "type": "STRING", "mode": "NULLABLE"},
            {"name": "column3", "type": "STRING", "mode": "NULLABLE"},
        ],
    )
