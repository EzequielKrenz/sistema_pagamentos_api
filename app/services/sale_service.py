from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.crud import obter_ou_404
from app.schemas import VendaCreate


def criar_venda(db: Session, payload: VendaCreate) -> models.Venda:
    obter_ou_404(db, models.Cliente, payload.cliente_id)
    obter_ou_404(db, models.CondicaoPagamento, payload.condicao_pagamento_id)

    venda = models.Venda(
        cliente_id=payload.cliente_id,
        condicao_pagamento_id=payload.condicao_pagamento_id,
        total=Decimal("0.00"),
    )
    db.add(venda)
    db.flush()

    total = Decimal("0.00")
    for item_payload in payload.itens:
        produto = obter_ou_404(db, models.Produto, item_payload.produto_id)
        if not produto.ativo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Produto {produto.id} está inativo.",
            )
        subtotal = Decimal(item_payload.quantidade) * Decimal(item_payload.preco_unitario)
        item = models.VendaItem(
            venda_id=venda.id,
            produto_id=item_payload.produto_id,
            quantidade=item_payload.quantidade,
            preco_unitario=item_payload.preco_unitario,
            subtotal=subtotal,
        )
        db.add(item)
        total += subtotal

    venda.total = total
    db.commit()
    db.refresh(venda)
    return venda
