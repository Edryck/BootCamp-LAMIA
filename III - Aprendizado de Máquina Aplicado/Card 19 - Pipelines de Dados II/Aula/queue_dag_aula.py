from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator

from datetime import datetime

default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow',
    'email': 'owner@test.com'
}

# Tecnicamente, funciona com o CeleryExecutor e com no minimo um worker
# executando cada fila declarada abaixo
# Sem isso a task fica presa no queued e sem erro aparente
# Mas a ideia e que tasks que precisa de um hardware diferente vai para workers
# diferentes e não todas competirem pelo mesmo pool de maquinas
with DAG(dag_id='queue_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:

    # tasks de entrada e saida intensivo, um fila de um worker com ssd
    t_1_ssd = BashOperator(task_id='t_1_ssd', bash_command='echo "I/O intensive task"', queue='worker_ssd')

    t_2_ssd = BashOperator(task_id='t_2_ssd', bash_command='echo "I/O intensive task"', queue='worker_ssd')

    t_3_ssd = BashOperator(task_id='t_3_ssd', bash_command='echo "I/O intensive task"', queue='worker_ssd')

    # tasks de cpu intensiva, uma fila de um worker com mais nucleos
    t_4_cpu = BashOperator(task_id='t_4_cpu', bash_command='echo "CPU instensive task"', queue='worker_cpu')

    t_5_cpu = BashOperator(task_id='t_5_cpu', bash_command='echo "CPU instensive task"', queue='worker_cpu')

    # tasks dependecia mais especifica, neste caso, um worker que tem o Spark
    t_6_spark = BashOperator(task_id='t_6_spark', bash_command='echo "Spark dependency task"', queue='worker_spark')

    # ultima task que nao executa nada, ele so e o ponto de juncao do grafo
    task_7 = DummyOperator(task_id='task_7')

    # a task 7 depende de todas as 6 tasks acima
    # cada uma rodando em sua fila
    [t_1_ssd, t_2_ssd, t_3_ssd, t_4_cpu, t_5_cpu, t_6_spark] >> task_7
        