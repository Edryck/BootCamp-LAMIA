import pendulum
from airflow import DAG
from airflow.utils import timezone
from airflow.operators.dummy_operator import DummyOperator

from datetime import timedelta, datetime
# Define o local com o fuso horário de Paris na Europa
local_tz = pendulum.timezone("Europe/Paris")

# Argumentos padrão para o DAG
default_args = {
    # Data agendada para ele iniciar, com o fuso horário ali de cima 
    'start_date': datetime(2019, 3, 29, 2, tzinfo=local_tz),
    # Dono da tarefa
    'owner': 'Airflow'
}

# Instancia um DAG, os argumentos:
# dag_id: o id do DAG
# schedule_interval: intervalo que ele ocorre, da esquerda para direita, os asteriscos correspondem a min, h, dia do mes, mes, dia da semana
# neste caso, todo dia as duas da manhã é o interval que ele vai iniciar
# e os argumentos padrões: default_args
with DAG(dag_id='tz_dag', schedule_interval="0 2 * * *", default_args=default_args) as dag:
    # Uma tarefa fictícia, usada só para exemplo
    dummy_task = DummyOperator(task_id='dummy_task')
    
    # Pega a data de execução
    run_dates = dag.get_run_dates(start_date=dag.start_date)
    # Pega a próxima data de execução
    next_execution_date = run_dates[-1] if len(run_dates) != 0 else None
    
    # Printa na tela com a data e hora do python e do airflow para comparação e data e hora do DAG
    print('datetime from Python is Naive: {0}'.format(timezone.is_naive(datetime(2019, 9, 19))))
    print('datetime from Airflow is Aware: {0}'.format(timezone.is_naive(timezone.datetime(2019, 9, 19)) == False))
    print('[DAG:tz_dag] timezone: {0} - start_date: {1} - schedule_interval: {2} - Last execution_date: {3} - next execution_date {4} in UTC - next execution_date {5} in local time'.format(
        dag.timezone, 
        dag.default_args['start_date'], 
        dag._schedule_interval, 
        dag.latest_execution_date, 
        next_execution_date,
        local_tz.convert(next_execution_date) if next_execution_date is not None else None
        ))