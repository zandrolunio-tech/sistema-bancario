from decimal import Decimal
from app.models.cliente import Cliente


class Conta:
    def __init__(
        self,
        cliente: Cliente,
        saldo: Decimal = Decimal("0.00"),
        limite: Decimal = Decimal("500.00")
    ):
        self.cliente = cliente
        self.saldo = Decimal(str(saldo))
        self.limite = Decimal(str(limite))

    def depositar(self, valor: Decimal) -> bool:
        valor = Decimal(str(valor))

        if valor <= Decimal("0"):
            return False

        self.saldo += valor
        return True

    def sacar(self, valor: Decimal) -> bool:
        valor = Decimal(str(valor))

        if valor <= Decimal("0"):
            return False

        disponivel = self.saldo + self.limite

        if valor > disponivel:
            return False

        self.saldo -= valor
        return True

    def consultar_saldo(self) -> Decimal:
        return self.saldo

    def consultar_disponivel(self) -> Decimal:
        return self.saldo + self.limite