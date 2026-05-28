# Rotas principais da API

Após iniciar o projeto, acesse:

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

## Clientes

- `POST /clientes/`
- `GET /clientes/`
- `GET /clientes/{cliente_id}`
- `PUT /clientes/{cliente_id}`
- `DELETE /clientes/{cliente_id}`

## Produtos

- `POST /produtos/`
- `GET /produtos/`
- `GET /produtos/{produto_id}`
- `PUT /produtos/{produto_id}`
- `DELETE /produtos/{produto_id}`

## Condições de pagamento

- `POST /condicoes-pagamento/`
- `GET /condicoes-pagamento/`
- `GET /condicoes-pagamento/{condicao_id}`
- `PUT /condicoes-pagamento/{condicao_id}`
- `DELETE /condicoes-pagamento/{condicao_id}`

## Tabela de preços do cliente

- `POST /precos-clientes/`
- `GET /precos-clientes/`
- `GET /precos-clientes/{preco_id}`
- `PUT /precos-clientes/{preco_id}`
- `DELETE /precos-clientes/{preco_id}`

Exemplo para baixar preço e gerar evento de notificação:

```json
{
  "preco": 80.00
}
```

Enviar esse JSON em: `PUT /precos-clientes/1`

## Vendas

- `POST /vendas/`
- `GET /vendas/`
- `GET /vendas/{venda_id}`
- `DELETE /vendas/{venda_id}`

Exemplo de venda:

```json
{
  "cliente_id": 1,
  "condicao_pagamento_id": 1,
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 2,
      "preco_unitario": 100.00
    }
  ]
}
```

## Notificações

- `GET /notificacoes/`
- `GET /notificacoes/?cliente_id=1`
- `PATCH /notificacoes/{notificacao_id}/ler`
- `DELETE /notificacoes/{notificacao_id}`

## Relatório

Buscar por CNPJ:

`GET /relatorios/vendas-cliente?cnpj=12.345.678/0001-99`

Buscar por razão social:

`GET /relatorios/vendas-cliente?razao_social=Mercado`
