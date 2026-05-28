from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import atualizar, criar, listar, obter_ou_404, remover
from app.database import get_db

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("/", response_model=schemas.ProdutoResponse, status_code=201)
def criar_produto(payload: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return criar(db, models.Produto, payload.model_dump())


@router.get("/", response_model=List[schemas.ProdutoResponse])
def listar_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return listar(db, models.Produto, skip, limit)


@router.get("/{produto_id}", response_model=schemas.ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    return obter_ou_404(db, models.Produto, produto_id)


@router.put("/{produto_id}", response_model=schemas.ProdutoResponse)
def atualizar_produto(produto_id: int, payload: schemas.ProdutoUpdate, db: Session = Depends(get_db)):
    produto = obter_ou_404(db, models.Produto, produto_id)
    return atualizar(db, produto, payload.model_dump(exclude_unset=True))


@router.delete("/{produto_id}", status_code=204)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = obter_ou_404(db, models.Produto, produto_id)
    return remover(db, produto)
