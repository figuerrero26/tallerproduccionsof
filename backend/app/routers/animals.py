from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.animal import AnimalCreate, AnimalUpdate, AnimalOut
from app.crud import animal as crud

router = APIRouter(prefix="/animales", tags=["animales"])


@router.get("", response_model=List[AnimalOut])
def listar(estado: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_all(db, estado=estado)


@router.get("/{animal_id}", response_model=AnimalOut)
def detalle(animal_id: int, db: Session = Depends(get_db)):
    obj = crud.get_one(db, animal_id)
    if not obj:
        raise HTTPException(404, "Animal no encontrado")
    return obj


@router.post("", response_model=AnimalOut, status_code=201)
def crear(data: AnimalCreate, db: Session = Depends(get_db)):
    return crud.create(db, data)


@router.put("/{animal_id}", response_model=AnimalOut)
def editar(animal_id: int, data: AnimalUpdate, db: Session = Depends(get_db)):
    obj = crud.update(db, animal_id, data)
    if not obj:
        raise HTTPException(404, "Animal no encontrado")
    return obj


@router.delete("/{animal_id}", status_code=204)
def eliminar(animal_id: int, db: Session = Depends(get_db)):
    if not crud.delete(db, animal_id):
        raise HTTPException(404, "Animal no encontrado")
    return None
