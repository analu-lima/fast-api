from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def teste_listar_alunos():
    response = client.get("/alunos")
    assert response.status_code == 200
    assert "alunos" in response.json()

def teste_buscar_aluno_existente():
    response = client.get("/alunos/1")
    assert response.status_code == 200
    assert response.json()["aluno"]["id"] == 1

def teste_buscar_aluno_inexistente():
    response = client.get("/alunos/999")
    assert response.status_code == 404

def test_criar_aluno():
    novo_aluno = {
        "nome": "Ana Luisa Lima",
        "email": "analima@gmail.com",
    }
    response = client.post("/alunos", json=novo_aluno)
    assert response.status_code == 200
    assert response.json()["aluno"]["nome"] == "Ana Luisa Lima"

def teste_criar_aluno_dados_incompletos():
    aluno_incompleto = {"nome": "Somente o nome"}
    response = client.post("/alunos", json=aluno_incompleto)
    assert response.status_code == 200
    assert response.json()["aluno"]["email"] is None

@pytest.mark.xfail(reason="Este teste demonstra uma falha esperada...")
def teste_criar_aluno_sem_campo_obrigatorio():
    response = client.post(
        "/alunos",
        json={"email": "semnome@exemplo.com"},
    )
    assert response.status_code == 422
    assert "Campo 'nome' é obrigatório" in response.json()["detail"]