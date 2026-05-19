from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime

client = TestClient(app)

# Teste de cadastrar aluno
def test_post():
    lista = client.get("/api/v1/alunos/").json()

    # Filtra os alunos do curso GES para encontrar a última matrícula
    ges_existentes = [
        aluno for aluno in lista
        if aluno["curso"] == "GES"
    ]
    ultimo = max([a["matricula"] for a in ges_existentes], default=0)

    # Cria três alunos GES
    for i in range(1, 4):
        res = client.post("/api/v1/alunos/", json={
            "nome": f"GES{i}",
            "email": f"ges{i}@hotmail.com",
            "curso": "GES"
        })
        assert res.status_code == 201
        assert res.json()["id"] == f"GES{i + ultimo}"
        assert res.json()["matricula"] == i + ultimo
        assert res.json()["nome"] == f"GES{i}"
        assert res.json()["email"] == f"ges{i}@hotmail.com"
        assert res.json()["curso"] == "GES"

    # Filtra os alunos do curso GEC para encontrar a última matrícula
    gec_existentes = [
        aluno for aluno in lista
        if aluno["curso"] == "GEC"
    ]
    ultimo = max([a["matricula"] for a in gec_existentes], default=0)

    # Cria três alunos GEC
    for i in range(1, 4):
        res = client.post("/api/v1/alunos/", json={
            "nome": f"GEC{i}",
            "email": f"gec{i}@hotmail.com",
            "curso": "GEC"
        })
        assert res.status_code == 201
        assert res.json()["id"] == f"GEC{i + ultimo}"
        assert res.json()["matricula"] == i + ultimo
        assert res.json()["nome"] == f"GEC{i}"
        assert res.json()["email"] == f"gec{i}@hotmail.com"
        assert res.json()["curso"] == "GEC"

# Teste de listar alunos
def test_get_all():
    aluno = criar_aluno()

    res = client.get("/api/v1/alunos/")
    assert res.status_code == 200
    assert any(a["id"] == aluno["id"] for a in res.json())

# Teste de buscar aluno por ID
def test_get_by_id():
    aluno = criar_aluno()
    
    res = client.get(f"/api/v1/alunos/{aluno['id']}")
    assert res.status_code == 200
    assert res.json()["id"] == f"{aluno['id']}"
    assert res.json()["matricula"] == aluno['matricula']
    assert res.json()["nome"] == aluno["nome"]
    assert res.json()["email"] == aluno["email"]
    assert res.json()["curso"] == aluno["curso"]

# Teste de atualizar aluno por completo
def test_put():
    aluno = criar_aluno()
    
    put = client.put(f"/api/v1/alunos/{aluno['id']}", json={
        "nome": "GEP_put",
        "email": "gep_put@hotmail.com",
        "curso": "GEP"
    })
    assert put.status_code == 200
    assert put.json()["nome"] == "GEP_put"
    assert put.json()["email"] == "gep_put@hotmail.com"
    assert put.json()["curso"] == "GEP"

    res = client.get(f"/api/v1/alunos/{put.json()['id']}")
    assert res.status_code == 200
    assert res.json()["id"] == aluno["id"]
    assert res.json()["matricula"] == aluno["matricula"]
    assert res.json()["nome"] == "GEP_put"
    assert res.json()["email"] == "gep_put@hotmail.com"
    assert res.json()["curso"] == "GEP"

# Teste de atualizar aluno parcialmente
def test_patch(): 
    aluno = criar_aluno(curso="GEC")

    res = client.patch(f"/api/v1/alunos/{aluno['id']}", json={
        "nome": "GEC_patch_novo"
    })
    assert res.status_code == 200
    assert res.json()["nome"] == "GEC_patch_novo"
    assert res.json()["email"] == aluno["email"]
    assert res.json()["curso"] == "GEC"

    res = client.get(f"/api/v1/alunos/{aluno['id']}")
    assert res.status_code == 200
    assert res.json()["id"] == aluno["id"]
    assert res.json()["matricula"] == aluno["matricula"]
    assert res.json()["nome"] == "GEC_patch_novo"
    assert res.json()["email"] == aluno["email"]
    assert res.json()["curso"] == "GEC"

# Teste de deletar aluno
def test_delete():
    aluno = criar_aluno()

    res = client.delete(f"/api/v1/alunos/{aluno['id']}")
    assert res.status_code == 200

    res = client.get(f"/api/v1/alunos/{aluno['id']}")
    assert res.status_code == 404

# Teste de cadastrar aluno após deletar outro
def test_cadastro_apos_delete():
    aluno = criar_aluno()
    res = client.delete(f"/api/v1/alunos/{aluno['id']}")
    assert res.status_code == 200

    res = criar_aluno()
    assert res["id"] == f"GES{aluno['matricula'] + 1}"
    assert res["matricula"] == aluno['matricula'] + 1

# Função auxiliar pra criar um aluno com dados aleatorios
def criar_aluno(curso="GES"):
    ts = int(datetime.now().timestamp())
    res = client.post("/api/v1/alunos/", json={
        "nome": f"{curso}{ts}",
        "email": f"{curso}_{ts}@hotmail.com",
        "curso": curso
    })
    return res.json()
