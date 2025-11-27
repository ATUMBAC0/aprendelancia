# Aprendelandia — Plataforma de Cursos Online

Bienvenido a Aprendelandia, una plataforma de cursos online escalable basada en **microservicios**.

## ¿Qué es esto?

Una arquitectura de **FastAPI + Flask + PostgreSQL + MongoDB** con un API Gateway centralizado. Perfecta para:

-  Estudiantes: registrarse, ver cursos, responder evaluaciones, tracking de progreso
-  Instructores: gestionar cursos, módulos, lecciones, cuestionarios
-  Seguridad: JWT tokens, roles (estudiante/instructor), autenticación

## Inicio Rápido (Docker)

```bash
# Configurar
cp .env.example .env

# Levantar todo
docker-compose up --build

# Abrir en navegador
# Frontend:  http://localhost:5000
# Gateway:   http://localhost:8000/docs
```

## Estructura

- **Frontend** (Flask): `frontend/app.py` (puerto 5000)
- **API Gateway** (FastAPI): `api-gateway/main.py` (puerto 8000)
- **Servicios:**
  - `authentication` (MongoDB, puerto 8001)
  - `cursos` (PostgreSQL, puerto 8002)
  - `evaluaciones` (PostgreSQL, puerto 8003)
  - `progreso` (PostgreSQL, puerto 8004)

## Documentación Completa

- [Arquitectura](architecture.md) — Diagrama y conceptos
- [Setup & Configuración](setup.md) — Cómo correr localmente
- [API Reference](api.md) — Todos los endpoints
- [Desarrollo](development.md) — Testing y contribuciones
