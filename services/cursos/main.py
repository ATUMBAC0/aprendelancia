from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Cursos Service")


class Curso(BaseModel):
    id: str
    titulo: str
    descripcion: str
    instructor_id: str
    duracion_horas: int
    rating: float
    nivel: Optional[str] = "Básico"

# Simple in-memory mock data compatible with frontend MockStore
DATA = {
    "cursos": [
        {"id": "curso1", "titulo": "Python Básico", "descripcion": "Aprende Python desde cero", "instructor_id": "inst1", "duracion_horas": 40, "rating": 4.8},
        {"id": "curso2", "titulo": "Web Development", "descripcion": "Desarrollo web con Flask", "instructor_id": "inst2", "duracion_horas": 60, "rating": 4.6},
    ],
    "modulos": {
        "curso1": [
            {"id": "mod1", "curso_id": "curso1", "titulo": "Fundamentos", "descripcion": "Variables, tipos de datos", "orden": 1},
            {"id": "mod2", "curso_id": "curso1", "titulo": "Funciones", "descripcion": "Definición y uso de funciones", "orden": 2},
        ]
    },
    "lecciones": {
        "mod1": [
            {"id": "lec1", "modulo_id": "mod1", "titulo": "Variables y Tipos", "contenido": "https://example.com/video1", "duracion_minutos": 30, "orden": 1},
            {"id": "lec2", "modulo_id": "mod1", "titulo": "Operadores", "contenido": "https://example.com/video2", "duracion_minutos": 25, "orden": 2},
        ]
    }
}


@app.get("/")
def list_cursos():
    return {"cursos": DATA.get("cursos", [])}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/{curso_id}")
def get_curso(curso_id: str):
    for c in DATA.get("cursos", []):
        if c.get("id") == curso_id:
            return c
    raise HTTPException(status_code=404, detail="Curso no encontrado")


@app.get("/{curso_id}/modulos")
def get_modulos(curso_id: str):
    return {"modulos": DATA.get("modulos", {}).get(curso_id, [])}


@app.get("/modulos/{modulo_id}/lecciones")
def get_lecciones(modulo_id: str):
    return {"lecciones": DATA.get("lecciones", {}).get(modulo_id, [])}


@app.post("/cursos")
def create_curso(curso: Curso):
    """Crear un nuevo curso"""
    # Verificar si ya existe
    for c in DATA.get("cursos", []):
        if c.get("id") == curso.id:
            raise HTTPException(status_code=400, detail="Curso ya existe")
    
    DATA["cursos"].append(curso.dict())
    return {"message": "Curso creado", "curso": curso.dict()}

