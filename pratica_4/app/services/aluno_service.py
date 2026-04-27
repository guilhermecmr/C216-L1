from app.schemas.aluno import Aluno, AlunoCreate

class AlunoService:
    def __init__(self):
        self.alunos = {}
        self.cont_curso = {}

    def gerar_matricula(self, curso: str):
        if curso.upper() not in self.cont_curso:
            self.cont_curso[curso.upper()] = 1
        else:
            self.cont_curso[curso.upper()] += 1

        return self.cont_curso[curso.upper()]

    def listar(self):
        return list(self.alunos.values())

    def buscar(self, aluno_id: str):
        return self.alunos.get(aluno_id)

    def criar(self, aluno_data: AlunoCreate):
        matricula = str(self.gerar_matricula(aluno_data.curso))
        aluno_id = f"{aluno_data.curso.upper()}{matricula}"

        aluno = Aluno(
            id=aluno_id,
            matricula=matricula,
            nome=aluno_data.nome,
            email=aluno_data.email,
            curso=aluno_data.curso.upper()
        )

        self.alunos[aluno_id] = aluno
        return aluno

    def atualizar(self, aluno_id: str, aluno_data: AlunoCreate):
        aluno = self.buscar(aluno_id)
        if not aluno:
            return None

        aluno.nome = aluno_data.nome
        aluno.email = aluno_data.email
        aluno.curso = aluno_data.curso.upper()
        return aluno

    def patch(self, aluno_id: str, dados: dict):
        aluno = self.buscar(aluno_id)
        if not aluno:
            return None

        if "nome" in dados:
            aluno.nome = dados["nome"]
        if "email" in dados:
            aluno.email = dados["email"]
        if "curso" in dados:
            aluno.curso = dados["curso"].upper()

        return aluno

    def deletar(self, aluno_id: str):
        if aluno_id in self.alunos:
            del self.alunos[aluno_id]
            return True
        return False

    def resetar(self):
        self.alunos.clear()
        self.cont_curso.clear()