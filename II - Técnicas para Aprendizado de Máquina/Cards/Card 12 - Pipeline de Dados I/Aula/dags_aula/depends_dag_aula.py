from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from datetime import datetime, timedelta

default_args = {
    # Data de início do DAG
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow'
}

def second_task():
    print('Hello from second_task')
    #raise ValueError('This will turns the python task in failed state')

def third_task():
    print('Hello from third_task')
    #raise ValueError('This will turns the python task in failed state')

# Ele é executado todo dia à meia noite, como pode ver no schedule_interval
with DAG(dag_id='depends_task', schedule_interval="0 0 * * *", default_args=default_args) as dag:
    
    # Task 1, ela executa um comando para imprimir first task
    # Com o wait_for_downstream, ela vai esperar que todas as tarefas anteriores, da instância anterior, terminem com sucesso antes de ser executada
    bash_task_1 = BashOperator(task_id='bash_task_1', bash_command="echo 'first task'", wait_for_downstream=True)
    
    # Task 2, nessa, ela chama da função second_task, que por sua vez, imprime o print dentro da função
    # o depends_on_past recebendo True faz ela depender da última execução, se na última execução
    # ter falhado, na próxima ela não vai fazer nada
    # python_task_2 = PythonOperator(task_id='python_task_2', python_callable=second_task. depends_on_past=True)
    python_task_2 = PythonOperator(task_id='python_task_2', python_callable=second_task)

    # Task 3, quase o mesmo que a segunda, de diferente ela tem o id e chama a função third_task
    python_task_3 = PythonOperator(task_id='python_task_3', python_callable=third_task)

    bash_task_1 >> python_task_2 >> python_task_3