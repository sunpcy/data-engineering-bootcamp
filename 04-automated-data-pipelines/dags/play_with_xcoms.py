from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def _hey(**context):
    context["ti"].xcom_push(key="this_is_my_xcom", value="Hey")
    return "Hey"


def _print_hey(**context):
    print(context)
    # value = context["ti"].xcom_pull(task_ids="hey", key="return_value")
    value = context["ti"].xcom_pull(task_ids="hey", key="this_is_my_xcom")
    print(value)



with DAG(
    dag_id="play_with_xcoms",
    schedule="@hourly",
    start_date=timezone.datetime(2024, 10, 3),
    catchup=False,
    tags=["DEB", "Skooldio"],
):
    hey = PythonOperator(
        task_id="hey",
        python_callable=_hey,
    )

    print_hey = PythonOperator(
        task_id="print_hey",
        python_callable=_print_hey,
    )

    hey >> print_hey

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