from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# TODO: Importa la base declarativa del archivo models.py
# from .models import Base

# Obtiene la URL de la base de datos de las variables de entorno.
# Asegúrate de que esta variable esté definida en el archivo docker-compose.yml.
DATABASE_URL = os.getenv("DATABASE_URL")

# Crea el motor de la base de datos.
engine = create_engine(DATABASE_URL, echo=True)

# Configura la sesión de la base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """Crea todas las tablas definidas en models.py si no existen."""
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
