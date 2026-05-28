from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import atualizar, criar, listar, obter_ou_404, remover
from app.database import get_db

router = APIRouter(prefix="/condicoes-pagamento", tags=["Condições de pagamento"])


@router.post("/", response_model=schemas.CondicaoPagamentoResponse, status_code=201)
def criar_condicao(payload: schemas.CondicaoPagamentoCreate, db: Session = Depends(get_db)):
    return criar(db, models.CondicaoPagamento, payload.model_dump())


@router.get("/", response_model=List[schemas.CondicaoPagamentoResponse])
def listar_condicoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return listar(db, models.CondicaoPagamento, skip, limit)


@router.get("/{condicao_id}", response_model=schemas.CondicaoPagamentoResponse)
def buscar_condicao(condicao_id: int, db: Session = Depends(get_db)):
    return obter_ou_404(db, models.CondicaoPagamento, condicao_id)


@router.put("/{condicao_id}", response_model=schemas.CondicaoPagamentoResponse)
def atualizar_condicao(condicao_id: int, payload: schemas.CondicaoPagamentoUpdate, db: Session = Depends(get_db)):
    condicao = obter_ou_404(db, models.CondicaoPagamento, condicao_id)
    return atualizar(db, condicao, payload.model_dump(exclude_unset=True))


@router.delete("/{condicao_id}", status_code=204)
def remover_condicao(condicao_id: int, db: Session = Depends(get_db)):
    condicao = obter_ou_404(db, models.CondicaoPagamento, condicao_id)
    return remover(db, condicao)
