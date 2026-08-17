from decimal import Decimal, InvalidOperation

from app.services.cliente_service import ClienteService
from app.services.conta_service import ContaService


def ler_inteiro(mensagem):
    """
    Lê um número inteiro informado pelo usuário.
    """
    try:
        valor = input(mensagem).strip()

        if not valor:
            raise ValueError

        return int(valor)

    except ValueError:
        raise ValueError("O valor deve ser um número inteiro.")


def ler_decimal(mensagem):
    """
    Lê um valor monetário informado pelo usuário.
    """
    try:
        valor = input(mensagem).strip()

        if not valor:
            raise ValueError(
                "O valor não pode ficar vazio."
            )

        valor = valor.replace(",", ".")

        return Decimal(valor)

    except InvalidOperation:
        raise ValueError(
            "Valor monetário inválido."
        )


def mostrar_menu():
    print("\n" + "=" * 50)
    print("              SISTEMA BANCÁRIO")
    print("=" * 50)
    print("1 - Cadastrar cliente")
    print("2 - Criar conta")
    print("3 - Depositar")
    print("4 - Sacar")
    print("5 - Consultar saldo")
    print("6 - Consultar disponível")
    print("7 - Consultar extrato")
    print("8 - Listar clientes")
    print("9 - Sair")
    print("=" * 50)


def cadastrar_cliente(cliente_service):
    print("\n--- CADASTRAR CLIENTE ---")

    nome = input("Nome: ").strip()
    cpf = input("CPF: ").strip()

    try:
        idade = ler_inteiro("Idade: ")

        cliente_id = cliente_service.cadastrar_cliente(
            nome=nome,
            cpf=cpf,
            idade=idade
        )

        print(
            "\nCliente cadastrado com sucesso!"
        )
        print(f"ID: {cliente_id}")

    except ValueError as erro:
        print(f"\nErro: {erro}")


def criar_conta(conta_service):
    print("\n--- CRIAR CONTA ---")

    try:
        cliente_id = ler_inteiro(
            "ID do cliente: "
        )

        saldo_inicial = ler_decimal(
            "Saldo inicial: "
        )

        limite = ler_decimal(
            "Limite: "
        )

        conta_id = conta_service.criar_conta(
            cliente_id=cliente_id,
            saldo_inicial=saldo_inicial,
            limite=limite
        )

        print(
            "\nConta criada com sucesso!"
        )
        print(f"ID da conta: {conta_id}")

    except ValueError as erro:
        print(f"\nErro: {erro}")


def depositar(conta_service):
    print("\n--- DEPÓSITO ---")

    try:
        conta_id = ler_inteiro(
            "ID da conta: "
        )

        valor = ler_decimal(
            "Valor do depósito: "
        )

        novo_saldo = conta_service.depositar(
            conta_id,
            valor
        )

        print(
            "\nDepósito realizado com sucesso!"
        )
        print(
            f"Novo saldo: {novo_saldo:.2f}"
        )

    except ValueError as erro:
        print(f"\nErro: {erro}")


def sacar(conta_service):
    print("\n--- SAQUE ---")

    try:
        conta_id = ler_inteiro(
            "ID da conta: "
        )

        valor = ler_decimal(
            "Valor do saque: "
        )

        novo_saldo = conta_service.sacar(
            conta_id,
            valor
        )

        print(
            "\nSaque realizado com sucesso!"
        )
        print(
            f"Novo saldo: {novo_saldo:.2f}"
        )

    except ValueError as erro:
        print(f"\nErro: {erro}")


def consultar_saldo(conta_service):
    print("\n--- CONSULTAR SALDO ---")

    try:
        conta_id = ler_inteiro(
            "ID da conta: "
        )

        saldo = conta_service.consultar_saldo(
            conta_id
        )

        print(
            f"\nSaldo: {saldo:.2f}"
        )

    except ValueError as erro:
        print(f"\nErro: {erro}")


def consultar_disponivel(conta_service):
    print("\n--- CONSULTAR DISPONÍVEL ---")

    try:
        conta_id = ler_inteiro(
            "ID da conta: "
        )

        disponivel = (
            conta_service.consultar_disponivel(
                conta_id
            )
        )

        print(
            f"\nDisponível: {disponivel:.2f}"
        )

    except ValueError as erro:
        print(f"\nErro: {erro}")


def consultar_extrato(conta_service):
    print("\n--- EXTRATO BANCÁRIO ---")

    try:
        conta_id = ler_inteiro(
            "ID da conta: "
        )

        extrato = conta_service.consultar_extrato(
            conta_id
        )

        cliente = extrato["cliente"]
        conta = extrato["conta"]
        transacoes = extrato["transacoes"]

        print("\n" + "=" * 50)
        print("              EXTRATO BANCÁRIO")
        print("=" * 50)

        print(f"Cliente: {cliente['nome']}")
        print(f"CPF: {cliente['cpf']}")
        print(f"Conta: {conta['id']}")

        print("-" * 50)

        print(
            f"Saldo:       "
            f"{extrato['saldo']:.2f}"
        )

        print(
            f"Limite:      "
            f"{extrato['limite']:.2f}"
        )

        print(
            f"Disponível:  "
            f"{extrato['disponivel']:.2f}"
        )

        print("-" * 50)

        print(
            "Total de transações: "
            f"{extrato['total_transacoes']}"
        )

        print("-" * 50)

        if not transacoes:
            print(
                "Nenhuma transação encontrada."
            )
        else:
            for transacao in transacoes:
                print(
                    f"ID: {transacao['id']} | "
                    f"{transacao['tipo']} | "
                    f"Valor: "
                    f"{transacao['valor']} | "
                    f"Saldo: "
                    f"{transacao['saldo_posterior']}"
                )

        print("=" * 50)

    except ValueError as erro:
        print(f"\nErro: {erro}")


def listar_clientes(cliente_service):
    print("\n--- CLIENTES ---")

    try:
        clientes = (
            cliente_service.listar_clientes()
        )

        if not clientes:
            print(
                "Nenhum cliente cadastrado."
            )
            return

        print()

        for cliente in clientes:
            print(
                f"ID: {cliente['id']} | "
                f"Nome: {cliente['nome']} | "
                f"CPF: {cliente['cpf']} | "
                f"Idade: {cliente['idade']}"
            )

    except ValueError as erro:
        print(f"\nErro: {erro}")


def main():
    cliente_service = ClienteService()
    conta_service = ContaService()

    while True:
        mostrar_menu()

        opcao = input(
            "Escolha uma opção: "
        ).strip()

        if opcao == "1":
            cadastrar_cliente(
                cliente_service
            )

        elif opcao == "2":
            criar_conta(
                conta_service
            )

        elif opcao == "3":
            depositar(
                conta_service
            )

        elif opcao == "4":
            sacar(
                conta_service
            )

        elif opcao == "5":
            consultar_saldo(
                conta_service
            )

        elif opcao == "6":
            consultar_disponivel(
                conta_service
            )

        elif opcao == "7":
            consultar_extrato(
                conta_service
            )

        elif opcao == "8":
            listar_clientes(
                cliente_service
            )

        elif opcao == "9":
            print(
                "\nSistema encerrado."
            )
            break

        else:
            print(
                "\nErro: opção inválida."
            )


if __name__ == "__main__":
    main()