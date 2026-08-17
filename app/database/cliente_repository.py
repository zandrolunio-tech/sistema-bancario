from app.database.database import conectar
from app.models.cliente import Cliente


class ClienteRepository:

    def criar(self, cliente: Cliente) -> int:

        conexao = conectar()

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                INSERT INTO clientes (
                    nome,
                    cpf,
                    idade
                )
                VALUES (?, ?, ?)
                """,
                (
                    cliente.nome,
                    cliente.cpf,
                    cliente.idade
                )
            )

            conexao.commit()

            return cursor.lastrowid

        finally:
            conexao.close()

    def buscar_por_id(self, cliente_id: int):

        conexao = conectar()

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    nome,
                    cpf,
                    idade,
                    criado_em
                FROM clientes
                WHERE id = ?
                """,
                (cliente_id,)
            )

            return cursor.fetchone()

        finally:
            conexao.close()

    def buscar_por_cpf(self, cpf: str):

        conexao = conectar()

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    nome,
                    cpf,
                    idade,
                    criado_em
                FROM clientes
                WHERE cpf = ?
                """,
                (cpf,)
            )

            return cursor.fetchone()

        finally:
            conexao.close()

    def listar_todos(self):

        conexao = conectar()

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    nome,
                    cpf,
                    idade,
                    criado_em
                FROM clientes
                ORDER BY id
                """
            )

            return cursor.fetchall()

        finally:
            conexao.close()
