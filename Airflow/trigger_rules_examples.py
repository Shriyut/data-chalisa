from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.helpers import cross_downstream
from airflow.models.baseoperator import cross_downstream, chain

from datetime import datetime, timedelta

default_args = {
    "email": ["#######@gmail.com"],
    "email_on_retry": True,
    "email_on_failure": False
}

def _my_func(execution_date):
    if execution_date.day == 5:
        raise ValueError("Error")

with DAG("my_dag_v_1_0_0", default_args=default_args, start_date=datetime(2021, 1, 1),
         schedule_interval='@daily', catchup=False) as dag:

    extract_a = BashOperator(
        owner='john',
        task_id="extract_a",
        bash_command="echo 'task_a' && sleep 10",
        wait_for_downstream=True,
    )

    extract_b = BashOperator(
        owner='john',
        task_id="extract_b",
        bash_command="echo 'task_a' && sleep 10",
        wait_for_downstream=True,
    )

    process_a = BashOperator(
        owner='marc',
        task_id="process_a",
        retries=3,
        retry_exponential_backoff=True,
        retry_delay=timedelta(seconds=10),
        bash_command="echo '{{ ti.priority_weight }}' && sleep 20",
        priority_weight=2,
        pool="process_tasks"
    )

    clean_a = BashOperator(
        owner='marc',
        task_id="clean_a",
        bash_command="echo 'clean process_a'",
        trigger_rule='all_failed'
    )

    process_b = BashOperator(
        owner='marc',
        task_id="process_b",
        retries=3,
        retry_exponential_backoff=True,
        retry_delay=timedelta(seconds=10),
        bash_command="echo '{{ ti.priority_weight }}' && sleep 20",
        pool="process_tasks"
    )

    clean_b = BashOperator(
        owner='marc',
        task_id="clean_b",
        bash_command="echo 'clean process_b'",
        trigger_rule='all_failed'
    )

    process_c = BashOperator(
        owner='marc',
        task_id="process_c",
        retries=3,
        retry_exponential_backoff=True,
        retry_delay=timedelta(seconds=10),
        bash_command="echo '{{ ti.priority_weight }}' && sleep 20",
        priority_weight=3,
        pool="process_tasks"
    )

    clean_c = BashOperator(
        owner='marc',
        task_id="clean_c",
        bash_command="echo 'clean process_c'",
        trigger_rule='all_failed'
    )

    store = PythonOperator(
        task_id="store",
        python_callable=_my_func,
        depends_on_past=True
    )

    cross_downstream([extract_a, extract_b], [process_a, process_b, process_c])
    process_a >> clean_a
    process_b >> clean_b
    process_c >> clean_c
    [process_a, process_b, process_c] >> store

# example usage of cross downstream and chain functionality
    # cross_downstream([extract_a, extract_b], [process_a, process_b, process_c])
    # chain([process_a, process_b, process_c], [clean_a, clean_b, clean_c])
    # cross_downstream([process_a, process_b, process_c], store)