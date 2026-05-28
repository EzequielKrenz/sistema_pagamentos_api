from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import listar, obter_ou_404, remover
from app.database import get_db
from app.services.sale_service import criar_venda

router = APIRouter(prefix="/vendas", tags=["Vendas"])


@router.post("/", response_model=schemas.VendaResponse, status_code=201)
def cadastrar_venda(payload: schemas.VendaCreate, db: Session = Depends(get_db)):
    return criar_venda(db, payload)


@router.get("/", response_model=List[schemas.VendaResponse])
def listar_vendas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return listar(db, models.Venda, skip, limit)


@router.get("/{venda_id}", response_model=schemas.VendaResponse)
def buscar_venda(venda_id: int, db: Session = Depends(get_db)):
    return obter_ou_404(db, models.Venda, venda_id)


@router.delete("/{venda_id}", status_code=204)
def remover_venda(venda_id: int, db: Session = Depends(get_db)):
    venda = obter_ou_404(db, models.Venda, venda_id)
    return remover(db, venda)
