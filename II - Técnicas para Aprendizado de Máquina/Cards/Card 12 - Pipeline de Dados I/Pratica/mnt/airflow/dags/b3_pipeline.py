from airflow import DAG
from airflow.sensors.python import PythonSensor
from airflow.operators.python import PythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime, timedelta
import yfinance_cache as yfc
import pandas as pd
import json

# Ações da B3, bolsa de valores brasileira
# OBS.: No yfinance é necessário colocar o .SA, ele indica ao Yahoo Finance qye está sendo buscado o ativo no mercado brasileiro
tickers = ["PETR4.SA", # Petrobras
           "VALE3.SA", # Vale
           "ITUB4.SA", # Itaú
           "BBDC4.SA", # Bradesco
           "WEGE3.SA", # Weg
           "BBAS3.SA", # Banco do Brasil
           "ABEV3.SA"] # Ambev

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes = 5)
}

def check_yahoo():
    df = yfc.download(tickers = "PETR4.SA", period="1d", progress=False)
    return not df.empty

def download_b3_data():
    # lista onde vai ser armazenado os dataframes
    all_data = []

    for ticker in tickers:
        # Armazena em um dataframe, o yf.download retorna um dataframe
        df = yfc.download(
            ticker,
            period = "1d", # Pega o último dia 1 dia
            interval = "1d", # Em intervalos de um dia
            progress = False
        )

        # Verifica se os dados do ticker estão vazios, se estiver, ele só pula pra o próximo
        if df.empty:
            print(f"Sem dados para {ticker}")
            continue

        # Adiciona coluna com o nome do ticker
        df["Ticker"] = ticker
        df.reset_index(inplace = True)
        all_data.append(df)
        # printa a quantidadde de registros extraídos do ticker
        print(f"{ticker}: {len(df)} registros baixados")

    if not all_data:
        raise ValueError("Nenhum dado foi baixado")

    # Junta todos os dataframes em um único dataframe
    combined = pd.concat(all_data, ignore_index = True)
    # Printa na tela a quantidade de registros de extraídos no total
    print(f"Total de registros: {len(combined)}")
    # O orient é um método do Pandas que define a estrutura do JSON gerado,
    # no caso do records, significa que a estrutura gerada é uma lista de dicionários
    return combined.to_json(orient = "records")

# Pega os dados baixados pela tarefa e salva em um arquivo CSV com a data atual
def save_to_csv(**context):
    # Pega os dados do task anterior via XCom
    json_data = context["ti"].xcom_pull(task_ids = "download_b3_data")

    # Mostra na tela que não foi recebido nenhum dado da outra tarefa, no caso de vir uma JSON vazio
    # Basicamente, o raise ValueError está substituindo o bloco try/catch/finally
    if not json_data:
        raise ValueError("Nenhum dado recebido da tarefa anterior")

    # Lê o JSON e passa os dados para um dataframe
    df = pd.read_json(json_data)

    # Nome do arquivo com a data de execução
    execution_date = context["execution_date"].strftime("%Y-%m-%d")
    filename = f"/usr/local/airflow/data/b3_data_{execution_date}.csv"
    # Salva como um CSV na pasta acima com a data de execução
    df.to_csv(filename, index = False)
    print(f"Quantidade total de registros salvos: {len(df)}")

