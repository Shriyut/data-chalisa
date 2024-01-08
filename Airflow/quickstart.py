import datetime

import airflow
from airflow.operators import bash_operator

# Set the DAG's start date to a time in the past to trigger an initial run
YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)
default_args = {
    "owner": "Composer Example",
    "depends_on_past": False,
    "email": [""],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
    "start_date": YESTERDAY,  # Use the specific start date
}

with airflow.DAG(
        "composer_sample_dag",
        catchup=False,  # Prevent backfilling of missed runs
        default_args=default_args,
        schedule_interval=datetime.timedelta(minutes=5),  # Run every 5 minutes
) as dag:
    # Print the dag_run id from the Airflow logs
    print_dag_run_conf = bash_operator.BashOperator(
        task_id="print_dag_run_conf", bash_command="echo {{ dag_run.id }}"
    )