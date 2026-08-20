import airflow
import requests
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator

default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

# Sao tres apis diferentes de geolocalizacao por ip, a ideia da dag
# e descobrir quais delas estao respondendo corretamente no momento da execucao
# e seguir so pelos caminhos das que funcionaram
IP_GEOLOCATION_APIS = {
    'ip-api': 'http://ip-api.com/json/',
    'ipstack': 'https://api.ipstack.com/',
    'ipinfo': 'https://ipinfo.io/json'
}

# Try to get the country_code field from each API
# If given, the API is returned and the next task corresponding
# to this API will be executed
def check_api():
    apis = []
    for api, link in IP_GEOLOCATION_APIS.items():
        r = requests.get(link)
        try:
            data = r.json()
            # So considera se a api e boa, se ela devolveu um json valido
            # e o campo country veio preenchido
            if data and 'country' in data and len(data['country']):
                # a api aqui e a chave do dict o que tambem é o task_id do DummyyOperator criado
                # mais para baixo para essa api
                apis.append(api)
        except ValueError:
            # se o r.json() falhou, a resposta nao era json valido, a api fora do ar, por exemplo, simplesmente
            # ignora continua
            pass
    # O BranchPythonOperator tem o retorno que decide quais taks_id rodam em seguida
    # Pode ser uma lista com varios caminhos ou uma string unica, se nenhuma api respondeu,
    # cai no caminho none
    return apis if len(apis) > 0 else 'none'

with DAG(dag_id='branch_dag', 
    default_args=default_args, 
    schedule_interval="@once") as dag:

    # BranchPythonOperator
    # The next task depends on the return from the
    # python function check_api

    check_api = BranchPythonOperator(
        task_id='check_api',
        python_callable=check_api
    )

    none = DummyOperator(
        task_id='none'
    )

    # O trigger rule e o que vai permitir essa task rodar mesmo que as outras tasks tenham ficado skipped
    # o padrão do trigger e all_success, o save nao rodaria porque sempre existe pelo menos um caminho skipped
    save = DummyOperator(task_id='save', trigger_rule='one_success')

    check_api >> none >> save

    # Dynamically create tasks according to the APIs
    # Gera dinamicamente uma task por api, com task_id igual o nome da api, por isso o retorno de check_api()
    # bate com as task_ids
    for api in IP_GEOLOCATION_APIS:
        process = DummyOperator(
            task_id=api
        )
    
        check_api >> process >> save