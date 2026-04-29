from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class RegistrationBase(BaseModel):
    animal_id: int
    event_id: Optional[int] = None
    nombre: str
    email: str
    telefono: Optional[str] = None
    mensaje: Optional[str] = None


class RegistrationCreate(RegistrationBase):
    pass


class RegistrationOut(RegistrationBase):
    id: int
    fecha: datetime
    model_config = ConfigDict(from_attributes=True)
