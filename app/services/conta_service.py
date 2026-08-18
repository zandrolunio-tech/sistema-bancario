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

    # =========================================================
    # CRIAR CONTA
    # =========================================================

    def criar_conta(
        self,
        cliente_id: int,
        saldo_inicial: Decimal = Decimal("0.00"),
        limite: Decimal = Decimal("500.00")
    ) -> int:

        self._validar_id(
            cliente_id,
            "ID do cliente"
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

    # =========================================================
    # DEPÓSITO
    # =========================================================

    def depositar(
        self,
        conta_id: int,
        valor: Decimal
    ) -> Decimal:

        self._validar_id(
            conta_id,
            "ID da conta"
        )

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

    # =========================================================
    # SAQUE
    # =========================================================

    def sacar(
        self,
        conta_id: int,
        valor: Decimal
    ) -> Decimal:

        self._validar_id(
            conta_id,
            "ID da conta"
        )

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

    # =========================================================
    # TRANSFERÊNCIA
    # =========================================================

    def transferir(
        self,
        conta_origem_id: int,
        conta_destino_id: int,
        valor: Decimal
    ) -> None:

        self._validar_id(
            conta_origem_id,
            "ID da conta de origem"
        )

        self._validar_id(
            conta_destino_id,
            "ID da conta de destino"
        )

        if conta_origem_id == conta_destino_id:
            raise ValueError(
                "A conta de origem e a conta de destino devem ser diferentes."
            )

        valor = self._converter_decimal(valor)

        if valor <= Decimal("0.00"):
            raise ValueError(
                "O valor da transferência deve ser maior que zero."
            )

        conexao = conectar()

        try:
            conta_origem = (
                self.conta_repository.buscar_por_id(
                    conta_origem_id
                )
            )

            if not conta_origem:
                raise ValueError(
                    "Conta de origem não encontrada."
                )

            conta_destino = (
                self.conta_repository.buscar_por_id(
                    conta_destino_id
                )
            )

            if not conta_destino:
                raise ValueError(
                    "Conta de destino não encontrada."
                )

            saldo_origem_anterior = Decimal(
                str(conta_origem["saldo"])
            )

            limite_origem = Decimal(
                str(conta_origem["limite"])
            )

            saldo_destino_anterior = Decimal(
                str(conta_destino["saldo"])
            )

            disponivel_origem = (
                saldo_origem_anterior
                + limite_origem
            )

            if valor > disponivel_origem:
                raise ValueError(
                    "Saldo e limite insuficientes para realizar a transferência."
                )

            saldo_origem_posterior = (
                saldo_origem_anterior - valor
            )

            saldo_destino_posterior = (
                saldo_destino_anterior + valor
            )

            origem_atualizada = (
                self.conta_repository.atualizar_saldo(
                    conta_origem_id,
                    saldo_origem_posterior,
                    conexao=conexao
                )
            )

            if not origem_atualizada:
                raise ValueError(
                    "Não foi possível atualizar a conta de origem."
                )

            destino_atualizado = (
                self.conta_repository.atualizar_saldo(
                    conta_destino_id,
                    saldo_destino_posterior,
                    conexao=conexao
                )
            )

            if not destino_atualizado:
                raise ValueError(
                    "Não foi possível atualizar a conta de destino."
                )

            self.transacao_repository.criar(
                conta_id=conta_origem_id,
                tipo="TRANSFERENCIA_ENVIADA",
                valor=valor,
                saldo_anterior=saldo_origem_anterior,
                saldo_posterior=saldo_origem_posterior,
                conexao=conexao
            )

            self.transacao_repository.criar(
                conta_id=conta_destino_id,
                tipo="TRANSFERENCIA_RECEBIDA",
                valor=valor,
                saldo_anterior=saldo_destino_anterior,
                saldo_posterior=saldo_destino_posterior,
                conexao=conexao
            )

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    # =========================================================
    # CONSULTAR SALDO
    # =========================================================

    def consultar_saldo(
        self,
        conta_id: int
    ) -> Decimal:

        self._validar_id(
            conta_id,
            "ID da conta"
        )

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

    # =========================================================
    # CONSULTAR DISPONÍVEL
    # =========================================================

    def consultar_disponivel(
        self,
        conta_id: int
    ) -> Decimal:

        self._validar_id(
            conta_id,
            "ID da conta"
        )

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

    # =========================================================
    # BUSCAR CONTA
    # =========================================================

    def buscar_conta(
        self,
        conta_id: int
    ):

        self._validar_id(
            conta_id,
            "ID da conta"
        )

        conta = self.conta_repository.buscar_por_id(
            conta_id
        )

        if not conta:
            raise ValueError(
                "Conta não encontrada."
            )

        return conta

    # =========================================================
    # LISTAR TRANSAÇÕES
    # =========================================================

    def listar_transacoes(
        self,
        conta_id: int
    ):

        self._validar_id(
            conta_id,
            "ID da conta"
        )

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

    # =========================================================
    # CONSULTAR EXTRATO
    # =========================================================

    def consultar_extrato(
        self,
        conta_id: int
    ):

        self._validar_id(
            conta_id,
            "ID da conta"
        )

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

    # =========================================================
    # VALIDAÇÃO DE ID
    # =========================================================

    @staticmethod
    def _validar_id(
        valor,
        nome: str
    ) -> None:

        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError(
                f"{nome} deve ser um número inteiro."
            )

        if valor <= 0:
            raise ValueError(
                f"{nome} deve ser maior que zero."
            )

    # =========================================================
    # CONVERSÃO MONETÁRIA
    # =========================================================

    @staticmethod
    def _converter_decimal(
        valor
    ) -> Decimal:

        try:
            decimal = Decimal(str(valor))

            if not decimal.is_finite():
                raise ValueError(
                    "Valor monetário inválido."
                )

            return decimal.quantize(
                Decimal("0.01")
            )

        except (
            InvalidOperation,
            ValueError,
            TypeError
        ) as erro:

            if str(erro) == "Valor monetário inválido.":
                raise

            raise ValueError(
                "Valor monetário inválido."
	 ) from erro
