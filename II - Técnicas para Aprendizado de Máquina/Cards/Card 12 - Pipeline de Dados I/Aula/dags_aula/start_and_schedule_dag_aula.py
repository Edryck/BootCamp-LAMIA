from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

from datetime import datetime, timedelta

default_args = {
    'start_date': datetime(2019, 3, 29, 1),
    'owner': 'Airflow'
}

# Teoricamente, a DAG deveria começar a executar toda hora, uma vez por hora
with DAG(dag_id='start_and_schedule_dag', schedule_interval="0 * * * *", default_args=default_args) as dag:
    
    # Task 1
    dummy_task_1 = DummyOperator(task_id='dummy_task_1')
    
    # Task 2
    dummy_task_2 = DummyOperator(task_id='dummy_task_2')
    
    dummy_task_1 >> dummy_task_2
    
    # Porém, a data de inicio e a data agendada não é a mesma, as DAG tem o até uma hora para iniciar
    # Em alguns momentos ela vai estar agendada para começar no miniuto 0 da cada hora, pode acabar começando
    # uma hora depois, basicamente é para mostrar a diferença da data de execução e do real gatilho, onde
    # vai realmente acontecer a execução
    # Logs to help you (printed from the web server logs)
    # Uncomment when you use the DAG, comment when not
    run_dates = dag.get_run_dates(start_date=dag.start_date)
    next_execution_date = run_dates[-1] if len(run_dates) != 0 else None
    print('[DAG:start_and_schedule_dag] start_date: {0} - schedule_interval: {1} - Last execution_date: {2} - next execution_date {3} in UTC'.format(
        dag.default_args['start_date'], 
        dag._schedule_interval, 
        dag.latest_execution_date, 
        next_execution_date
        ))