from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Evaluaciones Service")


class Evaluacion(BaseModel):
    id: str
    curso_id: str
    titulo: str
    tipo: str
    preguntas: Optional[int] = None
    duracion_minutos: Optional[int] = None
    puntos_totales: int
    descripcion: Optional[str] = None

# Simple mock cuestionarios
DATA = {
    "cuestionarios": {
        "c1": {
            "id": "c1",
            "titulo": "Evaluación Inicial Python",
            "preguntas": [
                {"id": "p1", "tipo": "opcion", "texto": "¿Qué imprime print(1+1)?", "opciones": ["1", "2", "11"], "respuesta": 1},
            ]
        }
    }
}


@app.get("/")
def read_root():
    return {"message": "Servicio de Evaluaciones en funcionamiento."}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/{cuestionario_id}")
def get_cuestionario(cuestionario_id: str):
    q = DATA.get("cuestionarios", {}).get(cuestionario_id)
    if not q:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    # Do not expose answers in the response
    safe = {"id": q["id"], "titulo": q["titulo"], "preguntas": []}
    for p in q.get("preguntas", []):
        qp = p.copy()
        qp.pop("respuesta", None)
        safe["preguntas"].append(qp)
    return safe


class Respuestas(BaseModel):
    respuestas: dict


@app.post("/evaluaciones")
def create_evaluacion(evaluacion: Evaluacion):
    """Crear una nueva evaluación"""
    if evaluacion.id in DATA.get("cuestionarios", {}):
        raise HTTPException(status_code=400, detail="Evaluación ya existe")
    
    DATA.setdefault("cuestionarios", {})[evaluacion.id] = evaluacion.dict()
    return {"message": "Evaluación creada", "evaluacion": evaluacion.dict()}


@app.post("/{cuestionario_id}/responder")
def responder(cuestionario_id: str, body: Respuestas):
    # very simple auto-grading using the stored answers if present
    q = DATA.get("cuestionarios", {}).get(cuestionario_id)
    if not q:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    correct = 0
    total = len(q.get("preguntas", []))
    for p in q.get("preguntas", []):
        pid = p.get("id")
        if pid in (body.respuestas or {}) and body.respuestas[pid] == p.get("respuesta"):
            correct += 1
    score = (correct / total * 100) if total else 0
    return {"score": score, "correct": correct, "total": total}

