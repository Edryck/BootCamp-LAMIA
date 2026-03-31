from airflow import DAG
# Sensores
from airflow.sensors.http_sensor import HttpSensor
from airflow.contrib.sensors.file_sensor import FileSensor
# Operadores
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.hive_operator import HiveOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.slack_operator import SlackAPIPostOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta

import csv
import requests
import json

default_args = {
            # Dono de tarefa
            "owner": "airflow",
            # Data de início
            "start_date": datetime(2019, 1, 1),
            # Não depende da anterior
            "depends_on_past": False,
            # Não vai enviar um email caso tenha falhado
            "email_on_failure": False,
            # Nõa vai enviar um email em uma nova tentativa
            "email_on_retry": False,
            # Email que será enviado
            "email": "youremail@host.com",
            # Número de tentativa, vai fazer apenas uma vez
            "retries": 1,
            # Tempo de espera para fazer uma nova tentativa
            "retry_delay": timedelta(minutes=5)
        }

# Função para baixar as moedas e suas taxas de conversões
def download_rates():
    # Abre o arquivo CSV de moedas
    with open('/usr/local/airflow/dags/files/forex_currencies.csv') as forex_currencies:
        # Vai ler linha por linha
        reader = csv.DictReader(forex_currencies, delimiter=';')
        for row in reader:
            # Pega a moeda base
            base = row['base']
            # Pega as moedas de conversões
            with_pairs = row['with_pairs'].split(' ')
            # Envia uma requisição para API, usa a moeda base e traz as taxas de conversões em um JSON
            indata = requests.get('https://api.exchangeratesapi.io/latest?base=' + base).json()
            # Filtra os resultados da requisição para ter apenas a moeda base e as taxas de conversões do CSV e sua última atualização
            outdata = {'base': base, 'rates': {}, 'last_update': indata['date']}
            for pair in with_pairs:
                outdata['rates'][pair] = indata['rates'][pair]
            # Abre um arquivo, se não existir, vai criar ele, com as taxas de conversões e a moeda base
            with open('/usr/local/airflow/dags/files/forex_rates.json', 'a') as outfile:
                # Apaga o antigo
                json.dump(outdata, outfile)
                # Escreve o novo
                outfile.write('\n')

# Instancia uma DAG nova, os argumentos são:
# dag_id: o id, basicamente o identificador
# schedule_interval: intervalo de execução, neste caso, uma vez por dia
# default_args: argumentos padrão que vai ser utilizado para criar uma tarefa
# catchup: não entendi esse, mas na aula, ele diz que é False para evitar que o DAG ultrapasse diagramas
with DAG(dag_id="forex_data_pipeline", schedule_interval="@daily", default_args=default_args, catchup=False) as dag:
    
    # Para ver se as taxas estão disponíveis
    is_forex_rates_available = HttpSensor(
        # id da tarefa
        task_id="is_forex_rates_available",
        # Tipo de requisição
        method="GET",
        # id da conexão criada no airflow
        http_conn_id="forex_api",
        # Final da URL
        endpoint="latest",
        # Verificação da resposta, usa uma função lambda para checar se as taxas estão na resposta
        response_check=lambda response: "rates" in response.text,
        # Quantidade de verificações
        poke_interval=5,
        # Tempo em que vai ficar realizando a verificação, quando passar deste tempo, ela para
        timeout=20
    )

    # Para ver se o arquivo das moedas está disponível
    is_forex_currencies_file_available = FileSensor(
        # id da tarefa
        task_id="is_forex_currencies_file_available",
        # Conexão criada no airflow, nela está o caminho do arquivo dentro do contêiner
        fs_conn_id="forex_path",
        # Caminho do arquivo CSV
        filepath="forex_currencies.csv",
        # Quantidade de verificações que irá fazer
        poke_interval=5,
        # Tempo em que irá estar fazendo as verificações
        timeout=20
    )

    # Tarefa para baixar as taxas, ela irá chamar a função feita lá em ci
    downloading_rates = PythonOperator(
        # id da tarefa
        task_id="downloading_rates",
        # Função python que será chamada
        python_callable=download_rates
    )

    # Tarefa para salvar as taxas
    saving_rates = BashOperator(
        # id da tarefa
        task_id="saving_rates",
        # Comando bash que será feito dentro do contêiner
        bash_command="""
            hdfs dfs -mkdir -p /forex && \
            hdfs dfs -put -f $AIRFLOW_HOME/dags/files/forex_rates.json /forex
            """
    )

    # Tarefa para criar a tabela da taxas no Hive
    creating_forex_rates_table = HiveOperator(
        # id da tarefa
        task_id="creating_forex_rates_table",
        # Conexão do Hive criada no airflow
        hive_cli_conn_id="hive_conn",
        # Código SQL que será executado, se a tabela não existe (primeiro caso), ele cria uma, senão, não faz nada
        hql="""
            CREATE EXTERNAL TABLE IF NOT EXISTS forex_rates(
                base STRING,
                last_update DATE,
                eur DOUBLE,
                usd DOUBLE,
                nzd DOUBLE,
                gbp DOUBLE,
                jpy DOUBLE,
                cad DOUBLE
                )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """
    )

    # Tarefa para processar as taxas de conversão, notei agora que seria mais correto chamar de câmbio
    forex_processing = SparkSubmitOperator(
        # id da tarefa
        task_id="forex_processing",
        # Conexão, com o Spark, criada no airflow 
        conn_id="spark_conn",
        # Local do arquivo python que irá processar as taxas
        application="/usr/local/airflow/dags/scripts/forex_processing.py",
        verbose=False
    )

    # Tarefa para enviar o email caso tenha sido realizado com sucesso a pipeline
    sending_email_notification = EmailOperator(
        # id da tarefa
        task_id="sending_email",
        # Email para quem será enviado
        to="airflow_course@yopmail.com",
        # Assunto do email
        subject="forex_data_pipeline",
        # Conteúdo do email em HTML
        html_content="""
            <h3>forex_data_pipeline succeeded</h3>
        """
    )

    # Tarefa semelhante com a anterior, ela vai mandar no chat do Slack
    sending_slack_notification = SlackAPIPostOperator(
        # id da tarefa
        task_id="sending_slack",
        # Conexão criada no airfow, nela está a URL da API
        slack_conn_id="slack_conn",
        # Nome do bot criado no Slack
        username="airflow",
        # Texto que será enviado
        text="DAG forex_data_pipeline: DONE",
        # Canal onde o texto será enviado
        channel="#airflow-exploit"
    )