from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta

# Um callback exemplo no caso de sucesso
def on_success_dag(dict):
    print("on_success_dag")
    print(dict)

# Um callback exemplo no caso de falha
def on_failure_dag(dict):
    print("on_failure_dag")
    print(dict)

default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow',
    'retries': 3, # Tentará 3 vezes
    'retry_delay': timedelta(seconds=60), # Tempo de espera para repetir
    'emails': ['owner@test.com'], # Email para quem será enviado em caso de falha
    'email_on_failure': True, # Envia, no caso de falha, o email
    'email_on_retry': True, # Envia um email para avaisar que está realizando uma nova tentativa
    # Callbacks
    'on_success_callback': on_success_dag,
    'on_failure_callback': on_failure_dag
}

with DAG(dag_id='alert_dag', 
         schedule_interval="0 0 * * *", 
         default_args=default_args, 
         catchup=True, 
         dagrun_timeout=timedelta(seconds=75), # Vai definir um limite de 75 segundos para a DAG finalizar, se não finalizar neste tempo, ela falha
         on_success_callback=on_success_dag, # Se finalizar com sucesso, chama a função de callback de sucesso 
         on_failure_callback=on_failure_dag # Se falhar, chama a função de callback de falha
         ) as dag:
    
    # Task 1
    t1 = BashOperator(task_id='t1', bash_command="exit 1")
    
    # Task 2
    t2 = BashOperator(task_id='t2', bash_command="echo 'second task'")

    t1 >> t2