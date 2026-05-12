from app.schemas.aluno import Aluno, AlunoCreate
from app.db.connection import get_connection

class AlunoService:
    async def gerar_matricula(self, curso: str):
        conn = await get_connection()

        try:
            curso = curso.upper()
            row = await conn.fetchrow(
                """
                SELECT ultimo_numero
                FROM contadores
                WHERE curso = $1
                """,
                curso
            )

            if row:
                novo_numero = row["ultimo_numero"] + 1
                await conn.execute(
                    """
                    UPDATE contadores
                    SET ultimo_numero = $1
                    WHERE curso = $2
                    """,
                    novo_numero,
                    curso
                )

            else:
                novo_numero = 1
                await conn.execute(
                    """
                    INSERT INTO contadores (curso, ultimo_numero)
                    VALUES ($1, $2)
                    """,
                    curso,
                    novo_numero
                )

            return novo_numero

        finally:
            await conn.close()

    async def listar(self):
        conn = await get_connection()

        try:
            rows = await conn.fetch(
                "SELECT * FROM alunos ORDER BY id"
            )
            return [dict(row) for row in rows]

        finally:
            await conn.close()

    async def buscar(self, aluno_id: str):
        conn = await get_connection()

        try:
            row = await conn.fetchrow(
                "SELECT * FROM alunos WHERE id = $1",
                aluno_id
            )
            return dict(row) if row else None

        finally:
            await conn.close()

    async def criar(self, aluno_data: AlunoCreate):
        conn = await get_connection()

        try:
            curso = aluno_data.curso.upper()
            matricula = await self.gerar_matricula(curso)
            aluno_id = f"{curso}{matricula}"
            row = await conn.fetchrow(
                """
                INSERT INTO alunos (id, matricula, nome, email, curso)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING *
                """,
                aluno_id,
                matricula,
                aluno_data.nome,
                aluno_data.email,
                curso
            )
            return dict(row)

        finally:
            await conn.close()

    async def atualizar(self, aluno_id: str, aluno_data: AlunoCreate):
        conn = await get_connection()

        try:
            row = await conn.fetchrow(
                """
                UPDATE alunos
                SET nome = $1,
                    email = $2,
                    curso = $3
                WHERE id = $4
                RETURNING *
                """,
                aluno_data.nome,
                aluno_data.email,
                aluno_data.curso.upper(),
                aluno_id
            )
            return dict(row) if row else None

        finally:
            await conn.close()

    async def patch(self, aluno_id: str, dados: dict):
        conn = await get_connection()

        try:
            aluno = await self.buscar(aluno_id)
            if not aluno:
                return None
            nome = dados.get("nome", aluno["nome"])
            email = dados.get("email", aluno["email"])
            curso = dados.get("curso", aluno["curso"]).upper()
            row = await conn.fetchrow(
                """
                UPDATE alunos
                SET nome = $1,
                    email = $2,
                    curso = $3
                WHERE id = $4
                RETURNING *
                """,
                nome,
                email,
                curso,
                aluno_id
            )
            return dict(row)

        finally:
            await conn.close()

    async def deletar(self, aluno_id: str):
        conn = await get_connection()

        try:
            result = await conn.execute(
                "DELETE FROM alunos WHERE id = $1",
                aluno_id
            )
            return result == "DELETE 1"

        finally:
            await conn.close()

    async def resetar(self):
        conn = await get_connection()

        try:
            await conn.execute("DELETE FROM alunos")
            await conn.execute("DELETE FROM contadores")

        finally:
            await conn.close()