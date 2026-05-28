from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import atualizar, criar, listar, obter_ou_404, remover
from app.database import get_db

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=schemas.ClienteResponse, status_code=201)
def criar_cliente(payload: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return criar(db, models.Cliente, payload.model_dump())


@router.get("/", response_model=List[schemas.ClienteResponse])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return listar(db, models.Cliente, skip, limit)


@router.get("/{cliente_id}", response_model=schemas.ClienteResponse)
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return obter_ou_404(db, models.Cliente, cliente_id)


@router.put("/{cliente_id}", response_model=schemas.ClienteResponse)
def atualizar_cliente(cliente_id: int, payload: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    cliente = obter_ou_404(db, models.Cliente, cliente_id)
    return atualizar(db, cliente, payload.model_dump(exclude_unset=True))


@router.delete("/{cliente_id}", status_code=204)
def remover_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = obter_ou_404(db, models.Cliente, cliente_id)
    return remover(db, cliente)
