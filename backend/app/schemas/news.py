from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class NewsBase(BaseModel):
    titulo: str
    contenido: str
    autor: Optional[str] = None


class NewsCreate(NewsBase):
    pass


class NewsUpdate(NewsBase):
    pass


class NewsOut(NewsBase):
    id: int
    fecha_publicacion: datetime
    model_config = ConfigDict(from_attributes=True)
