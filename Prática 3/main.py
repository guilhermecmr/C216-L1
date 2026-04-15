from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

alunos = {}
cont_curso = {}

# Schemas
class AlunoCreate(BaseModel):
    nome: str
    email: str
    curso: str

class AlunoUpdate(BaseModel):
    nome: str
    email: str
    curso: str

class AlunoPatch(BaseModel):
    nome: str | None = None
    email: str | None = None
    curso: str | None = None

# Gera a matricula automaticamente baseada no curso
def gerar_matricula(curso: str):
    if curso not in cont_curso:
        cont_curso[curso] = 1
    else:
        cont_curso[curso] += 1

    return f"{curso}{cont_curso[curso]}"

# GET - lista todos os alunos
@app.get("/alunos")
def listar_alunos():
    return alunos

# GET - busca aluno por matrícula
@app.get("/alunos/{matricula}")
def buscar_aluno(matricula: str):
    if matricula not in alunos:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return alunos[matricula]

# POST - cadastra aluno
@app.post("/alunos")
def cadastrar_aluno(aluno: AlunoCreate):
    matricula = gerar_matricula(aluno.curso)

    alunos[matricula] = {
        "nome": aluno.nome,
        "email": aluno.email,
        "curso": aluno.curso
    }

    return {
        "mensagem": "Aluno cadastrado com sucesso",
        "matricula": matricula
    }

# PUT - atualiza aluno completamente
@app.put("/alunos/{matricula}")
def atualizar_aluno(matricula: str, aluno: AlunoUpdate):
    if matricula not in alunos:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    alunos[matricula] = {
        "nome": aluno.nome,
        "email": aluno.email,
        "curso": aluno.curso
    }

    return {"mensagem": "Aluno atualizado com sucesso"}

# PATCH - atualiza aluno parcialmente
@app.patch("/alunos/{matricula}")
def atualizar_parcial(matricula: str, aluno: AlunoPatch):
    if matricula not in alunos:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    if aluno.nome is not None:
        alunos[matricula]["nome"] = aluno.nome

    if aluno.email is not None:
        alunos[matricula]["email"] = aluno.email

    if aluno.curso is not None:
        alunos[matricula]["curso"] = aluno.curso

    return {"mensagem": "Aluno atualizado parcialmente"}

# DELETE - remove aluno
@app.delete("/alunos/{matricula}")
def deletar_aluno(matricula: str):
    if matricula not in alunos:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    del alunos[matricula]

    return {"mensagem": "Aluno removido com sucesso"}