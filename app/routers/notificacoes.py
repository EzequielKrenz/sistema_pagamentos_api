from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import listar, obter_ou_404, remover
from app.database import get_db
from app.services.notification_service import marcar_como_lida

router = APIRouter(prefix="/notificacoes", tags=["Notificações"])


@router.get("/", response_model=List[schemas.NotificacaoResponse])
def listar_notificacoes(
    cliente_id: Optional[int] = None,
    status_notificacao: Optional[str] = None,
    db: Session = Depends(get_db),
):
    consulta = db.query(models.Notificacao)
    if cliente_id is not None:
        consulta = consulta.filter(models.Notificacao.cliente_id == cliente_id)
    if status_notificacao is not None:
        consulta = consulta.filter(models.Notificacao.status == status_notificacao.upper())
    return consulta.order_by(models.Notificacao.criado_em.desc()).all()


@router.get("/{notificacao_id}", response_model=schemas.NotificacaoResponse)
def buscar_notificacao(notificacao_id: int, db: Session = Depends(get_db)):
    return obter_ou_404(db, models.Notificacao, notificacao_id)


@router.patch("/{notificacao_id}/ler", response_model=schemas.NotificacaoResponse)
def ler_notificacao(notificacao_id: int, db: Session = Depends(get_db)):
    notificacao = marcar_como_lida(db, notificacao_id)
    if not notificacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notificação não encontrada.")
    return notificacao


@router.delete("/{notificacao_id}", status_code=204)
def remover_notificacao(notificacao_id: int, db: Session = Depends(get_db)):
    notificacao = obter_ou_404(db, models.Notificacao, notificacao_id)
    return remover(db, notificacao)
