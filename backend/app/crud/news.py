from sqlalchemy.orm import Session

from app.models.news import News
from app.schemas.news import NewsCreate, NewsUpdate


def get_all(db: Session):
    return db.query(News).order_by(News.fecha_publicacion.desc()).all()


def get_one(db: Session, news_id: int):
    return db.query(News).filter(News.id == news_id).first()


def create(db: Session, data: NewsCreate):
    obj = News(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, news_id: int, data: NewsUpdate):
    obj = get_one(db, news_id)
    if not obj:
        return None
    for k, v in data.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, news_id: int):
    obj = get_one(db, news_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
