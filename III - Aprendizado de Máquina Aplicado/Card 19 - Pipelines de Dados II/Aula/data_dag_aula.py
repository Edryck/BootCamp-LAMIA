import pprint as pp
import airflow.utils.dates
from airflow import DAG, macros
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# o days_ago(10) com o catchup padrao faz o airflow disparar 10 DagRuns de uma vez
# quando ativar a dag para gerar um histórico instantaneo para popular dashboards de metricas
default_args = {
        "owner": "airflow", 
        "start_date": airflow.utils.dates.days_ago(10),
    }

with DAG(dag_id="data_dag", default_args=default_args, schedule_interval="@daily") as dag:

    upload = DummyOperator(task_id="upload")

    process = BashOperator(
            task_id="process",
            bash_command="echo 'processing'"
        )

    # This task will fail half the time based
    # based on the day of the execution date modulo 2
    # If day 16 % 2 = exit 0
    # If day 17 % 2 = exit 1

    # O {{macros.ds_format(...)}} e um template Jinja que vai ser renderizado em tempo de execucao
    # so extrai o dia da execution_date, o resto do bash_command e um script comum que decide o 
    # exit code no dia
    # Os resultados seriam a task falhar em dias impares e passar em dias pares de forma deterministica
    # o que e util para gerar as metricas de sucesso ou falha previsiveis no dashboard de teste
    fail = BashOperator(
            task_id="fail",
            bash_command="""
                valid={{macros.ds_format(ds, "%Y-%m-%d", "%d")}}
                if [ $(($valid % 2)) == 1 ]; then
                        exit 1
                else
                        exit 0
                fi
            """
        )

    upload >> process >> fail