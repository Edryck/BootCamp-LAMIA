# Script to add new DAGs folders using 
# the class DagBag
# Paths must be absolute
# Este script é o exemplo para organizar as DAGs em pastas, neste caso, projetc_a_aula e project_b_aula
import os
from airflow.models import DagBag
dags_dirs = [
               # Caminhos necessários para acessar
                '/usr/local/airflow/project_a_aula', 
                '/usr/local/airflow/project_b_aula'
            ]

# Para cada diretório na lista de diretórios
for dir in dags_dirs:
   # Armazena cada dag
   dag_bag = DagBag(os.path.expanduser(dir))


   if dag_bag:
      # Vai pegar cada dag
      for dag_id, dag in dag_bag.dags.items():
         # E adicionar em dicionário
         globals()[dag_id] = dag