import pprint as pp
import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# Tem o owner airflow e eh para a config filter_by_owner
# ele vai comparar com o username logado na ui, a dag existe junto com a de marketing
# a ideia era trocar o owne de cada um e criar um user para cada
# depois ver se a dag aparece ou nao para cada user
default_args = {
        "owner": "airflow", 
        "start_date": airflow.utils.dates.days_ago(1)
    }

with DAG(dag_id="finance_dag", default_args=default_args, schedule_interval="@daily") as dag:

    t1 = DummyOperator(task_id="t1")

    t2 = BashOperator(
            task_id="t2",
            bash_command="echo 'It works'"
        )

    t1 >> t2