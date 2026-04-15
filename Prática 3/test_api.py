from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Testar a criação de um aluno
def test_criar_aluno():
    response = client.post("/alunos", json={
        "nome": "Guilherme",
        "email": "guilherme123@hotmail.com",
        "curso": "GES"
    })

    assert response.status_code == 200
    assert "matricula" in response.json()

# Testar a listagem de alunos
def test_listar_alunos():
    response = client.get("/alunos")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Testar a busca de um aluno por matrícula
def test_buscar_aluno():
    res = client.post("/alunos", json={
        "nome": "GuilhermeBusca",
        "email": "guibusca@hotmail.com",
        "curso": "GEC"
    })
    matricula = res.json()["matricula"]

    response = client.get(f"/alunos/{matricula}")

    assert response.status_code == 200
    assert response.json()["nome"] == "GuilhermeBusca"
    assert response.json()["email"] == "guibusca@hotmail.com"
    assert response.json()["curso"] == "GEC"

# Testar a busca de um aluno inexistente
def test_buscar_aluno_inexistente():
    response = client.get("/alunos/999")

    assert response.status_code == 404

# Testar a atualização completa de um aluno
def test_atualizar_aluno():
    response = client.post("/alunos", json={
        "nome": "GuilhermeUpdate",
        "email": "guiupdate@hotmail.com",
        "curso": "GES"
    })
    matricula = response.json()["matricula"]

    response = client.put(f"/alunos/{matricula}", json={
        "nome": "GuiNovo",
        "email": "guinovo@hotmail.com",
        "curso": "GES"
    })

    assert response.status_code == 200

    response = client.get(f"/alunos/{matricula}")
    dados = response.json()

    assert response.status_code == 200
    assert dados["nome"] == "GuiNovo"
    assert dados["email"] == "guinovo@hotmail.com"

# Testar a atualização parcial de um aluno
def test_atualizar_patch_aluno():
    res = client.post("/alunos", json={
        "nome": "GuilhermePatch",
        "email": "guipatch@hotmail.com",
        "curso": "GES"
    })
    matricula = res.json()["matricula"]

    client.patch(f"/alunos/{matricula}", json={
        "nome": "GuilhermeNovo"
    })

    response = client.get(f"/alunos/{matricula}")

    assert response.status_code == 200
    assert response.json()["nome"] == "GuilhermeNovo"
    assert response.json()["email"] == "guipatch@hotmail.com"
    assert response.json()["curso"] == "GES"

# Testar a exclusão de um aluno
def test_deletar_aluno():
    res = client.post("/alunos", json={
        "nome": "GuilhermeDelete",
        "email": "guidel@hotmail.com",
        "curso": "GES"
    })
    matricula = res.json()["matricula"]

    response_delete = client.delete(f"/alunos/{matricula}")

    assert response_delete.status_code == 200

    response_get = client.get(f"/alunos/{matricula}")

    assert response_get.status_code == 404