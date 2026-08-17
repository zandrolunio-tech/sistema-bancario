from app.database.cliente_repository import ClienteRepository
from app.models.cliente import Cliente


class ClienteService:

    def __init__(self):
        self.repository = ClienteRepository()

    def cadastrar_cliente(
        self,
        nome: str,
        cpf: str,
        idade: int
    ) -> int:

        nome = nome.strip()
        cpf = cpf.strip()

        if not nome:
            raise ValueError(
                "Nome é obrigatório."
            )

        if not cpf.isdigit():
            raise ValueError(
                "CPF deve conter apenas números."
            )

        if len(cpf) != 11:
            raise ValueError(
                "CPF deve possuir 11 números."
            )

        if idade < 18:
            raise ValueError(
                "Cliente deve possuir pelo menos 18 anos."
            )

        cliente_existente = (
            self.repository.buscar_por_cpf(cpf)
        )

        if cliente_existente:
            raise ValueError(
                "CPF já cadastrado."
            )

        cliente = Cliente(
            nome=nome,
            cpf=cpf,
            idade=idade
        )

        return self.repository.criar(cliente)

    def buscar_por_cpf(self, cpf: str):

        cpf = cpf.strip()

        if not cpf.isdigit():
            raise ValueError(
                "CPF deve conter apenas números."
            )

        if len(cpf) != 11:
            raise ValueError(
                "CPF deve possuir 11 números."
            )

        return self.repository.buscar_por_cpf(cpf)

    def listar_clientes(self):

        return self.repository.listar_todos()