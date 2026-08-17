from decimal import Decimal

from app.database.database import conectar


class TransacaoRepository:

    def criar(
        self,
        conta_id: int,
        tipo: str,
        valor: Decimal,
        saldo_anterior: Decimal,
        saldo_posterior: Decimal,
        conexao=None
    ) -> int:

        conexao_propria = False

        if conexao is None:
            conexao = conectar()
            conexao_propria = True

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                INSERT INTO transacoes (
                    conta_id,
                    tipo,
                    valor,
                    saldo_anterior,
                    saldo_posterior
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    conta_id,
                    tipo,
                    str(Decimal(str(valor))),
                    str(Decimal(str(saldo_anterior))),
                    str(Decimal(str(saldo_posterior)))
                )
            )

            if conexao_propria:
                conexao.commit()

            return cursor.lastrowid

        finally:
            if conexao_propria:
                conexao.close()

    def buscar_por_id(self, transacao_id: int):

        conexao = conectar()

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    conta_id,
                    tipo,
                    valor,
                    saldo_anterior,
                    saldo_posterior,
                    criado_em
                FROM transacoes
                WHERE id = ?
                """,
                (transacao_id,)
            )

            return cursor.fetchone()

        finally:
            conexao.close()

    def listar_por_conta(self, conta_id: int):

        conexao = conectar()

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    conta_id,
                    tipo,
                    valor,
                    saldo_anterior,
                    saldo_posterior,
                    criado_em
                FROM transacoes
                WHERE conta_id = ?
                ORDER BY id
                """,
                (conta_id,)
            )

            return cursor.fetchall()

        finally:
            conexao.close()

    def listar_por_conta_desc(self, conta_id: int):

        conexao = conectar()

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    conta_id,
                    tipo,
                    valor,
                    saldo_anterior,
                    saldo_posterior,
                    criado_em
                FROM transacoes
                WHERE conta_id = ?
                ORDER BY id DESC
                """,
                (conta_id,)
            )

            return cursor.fetchall()

        finally:
            conexao.close()

    def listar_todas(self):

        conexao = conectar()

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    conta_id,
                    tipo,
                    valor,
                    saldo_anterior,
                    saldo_posterior,
                    criado_em
                FROM transacoes
                ORDER BY id
                """
            )

            return cursor.fetchall()

        finally:
            conexao.close()
