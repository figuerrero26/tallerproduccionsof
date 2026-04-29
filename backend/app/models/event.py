from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from tallerproduccionsof.backend.app.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    descripcion = Column(Text)
    fecha = Column(DateTime)
    lugar = Column(String(120))
    cupo = Column(Integer)

    registrations = relationship("Registration", back_populates="event")
