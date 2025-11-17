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
    
    # Verificar si no existe o si existe pero está vacío
    if not existing or not existing.get("cursos"):
        try:
            resp = requests.get(f"{CURSOS_SERVICE_URL}/", timeout=3)
            resp.raise_for_status()
            cursos = resp.json().get("cursos", [])
        except Exception as e:
            print(f"Error obteniendo cursos: {e}")
            cursos = []

        if cursos:
            # Seleccionar entre 3 y 5 cursos aleatorios
            num_cursos = min(random.randint(3, 5), len(cursos))
            seleccion = random.sample(cursos, k=num_cursos)
            cursos_asignados = []
            
            for c in seleccion:
                pct = random.randint(10, 95)
                # Calificación solo si completado >= 75%
                calificacion = None if pct < 75 else round(random.uniform(3.5, 5.0), 1)
                
                item = {
                    "curso_id": c.get("id"),
                    "completado_pct": pct,
                    "tiempo_invertido_horas": random.randint(1, 40),
                    "ultima_leccion": f"Lección {random.randint(1, 10)}",
                    "fecha_inicio": "2025-01-15",
                    "fecha_ultima_actividad": "2025-11-17",
                    "calificacion": calificacion,
                }
                cursos_asignados.append(item)
            
            DATA["progreso"][estudiante_id] = {"cursos": cursos_asignados}
            return DATA["progreso"][estudiante_id]
        else:
            # No hay cursos disponibles
            return {"cursos": []}
    
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


@app.post("/estudiantes/{estudiante_id}/asignar-cursos")
def asignar_cursos_aleatorios(estudiante_id: str):
    """
    Asignar cursos aleatorios con progreso y calificaciones a un estudiante.
    Este endpoint POST fuerza la asignación de cursos nuevos.
    """
    try:
        resp = requests.get(f"{CURSOS_SERVICE_URL}/")
        resp.raise_for_status()
        cursos = resp.json().get("cursos", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo cursos: {e}")

    if not cursos:
        raise HTTPException(status_code=404, detail="No hay cursos disponibles")

    # Seleccionar entre 3 y 5 cursos aleatorios
    num_cursos = min(random.randint(3, 5), len(cursos))
    seleccion = random.sample(cursos, k=num_cursos)
    
    cursos_asignados = []
    for c in seleccion:
        pct = random.randint(5, 100)
        # Calificación solo si progreso >= 80%
        calificacion = round(random.uniform(3.5, 5.0), 1) if pct >= 80 else None
        
        item = {
            "curso_id": c.get("id"),
            "completado_pct": pct,
            "tiempo_invertido_horas": random.randint(1, 50),
            "ultima_leccion": f"Lección {random.randint(1, 10)}",
            "fecha_inicio": "2025-01-15",
            "fecha_ultima_actividad": "2025-11-17",
            "calificacion": calificacion,
        }
        cursos_asignados.append(item)
    
    # Reemplazar cursos del estudiante
    DATA["progreso"][estudiante_id] = {"cursos": cursos_asignados}
    
    return {
        "message": f"{num_cursos} cursos asignados exitosamente",
        "estudiante_id": estudiante_id,
        "cursos": cursos_asignados
    }

