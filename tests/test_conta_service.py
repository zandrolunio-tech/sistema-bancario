from app.models.cliente import Cliente

from decimal import Decimal

import pytest

from app.database.cliente_repository import ClienteRepository
from app.services.cliente_service import ClienteService
from app.services.conta_service import ContaService


def criar_cliente_teste():
    cliente_service = ClienteService()

    return cliente_service.cadastrar_cliente(
        nome="Cliente Conta",
        cpf="11111111111",
        idade=30
    )


def criar_conta_teste():
    cliente_id = criar_cliente_teste()

    conta_service = ContaService()

    conta_id = conta_service.criar_conta(
        cliente_id=cliente_id,
        saldo_inicial=Decimal("100.00"),
        limite=Decimal("500.00")
    )

    return conta_service, conta_id


def test_criar_conta_com_sucesso(banco_teste):
    cliente_id = criar_cliente_teste()

    service = ContaService()

    conta_id = service.criar_conta(
        cliente_id=cliente_id,
        saldo_inicial=Decimal("100.00"),
        limite=Decimal("500.00")
    )

    assert conta_id == 1


def test_criar_conta_cliente_inexistente(banco_teste):
    service = ContaService()

    with pytest.raises(
        ValueError,
        match="Cliente não encontrado."
    ):
        service.criar_conta(
            cliente_id=999,
            saldo_inicial=Decimal("100.00"),
            limite=Decimal("500.00")
        )


def test_saldo_inicial_negativo(banco_teste):
    cliente_id = criar_cliente_teste()

    service = ContaService()

    with pytest.raises(
        ValueError,
        match="Saldo inicial não pode ser negativo."
    ):
        service.criar_conta(
            cliente_id=cliente_id,
            saldo_inicial=Decimal("-100.00"),
            limite=Decimal("500.00")
        )


def test_limite_negativo(banco_teste):
    cliente_id = criar_cliente_teste()

    service = ContaService()

    with pytest.raises(
        ValueError,
        match="Limite não pode ser negativo."
    ):
        service.criar_conta(
            cliente_id=cliente_id,
            saldo_inicial=Decimal("100.00"),
            limite=Decimal("-500.00")
        )


def test_consultar_saldo(banco_teste):
    service, conta_id = criar_conta_teste()

    saldo = service.consultar_saldo(conta_id)

    assert saldo == Decimal("100.00")


def test_consultar_disponivel(banco_teste):
    service, conta_id = criar_conta_teste()

    disponivel = service.consultar_disponivel(
        conta_id
    )

    assert disponivel == Decimal("600.00")


def test_depositar_com_sucesso(banco_teste):
    service, conta_id = criar_conta_teste()

    novo_saldo = service.depositar(
        conta_id,
        Decimal("50.00")
    )

    assert novo_saldo == Decimal("150.00")

    saldo = service.consultar_saldo(conta_id)

    assert saldo == Decimal("150.00")


def test_deposito_zero_deve_gerar_erro(banco_teste):
    service, conta_id = criar_conta_teste()

    with pytest.raises(
        ValueError,
        match="maior que zero"
    ):
        service.depositar(
            conta_id,
            Decimal("0.00")
        )


def test_deposito_negativo_deve_gerar_erro(banco_teste):
    service, conta_id = criar_conta_teste()

    with pytest.raises(
        ValueError,
        match="maior que zero"
    ):
        service.depositar(
            conta_id,
            Decimal("-10.00")
        )


def test_deposito_conta_inexistente(banco_teste):
    service = ContaService()

    with pytest.raises(
        ValueError,
        match="Conta não encontrada."
    ):
        service.depositar(
            999,
            Decimal("50.00")
        )


def test_sacar_com_sucesso(banco_teste):
    service, conta_id = criar_conta_teste()

    novo_saldo = service.sacar(
        conta_id,
        Decimal("30.00")
    )

    assert novo_saldo == Decimal("70.00")

    saldo = service.consultar_saldo(conta_id)

    assert saldo == Decimal("70.00")


def test_saque_zero_deve_gerar_erro(banco_teste):
    service, conta_id = criar_conta_teste()

    with pytest.raises(
        ValueError,
        match="maior que zero"
    ):
        service.sacar(
            conta_id,
            Decimal("0.00")
        )


