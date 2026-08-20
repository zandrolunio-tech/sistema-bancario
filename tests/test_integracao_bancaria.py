from decimal import Decimal

from app.services.cliente_service import ClienteService
from app.services.conta_service import ContaService


def test_fluxo_completo_bancario(banco_teste):
    cliente_service = ClienteService()
    conta_service = ContaService()

    # ==========================================
    # 1. CADASTRAR CLIENTE
    # ==========================================

    cliente_id = cliente_service.cadastrar_cliente(
        nome="João da Silva",
        cpf="12345678901",
        idade=30
    )

    assert cliente_id > 0

    cliente = cliente_service.buscar_por_cpf(
        "12345678901"
    )

    assert cliente is not None
    assert cliente["nome"] == "João da Silva"


    # ==========================================
    # 2. CRIAR CONTA
    # ==========================================

    conta_id = conta_service.criar_conta(
        cliente_id=cliente_id,
        saldo_inicial=Decimal("1000.00"),
        limite=Decimal("500.00")
    )

    assert conta_id > 0


    # ==========================================
    # 3. CONSULTAR SALDO INICIAL
    # ==========================================

    saldo = conta_service.consultar_saldo(
        conta_id
    )

    assert saldo == Decimal("1000.00")


    # ==========================================
    # 4. FAZER DEPÓSITO
    # ==========================================

    novo_saldo = conta_service.depositar(
        conta_id,
        Decimal("500.00")
    )

    assert novo_saldo == Decimal("1500.00")


    # ==========================================
    # 5. FAZER SAQUE
    # ==========================================

    novo_saldo = conta_service.sacar(
        conta_id,
        Decimal("200.00")
    )

    assert novo_saldo == Decimal("1300.00")


    # ==========================================
    # 6. VERIFICAR DISPONÍVEL
    # ==========================================

    disponivel = conta_service.consultar_disponivel(
        conta_id
    )

    assert disponivel == Decimal("1800.00")


    # ==========================================
    # 7. CONSULTAR EXTRATO
    # ==========================================

    extrato = conta_service.consultar_extrato(
        conta_id
    )

    assert extrato["saldo"] == Decimal("1300.00")
    assert extrato["limite"] == Decimal("500.00")
    assert extrato["disponivel"] == Decimal("1800.00")

    assert extrato["total_transacoes"] == 2
