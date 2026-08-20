from decimal import Decimal

import pytest

from app.database.cliente_repository import ClienteRepository
from app.database.conta_repository import ContaRepository
from app.database.transacao_repository import TransacaoRepository
from app.models.cliente import Cliente


def criar_conta_teste():
    cliente_repository = ClienteRepository()
    conta_repository = ContaRepository()

    cliente_id = cliente_repository.criar(
        Cliente(
            nome="Cliente Transação",
            cpf="11111111111",
            idade=30
        )
    )

    conta_id = conta_repository.criar(
        cliente_id=cliente_id,
        saldo=Decimal("100.00"),
        limite=Decimal("500.00")
    )

    return conta_id


def test_criar_transacao(banco_teste):
    conta_id = criar_conta_teste()

    repository = TransacaoRepository()

    transacao_id = repository.criar(
        conta_id=conta_id,
        tipo="DEPOSITO",
        valor=Decimal("50.00"),
        saldo_anterior=Decimal("100.00"),
        saldo_posterior=Decimal("150.00")
    )

    assert transacao_id == 1


def test_buscar_transacao_por_id(banco_teste):
    conta_id = criar_conta_teste()

    repository = TransacaoRepository()

    transacao_id = repository.criar(
        conta_id=conta_id,
        tipo="DEPOSITO",
        valor=Decimal("50.00"),
        saldo_anterior=Decimal("100.00"),
        saldo_posterior=Decimal("150.00")
    )

    transacao = repository.buscar_por_id(
        transacao_id
    )

    assert transacao is not None
    assert transacao["id"] == transacao_id
    assert transacao["conta_id"] == conta_id
    assert transacao["tipo"] == "DEPOSITO"
    assert transacao["valor"] == "50.00"
    assert transacao["saldo_anterior"] == "100.00"
    assert transacao["saldo_posterior"] == "150.00"


def test_buscar_transacao_inexistente(banco_teste):
    repository = TransacaoRepository()

    transacao = repository.buscar_por_id(999)

    assert transacao is None


def test_listar_transacoes_por_conta(banco_teste):
    conta_id = criar_conta_teste()

    repository = TransacaoRepository()

    repository.criar(
        conta_id=conta_id,
        tipo="DEPOSITO",
        valor=Decimal("50.00"),
        saldo_anterior=Decimal("100.00"),
        saldo_posterior=Decimal("150.00")
    )

    repository.criar(
        conta_id=conta_id,
        tipo="SAQUE",
        valor=Decimal("30.00"),
        saldo_anterior=Decimal("150.00"),
        saldo_posterior=Decimal("120.00")
    )

    transacoes = repository.listar_por_conta(
        conta_id
    )

    assert len(transacoes) == 2
    assert transacoes[0]["tipo"] == "DEPOSITO"
    assert transacoes[1]["tipo"] == "SAQUE"


def test_listar_transacoes_por_conta_desc(banco_teste):
    conta_id = criar_conta_teste()

    repository = TransacaoRepository()

    repository.criar(
        conta_id=conta_id,
        tipo="DEPOSITO",
        valor=Decimal("50.00"),
        saldo_anterior=Decimal("100.00"),
        saldo_posterior=Decimal("150.00")
    )

    repository.criar(
        conta_id=conta_id,
        tipo="SAQUE",
        valor=Decimal("30.00"),
        saldo_anterior=Decimal("150.00"),
        saldo_posterior=Decimal("120.00")
    )

    transacoes = repository.listar_por_conta_desc(
        conta_id
    )

    assert len(transacoes) == 2
    assert transacoes[0]["tipo"] == "SAQUE"
    assert transacoes[1]["tipo"] == "DEPOSITO"


def test_listar_transacoes_conta_sem_transacoes(
    banco_teste
):
    conta_id = criar_conta_teste()

    repository = TransacaoRepository()

    transacoes = repository.listar_por_conta(
        conta_id
    )

    assert transacoes == []


def test_listar_todas_as_transacoes(banco_teste):
    cliente_repository = ClienteRepository()
    conta_repository = ContaRepository()
    repository = TransacaoRepository()

    cliente_id = cliente_repository.criar(
        Cliente(
            nome="Cliente Um",
            cpf="22222222222",
            idade=30
        )
    )

    conta_um = conta_repository.criar(
        cliente_id=cliente_id,
        saldo=Decimal("100.00"),
        limite=Decimal("500.00")
    )

    cliente_id = cliente_repository.criar(
        Cliente(
            nome="Cliente Dois",
            cpf="33333333333",
            idade=30
        )
    )

    conta_dois = conta_repository.criar(
        cliente_id=cliente_id,
        saldo=Decimal("200.00"),
        limite=Decimal("500.00")
    )

    repository.criar(
        conta_id=conta_um,
        tipo="DEPOSITO",
        valor=Decimal("50.00"),
        saldo_anterior=Decimal("100.00"),
        saldo_posterior=Decimal("150.00")
    )

    repository.criar(
        conta_id=conta_dois,
        tipo="DEPOSITO",
        valor=Decimal("100.00"),
        saldo_anterior=Decimal("200.00"),
        saldo_posterior=Decimal("300.00")
    )

    transacoes = repository.listar_todas()

    assert len(transacoes) == 2
    assert transacoes[0]["conta_id"] == conta_um
    assert transacoes[1]["conta_id"] == conta_dois


def test_criar_transacao_com_conexao_externa(
    banco_teste
):
    conta_id = criar_conta_teste()

    repository = TransacaoRepository()

    from app.database.database import conectar

    conexao = conectar()

    try:
        transacao_id = repository.criar(
            conta_id=conta_id,
            tipo="DEPOSITO",
            valor=Decimal("25.00"),
            saldo_anterior=Decimal("100.00"),
            saldo_posterior=Decimal("125.00"),
            conexao=conexao
        )

        conexao.commit()

    finally:
        conexao.close()

    transacao = repository.buscar_por_id(
        transacao_id
    )

    assert transacao is not None
    assert transacao["tipo"] == "DEPOSITO"
    assert transacao["valor"] == "25.00"


def test_criar_transacao_conta_inexistente(
    banco_teste
):
    repository = TransacaoRepository()

    with pytest.raises(Exception):
        repository.criar(
            conta_id=999,
            tipo="DEPOSITO",
            valor=Decimal("50.00"),
            saldo_anterior=Decimal("100.00"),
            saldo_posterior=Decimal("150.00")
        )