def test_saque_negativo_deve_gerar_erro(banco_teste):
    service, conta_id = criar_conta_teste()

    with pytest.raises(
        ValueError,
        match="maior que zero"
    ):
        service.sacar(
            conta_id,
            Decimal("-20.00")
        )


def test_saque_acima_do_disponivel(banco_teste):
    service, conta_id = criar_conta_teste()

    with pytest.raises(
        ValueError,
        match="Saldo e limite insuficientes."
    ):
        service.sacar(
            conta_id,
            Decimal("601.00")
        )

    saldo = service.consultar_saldo(conta_id)

    assert saldo == Decimal("100.00")


def test_saque_conta_inexistente(banco_teste):
    service = ContaService()

    with pytest.raises(
        ValueError,
        match="Conta não encontrada."
    ):
        service.sacar(
            999,
            Decimal("50.00")
        )


def test_deposito_cria_transacao(banco_teste):
    service, conta_id = criar_conta_teste()

    service.depositar(
        conta_id,
        Decimal("50.00")
    )

    transacoes = service.listar_transacoes(
        conta_id
    )

    assert len(transacoes) == 1

    transacao = transacoes[0]

    assert transacao["tipo"] == "DEPOSITO"
    assert transacao["valor"] == "50.00"
    assert transacao["saldo_anterior"] == "100.00"
    assert transacao["saldo_posterior"] == "150.00"


def test_saque_cria_transacao(banco_teste):
    service, conta_id = criar_conta_teste()

    service.sacar(
        conta_id,
        Decimal("30.00")
    )

    transacoes = service.listar_transacoes(
        conta_id
    )

    assert len(transacoes) == 1

    transacao = transacoes[0]

    assert transacao["tipo"] == "SAQUE"
    assert transacao["valor"] == "30.00"
    assert transacao["saldo_anterior"] == "100.00"
    assert transacao["saldo_posterior"] == "70.00"


def test_deposito_e_saque_registram_duas_transacoes(
    banco_teste
):
    service, conta_id = criar_conta_teste()

    service.depositar(
        conta_id,
        Decimal("50.00")
    )

    service.sacar(
        conta_id,
        Decimal("30.00")
    )

    transacoes = service.listar_transacoes(
        conta_id
    )

    assert len(transacoes) == 2

    assert transacoes[0]["tipo"] == "DEPOSITO"
    assert transacoes[1]["tipo"] == "SAQUE"


def test_consultar_extrato(banco_teste):
    service, conta_id = criar_conta_teste()

    service.depositar(
        conta_id,
        Decimal("50.00")
    )

    service.sacar(
        conta_id,
        Decimal("30.00")
    )

    extrato = service.consultar_extrato(
        conta_id
    )

    assert extrato["conta"]["id"] == conta_id

    assert extrato["cliente"]["nome"] == (
        "Cliente Conta"
    )

    assert extrato["saldo"] == Decimal("120.00")

    assert extrato["limite"] == Decimal("500.00")

    assert extrato["disponivel"] == Decimal("620.00")

    assert extrato["total_transacoes"] == 2

    assert len(extrato["transacoes"]) == 2

    assert extrato["transacoes"][0]["tipo"] == (
        "SAQUE"
    )

    assert extrato["transacoes"][1]["tipo"] == (
        "DEPOSITO"
    )
def test_transferencia_com_sucesso(banco_teste):
    service, conta_origem_id = criar_conta_teste()

    cliente_repository = ClienteRepository()
    cliente_id = cliente_repository.criar(
        Cliente(
            nome="Cliente Destino",
            cpf="55555555555",
            idade=30
        )
    )

    conta_destino_id = service.criar_conta(
        cliente_id=cliente_id,
        saldo_inicial=Decimal("100.00"),
        limite=Decimal("500.00")
    )

    service.transferir(
        conta_origem_id,
        conta_destino_id,
        Decimal("50.00")
    )

    saldo_origem = service.consultar_saldo(
        conta_origem_id
    )

    saldo_destino = service.consultar_saldo(
        conta_destino_id
    )

    assert saldo_origem == Decimal("50.00")
    assert saldo_destino == Decimal("150.00")


