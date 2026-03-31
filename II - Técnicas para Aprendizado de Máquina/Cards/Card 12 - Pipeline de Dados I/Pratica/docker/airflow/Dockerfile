FROM python:3.11-slim

ARG AIRFLOW_HOME=/usr/local/airflow
ENV AIRFLOW_HOME=${AIRFLOW_HOME}

# Instala dependências do sistema
RUN apt-get update -y && \
    apt-get install -yqq --no-install-recommends \
    netcat-traditional \
    curl \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get autoremove -yqq --purge && apt-get clean

# Cria usuário airflow
RUN useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow

# Instala Airflow e dependências do projeto, é equivalente a um requirements
RUN pip install --upgrade pip && \
    pip install \
    "apache-airflow==2.8.1" \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.11.txt" && \
    pip install \
    "apache-airflow-providers-mysql==3.4.0" \
    "apache-airflow-providers-http==4.10.1" \
    "mysqlclient==2.1.1" \
    "yfinance_cache==0.8.0"

RUN chown -R airflow: ${AIRFLOW_HOME}

COPY ./start-airflow.sh ./start-airflow.sh
RUN chmod +x ./start-airflow.sh

USER airflow
RUN mkdir -p ${AIRFLOW_HOME}/dags ${AIRFLOW_HOME}/data

EXPOSE 8080

CMD ["./start-airflow.sh"]
