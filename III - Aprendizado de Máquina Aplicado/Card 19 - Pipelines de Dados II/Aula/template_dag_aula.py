import sys
import airflow
from airflow import DAG, macros
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta

# Would be cleaner to add the path to the PYTHONPATH variable
# Gambiarra... digo, AT (ajuste técnico)
# o certo e configurar o PYTHONPATH na imagem, não colocar o path manualmente
sys.path.insert(1, '/usr/local/airflow/dags/scripts')

from process_logs import process_logs_func

# String de template para a pasta de logs, que e usado em varias tasks
# var.value.source_path vem de uma Variable cadastrada nas Variables do Airflow
# macros.ds_format reformata a data em tempo de execucao quando a task roda
TEMPLATED_LOG_DIR = """{{ var.value.source_path }}/data/{{ macros.ds_format(ts_nodash, "%Y%m%dT%H%M%S", "%Y-%m-%d-%H-%M") }}/"""

default_args = {
            "owner": "Airflow",
            "start_date": airflow.utils.dates.days_ago(1),
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "email": "youremail@host.com",
            "retries": 1
        }

with DAG(dag_id="template_dag", schedule_interval="@daily", default_args=default_args) as dag:

    # serve para ver o resultado da render do template
    t0 = BashOperator(
            task_id="t0",
            bash_command="echo {{ ts_nodash }} - {{ macros.ds_format(ts_nodash, '%Y%m%dT%H%M%S', '%Y-%m-%d-%H-%M') }}")

    # o bash_command é um template do BashOperator e por aceitar um path de arquivo .sh
    # o conteudo do script e renderizado com Jinja
    t1 = BashOperator(
            task_id="generate_new_logs",
            bash_command="./scripts/generate_new_logs.sh",
            # nao templatizado, e valor estatico
            params={'filename': 'log.csv'}) 

    # test -f retorna exit code 1 se o arquivo nao existir
    # a task via falhar
    t2 = BashOperator(
            task_id="logs_exist",
            bash_command="test -f " + TEMPLATED_LOG_DIR + "log.csv",
            )

    t3 = PythonOperator(
            task_id="process_logs",
            python_callable=process_logs_func,
            provide_context=True,
            # forma de entregar um valor templatizado para o PythonOperator
            templates_dict={'log_dir': TEMPLATED_LOG_DIR},
            # chega cru, nao como o templates_dict
            params={'filename': 'log.csv'}
            )

    t0 >> t1 >> t2 >> t3