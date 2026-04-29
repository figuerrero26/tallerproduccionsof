import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.orm import relationship

from app.database import Base


class EstadoAnimal(str, enum.Enum):
    disponible = "disponible"
    en_proceso = "en_proceso"
    adoptado = "adoptado"


class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(80), nullable=False)
    especie = Column(String(40), nullable=False)
    edad = Column(Integer)
    estado = Column(Enum(EstadoAnimal), default=EstadoAnimal.disponible)
    descripcion = Column(Text)
    foto_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    registrations = relationship("Registration", back_populates="animal")
