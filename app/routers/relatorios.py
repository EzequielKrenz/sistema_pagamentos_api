from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/vendas-cliente", response_model=List[schemas.RelatorioClienteResponse])
def relatorio_vendas_cliente(
    cnpj: Optional[str] = None,
    razao_social: Optional[str] = None,
    db: Session = Depends(get_db),
):
    if not cnpj and not razao_social:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Informe CNPJ ou Razão Social para localizar o cliente.",
        )

    consulta_clientes = db.query(models.Cliente)
    if cnpj:
        consulta_clientes = consulta_clientes.filter(models.Cliente.cnpj == cnpj)
    if razao_social:
        consulta_clientes = consulta_clientes.filter(models.Cliente.razao_social.ilike(f"%{razao_social}%"))

    clientes = consulta_clientes.all()
    if not clientes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado.")

    relatorios = []
    for cliente in clientes:
        vendas = (
            db.query(models.Venda)
            .options(
                joinedload(models.Venda.condicao_pagamento),
                joinedload(models.Venda.itens).joinedload(models.VendaItem.produto),
            )
            .filter(models.Venda.cliente_id == cliente.id)
            .order_by(models.Venda.data_venda.desc())
            .all()
        )

        vendas_relatorio = []
        total_geral = Decimal("0.00")
        for venda in vendas:
            total_geral += Decimal(venda.total)
            produtos = [
                schemas.RelatorioItemProduto(
                    produto_id=item.produto_id,
                    sku=item.produto.sku,
                    descricao=item.produto.descricao,
                    quantidade=item.quantidade,
                    preco_unitario=item.preco_unitario,
                    subtotal=item.subtotal,
                )
                for item in venda.itens
            ]
            vendas_relatorio.append(
                schemas.RelatorioVenda(
                    venda_id=venda.id,
                    data_venda=venda.data_venda,
                    condicao_pagamento=venda.condicao_pagamento.descricao,
                    total=venda.total,
                    produtos=produtos,
                )
            )

        relatorios.append(
            schemas.RelatorioClienteResponse(
                cliente_id=cliente.id,
                cnpj=cliente.cnpj,
                razao_social=cliente.razao_social,
                total_geral=total_geral,
                vendas=vendas_relatorio,
            )
        )

    return relatorios
