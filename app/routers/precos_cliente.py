from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import listar, obter_ou_404, remover
from app.database import get_db
from app.services.price_service import criar_preco_cliente, atualizar_preco_cliente

router = APIRouter(prefix="/precos-clientes", tags=["Tabela de preços do cliente"])


@router.post("/", response_model=schemas.PrecoClienteResponse, status_code=201)
def criar_preco(payload: schemas.PrecoClienteCreate, db: Session = Depends(get_db)):
    return criar_preco_cliente(db, payload)


@router.get("/", response_model=List[schemas.PrecoClienteResponse])
def listar_precos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return listar(db, models.PrecoCliente, skip, limit)


@router.get("/{preco_id}", response_model=schemas.PrecoClienteResponse)
def buscar_preco(preco_id: int, db: Session = Depends(get_db)):
    return obter_ou_404(db, models.PrecoCliente, preco_id)


@router.put("/{preco_id}", response_model=schemas.PrecoClienteResponse)
def atualizar_preco(preco_id: int, payload: schemas.PrecoClienteUpdate, db: Session = Depends(get_db)):
    return atualizar_preco_cliente(db, preco_id, payload)


@router.delete("/{preco_id}", status_code=204)
def remover_preco(preco_id: int, db: Session = Depends(get_db)):
    preco = obter_ou_404(db, models.PrecoCliente, preco_id)
    return remover(db, preco)
