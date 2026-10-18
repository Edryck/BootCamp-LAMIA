from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import arxiv
import json
import os
import requests
import time

# categorias para ingestao
# Para adicionar uma categoria é só adicionar uma linha aqui, depois uma nova task vai aparecer no grafo
# Acessa o link abaixo para ver todas as categorias do arxiv
# https://arxiv.org/category_taxonomy
categorias = [
    # "cs.LG", # Machine Learning
    "cs.AI", # Artificial Intelligence
    "cs.CL", # Computation and Language (NLP)
    # "cs.AR", # Hardware Architecture
]

# Onde os arquivos sao gravados
# Tudo particionado por execution_date, entao reprocessar o mesmo dia sobreescreve em vez de duplicar
CAMINHO = "/opt/airflow/data"

MAX_RESULTS = 100

# Quantos PDFs baixar por dia 
# Pra baixar todos e so trocar por None, mas conta ~4s por PDF: 300 papers no dia = mais de 20 min so de download
MAX_PDFS_POR_DIA = 25

# Pausa entre um download e outro, o arXiv pede no minimo 3s entre requisicoes
PAUSA_PDF = 3

# Identifica quem ta baixando, o arXiv prefere isso a um User-Agent generico
HEADERS = {"User-Agent": "arxiv-airflow-lamia/1.0 (projeto academico)"}


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

    # A api do arxiv pede no minimo 3s entre requisicoes (usei 5s pra ter folga)
    # Se ela responder 429/503 a lib tenta de novo ate num_retries vezes antes de falhar a task
    cliente = arxiv.Client(page_size=100, delay_seconds=5.0, num_retries=5)
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


def baixar_pdfs(**context):
    """
    Baixa o PDF de cada paper unico do dia, direto do pdf_url que a api devolveu, para pdfs/<ds>/<id>.pdf

    Roda DEPOIS do finalizar de proposito: la o paper cross-listed ja foi desduplicado, entao cada PDF e baixado uma vez so
    E uma task unica (e nao uma por categoria) por causa do limite do arXiv de 1 requisicao a cada 3s: varias tasks em paralelo estourariam isso

    Se a task cair e o airflow tentar de novo, os PDFs que ja estao na pasta sao pulados
    Grava tambem um manifesto.json (id -> caminho do pdf) pra quem for consumir os PDFs depois
    """
    ti = context["ti"]
    ds = context["ds"]

    caminho_papers = ti.xcom_pull(task_ids="finalizar")
    with open(caminho_papers, encoding="utf-8") as f:
        papers = json.load(f)

    if MAX_PDFS_POR_DIA is not None:
        papers = papers[:MAX_PDFS_POR_DIA]

    pasta = os.path.join(CAMINHO, "pdfs", ds)
    os.makedirs(pasta, exist_ok=True)

    manifesto = {}
    falhas = []

    for p in papers:
        # O id novo e tipo 2510.01234v1, mas o formato antigo tem barra (hep-th/9901001) e barra nao serve de nome de arquivo
        destino = os.path.join(pasta, p["id"].replace("/", "_") + ".pdf")

        # Ja baixou numa tentativa anterior, nao precisa bater no arXiv de novo
        if os.path.exists(destino):
            manifesto[p["id"]] = destino
            continue

        try:
            # stream=True pra ir gravando aos poucos em vez de segurar o PDF inteiro na memoria
            with requests.get(p["pdf_url"], headers=HEADERS, timeout=60, stream=True) as r:
                r.raise_for_status()
                # Grava num .part e so renomeia no final: se cair no meio nao fica um PDF pela metade com nome de PDF bom
                with open(destino + ".part", "wb") as f:
                    for i, bloco in enumerate(r.iter_content(chunk_size=65536)):
                        # Todo PDF comeca com %PDF. Se nao comecar, veio uma pagina de erro em html
                        if i == 0 and not bloco.startswith(b"%PDF"):
                            raise ValueError("a resposta nao e um PDF")
                        f.write(bloco)
            os.replace(destino + ".part", destino)
            manifesto[p["id"]] = destino
        except Exception as e:
            falhas.append("%s: %s" % (p["id"], e))

        # So pausa quando bateu no arXiv (os que foram pulados acima nao passam por aqui)
        time.sleep(PAUSA_PDF)

    with open(os.path.join(pasta, "manifesto.json"), "w", encoding="utf-8") as f:
        json.dump(manifesto, f, ensure_ascii=False, indent=2)

    print("%d de %d PDFs em %s" % (len(manifesto), len(papers), pasta))

    if falhas:
        # Levanta depois de tentar todos: o retry do airflow so refaz os que faltaram (os outros sao pulados)
        raise ValueError("Falhou o download de %d PDF(s):\n%s" % (len(falhas), "\n".join(falhas)))

    return pasta


default_args = {
    "owner": "edryck",
    # Mudei de 2026-08-01 pra 2026-10-04: com catchup=True (abaixo) a primeira execucao
    # processa cada dia desde essa data ate ontem, uns 10 dias de papers de uma vez
    # Pra pegar mais dias e so voltar essa data
    "start_date": datetime(2026, 10, 4),
    # O 429 do arXiv e' bloqueio temporario: esperar mais entre as tentativas resolve
    # 5min, 10min, 20min... (ate no maximo 30min)
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=30),
    "email_on_failure": False,
}

with DAG(
    dag_id="arxiv_dag",
    default_args=default_args,
    schedule="@daily",
    # catchup=True: sem isso o start_date nao adianta nada, o airflow so rodaria o ultimo dia
    # Com max_active_runs=1 os dias atrasados rodam um de cada vez, o que tambem ajuda a respeitar o limite do arXiv
    catchup=True,
    max_active_runs=1,
    tags=["arxiv", "ingestao", "minicurso"],
) as dag:

    # Uma task por categoria, independentes entre si (mas com max_active_tis_per_dag=1 abaixo elas rodam uma por vez)
    ingestoes = []
    for categoria in categorias:
        # task_id nao aceita ponto de forma confiavel na UI, entao cs.LG vira cs_LG
        t = PythonOperator(
            task_id="ingest_%s" % categoria.replace(".", "_"),
            python_callable=ingerir,
            op_kwargs={"categoria": categoria},
            # O limite do arXiv (1 requisicao a cada 3s) vale pro IP inteiro, nao por task
            # Com as 3 categorias em paralelo elas estouravam o limite juntas (HTTP 429)
            # 1 = roda uma ingestao por vez, na mesma DAG run
            max_active_tis_per_dag=1,
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

    baixar_pdfs_task = PythonOperator(
        task_id="baixar_pdfs",
        python_callable=baixar_pdfs,
    )

    # Uma lista >> uma task = a task depende de todas as da lista.
    ingestoes >> validar_task >> finalizar_task >> baixar_pdfs_task