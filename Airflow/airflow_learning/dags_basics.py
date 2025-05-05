import datetime
from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator

with DAG(
    dag_id="basic_dag",
    schedule="@daily",
    start_date=datetime.datetime(2025, 5, 5),
    # catchup=False,
    # default_args={
    #     "owner": "airflow",
    #     "retries": 1,
    #     "retry_delay": datetime.timedelta(minutes=5),
    # },
):
    EmptyOperator(task_id="test")