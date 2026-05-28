from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import criar_tabelas
from app.routers import (
    clientes,
    condicoes_pagamento,
    notificacoes,
    precos_cliente,
    produtos,
    relatorios,
    vendas,
)

criar_tabelas()

app = FastAPI(
    title="Sistema de Pagamentos API",
    description="API REST para clientes, produtos, condições de pagamento, tabela de preços, vendas, notificações assíncronas e relatórios.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router)
app.include_router(produtos.router)
app.include_router(condicoes_pagamento.router)
app.include_router(precos_cliente.router)
app.include_router(vendas.router)
app.include_router(notificacoes.router)
app.include_router(relatorios.router)


@app.get("/", tags=["Status"])
def status_api():
    return {
        "mensagem": "Sistema de Pagamentos API online",
        "documentacao": "/docs",
    }
