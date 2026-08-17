from decimal import Decimal

from app.database.database import conectar


class ContaRepository:

    def criar(
        self,
        cliente_id: int,
        saldo: Decimal = Decimal("0.00"),
        limite: Decimal = Decimal("500.00")
    ) -> int:

        conexao = conectar()

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                INSERT INTO contas (
                    cliente_id,
                    saldo,
                    limite
                )
                VALUES (?, ?, ?)
                """,
                (
                    cliente_id,
                    str(Decimal(str(saldo))),
                    str(Decimal(str(limite)))
                )
            )

            conexao.commit()

            return cursor.lastrowid

        finally:
            conexao.close()

    def buscar_por_id(self, conta_id: int):

        conexao = conectar()

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    cliente_id,
                    saldo,
                    limite,
                    criada_em
                FROM contas
                WHERE id = ?
                """,
                (conta_id,)
            )

            return cursor.fetchone()

        finally:
            conexao.close()

    def buscar_por_cliente_id(self, cliente_id: int):

        conexao = conectar()

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    cliente_id,
                    saldo,
                    limite,
                    criada_em
                FROM contas
                WHERE cliente_id = ?
                ORDER BY id
                """,
                (cliente_id,)
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
                    cliente_id,
                    saldo,
                    limite,
                    criada_em
                FROM contas
                ORDER BY id
                """
            )

            return cursor.fetchall()

        finally:
            conexao.close()

    def atualizar_saldo(
        self,
        conta_id: int,
        saldo: Decimal,
        conexao=None
    ) -> bool:

        conexao_propria = False

        if conexao is None:
            conexao = conectar()
            conexao_propria = True

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                UPDATE contas
                SET saldo = ?
                WHERE id = ?
                """,
                (
                    str(Decimal(str(saldo))),
                    conta_id
                )
            )

            if conexao_propria:
                conexao.commit()

            return cursor.rowcount > 0

        finally:
            if conexao_propria:
                conexao.close()

    def atualizar_limite(
        self,
        conta_id: int,
        limite: Decimal,
        conexao=None
    ) -> bool:

        conexao_propria = False

        if conexao is None:
            conexao = conectar()
            conexao_propria = True

        try:
            cursor = conexao.cursor()

            cursor.execute(
                """
                UPDATE contas
                SET limite = ?
                WHERE id = ?
                """,
                (
                    str(Decimal(str(limite))),
                    conta_id
                )
            )

            if conexao_propria:
                conexao.commit()

            return cursor.rowcount > 0

        finally:
            if conexao_propria:
                conexao.close()
