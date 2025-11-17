from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class YourModel(Base):
    __tablename__ = "[nombre_de_tu_tabla]"
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