def test_transferencia_cria_duas_transacoes(
    banco_teste
):
    service, conta_origem_id = criar_conta_teste()

    cliente_repository = ClienteRepository()

    cliente_id = cliente_repository.criar(
        Cliente(
            nome="Cliente Destino",
            cpf="66666666666",
            idade=30
        )
    )

    conta_destino_id = service.criar_conta(
        cliente_id=cliente_id,
        saldo_inicial=Decimal("100.00"),
        limite=Decimal("500.00")
    )

    service.transferir(
        conta_origem_id,
        conta_destino_id,
        Decimal("50.00")
    )

    transacoes_origem = service.listar_transacoes(
        conta_origem_id
    )

    transacoes_destino = service.listar_transacoes(
        conta_destino_id
    )

    assert len(transacoes_origem) == 1
    assert len(transacoes_destino) == 1

    assert transacoes_origem[0]["tipo"] == (
        "TRANSFERENCIA_ENVIADA"
    )

    assert transacoes_destino[0]["tipo"] == (
        "TRANSFERENCIA_RECEBIDA"
    )


def test_transferencia_zero_deve_gerar_erro(
    banco_teste
):
    service, conta_origem_id = criar_conta_teste()

    cliente_repository = ClienteRepository()

    cliente_id = cliente_repository.criar(
        Cliente(
            nome="Cliente Destino",
            cpf="77777777777",
            idade=30
        )
    )

    conta_destino_id = service.criar_conta(
        cliente_id=cliente_id
    )

    try:
        service.transferir(
            conta_origem_id,
            conta_destino_id,
            Decimal("0.00")
        )

        assert False, (
            "Era esperado erro para transferência zero."
        )

    except ValueError as erro:
        assert "maior que zero" in str(erro)


def test_transferencia_negativa_deve_gerar_erro(
    banco_teste
):
    service, conta_origem_id = criar_conta_teste()

    cliente_repository = ClienteRepository()

    cliente_id = cliente_repository.criar(
        Cliente(
            nome="Cliente Destino",
            cpf="88888888888",
            idade=30
        )
    )

    conta_destino_id = service.criar_conta(
        cliente_id=cliente_id
    )

    try:
        service.transferir(
            conta_origem_id,
            conta_destino_id,
            Decimal("-10.00")
        )

        assert False, (
            "Era esperado erro para transferência negativa."
        )

    except ValueError as erro:
        assert "maior que zero" in str(erro)


def test_transferencia_conta_origem_inexistente(
    banco_teste
):
    service, conta_destino_id = criar_conta_teste()

    try:
        service.transferir(
            999,
            conta_destino_id,
            Decimal("50.00")
        )

        assert False, (
            "Era esperado erro para conta de origem inexistente."
        )

    except ValueError as erro:
        assert "origem" in str(erro).lower()


def test_transferencia_conta_destino_inexistente(
    banco_teste
):
    service, conta_origem_id = criar_conta_teste()

    try:
        service.transferir(
            conta_origem_id,
            999,
            Decimal("50.00")
        )

        assert False, (
            "Era esperado erro para conta de destino inexistente."
        )

    except ValueError as erro:
        assert "destino" in str(erro).lower()


def test_transferencia_para_mesma_conta(
    banco_teste
):
    service, conta_id = criar_conta_teste()

    try:
        service.transferir(
            conta_id,
            conta_id,
            Decimal("50.00")
        )

        assert False, (
            "Era esperado erro ao transferir para a própria conta."
        )

    except ValueError as erro:
        assert "diferentes" in str(erro)


def test_transferencia_acima_do_disponivel(
    banco_teste
):
    service, conta_origem_id = criar_conta_teste()

    cliente_repository = ClienteRepository()

    cliente_id = cliente_repository.criar(
        Cliente(
            nome="Cliente Destino",
            cpf="99999999999",
            idade=30
        )
    )

    conta_destino_id = service.criar_conta(
        cliente_id=cliente_id
    )

    try:
        service.transferir(
            conta_origem_id,
            conta_destino_id,
            Decimal("601.00")
        )

        assert False, (
            "Era esperado erro por falta de saldo e limite."
        )

    except ValueError as erro:
        assert "insuficientes" in str(erro).lower()
