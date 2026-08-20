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
def test_nome_vazio_deve_gerar_erro(banco_teste):
    service = ClienteService()

    try:
        service.cadastrar_cliente(
            nome="   ",
            cpf="77777777777",
            idade=25
        )

        assert False, (
            "Era esperado erro para nome vazio."
        )

    except ValueError as erro:
        assert str(erro) == "Nome é obrigatório."


def test_cpf_com_letras_deve_gerar_erro(banco_teste):
    service = ClienteService()

    try:
        service.cadastrar_cliente(
            nome="Cliente Teste",
            cpf="1234567890A",
            idade=25
        )

        assert False, (
            "Era esperado erro para CPF com letras."
        )

    except ValueError as erro:
        assert (
            str(erro)
            == "CPF deve conter apenas números."
        )


def test_buscar_cpf_inexistente(banco_teste):
    service = ClienteService()

    cliente = service.buscar_por_cpf(
        "88888888888"
    )

    assert cliente is None


def test_buscar_cpf_com_letras_deve_gerar_erro(banco_teste):
    service = ClienteService()

    try:
        service.buscar_por_cpf(
            "1234567890A"
        )

        assert False, (
            "Era esperado erro para CPF com letras."
        )

    except ValueError as erro:
        assert (
            str(erro)
            == "CPF deve conter apenas números."
        )
def test_buscar_cpf_com_tamanho_invalido_deve_gerar_erro(banco_teste):
    service = ClienteService()

    try:
        service.buscar_por_cpf(
            "123456789"
        )

        assert False, (
            "Era esperado erro para CPF com tamanho inválido."
        )

    except ValueError as erro:
        assert (
            str(erro)
            == "CPF deve possuir 11 números."
        )
def test_idade_18_anos_deve_ser_valida(banco_teste):
    service = ClienteService()

    cliente_id = service.cadastrar_cliente(
        nome="Cliente Maior",
        cpf="99999999999",
        idade=18
    )

    assert cliente_id == 1


def test_idade_zero_deve_gerar_erro(banco_teste):
    service = ClienteService()

    try:
        service.cadastrar_cliente(
            nome="Cliente Teste",
            cpf="10101010101",
            idade=0
        )

        assert False, (
            "Era esperado erro para idade zero."
        )

    except ValueError as erro:
        assert (
            str(erro)
            == "Cliente deve possuir pelo menos 18 anos."
        )


def test_idade_negativa_deve_gerar_erro(banco_teste):
    service = ClienteService()

    try:
        service.cadastrar_cliente(
            nome="Cliente Teste",
            cpf="20202020202",
            idade=-1
        )

        assert False, (
            "Era esperado erro para idade negativa."
        )

    except ValueError as erro:
        assert (
            str(erro)
            == "Cliente deve possuir pelo menos 18 anos."
        )


def test_idade_string_deve_gerar_erro(banco_teste):
    service = ClienteService()

    try:
        service.cadastrar_cliente(
            nome="Cliente Teste",
            cpf="30303030303",
            idade="18"
        )

        assert False, (
            "Era esperado erro para idade inválida."
        )

    except (ValueError, TypeError) as erro:
        assert erro is not None


def test_idade_float_deve_gerar_erro(banco_teste):
    service = ClienteService()

    try:
        service.cadastrar_cliente(
            nome="Cliente Teste",
            cpf="40404040404",
            idade=18.5
        )

        assert False, (
            "Era esperado erro para idade inválida."
        )

    except (ValueError, TypeError) as erro:
        assert erro is not None


def test_idade_booleano_deve_gerar_erro(banco_teste):
    service = ClienteService()

    try:
        service.cadastrar_cliente(
            nome="Cliente Teste",
            cpf="50505050505",
            idade=True
        )

        assert False, (
            "Era esperado erro para idade inválida."
        )

    except (ValueError, TypeError) as erro:
        assert erro is not None
