from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.utils import timezone


with DAG(
    dag_id="my_first_dag",
    schedule="@hourly",
    start_date=timezone.datetime(2024, 10, 3),
    catchup=False,
    tags=["DEB", "Skooldio"],
):

    t1 = EmptyOperator(task_id="t1")
    t2 = EmptyOperator(task_id="t2")
    t3 = EmptyOperator(task_id="t3")
    hello = BashOperator(
        task_id="hello",
        bash_command="echo hello"
    )

    t1 >> [t2, t3] >> hello

    # t1 >> t2
    # t1 >> t3