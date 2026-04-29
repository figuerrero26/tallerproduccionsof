from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from tallerproduccionsof.backend.app.models.animal import EstadoAnimal


class AnimalBase(BaseModel):
    nombre: str
    especie: str
    edad: Optional[int] = None
    estado: EstadoAnimal = EstadoAnimal.disponible
    descripcion: Optional[str] = None
    foto_url: Optional[str] = None


class AnimalCreate(AnimalBase):
    pass


class AnimalUpdate(AnimalBase):
    pass


class AnimalOut(AnimalBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
