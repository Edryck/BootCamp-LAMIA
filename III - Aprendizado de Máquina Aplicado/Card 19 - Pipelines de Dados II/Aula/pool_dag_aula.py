from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.bash_operator import BashOperator

from datetime import datetime

default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow',
    'email': 'owner@test.com'
}

# No exemplo, uma api com rate limit (precisa criar no Airflow pools com pouco slot), sem o pool, as 3 tasks de cambio
# disparam ao mesmo tempo e a api provavelmente, deveria, retornar um erro de limite excedido
with DAG(dag_id='pool_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    # get forex rates of JPY and push them into XCOM
    # o priority_weight define a prioridade, basicamente, ela vai ser a ultima a pegar o slot do pool na disputa entre as 3
    get_forex_rate_EUR = SimpleHttpOperator(
        task_id='get_forex_rate_EUR',
        method='GET',
        priority_weight=1,
        pool='forex_api_pool',
        http_conn_id='forex_api',
        endpoint='/latest?base=EUR',
        xcom_push=True
    )
 
    # get forex rates of JPY and push them into XCOM
    # esse tem uma prioridade maior, ele seria o intermediario
    get_forex_rate_USD = SimpleHttpOperator(
        task_id='get_forex_rate_USD',
        method='GET',
        priority_weight=2,
        pool='forex_api_pool',
        http_conn_id='forex_api',
        endpoint='/latest?base=USD',
        xcom_push=True
    )

    # get forex rates of JPY and push them into XCOM
    # o com  prioridade mais alta, ela iria ser a primeira a pegar o slot
    get_forex_rate_JPY = SimpleHttpOperator(
        task_id='get_forex_rate_JPY',
        method='GET',
        priority_weight=3,
        pool='forex_api_pool',
        http_conn_id='forex_api',
        endpoint='/latest?base=JPY',
        xcom_push=True
    )
 
    # Templated command with macros
    # Jinja itera todas as task_ids da dag e para cada uma puxa o xcom correspondente
    # via ti.xcom_pull(task) e assim o bash vai imprimir o resultado de cada chamada http
    # sem precisar hardcodar os nomes das tasks um por um
    bash_command="""
        {% for task in dag.task_ids %}
            echo "{{ task }}"
            echo "{{ ti.xcom_pull(task) }}"
        {% endfor %}
    """

    # Show rates
    show_data = BashOperator(
        task_id='show_result',
        bash_command=bash_command
    )

    # Uma lista de tasks para um task, o show_data depende de todas as 3 chamadas terminarem
    # com o pool de 1 slot, a ordem de execucao delas no Gantt View aparece em cascata
    # do priority_weight maior para o menor
    [get_forex_rate_EUR, get_forex_rate_USD, get_forex_rate_JPY] >> show_data