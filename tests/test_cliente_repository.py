import sqlite3

import pytest

from app.database.cliente_repository import ClienteRepository
from app.models.cliente import Cliente


def criar_cliente_teste(
    nome="Maria Teste",
    cpf="12345678900",
    idade=30
):
    return Cliente(
        nome=nome,
        cpf=cpf,
        idade=idade
    )


def test_criar_cliente(banco_teste):

    repository = ClienteRepository()

    cliente = criar_cliente_teste()

    cliente_id = repository.criar(cliente)

    assert cliente_id == 1


def test_buscar_cliente_por_id(banco_teste):

    repository = ClienteRepository()

    cliente = criar_cliente_teste()

    cliente_id = repository.criar(cliente)

    resultado = repository.buscar_por_id(cliente_id)

    assert resultado is not None
    assert resultado["id"] == cliente_id
    assert resultado["nome"] == "Maria Teste"
    assert resultado["cpf"] == "12345678900"
    assert resultado["idade"] == 30


def test_buscar_cliente_inexistente(banco_teste):

    repository = ClienteRepository()

    resultado = repository.buscar_por_id(999)

    assert resultado is None


def test_buscar_cliente_por_cpf(banco_teste):

    repository = ClienteRepository()

    cliente = criar_cliente_teste()

    repository.criar(cliente)

    resultado = repository.buscar_por_cpf("12345678900")

    assert resultado is not None
    assert resultado["nome"] == "Maria Teste"
    assert resultado["cpf"] == "12345678900"
    assert resultado["idade"] == 30


def test_buscar_cliente_por_cpf_inexistente(banco_teste):

    repository = ClienteRepository()

    resultado = repository.buscar_por_cpf("99999999999")

    assert resultado is None


def test_listar_todos_clientes(banco_teste):

    repository = ClienteRepository()

    cliente1 = criar_cliente_teste(
        nome="Maria",
        cpf="11111111111",
        idade=30
    )

    cliente2 = criar_cliente_teste(
        nome="Joao",
        cpf="22222222222",
        idade=40
    )

    repository.criar(cliente1)
    repository.criar(cliente2)

    resultados = repository.listar_todos()

    assert len(resultados) == 2

    assert resultados[0]["nome"] == "Maria"
    assert resultados[0]["cpf"] == "11111111111"

    assert resultados[1]["nome"] == "Joao"
    assert resultados[1]["cpf"] == "22222222222"


def test_listar_todos_sem_clientes(banco_teste):

    repository = ClienteRepository()

    resultados = repository.listar_todos()

    assert resultados == []


def test_criar_cliente_com_conexao_externa(banco_teste):

    conexao = sqlite3.connect(banco_teste)
    conexao.row_factory = sqlite3.Row

    repository = ClienteRepository()

    cliente = criar_cliente_teste()

    # O método criar atualmente abre sua própria conexão.
    # Este teste confirma que o banco continua acessível
    # por uma conexão externa.
    cliente_id = repository.criar(cliente)

    resultado = conexao.execute(
        """
        SELECT id, nome, cpf, idade
        FROM clientes
        WHERE id = ?
        """,
        (cliente_id,)
    ).fetchone()

    conexao.close()

    assert resultado is not None
    assert resultado["nome"] == "Maria Teste"
    assert resultado["cpf"] == "12345678900"
    assert resultado["idade"] == 30


def test_cpf_duplicado_deve_gerar_erro(banco_teste):

    repository = ClienteRepository()

    cliente1 = criar_cliente_teste(
        nome="Maria",
        cpf="12345678900",
        idade=30
    )

    cliente2 = criar_cliente_teste(
        nome="Joao",
        cpf="12345678900",
        idade=40
    )

    repository.criar(cliente1)

    with pytest.raises(sqlite3.IntegrityError):
        repository.criar(cliente2)
