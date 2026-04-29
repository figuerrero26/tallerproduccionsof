from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    fecha: Optional[datetime] = None
    lugar: Optional[str] = None
    cupo: Optional[int] = None


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventOut(EventBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
