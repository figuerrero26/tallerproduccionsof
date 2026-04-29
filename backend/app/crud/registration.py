from sqlalchemy.orm import Session

from tallerproduccionsof.backend.app.models.registration import Registration
from tallerproduccionsof.backend.app.schemas.registration import RegistrationCreate


def get_all(db: Session):
    return db.query(Registration).order_by(Registration.fecha.desc()).all()


def get_one(db: Session, reg_id: int):
    return db.query(Registration).filter(Registration.id == reg_id).first()


def create(db: Session, data: RegistrationCreate):
    obj = Registration(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, reg_id: int):
    obj = get_one(db, reg_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
