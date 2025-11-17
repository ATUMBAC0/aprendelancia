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
        {"id": "curso1", "titulo": "Python Básico", "descripcion": "Aprende Python desde cero", "instructor_id": "inst1", "duracion_horas": 40, "rating": 4.8, "nivel": "Básico"},
        {"id": "curso2", "titulo": "Web Development", "descripcion": "Desarrollo web con Flask", "instructor_id": "inst2", "duracion_horas": 60, "rating": 4.6, "nivel": "Intermedio"},
        {"id": "curso3", "titulo": "JavaScript Avanzado", "descripcion": "Domina JavaScript ES6+ y frameworks modernos", "instructor_id": "inst1", "duracion_horas": 50, "rating": 4.7, "nivel": "Avanzado"},
        {"id": "curso4", "titulo": "Machine Learning", "descripcion": "Introducción al aprendizaje automático con Python", "instructor_id": "inst3", "duracion_horas": 80, "rating": 4.9, "nivel": "Avanzado"},
        {"id": "curso5", "titulo": "React Fundamentals", "descripcion": "Aprende React desde cero hasta crear aplicaciones completas", "instructor_id": "inst2", "duracion_horas": 45, "rating": 4.5, "nivel": "Intermedio"},
        {"id": "curso6", "titulo": "SQL y Bases de Datos", "descripcion": "Diseño y consultas en bases de datos relacionales", "instructor_id": "inst1", "duracion_horas": 35, "rating": 4.4, "nivel": "Básico"},
        {"id": "curso7", "titulo": "Docker y Kubernetes", "descripcion": "Containerización y orquestación de aplicaciones", "instructor_id": "inst3", "duracion_horas": 55, "rating": 4.8, "nivel": "Avanzado"},
        {"id": "curso8", "titulo": "Git y GitHub", "descripcion": "Control de versiones profesional", "instructor_id": "inst2", "duracion_horas": 25, "rating": 4.6, "nivel": "Básico"},
        {"id": "curso9", "titulo": "Node.js Backend", "descripcion": "Desarrollo de APIs REST con Node.js y Express", "instructor_id": "inst1", "duracion_horas": 65, "rating": 4.7, "nivel": "Intermedio"},
        {"id": "curso10", "titulo": "CSS Avanzado", "descripcion": "Flexbox, Grid, Animaciones y diseño responsive", "instructor_id": "inst2", "duracion_horas": 30, "rating": 4.5, "nivel": "Intermedio"},
        {"id": "curso11", "titulo": "Data Science con Python", "descripcion": "Análisis de datos con Pandas, NumPy y Matplotlib", "instructor_id": "inst3", "duracion_horas": 70, "rating": 4.9, "nivel": "Intermedio"},
        {"id": "curso12", "titulo": "TypeScript Profesional", "descripcion": "JavaScript tipado para aplicaciones escalables", "instructor_id": "inst1", "duracion_horas": 40, "rating": 4.6, "nivel": "Intermedio"},
        {"id": "curso13", "titulo": "DevOps Fundamentals", "descripcion": "CI/CD, infraestructura como código y automatización", "instructor_id": "inst3", "duracion_horas": 60, "rating": 4.8, "nivel": "Avanzado"},
        {"id": "curso14", "titulo": "Vue.js 3", "descripcion": "Framework progresivo para interfaces de usuario", "instructor_id": "inst2", "duracion_horas": 45, "rating": 4.5, "nivel": "Intermedio"},
        {"id": "curso15", "titulo": "MongoDB y NoSQL", "descripcion": "Bases de datos no relacionales y diseño de esquemas", "instructor_id": "inst1", "duracion_horas": 38, "rating": 4.7, "nivel": "Intermedio"},
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

