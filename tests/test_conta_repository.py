from decimal import Decimal

import sqlite3

from app.database.cliente_repository import ClienteRepository
from app.database.conta_repository import ContaRepository
from app.models.cliente import Cliente


def criar_cliente_teste():
    repository = ClienteRepository()

    return repository.criar(
        Cliente(
            nome="Cliente Conta",
            cpf="11111111111",
            idade=30
        )
    )


def criar_conta_teste():
    cliente_id = criar_cliente_teste()

    repository = ContaRepository()

    conta_id = repository.criar(
        cliente_id=cliente_id,
        saldo=Decimal("100.00"),
        limite=Decimal("500.00")
    )

    return repository, conta_id, cliente_id


def test_criar_conta(banco_teste):
    repository = ContaRepository()

    cliente_id = criar_cliente_teste()

    conta_id = repository.criar(
        cliente_id=cliente_id,
        saldo=Decimal("100.00"),
        limite=Decimal("500.00")
    )

    assert conta_id == 1


def test_buscar_conta_por_id(banco_teste):
    repository, conta_id, cliente_id = criar_conta_teste()

    conta = repository.buscar_por_id(conta_id)

    assert conta is not None
    assert conta["id"] == conta_id
    assert conta["cliente_id"] == cliente_id
    assert conta["saldo"] == "100.00"
    assert conta["limite"] == "500.00"


def test_buscar_conta_inexistente(banco_teste):
    repository = ContaRepository()

    conta = repository.buscar_por_id(999)

    assert conta is None


def test_buscar_contas_por_cliente_id(banco_teste):
    cliente_id = criar_cliente_teste()

    repository = ContaRepository()

    conta_1 = repository.criar(
        cliente_id=cliente_id,
        saldo=Decimal("100.00"),
        limite=Decimal("500.00")
    )

    conta_2 = repository.criar(
        cliente_id=cliente_id,
        saldo=Decimal("200.00"),
        limite=Decimal("300.00")
    )

    contas = repository.buscar_por_cliente_id(
        cliente_id
    )

    assert len(contas) == 2

    assert contas[0]["id"] == conta_1
    assert contas[1]["id"] == conta_2


def test_cliente_sem_contas(banco_teste):
    cliente_id = criar_cliente_teste()

    repository = ContaRepository()

    contas = repository.buscar_por_cliente_id(
        cliente_id
    )

    assert contas == []


def test_listar_todas_as_contas(banco_teste):
    cliente_repository = ClienteRepository()
    conta_repository = ContaRepository()

    cliente_1 = cliente_repository.criar(
        Cliente(
            nome="Cliente Um",
            cpf="22222222222",
            idade=30
        )
    )

    cliente_2 = cliente_repository.criar(
        Cliente(
            nome="Cliente Dois",
            cpf="33333333333",
            idade=35
        )
    )

    conta_1 = conta_repository.criar(
        cliente_id=cliente_1,
        saldo=Decimal("100.00"),
        limite=Decimal("500.00")
    )

    conta_2 = conta_repository.criar(
        cliente_id=cliente_2,
        saldo=Decimal("200.00"),
        limite=Decimal("300.00")
    )

    contas = conta_repository.listar_todas()

    assert len(contas) == 2

    assert contas[0]["id"] == conta_1
    assert contas[1]["id"] == conta_2


def test_atualizar_saldo(banco_teste):
    repository, conta_id, _ = criar_conta_teste()

    resultado = repository.atualizar_saldo(
        conta_id,
        Decimal("250.00")
    )

    assert resultado is True

    conta = repository.buscar_por_id(conta_id)

    assert conta["saldo"] == "250.00"


def test_atualizar_limite(banco_teste):
    repository, conta_id, _ = criar_conta_teste()

    resultado = repository.atualizar_limite(
        conta_id,
        Decimal("1000.00")
    )

    assert resultado is True

    conta = repository.buscar_por_id(conta_id)

    assert conta["limite"] == "1000.00"


def test_atualizar_saldo_conta_inexistente(banco_teste):
    repository = ContaRepository()

    resultado = repository.atualizar_saldo(
        999,
        Decimal("250.00")
    )

    assert resultado is False


def test_atualizar_limite_conta_inexistente(banco_teste):
    repository = ContaRepository()

    resultado = repository.atualizar_limite(
        999,
        Decimal("1000.00")
    )

    assert resultado is False


def test_atualizar_saldo_com_conexao_externa(
    banco_teste
):
    repository, conta_id, _ = criar_conta_teste()

    conexao = sqlite3.connect(banco_teste)
    conexao.row_factory = sqlite3.Row

    try:
        resultado = repository.atualizar_saldo(
            conta_id,
            Decimal("350.00"),
            conexao=conexao
        )

        assert resultado is True

        conexao.commit()

    finally:
        conexao.close()

    conta = repository.buscar_por_id(conta_id)

    assert conta["saldo"] == "350.00"


def test_atualizar_limite_com_conexao_externa(
    banco_teste
):
    repository, conta_id, _ = criar_conta_teste()

    conexao = sqlite3.connect(banco_teste)
    conexao.row_factory = sqlite3.Row

    try:
        resultado = repository.atualizar_limite(
            conta_id,
            Decimal("750.00"),
            conexao=conexao
        )

        assert resultado is True

        conexao.commit()

    finally:
        conexao.close()

    conta = repository.buscar_por_id(conta_id)

    assert conta["limite"] == "750.00"
