from fastapi import APIRouter, HTTPException
from app.schemas.aluno import Aluno, AlunoCreate
from app.services.aluno_service import AlunoService

router = APIRouter(prefix="/api/v1")
service = AlunoService()


@router.get("/alunos", response_model=list[Aluno])
async def listar_alunos():
    return await service.listar()


@router.get("/alunos/{aluno_id}", response_model=Aluno)
async def buscar_aluno(aluno_id: str):
    aluno = await service.buscar(aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


@router.post("/alunos", response_model=Aluno, status_code=201)
async def cadastrar_aluno(aluno: AlunoCreate):
    return await service.criar(aluno)


@router.put("/alunos/{aluno_id}", response_model=Aluno)
async def atualizar_aluno(aluno_id: str, aluno: AlunoCreate):
    atualizado = await service.atualizar(aluno_id, aluno)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return atualizado


@router.patch("/alunos/{aluno_id}", response_model=Aluno)
async def patch_aluno(aluno_id: str, dados: dict):
    atualizado = await service.patch(aluno_id, dados)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return atualizado


@router.delete("/alunos/{aluno_id}")
async def deletar_aluno(aluno_id: str):
    deletado = await service.deletar(aluno_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return {"mensagem": "Aluno removido"}


@router.delete("/alunos")
async def resetar():
    await service.resetar()
    return {"mensagem": "Lista resetada"}