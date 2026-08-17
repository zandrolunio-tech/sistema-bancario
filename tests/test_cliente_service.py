from app.services.cliente_service import ClienteService


def test_cadastrar_cliente_com_sucesso(banco_teste):
    service = ClienteService()

    cliente_id = service.cadastrar_cliente(
        nome="Cliente Teste",
        cpf="11111111111",
        idade=25
    )

    assert cliente_id == 1


def test_buscar_cliente_por_cpf(banco_teste):
    service = ClienteService()

    service.cadastrar_cliente(
        nome="Maria Teste",
        cpf="22222222222",
        idade=30
    )

    cliente = service.buscar_por_cpf(
        "22222222222"
    )

    assert cliente is not None
    assert cliente["nome"] == "Maria Teste"
    assert cliente["cpf"] == "22222222222"
    assert cliente["idade"] == 30


def test_cpf_duplicado_deve_gerar_erro(banco_teste):
    service = ClienteService()

    service.cadastrar_cliente(
        nome="Primeiro Cliente",
        cpf="33333333333",
        idade=25
    )

    try:
        service.cadastrar_cliente(
            nome="Segundo Cliente",
            cpf="33333333333",
            idade=30
        )

        assert False, (
            "Era esperado erro para CPF duplicado."
        )

    except ValueError as erro:
        assert str(erro) == "CPF já cadastrado."


def test_cpf_com_tamanho_invalido(banco_teste):
    service = ClienteService()

    try:
        service.cadastrar_cliente(
            nome="Cliente Teste",
            cpf="123456789",
            idade=25
        )

        assert False, (
            "Era esperado erro para CPF inválido."
        )

    except ValueError as erro:
        assert "11 números" in str(erro)


def test_idade_menor_de_18_deve_gerar_erro(banco_teste):
    service = ClienteService()

    try:
        service.cadastrar_cliente(
            nome="Cliente Teste",
            cpf="44444444444",
            idade=17
        )

        assert False, (
            "Era esperado erro para idade menor de 18."
        )

    except ValueError as erro:
        assert (
            str(erro)
            == "Cliente deve possuir pelo menos 18 anos."
        )


def test_listar_clientes(banco_teste):
    service = ClienteService()

    service.cadastrar_cliente(
        nome="Cliente Um",
        cpf="55555555555",
        idade=20
    )

    service.cadastrar_cliente(
        nome="Cliente Dois",
        cpf="66666666666",
        idade=30
    )

    clientes = service.listar_clientes()

    assert len(clientes) == 2
    assert clientes[0]["nome"] == "Cliente Um"
    assert clientes[1]["nome"] == "Cliente Dois"
