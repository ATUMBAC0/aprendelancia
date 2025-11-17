from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

from pydantic import BaseModel
from typing import Optional

# Define la base declarativa
Base = declarative_base()

# TODO: Crea tus modelos de datos aquí.
# Cada clase de modelo representa una tabla en tu base de datos.
# Debes renombrar YourModel por el nombre de la Clase según el servicio
class YourModel(Base):
    """
    Plantilla de modelo de datos para un recurso.
    Ajusta esta clase según los requisitos de tu tema.
    """
    __tablename__ = "[nombre_de_tu_tabla]"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<YourModel(id={self.id}, name='{self.name}')>"

class YourModelBase(BaseModel):
    name: str
    description: Optional[str] = None

class YourModelCreate(YourModelBase):
    pass

class YourModelRead(YourModelBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
