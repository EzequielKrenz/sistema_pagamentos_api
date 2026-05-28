from datetime import datetime
from decimal import Decimal
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models


def processar_eventos_pendentes(db: Session, limite: int = 20) -> int:
    eventos = (
        db.query(models.EventoPreco)
        .filter(models.EventoPreco.status == "PENDENTE")
        .order_by(models.EventoPreco.criado_em.asc())
        .limit(limite)
        .all()
    )

    processados = 0
    for evento in eventos:
        try:
            evento.status = "PROCESSANDO"
            db.commit()

            produto = db.get(models.Produto, evento.produto_id)
            if not produto:
                evento.status = "ERRO"
                evento.erro = "Produto do evento não encontrado."
                evento.processado_em = datetime.utcnow()
                db.commit()
                continue

            compras_por_cliente = (
                db.query(
                    models.Venda.cliente_id.label("cliente_id"),
                    func.max(models.VendaItem.preco_unitario).label("maior_preco_pago"),
                )
                .join(models.VendaItem, models.VendaItem.venda_id == models.Venda.id)
                .filter(
                    models.VendaItem.produto_id == evento.produto_id,
                    models.VendaItem.preco_unitario > evento.novo_preco,
                )
                .group_by(models.Venda.cliente_id)
                .all()
            )

            for compra in compras_por_cliente:
                cliente = db.get(models.Cliente, compra.cliente_id)
                preco_pago = Decimal(compra.maior_preco_pago)
                mensagem = (
                    f"O produto '{produto.descricao}' agora está sendo vendido por "
                    f"R$ {Decimal(evento.novo_preco):.2f}, valor inferior ao preço "
                    f"já pago por este cliente: R$ {preco_pago:.2f}."
                )

                notificacao = models.Notificacao(
                    cliente_id=compra.cliente_id,
                    produto_id=evento.produto_id,
                    evento_preco_id=evento.id,
                    mensagem=mensagem,
                    preco_pago=preco_pago,
                    novo_preco=evento.novo_preco,
                    status="PENDENTE",
                )
                db.add(notificacao)

            evento.status = "CONCLUIDO"
            evento.processado_em = datetime.utcnow()
            evento.erro = None
            db.commit()
            processados += 1
        except Exception as exc:  # noqa: BLE001 - salva o erro do worker sem derrubar a fila inteira
            db.rollback()
            evento = db.get(models.EventoPreco, evento.id)
            if evento:
                evento.status = "ERRO"
                evento.erro = str(exc)
                evento.processado_em = datetime.utcnow()
                db.commit()

    return processados


def marcar_como_lida(db: Session, notificacao_id: int) -> models.Notificacao | None:
    notificacao = db.get(models.Notificacao, notificacao_id)
    if not notificacao:
        return None
    notificacao.status = "LIDA"
    notificacao.lida_em = datetime.utcnow()
    db.commit()
    db.refresh(notificacao)
    return notificacao
