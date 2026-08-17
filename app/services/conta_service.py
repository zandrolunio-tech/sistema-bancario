from decimal import Decimal, InvalidOperation

from app.database.cliente_repository import ClienteRepository
from app.database.conta_repository import ContaRepository
from app.database.transacao_repository import TransacaoRepository
from app.database.database import conectar


class ContaService:

    def __init__(self):
        self.conta_repository = ContaRepository()
        self.cliente_repository = ClienteRepository()
        self.transacao_repository = TransacaoRepository()

    def criar_conta(
        self,
        cliente_id: int,
        saldo_inicial: Decimal = Decimal("0.00"),
        limite: Decimal = Decimal("500.00")
    ) -> int:

        if not isinstance(cliente_id, int):
            raise ValueError(
                "ID do cliente deve ser um número inteiro."
            )

        cliente = self.cliente_repository.buscar_por_id(
            cliente_id
        )

        if not cliente:
            raise ValueError(
                "Cliente não encontrado."
            )

        saldo_inicial = self._converter_decimal(
            saldo_inicial
        )

        limite = self._converter_decimal(
            limite
        )

        if saldo_inicial < Decimal("0.00"):
            raise ValueError(
                "Saldo inicial não pode ser negativo."
            )

        if limite < Decimal("0.00"):
            raise ValueError(
                "Limite não pode ser negativo."
            )

        return self.conta_repository.criar(
            cliente_id=cliente_id,
            saldo=saldo_inicial,
            limite=limite
        )

    def depositar(
        self,
        conta_id: int,
        valor: Decimal
    ) -> Decimal:

        valor = self._converter_decimal(valor)

        if valor <= Decimal("0.00"):
            raise ValueError(
                "O valor do depósito deve ser maior que zero."
            )

        conexao = conectar()

        try:
            conta = self.conta_repository.buscar_por_id(
                conta_id
            )

            if not conta:
                raise ValueError(
                    "Conta não encontrada."
                )

            saldo_anterior = Decimal(
                str(conta["saldo"])
            )

            novo_saldo = saldo_anterior + valor

            atualizou = self.conta_repository.atualizar_saldo(
                conta_id,
                novo_saldo,
                conexao=conexao
            )

            if not atualizou:
                raise ValueError(
                    "Não foi possível atualizar o saldo."
                )

            self.transacao_repository.criar(
                conta_id=conta_id,
                tipo="DEPOSITO",
                valor=valor,
                saldo_anterior=saldo_anterior,
                saldo_posterior=novo_saldo,
                conexao=conexao
            )

            conexao.commit()

            return novo_saldo

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    def sacar(
        self,
        conta_id: int,
        valor: Decimal
    ) -> Decimal:

        valor = self._converter_decimal(valor)

        if valor <= Decimal("0.00"):
            raise ValueError(
                "O valor do saque deve ser maior que zero."
            )

        conexao = conectar()

        try:
            conta = self.conta_repository.buscar_por_id(
                conta_id
            )

            if not conta:
                raise ValueError(
                    "Conta não encontrada."
                )

            saldo_anterior = Decimal(
                str(conta["saldo"])
            )

            limite = Decimal(
                str(conta["limite"])
            )

            disponivel = saldo_anterior + limite

            if valor > disponivel:
                raise ValueError(
                    "Saldo e limite insuficientes."
                )

            novo_saldo = saldo_anterior - valor

            atualizou = self.conta_repository.atualizar_saldo(
                conta_id,
                novo_saldo,
                conexao=conexao
            )

            if not atualizou:
                raise ValueError(
                    "Não foi possível atualizar o saldo."
                )

            self.transacao_repository.criar(
                conta_id=conta_id,
                tipo="SAQUE",
                valor=valor,
                saldo_anterior=saldo_anterior,
                saldo_posterior=novo_saldo,
                conexao=conexao
            )

            conexao.commit()

            return novo_saldo

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    def consultar_saldo(
        self,
        conta_id: int
    ) -> Decimal:

        conta = self.conta_repository.buscar_por_id(
            conta_id
        )

        if not conta:
            raise ValueError(
                "Conta não encontrada."
            )

        return Decimal(
            str(conta["saldo"])
        )

    def consultar_disponivel(
        self,
        conta_id: int
    ) -> Decimal:

        conta = self.conta_repository.buscar_por_id(
            conta_id
        )

        if not conta:
            raise ValueError(
                "Conta não encontrada."
            )

        saldo = Decimal(
            str(conta["saldo"])
        )

        limite = Decimal(
            str(conta["limite"])
        )

        return saldo + limite

    def buscar_conta(
        self,
        conta_id: int
    ):

        conta = self.conta_repository.buscar_por_id(
            conta_id
        )

        if not conta:
            raise ValueError(
                "Conta não encontrada."
            )

        return conta

    def listar_transacoes(
        self,
        conta_id: int
    ):

        conta = self.conta_repository.buscar_por_id(
            conta_id
        )

        if not conta:
            raise ValueError(
                "Conta não encontrada."
            )

        return self.transacao_repository.listar_por_conta(
            conta_id
        )


    def consultar_extrato(self, conta_id: int):

        conta = self.conta_repository.buscar_por_id(
            conta_id
        )

        if not conta:
            raise ValueError(
                "Conta não encontrada."
            )

        cliente = self.cliente_repository.buscar_por_id(
            conta["cliente_id"]
        )

        if not cliente:
            raise ValueError(
                "Cliente não encontrado."
            )

        saldo = Decimal(
            str(conta["saldo"])
        )

        limite = Decimal(
            str(conta["limite"])
        )

        disponivel = saldo + limite

        transacoes = (
            self.transacao_repository.listar_por_conta_desc(
                conta_id
            )
        )

        return {
            "conta": conta,
            "cliente": cliente,
            "saldo": saldo,
            "limite": limite,
            "disponivel": disponivel,
            "transacoes": transacoes,
            "total_transacoes": len(transacoes)
        }

    @staticmethod
    def _converter_decimal(valor: Decimal) -> Decimal:

        try:
            valor = Decimal(str(valor))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError(
                "Valor monetário inválido."
            )

        return valor.quantize(Decimal("0.01"))
