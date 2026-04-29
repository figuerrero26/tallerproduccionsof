from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.event import EventCreate, EventUpdate, EventOut
from app.crud import event as crud

router = APIRouter(prefix="/eventos", tags=["eventos"])


@router.get("", response_model=List[EventOut])
def listar(db: Session = Depends(get_db)):
    return crud.get_all(db)


@router.get("/{event_id}", response_model=EventOut)
def detalle(event_id: int, db: Session = Depends(get_db)):
    obj = crud.get_one(db, event_id)
    if not obj:
        raise HTTPException(404, "Evento no encontrado")
    return obj


@router.post("", response_model=EventOut, status_code=201)
def crear(data: EventCreate, db: Session = Depends(get_db)):
    return crud.create(db, data)


@router.put("/{event_id}", response_model=EventOut)
def editar(event_id: int, data: EventUpdate, db: Session = Depends(get_db)):
    obj = crud.update(db, event_id, data)
    if not obj:
        raise HTTPException(404, "Evento no encontrado")
    return obj


@router.delete("/{event_id}", status_code=204)
def eliminar(event_id: int, db: Session = Depends(get_db)):
    if not crud.delete(db, event_id):
        raise HTTPException(404, "Evento no encontrado")
    return None
