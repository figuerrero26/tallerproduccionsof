from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from tallerproduccionsof.backend.app.database import get_db
from tallerproduccionsof.backend.app.schemas.news import NewsCreate, NewsUpdate, NewsOut
from tallerproduccionsof.backend.app.crud import news as crud

router = APIRouter(prefix="/noticias", tags=["noticias"])


@router.get("", response_model=List[NewsOut])
def listar(db: Session = Depends(get_db)):
    return crud.get_all(db)


@router.get("/{news_id}", response_model=NewsOut)
def detalle(news_id: int, db: Session = Depends(get_db)):
    obj = crud.get_one(db, news_id)
    if not obj:
        raise HTTPException(404, "Noticia no encontrada")
    return obj


@router.post("", response_model=NewsOut, status_code=201)
def crear(data: NewsCreate, db: Session = Depends(get_db)):
    return crud.create(db, data)


@router.put("/{news_id}", response_model=NewsOut)
def editar(news_id: int, data: NewsUpdate, db: Session = Depends(get_db)):
    obj = crud.update(db, news_id, data)
    if not obj:
        raise HTTPException(404, "Noticia no encontrada")
    return obj


@router.delete("/{news_id}", status_code=204)
def eliminar(news_id: int, db: Session = Depends(get_db)):
    if not crud.delete(db, news_id):
        raise HTTPException(404, "Noticia no encontrada")
    return None
