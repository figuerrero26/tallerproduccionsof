from sqlalchemy.orm import Session

from tallerproduccionsof.backend.app.models.event import Event
from tallerproduccionsof.backend.app.schemas.event import EventCreate, EventUpdate


def get_all(db: Session):
    return db.query(Event).order_by(Event.fecha.asc()).all()


def get_one(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()


def create(db: Session, data: EventCreate):
    obj = Event(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, event_id: int, data: EventUpdate):
    obj = get_one(db, event_id)
    if not obj:
        return None
    for k, v in data.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, event_id: int):
    obj = get_one(db, event_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
