# Diagrama Entidade-Relacionamento proposto

```mermaid
erDiagram
    CLIENTE ||--o{ PRECO_CLIENTE : possui
    CLIENTE ||--o{ VENDA : realiza
    CLIENTE ||--o{ NOTIFICACAO : recebe

    PRODUTO ||--o{ PRECO_CLIENTE : tem_preco
    PRODUTO ||--o{ VENDA_ITEM : vendido_em
    PRODUTO ||--o{ EVENTO_PRECO : gera
    PRODUTO ||--o{ NOTIFICACAO : citado_em

    CONDICAO_PAGAMENTO ||--o{ PRECO_CLIENTE : define
    CONDICAO_PAGAMENTO ||--o{ VENDA : usada_em

    VENDA ||--o{ VENDA_ITEM : contem
    EVENTO_PRECO ||--o{ NOTIFICACAO : origina

    CLIENTE {
        int id PK
        string cnpj UK
        string razao_social
        string email
        bool ativo
    }

    PRODUTO {
        int id PK
        string sku UK
        string descricao
        bool ativo
    }

    CONDICAO_PAGAMENTO {
        int id PK
        string descricao
        int dias
        bool ativo
    }

    PRECO_CLIENTE {
        int id PK
        int cliente_id FK
        int produto_id FK
        int condicao_pagamento_id FK
        decimal preco
        bool ativo
    }

    VENDA {
        int id PK
        int cliente_id FK
        int condicao_pagamento_id FK
        datetime data_venda
        decimal total
    }

    VENDA_ITEM {
        int id PK
        int venda_id FK
        int produto_id FK
        int quantidade
        decimal preco_unitario
        decimal subtotal
    }

    EVENTO_PRECO {
        int id PK
        int produto_id FK
        decimal novo_preco
        string status
        datetime criado_em
    }

    NOTIFICACAO {
        int id PK
        int cliente_id FK
        int produto_id FK
        int evento_preco_id FK
        decimal preco_pago
        decimal novo_preco
        string status
    }
```

## Entidades novas criadas

1. **precos_cliente**: representa a tabela de preços praticada por cliente, produto e condição de pagamento.
2. **vendas**: cabeçalho da venda realizada para um cliente.
3. **venda_itens**: produtos vendidos em cada venda, mantendo o preço praticado no momento da compra.
4. **eventos_preco**: fila de mensagens de alteração de preço, usada para não travar a requisição HTTP.
5. **notificacoes**: notificações geradas para clientes que compraram um produto por valor maior que o preço atual.
