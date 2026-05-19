from pydantic import BaseModel

class Aluno(BaseModel):
    id: str
    matricula: int
    nome: str
    email: str
    curso: str

class AlunoCreate(BaseModel):
    nome: str
    email: str
    curso: str