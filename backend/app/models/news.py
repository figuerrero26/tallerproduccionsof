from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime

from app.database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    contenido = Column(Text, nullable=False)
    autor = Column(String(80))
    fecha_publicacion = Column(DateTime, default=datetime.utcnow)
