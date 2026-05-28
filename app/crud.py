from typing import Any, Dict, Iterable, Optional, Type
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def listar(db: Session, model: Type, skip: int = 0, limit: int = 100):
    return db.query(model).offset(skip).limit(limit).all()


def obter_ou_404(db: Session, model: Type, registro_id: int):
    registro = db.get(model, registro_id)
    if not registro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} não encontrado(a).",
        )
    return registro


def criar(db: Session, model: Type, dados: Dict[str, Any]):
    registro = model(**dados)
    db.add(registro)
    try:
        db.commit()
        db.refresh(registro)
        return registro
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registro duplicado ou relacionamento inválido.",
        ) from exc


def atualizar(db: Session, registro: Any, dados: Dict[str, Any]):
    for campo, valor in dados.items():
        if valor is not None:
            setattr(registro, campo, valor)
    try:
        db.commit()
        db.refresh(registro)
        return registro
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível atualizar: dados duplicados ou relacionamento inválido.",
        ) from exc


def remover(db: Session, registro: Any):
    try:
        db.delete(registro)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível excluir, pois há registros vinculados a este cadastro.",
        ) from exc
    return None
