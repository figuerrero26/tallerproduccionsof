from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False)
    telefono = Column(String(30))
    mensaje = Column(Text)
    fecha = Column(DateTime, default=datetime.utcnow)

    animal = relationship("Animal", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")
