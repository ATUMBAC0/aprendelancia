from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import random
import requests

app = FastAPI(title="Progreso Service")


class Progreso(BaseModel):
    estudiante_id: str
    curso_id: str
    completado_pct: int
    tiempo_invertido_horas: int
    ultima_leccion: str
    fecha_inicio: str
    fecha_ultima_actividad: str
    calificacion: Optional[float] = None

# Mock progreso data
DATA = {
    "progreso": {}
}

CURSOS_SERVICE_URL = os.getenv("CURSOS_SERVICE_URL", "http://cursos-service:8002")


@app.get("/")
def read_root():
    return {"message": "Servicio de Progreso en funcionamiento."}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/estudiantes/{estudiante_id}/cursos")
def progreso_estudiante(estudiante_id: str):
    # Si no hay progreso para este estudiante, asigna cursos aleatorios en caliente
    existing = DATA.get("progreso", {}).get(estudiante_id)
    if not existing:
        try:
            resp = requests.get(f"{CURSOS_SERVICE_URL}/")
            resp.raise_for_status()
            cursos = resp.json().get("cursos", [])
        except Exception:
            cursos = []

        seleccion = random.sample(cursos, k=min(3, len(cursos))) if cursos else []
        cursos_asignados = []
        for c in seleccion:
            pct = random.randint(10, 95)
            item = {
                "curso_id": c.get("id"),
                "completado_pct": pct,
                "tiempo_invertido_horas": random.randint(1, 40),
                "ultima_leccion": "",
                "fecha_inicio": "",
                "fecha_ultima_actividad": "",
                "calificacion": None if pct < 75 else round(random.uniform(3.0, 5.0), 1),
            }
            cursos_asignados.append(item)
        DATA["progreso"][estudiante_id] = {"cursos": cursos_asignados}
        return DATA["progreso"][estudiante_id]
    return existing


@app.post("/progreso")
def create_progreso(progreso: Progreso):
    """Crear o actualizar progreso de un estudiante en un curso"""
    estudiante_data = DATA["progreso"].setdefault(progreso.estudiante_id, {"cursos": []})
    
    # Verificar si ya existe progreso para este curso
    for idx, c in enumerate(estudiante_data["cursos"]):
        if c.get("curso_id") == progreso.curso_id:
            # Actualizar existente
            estudiante_data["cursos"][idx] = progreso.dict(exclude={"estudiante_id"})
            return {"message": "Progreso actualizado", "progreso": progreso.dict()}
    
    # Agregar nuevo
    estudiante_data["cursos"].append(progreso.dict(exclude={"estudiante_id"}))
    return {"message": "Progreso creado", "progreso": progreso.dict()}

