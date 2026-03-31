import pytest
from airflow.models import DagBag

# Uma função que é executada antes do teste para inserir dados nos testes
# O scope  de session define que a função será executada apenas uma vez
@pytest.fixture(scope="session")
def dagbag():
    return DagBag()