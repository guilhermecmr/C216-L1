from fastapi import APIRouter, HTTPException
from app.schemas.aluno import Aluno, AlunoCreate
from app.services.aluno_service import AlunoService

router = APIRouter(prefix="/api/v1")
service = AlunoService()

@router.get("/alunos", response_model=list[Aluno])
def listar_alunos():
    return service.listar()

@router.get("/alunos/{aluno_id}", response_model=Aluno)
def buscar_aluno(aluno_id: str):
    aluno = service.buscar(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.post("/alunos", response_model=Aluno)
def cadastrar_aluno(aluno: AlunoCreate):
    return service.criar(aluno)

@router.put("/alunos/{aluno_id}", response_model=Aluno)
def atualizar_aluno(aluno_id: str, aluno: AlunoCreate):
    atualizado = service.atualizar(aluno_id, aluno)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return atualizado

@router.patch("/alunos/{aluno_id}", response_model=Aluno)
def patch_aluno(aluno_id: str, dados: dict):
    atualizado = service.patch(aluno_id, dados)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return atualizado

@router.delete("/alunos/{aluno_id}")
def deletar_aluno(aluno_id: str):
    if not service.deletar(aluno_id):
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"mensagem": "Aluno removido"}

@router.delete("/alunos")
def resetar():
    service.resetar()
    return {"mensagem": "Lista resetada"}