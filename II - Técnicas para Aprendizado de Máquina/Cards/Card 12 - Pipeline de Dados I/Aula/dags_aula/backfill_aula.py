from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta

default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow'
}

# Vai rodar todo dia à meia noite
# O Catchup vai definir se o agendador vai realizar todas as instâncias passadas, desde a data de inicio (start_date)
with DAG(dag_id='backfill', schedule_interval="0 0 * * *", default_args=default_args, catchup=False) as dag:
    
    # Exemplo de tarefa
    # Task 1
    bash_task_1 = BashOperator(task_id='bash_task_1', bash_command="echo 'first task'")
    
    # Exemplo de tarefa 2
    # Task 2
    bash_task_2 = BashOperator(task_id='bash_task_2', bash_command="echo 'second task'")

    # Sequência de tarefas
    bash_task_1 >> bash_task_2