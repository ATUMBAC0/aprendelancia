# Desarrollo

## Estructura del Proyecto

```
aprendelancia/
├── frontend/              # Flask web UI
├── api-gateway/           # FastAPI router
├── services/              # Microservicios
│   ├── authentication/    # Auth + JWT
│   ├── cursos/           # Course catalog
│   ├── evaluaciones/     # Quizzes
│   └── progreso/         # Progress tracking
├── common/               # Shared code
│   ├── config.py         # Environment setup
│   └── helpers/
│       └── utils.py      # Utilities
├── tests/                # Tests
├── docs/                 # Documentación (mkdocs)
└── docker-compose.yml    # Orquestación
```

## Getting Started

### 1. Clonar y setup

```bash
git clone <repo-url>
cd aprendelancia

# Crear virtualenv
python3 -m venv .venv
source .venv/bin/activate

# Instalar todas las dependencias
pip install -r api-gateway/requirements.txt
pip install -r frontend/requirements.txt
for service in authentication cursos evaluaciones progreso; do
  pip install -r services/$service/requirements.txt
done

# Dev dependencies
pip install pytest flake8 mkdocs mkdocs-material
```

### 2. Ejecutar tests

```bash
# Health checks
pytest tests/test_health.py -v

# Con cobertura
pytest tests/ --cov=. --cov-report=html
```

### 3. Linting

```bash
# Verificar estilo
flake8 services/ api-gateway/ frontend/ --max-line-length=120

# Syntax check
python -m py_compile services/cursos/main.py
```

## Desarrollo de un Nuevo Servicio

Si necesitas agregar un nuevo microservicio (ejemplo: `notificaciones`):

### Paso 1: Crear estructura

```bash
mkdir -p services/notificaciones
cd services/notificaciones

# Crear archivos base
touch main.py requirements.txt Dockerfile
```

