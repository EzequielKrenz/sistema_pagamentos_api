# Sistema de Pagamentos API

API REST feita em Python com FastAPI, SQLAlchemy e SQLite para atender ao trabalho de Sistema de Pagamentos.

## O que o projeto entrega

1. **Novo modelo Entidade-Relacionamento**: mantém as entidades originais `cliente`, `produto` e `condicao_pagamento`, e adiciona `precos_cliente`, `vendas`, `venda_itens`, `eventos_preco` e `notificacoes`.
2. **CRUD completo**: clientes, produtos, condições de pagamento, tabela de preços, vendas e notificações.
3. **Cadastro de preços para aplicação web**: endpoint principal em `/precos-clientes/`.
4. **Notificação quando preço diminuir**: quando o preço de um produto é alterado, a API grava uma mensagem na fila `eventos_preco`. O worker processa depois e gera notificação para clientes que já compraram o produto por valor maior.
5. **Sem requisição HTTP para notificar**: a notificação não chama outro endpoint. Ela é processada por worker separado, usando uma fila no banco de dados.
6. **Relatório de vendas e produtos por cliente**: endpoint `/relatorios/vendas-cliente`, pesquisando por CNPJ ou Razão Social.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

## Como rodar no VS Code

Abra a pasta `sistema_pagamentos_api` no VS Code e rode os comandos abaixo no terminal.

### 1. Criar ambiente virtual

No Windows PowerShell:

```powershell
python3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, rode uma vez:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois ative novamente:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 3. Popular o banco com dados de exemplo

```powershell
python -m app.seed
```

### 4. Rodar a API

```powershell
uvicorn app.main:app --reload
```

Acesse no navegador:

```text
http://127.0.0.1:8000/docs
```

### 5. Rodar o worker de notificações

Abra outro terminal no VS Code, ative o ambiente virtual e execute:

```powershell
python -m app.worker
```

Esse worker é o responsável por processar a fila `eventos_preco` e gerar notificações sem prejudicar a performance da API.

## Teste rápido da regra de notificação

1. Rode o seed: `python -m app.seed`
2. Rode a API: `uvicorn app.main:app --reload`
3. Rode o worker em outro terminal: `python -m app.worker`
4. No Swagger, faça um `PUT /precos-clientes/1` com:

```json
{
  "preco": 80.00
}
```

5. Consulte:

```text
GET /notificacoes/?cliente_id=1
```

O cliente será notificado porque no seed ele comprou o produto por R$ 100,00 e o novo preço ficou R$ 80,00.

## Estrutura de pastas

```text
sistema_pagamentos_api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── seed.py
│   ├── worker.py
│   ├── routers/
│   │   ├── clientes.py
│   │   ├── produtos.py
│   │   ├── condicoes_pagamento.py
│   │   ├── precos_cliente.py
│   │   ├── vendas.py
│   │   ├── notificacoes.py
│   │   └── relatorios.py
│   └── services/
│       ├── price_service.py
│       ├── sale_service.py
│       └── notification_service.py
├── docs/
│   ├── diagrama-er.md
│   └── rotas.md
├── requirements.txt
├── .env.example
└── README.md
```
