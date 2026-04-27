from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

client.delete("/api/v1/alunos/") # Limpa os dados antes do teste

# Teste de cadastrar aluno
def test_post():
    # Cria três alunos GES
    for i in range(3):
        res = client.post("/api/v1/alunos/", json={
            "nome": f"GES{i}",
            "email": f"ges{i}@hotmail.com",
            "curso": "GES"
        })
        assert res.status_code == 200
        assert res.json()["id"] == f"GES{i+1}"
        assert res.json()["matricula"] == f"{i+1}"
        assert res.json()["nome"] == f"GES{i}"
        assert res.json()["email"] == f"ges{i}@hotmail.com"
        assert res.json()["curso"] == "GES"

    # Cria três alunos GEC
    for i in range(3):
        res = client.post("/api/v1/alunos/", json={
            "nome": f"GEC{i}",
            "email": f"gec{i}@hotmail.com",
            "curso": "GEC"
        })
        assert res.status_code == 200
        assert res.json()["id"] == f"GEC{i+1}"
        assert res.json()["matricula"] == f"{i+1}"
        assert res.json()["nome"] == f"GEC{i}"
        assert res.json()["email"] == f"gec{i}@hotmail.com"
        assert res.json()["curso"] == "GEC"

# Teste de listar alunos
def test_get_all():
    res = client.get("/api/v1/alunos/")
    assert res.status_code == 200
    assert len(res.json()) == 6

# Teste de buscar aluno por ID
def test_get_by_id():
    res = client.get("/api/v1/alunos/GES1")
    assert res.status_code == 200
    assert res.json()["id"] == "GES1"
    assert res.json()["matricula"] == "1"
    assert res.json()["nome"] == "GES0"
    assert res.json()["email"] == "ges0@hotmail.com"
    assert res.json()["curso"] == "GES"

    res = client.get("/api/v1/alunos/GEC2")
    assert res.status_code == 200
    assert res.json()["id"] == "GEC2"
    assert res.json()["matricula"] == "2"
    assert res.json()["nome"] == "GEC1"
    assert res.json()["email"] == "gec1@hotmail.com"
    assert res.json()["curso"] == "GEC"

# Teste de atualizar aluno por completo
def test_put():
    res = client.put("/api/v1/alunos/GES1", json={
        "nome": "GES0 put",
        "email": "ges0put@hotmail.com",
        "curso": "GEP"
    })
    assert res.status_code == 200
    assert res.json()["nome"] == "GES0 put"
    assert res.json()["email"] == "ges0put@hotmail.com"
    assert res.json()["curso"] == "GEP"
    
    res = client.get("/api/v1/alunos/GES1")
    assert res.status_code == 200
    assert res.json()["id"] == "GES1"
    assert res.json()["matricula"] == "1"
    assert res.json()["nome"] == "GES0 put"
    assert res.json()["email"] == "ges0put@hotmail.com"
    assert res.json()["curso"] == "GEP"

# Teste de atualizar aluno parcialmente
def test_patch(): 
    res = client.patch("/api/v1/alunos/GEC1", json={
        "nome": "GEC0 patch"
    })
    assert res.status_code == 200
    assert res.json()["nome"] == "GEC0 patch"
    assert res.json()["email"] == "gec0@hotmail.com"
    assert res.json()["curso"] == "GEC"

    res = client.get("/api/v1/alunos/GEC1")
    assert res.status_code == 200
    assert res.json()["id"] == "GEC1"
    assert res.json()["matricula"] == "1"
    assert res.json()["nome"] == "GEC0 patch"
    assert res.json()["email"] == "gec0@hotmail.com"
    assert res.json()["curso"] == "GEC"

# Teste de deletar aluno
def test_delete():
    res = client.delete("/api/v1/alunos/GES2")
    assert res.status_code == 200

    res = client.get("/api/v1/alunos/GES2")
    assert res.status_code == 404

# Teste de cadastrar aluno após deletar outro
def test_cadastro_apos_delete():
    res = client.delete("/api/v1/alunos/GES3")
    assert res.status_code == 200

    res = client.post("/api/v1/alunos/", json={
        "nome": "GES3 novo",
        "email": "ges3novo@hotmail.com",
        "curso": "GES"
    })
    assert res.status_code == 200
    assert res.json()["id"] == "GES4"
    assert res.json()["matricula"] == "4"

# Teste de resetar lista de alunos
def test_reset():
    res = client.delete("/api/v1/alunos/")
    assert res.status_code == 200

    res = client.get("/api/v1/alunos/")
    assert res.status_code == 200
    assert len(res.json()) == 0