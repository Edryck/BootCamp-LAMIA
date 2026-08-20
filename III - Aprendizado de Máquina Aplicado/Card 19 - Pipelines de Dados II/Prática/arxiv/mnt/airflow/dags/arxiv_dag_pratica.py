from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import arxiv
import json
import os

# categorias para ingestao
# Para adicionar uma categoria é só adicionar uma linha aqui, depois uma nova task vai aparecer no grafo
# Acessa o link abaixo para ver todas as categorias do arxiv
# https://arxiv.org/category_taxonomy
categorias = [
    "cs.LG", # Machine Learning
    "cs.AI", # Artificial Intelligence
    "cs.CL", # Computation and Language (NLP)
    # "cs.AR", # Hardware Architecture
]

# Onde os arquivos sao gravados
# Tudo particionado por execution_date, entao reprocessar o mesmo dia sobreescreve em vez de duplicar
CAMINHO = "/opt/airflow/data"

MAX_RESULTS = 100


def ingerir(categoria, **context):
    """
    Ele vai buscar os papers de uma categoria na data de execucao e gravar um json em raw/<ds>/<categoria>.json.

    Retorna o caminho do arquivo e nunca a lsita de papers
    Todo return do PythonOperator vira XCom e XCom e' para metadados, nao para dados
    """
    ds = context["ds"]

    # A api filtra por data no formato YYYYMMDDHHMM, sem separador, então montei uma janela de 24h do dia da execucao
    dia = datetime.strptime(ds, "%Y-%m-%d")
    inicio = dia.strftime("%Y%m%d0000")
    fim = dia.strftime("%Y%m%d2359")
    query = "cat:%s AND submittedDate:[%s TO %s]" % (categoria, inicio, fim)

    # A api do arxiv pede no minimo 3s entre requisicoes
    cliente = arxiv.Client(page_size=100, delay_seconds=3.0, num_retries=3)
    busca = arxiv.Search(
        query=query,
        max_results=MAX_RESULTS,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Ascending,
    )

    papers = []
    for r in cliente.results(busca):
        papers.append({
            "id": r.get_short_id(),
            "titulo": r.title.strip().replace("\n", " "),
            "resumo": r.summary.strip().replace("\n", " "),
            "autores": [a.name for a in r.authors],
            "published": r.published.strftime("%Y-%m-%d") if r.published else None,
            "updated": r.updated.strftime("%Y-%m-%d") if r.updated else None,
            "primary_category": r.primary_category,
            "categories": r.categories,
            "pdf_url": r.pdf_url,
            "abs_url": r.entry_id,
            "categoria_busca": categoria,
        })

    pasta = os.path.join(CAMINHO, "raw", ds)
    os.makedirs(pasta, exist_ok=True)
    destino = os.path.join(pasta, "%s.json" % categoria)

    with open(destino, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)

    print("[%s] %d papers -> %s" % (categoria, len(papers), destino))
    return destino


def validar(**context):
    """
    Confere o que as tasks de ingestao gravaram
    """
    ti = context["ti"]

    # Puxa os caminhos que cada task de ingestao empurrou no xcom
    tarefas = ["ingest_%s" % c.replace(".", "_") for c in categorias]
    caminhos = ti.xcom_pull(task_ids=tarefas)

    problemas = []
    total = 0

    for caminho in caminhos:
        if not os.path.exists(caminho):
            problemas.append("%s: arquivo nao existe" % caminho)
            continue

        with open(caminho, encoding="utf-8") as f:
            papers = json.load(f)

        total += len(papers)

        # Categoria vazia num dia isolado e normal (fim de semana, feriado)
        # Por isso nao to tratando len == 0 como um erro aqui
        for p in papers:
            if not p.get("titulo") or not p.get("resumo"):
                problemas.append("%s: paper %s sem titulo ou resumo" % (caminho, p.get("id")))
            if not p.get("pdf_url"):
                problemas.append("%s: paper %s sem pdf_url" % (caminho, p.get("id")))

    # O que nao pode e as tres categorias vim vazias no mesmo dia, isso seria um sinal que a api ta fora do ar
    if total == 0:
        problemas.append("nenhum paper em nenhuma categoria -- suspeita de falha na API do arXiv")

    if problemas:
        # Levantar excecao marca a task como 'failed' na UI.
        raise ValueError("Validacao falhou:\n" + "\n".join(problemas))

    print("Validacao OK: %d papers em %d categoria(s)" % (total, len(caminhos)))
    return caminhos


def finalizar(**context):
    """
    Junta os jsons das categorias em um arquivo, desduplicando pelo id do paper

    Um paper cross-listed (ex: cs.LG e cs.AI) aparece nos dois arquivos de origem, sem isso o dataset final conta o mesmo paper duas vezes
    """
    ti = context["ti"]
    ds = context["ds"]

    caminhos = ti.xcom_pull(task_ids="validar")

    vistos = {}
    for caminho in caminhos:
        with open(caminho, encoding="utf-8") as f:
            for p in json.load(f):
                # Primeiro que chegar vence; os seguintes sao a mesma coisa.
                if p["id"] not in vistos:
                    vistos[p["id"]] = p

    papers = list(vistos.values())

    pasta = os.path.join(CAMINHO, "processed", ds)
    os.makedirs(pasta, exist_ok=True)
    destino = os.path.join(pasta, "papers.json")

    with open(destino, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)

    print("%d papers unicos -> %s" % (len(papers), destino))
    return destino


default_args = {
    "owner": "edryck",
    "start_date": datetime(2026, 8, 1),
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
    "email_on_failure": False,
}

with DAG(
    dag_id="arxiv_dag",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["arxiv", "ingestao", "minicurso"],
) as dag:

    # Uma task por categoria, todas sao independentes entre si, e isso que permite o scheduler disparar em paralelo
    ingestoes = []
    for categoria in categorias:
        # task_id nao aceita ponto de forma confiavel na UI, entao cs.LG vira cs_LG
        t = PythonOperator(
            task_id="ingest_%s" % categoria.replace(".", "_"),
            python_callable=ingerir,
            op_kwargs={"categoria": categoria},
        )
        ingestoes.append(t)

    validar_task = PythonOperator(
        task_id="validar",
        python_callable=validar,
    )

    finalizar_task = PythonOperator(
        task_id="finalizar",
        python_callable=finalizar,
    )

    # Uma lista >> uma task = a task depende de todas as da lista.
    ingestoes >> validar_task >> finalizar_task