### Paso 2: Implementar main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Notificaciones Service", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def list_notificaciones():
    return {"notificaciones": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
```

### Paso 3: Agregar requirements.txt

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.4.2
```

### Paso 4: Crear Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
```

### Paso 5: Actualizar docker-compose.yml

```yaml
notificaciones-service:
  build: ./services/notificaciones
  container_name: notificaciones-service
  environment:
    - API_GATEWAY_URL=http://api-gateway:8000
  ports:
    - "8005:8005"
  networks:
    - app-network
```

### Paso 6: Actualizar api-gateway/main.py

```python
SERVICES = {
    "auth": "http://auth-service:8001",
    "cursos": "http://cursos-service:8002",
    "evaluaciones": "http://evaluaciones-service:8003",
    "progreso": "http://progreso-service:8004",
    "notificaciones": "http://notificaciones-service:8005"  # ← Agregar
}
```

### Paso 7: Levantar

```bash
docker-compose up --build
```

## Agregar Endpoints

### En un servicio existente (ej: cursos)

Editar `services/cursos/main.py`:

```python
@app.post("/{curso_id}/inscribir")
def inscribir_curso(curso_id: str):
    """Inscribir estudiante en un curso"""
    return {
        "curso_id": curso_id,
        "mensaje": "Inscripción exitosa"
    }
```

La ruta será accesible en:
- **Directa**: `POST http://localhost:8002/curso1/inscribir`
- **Via Gateway**: `POST http://localhost:8000/api/v1/cursos/curso1/inscribir`

### Con JWT protection

En `services/cursos/main.py` o en `api-gateway/main.py`:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()

@app.post("/crear")
def crear_curso(credentials: HTTPAuthCredentials = Depends(security)):
    token = credentials.credentials
    # Validar token aquí (o delegado al Gateway)
    return {"curso_id": "nuevo", "creado": True}
```

## Testing

### Tests básicos (pytest)

```bash
# Crear test file
mkdir -p tests
touch tests/test_cursos.py
```

```python
# tests/test_cursos.py
import pytest
import requests

BASE_URL = "http://localhost:8000/api/v1/cursos"

def test_list_cursos():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "cursos" in response.json()

def test_get_curso():
    response = requests.get(f"{BASE_URL}/curso1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "curso1"
```

Ejecutar:

```bash
pytest tests/test_cursos.py -v
```

### Mocking

Si necesitas mockear respuestas:

```python
from unittest.mock import patch

@patch("requests.get")
def test_with_mock(mock_get):
    mock_get.return_value.json.return_value = {"id": "curso1"}
    # Tu test aquí
```

## Variables de Entorno

Editar `.env` para cambiar configuración:

```bash
# API Gateway
API_GATEWAY_URL=http://localhost:8000

# Services
AUTH_SERVICE_URL=http://localhost:8001
CURSOS_SERVICE_URL=http://localhost:8002

# Bases de datos
AUTH_DATABASE_URL=mongodb://localhost:27017/auth_db
CURSOS_DATABASE_URL=postgresql://localhost/cursos_db

# Security
JWT_SECRET=your-secret-key-here
FLASK_SECRET=another-secret
```

Cargar en Python:

```python
from common.config import settings

print(settings.API_GATEWAY_URL)
print(settings.JWT_SECRET)
```

## Documentación (mkdocs)

### Editar documentación

Archivos en `docs/`:
- `index.md` — Página de inicio
- `architecture.md` — Diagramas
- `setup.md` — Setup guide
- `api.md` — API reference
- `development.md` — Este archivo

### Servidor local

```bash
mkdocs serve
# Abierto en http://127.0.0.1:8000/docs/
```

### Build static

```bash
mkdocs build
# Genera en ./site/
```

## CI/CD

GitHub Actions workflow en `.github/workflows/ci.yml`:

- **Lint**: flake8 syntax checks
- **Test**: pytest con postgres/mongo/redis services
- **Docs**: mkdocs build y deploy a GitHub Pages
- **Docker**: docker-compose build validation

Triggers: push a main/develop, PR a main

## Debugging

### Logs en Docker

```bash
# Ver logs de un servicio
docker-compose logs -f cursos-service

# Últimas 100 líneas
docker-compose logs --tail 100 cursos-service

# Todos los servicios
docker-compose logs -f
```

### Conectarse al contenedor

```bash
# Ejecutar bash en el contenedor
docker-compose exec cursos-service bash

# Dentro del contenedor:
pip list
python -c "import fastapi; print(fastapi.__version__)"
```

### Probar endpoint directamente

```bash
# Desde host
curl http://localhost:8000/api/v1/cursos/

# Con JWT
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/cursos/

# POST con JSON
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "pass"}'
```

## Problemas Comunes

### "Port already in use"

```bash
# Matar proceso
lsof -i :8000
kill -9 <PID>

# O usar otro puerto
docker-compose -p custom up
```

### "Module not found"

```bash
# Reinstalar en el service específico
docker-compose exec cursos-service pip install -r requirements.txt

# O reconstruir imagen
docker-compose build --no-cache cursos-service
```

### "Database connection refused"

```bash
# Verificar que DBs están corriendo
docker-compose ps | grep db

# Si no:
docker-compose up -d auth-db cursos-db
```

## Workflow Típico

```bash
# 1. Crear rama feature
git checkout -b feature/nueva-evaluacion

# 2. Hacer cambios (ej: services/evaluaciones/main.py)
vim services/evaluaciones/main.py

# 3. Tests locales
pytest tests/ -v

# 4. Linting
flake8 services/evaluaciones/

# 5. Commit
git add .
git commit -m "Add new evaluation endpoint"

# 6. Push
git push origin feature/nueva-evaluacion

# 7. GitHub Actions corre automáticamente
# (check .github/workflows/ci.yml results)

# 8. Merge a main
git checkout main
git merge feature/nueva-evaluacion
```

## Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Flask Docs](https://flask.palletsprojects.com)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [JWT Auth](https://tools.ietf.org/html/rfc7519)
- [MongoDB Python Driver](https://pymongo.readthedocs.io)
- [SQLAlchemy](https://sqlalchemy.org)