# Gera um resumo dos dados coletados com a maior alta e queda do dia e variação percentual de cada ação
def generate_summary(**context):
    # Esta tarefa teoricamente deveria rodar em paralelo com a de salvar em um CSV, ela não depende a save_to_csv
    # Recebe os dados de donwload, via XCom
    json_data = context["ti"].xcom_pull(task_ids = "download_b3_data")
    df = pd.read_json(json_data)

    # Pega apenas o último dia disponível para cada ticker
    df["Date"] = pd.to_datetime(df["Date"])
    latest = df.sort_values("Date").groupby("Ticker").last().reset_index()
    # Calcula variação percentual entre o valor da ação na abertura do mercado e no fechamento dele
    # Fórmula para calcular: Percentual de variação = (fechamento - abertura) / (abertura * 100)
    latest["Variacao_%"] = ((latest["Close"] - latest["Open"]) / latest["Open"] * 100).round(2)

    # Ordena por maior variação
    latest = latest.sort_values("Variacao_%", ascending = False)

    for i, row in latest.iterrows():
        # Alt + 30: ▲, significa que fechou em alta
        # Alt + 31: ▼, significa que fechou em baixa
        sinal = "▲" if row["Variacao_%"] > 0 else "▼"
        print(f"{row['Ticker']}: R${row['Close']:.2f} {sinal} {abs(row['Variacao_%'])}%")

    print(f"\nMaior alta: {latest.iloc[0]['Ticker']} ({latest.iloc[0]['Variacao_%']}%)")
    print(f"Maior queda: {latest.iloc[-1]['Ticker']} ({latest.iloc[-1]['Variacao_%']}%)")

    # Salva o resumo em JSON
    execution_date = context["execution_date"].strftime("%Y-%m-%d")
    summary_file = f"/usr/local/airflow/data/b3_summary_{execution_date}.json"
    latest[["Ticker", "Close", "Volume", "Variacao_%"]].to_json(summary_file, orient = "records", indent = 2)
    print(f"\nResumo salvo em: {summary_file}")


with DAG(
    dag_id = "b3_data_pipeline",
    schedule_interval = "@daily", # Todos os dias a meia noite
    default_args = default_args,
    catchup = False
    ) as dag:

    # Verifica se o Yahoo Finance está acessível
    is_yahoo_finance_available = PythonSensor(
        task_id = "is_yahoo_finance_available",
        python_callable = check_yahoo,
        poke_interval = 5,
        timeout = 20 # Finaliza depois de 20 segundos
    )

    # Baixa os dados de todas as ações da lista de tickers
    download_data = PythonOperator(
        task_id = "download_b3_data",
        python_callable = download_b3_data
    )

    # Salva os dados em uma arquivo CSV
    save_data = PythonOperator(
        task_id = "save_to_csv",
        python_callable = save_to_csv,
        provide_context = True
    )

    # Gera o resumo do diário
    summarize = PythonOperator(
        task_id = "generate_summary",
        python_callable = generate_summary,
        provide_context = True
    )

    # Envia um email quando a pipeline finalizar
    sending_email_notification = EmailOperator(
        task_id = "sending_email_notification",
        to = "edryckfreitas@gmail.com", # Para quem será enviado
        subject = "Pipeline de Dados B3", # Assunto do email
        # Conteúdo do email... Seria melhor fazer algo mais bonito, mas isso é só para teste
        html_content = """
            <h2>Pipeline de Dados B3 finalizada com sucesso!</h2>
        """
    )

    # Envia uma mensagem no discord
    sending_discord_message = SimpleHttpOperator(
        task_id = "sending_discord_message",
        http_conn_id = "discord_conn", # Conexão criada no airflow
        # var.value é usao para acessar a variável criada no Airflow diretamente, sem precisar
        # criar uma variável recebendo um get.Variable("<nome-da-variavel") e tendo que importar Variable
        endpoint = "/api/webhooks/{{ var.value.webhook_id }}/{{ var.value.webhook_token }}",
        method = "POST", # Tipo de requisição
        headers = {"Content-Type": "application/json"},
        data = json.dumps({"content": "Pipeline B3 finalizada com sucesso!"}), # Conteúdo da mensagem quserá enviada
        do_xcom_push=False # Não lembro para que serve, mas sem colocar ele como False dava erro, ele por padrão vem como True
    )

    # Ordem de execução das tasks
    is_yahoo_finance_available >> download_data >> save_data >> summarize >> sending_email_notification >> sending_discord_message
