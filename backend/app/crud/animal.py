from typing import Optional
from sqlalchemy.orm import Session

from app.models.animal import Animal
from app.schemas.animal import AnimalCreate, AnimalUpdate


def get_all(db: Session, estado: Optional[str] = None):
    q = db.query(Animal)
    if estado:
        q = q.filter(Animal.estado == estado)
    return q.all()


def get_one(db: Session, animal_id: int):
    return db.query(Animal).filter(Animal.id == animal_id).first()


def create(db: Session, data: AnimalCreate):
    obj = Animal(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, animal_id: int, data: AnimalUpdate):
    obj = get_one(db, animal_id)
    if not obj:
        return None
    for k, v in data.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, animal_id: int):
    obj = get_one(db, animal_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
