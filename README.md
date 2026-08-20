# Sistema Bancário

Sistema bancário desenvolvido em Python com SQLite, utilizando uma arquitetura organizada em modelos, repositórios e serviços.

O projeto permite cadastrar clientes, criar contas, realizar depósitos e saques, consultar saldo e limite disponível, além de consultar o extrato bancário e registrar todas as transações.

## Funcionalidades

* Cadastro de clientes
* Validação de CPF
* Validação de idade mínima
* Prevenção de CPF duplicado
* Consulta de cliente por CPF
* Listagem de clientes
* Criação de contas bancárias
* Definição de saldo inicial
* Definição de limite
* Consulta de saldo
* Consulta de valor disponível
* Depósitos
* Saques
* Validação de saldo e limite
* Registro de transações
* Extrato bancário
* Tratamento de erros
* Testes automatizados com pytest

## Tecnologias

* Python 3.12+
* SQLite
* pytest
* Git
* Decimal para operações monetárias

## Estrutura do projeto

```text
sistema-bancario/
├── app/
│   ├── database/
│   │   ├── cliente_repository.py
│   │   ├── conta_repository.py
│   │   ├── database.py
│   │   └── transacao_repository.py
│   │
│   ├── models/
│   │   ├── cliente.py
│   │   └── conta.py
│   │
│   ├── services/
│   │   ├── cliente_service.py
│   │   └── conta_service.py
│   │
│   └── utils/
│
├── data/
│   └── banco.db
│
├── tests/
│   ├── conftest.py
│   ├── test_cliente_service.py
│   └── test_conta_service.py
│
├── main.py
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
```

## Arquitetura

O projeto utiliza uma separação de responsabilidades:

### Models

Representam as entidades do sistema.

* `Cliente`
* `Conta`

### Repositories

Responsáveis pelo acesso ao banco de dados.

* `ClienteRepository`
* `ContaRepository`
* `TransacaoRepository`

### Services

Contêm as regras de negócio.

* `ClienteService`
* `ContaService`

### Database

Responsável pela conexão com o SQLite e criação das tabelas.

## Banco de dados

O projeto utiliza SQLite.

O banco local é criado em:

```text
data/banco.db
```

O arquivo do banco de dados não é versionado pelo Git, conforme definido no `.gitignore`.

As principais tabelas são:

* `clientes`
* `contas`
* `transacoes`

## Instalação

Clone o projeto:

```bash
git clone URL_DO_REPOSITORIO
cd sistema-bancario
```

Crie o ambiente virtual:

```bash
python3 -m venv .venv
```

Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executando o sistema

Com o ambiente virtual ativado:

```bash
python3 main.py
```

O sistema apresenta um menu semelhante a:

```text
==================================================
              SISTEMA BANCÁRIO
==================================================
1 - Cadastrar cliente
2 - Criar conta
3 - Depositar
4 - Sacar
5 - Consultar saldo
6 - Consultar disponível
7 - Consultar extrato
8 - Listar clientes
9 - Sair
==================================================
```

## Executando os testes

Para executar todos os testes:

```bash
pytest -q
```

Para executar com detalhes:

```bash
pytest -v
```

### Resultado atual

O projeto possui **91 testes automatizados**, todos passando:

```text
91 passed
```

Os testes cobrem:

* Cadastro de clientes
* Busca por CPF
* CPF duplicado
* CPF inválido
* Idade mínima
* Listagem de clientes
* Criação de contas
* Cliente inexistente
* Saldo inicial inválido
* Limite inválido
* Consulta de saldo
* Consulta de disponível
* Depósitos
* Saques
* Valores inválidos
* Contas inexistentes
* Limite disponível
* Registro de transações
* Extrato bancário

## Exemplo de operação

Uma conta pode iniciar com:

```text
Saldo: 100.00
Limite: 500.00
Disponível: 600.00
```

Depois de um depósito de `50.00`:

```text
Saldo: 150.00
Disponível: 650.00
```

Depois de um saque de `40.00`:

```text
Saldo: 110.00
Disponível: 610.00
```

As operações são registradas no histórico de transações.

## Segurança e consistência

As operações financeiras utilizam `Decimal` para evitar problemas comuns de precisão de ponto flutuante.

Depósitos e saques são registrados juntamente com:

* valor
* saldo anterior
* saldo posterior
* tipo da operação
* data e hora
* conta relacionada

As operações de alteração de saldo e registro da transação utilizam uma mesma conexão e transação SQLite, permitindo rollback caso ocorra algum erro.

## Git

O projeto utiliza Git para controle de versão.

Para verificar o estado:

```bash
git status
```

Para visualizar os commits:

```bash
git log --oneline
```

## Próximas melhorias

Possíveis evoluções do sistema:

* Transferências entre contas
* Autenticação de usuários
* Senhas/PIN
* Histórico completo de operações
* Paginação do extrato
* Relatórios
* API REST
* Interface web
* Interface gráfica
* Testes de integração
* Docker
* CI/CD
* PostgreSQL para ambiente de produção

## Status

**Versão atual: funcional**

* Cadastro de clientes: OK
* Contas: OK
* Depósitos: OK
* Saques: OK
* Limites: OK
* Transações: OK
* Extrato: OK
* Testes automatizados: 91/91 passando
* Git: configurado
