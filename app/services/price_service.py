from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.crud import obter_ou_404
from app.schemas import PrecoClienteCreate, PrecoClienteUpdate


def validar_relacionamentos_preco(db: Session, cliente_id: int, produto_id: int, condicao_pagamento_id: int) -> None:
    obter_ou_404(db, models.Cliente, cliente_id)
    obter_ou_404(db, models.Produto, produto_id)
    obter_ou_404(db, models.CondicaoPagamento, condicao_pagamento_id)


def enfileirar_evento_preco(
    db: Session,
    produto_id: int,
    novo_preco: Decimal,
    origem_preco_cliente_id: int | None = None,
) -> models.EventoPreco:
    evento = models.EventoPreco(
        produto_id=produto_id,
        novo_preco=novo_preco,
        origem_preco_cliente_id=origem_preco_cliente_id,
        status="PENDENTE",
    )
    db.add(evento)
    return evento


def criar_preco_cliente(db: Session, payload: PrecoClienteCreate) -> models.PrecoCliente:
    validar_relacionamentos_preco(
        db,
        payload.cliente_id,
        payload.produto_id,
        payload.condicao_pagamento_id,
    )

    preco_existente = (
        db.query(models.PrecoCliente)
        .filter(
            models.PrecoCliente.cliente_id == payload.cliente_id,
            models.PrecoCliente.produto_id == payload.produto_id,
            models.PrecoCliente.condicao_pagamento_id == payload.condicao_pagamento_id,
        )
        .first()
    )
    if preco_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe preço cadastrado para este cliente, produto e condição de pagamento.",
        )

    preco = models.PrecoCliente(**payload.model_dump())
    db.add(preco)
    db.flush()
    enfileirar_evento_preco(db, payload.produto_id, payload.preco, preco.id)
    db.commit()
    db.refresh(preco)
    return preco


def atualizar_preco_cliente(
    db: Session,
    preco_id: int,
    payload: PrecoClienteUpdate,
) -> models.PrecoCliente:
    preco = obter_ou_404(db, models.PrecoCliente, preco_id)
    dados = payload.model_dump(exclude_unset=True)

    cliente_id = dados.get("cliente_id", preco.cliente_id)
    produto_id = dados.get("produto_id", preco.produto_id)
    condicao_pagamento_id = dados.get("condicao_pagamento_id", preco.condicao_pagamento_id)
    validar_relacionamentos_preco(db, cliente_id, produto_id, condicao_pagamento_id)

    preco_anterior = Decimal(preco.preco)
    novo_preco = Decimal(dados.get("preco", preco.preco))

    for campo, valor in dados.items():
        setattr(preco, campo, valor)

    if novo_preco != preco_anterior:
        enfileirar_evento_preco(db, produto_id, novo_preco, preco.id)

    db.commit()
    db.refresh(preco)
    return preco
