import sqlite3

import pytest


@pytest.fixture
def banco_teste(monkeypatch, tmp_path):
    """
    Cria um banco SQLite temporário para os testes.

    O banco real data/banco.db nunca é utilizado pelos testes.
    """

    banco = tmp_path / "teste.db"

    conexao = sqlite3.connect(banco)

    conexao.execute("""
        CREATE TABLE clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            idade INTEGER NOT NULL,
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conexao.execute("""
        CREATE TABLE contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            saldo TEXT NOT NULL DEFAULT '0.00',
            limite TEXT NOT NULL DEFAULT '500.00',
            criada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (cliente_id)
                REFERENCES clientes(id)
        )
    """)

    conexao.execute("""
        CREATE TABLE transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conta_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            valor TEXT NOT NULL,
            saldo_anterior TEXT NOT NULL,
            saldo_posterior TEXT NOT NULL,
            criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (conta_id)
                REFERENCES contas(id)
        )
    """)

    conexao.commit()
    conexao.close()

    def conectar_teste():
        conexao = sqlite3.connect(banco)
        conexao.row_factory = sqlite3.Row
        return conexao

    monkeypatch.setattr(
        "app.database.database.conectar",
        conectar_teste
    )

    monkeypatch.setattr(
        "app.database.cliente_repository.conectar",
        conectar_teste
    )

    monkeypatch.setattr(
        "app.database.conta_repository.conectar",
        conectar_teste
    )

    monkeypatch.setattr(
        "app.database.transacao_repository.conectar",
        conectar_teste
    )

    # Importante:
    # ContaService importa conectar diretamente.
    monkeypatch.setattr(
        "app.services.conta_service.conectar",
        conectar_teste
    )

    return banco
