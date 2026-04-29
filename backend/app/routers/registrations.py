from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from tallerproduccionsof.backend.app.database import get_db
from tallerproduccionsof.backend.app.schemas.registration import RegistrationCreate, RegistrationOut
from tallerproduccionsof.backend.app.crud import registration as crud

router = APIRouter(prefix="/registros", tags=["registros"])


@router.get("", response_model=List[RegistrationOut])
def listar(db: Session = Depends(get_db)):
    return crud.get_all(db)


@router.get("/{reg_id}", response_model=RegistrationOut)
def detalle(reg_id: int, db: Session = Depends(get_db)):
    obj = crud.get_one(db, reg_id)
    if not obj:
        raise HTTPException(404, "Registro no encontrado")
    return obj


@router.post("", response_model=RegistrationOut, status_code=201)
def crear(data: RegistrationCreate, db: Session = Depends(get_db)):
    return crud.create(db, data)


@router.delete("/{reg_id}", status_code=204)
def eliminar(reg_id: int, db: Session = Depends(get_db)):
    if not crud.delete(db, reg_id):
        raise HTTPException(404, "Registro no encontrado")
    return None
