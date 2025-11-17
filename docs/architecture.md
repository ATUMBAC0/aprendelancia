# Arquitectura

## Visión General

Aprendelancia utiliza una arquitectura de **microservicios** con un **API Gateway centralizado**.

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Flask)                         │
│              http://localhost:5000                          │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              API Gateway (FastAPI)                          │
│              http://localhost:8000                          │
│     - Validación JWT                                        │
│     - Enrutamiento a servicios                              │
│     - CORS                                                  │
└─────────────────────────────────────────────────────────────┘
        │           │              │              │
        ▼           ▼              ▼              ▼
    ┌───────┐  ┌──────────┐  ┌─────────────┐  ┌────────┐
    │ Auth  │  │ Cursos   │  │ Evaluaciones│  │Progreso│
    │ :8001 │  │ :8002    │  │ :8003       │  │:8004   │
    └───────┘  └──────────┘  └─────────────┘  └────────┘
        │           │              │              │
        ▼           ▼              ▼              ▼
    MongoDB   PostgreSQL   PostgreSQL   PostgreSQL
```

## Componentes

### 1. Frontend (Flask)
- **Ruta**: `frontend/app.py`
- **Puerto**: 5000
- **Responsabilidades**:
  - UI para estudiantes/instructores
  - Llamadas HTTP al Gateway
  - Fallback a mock data si el Gateway no está disponible

### 2. API Gateway (FastAPI)
- **Ruta**: `api-gateway/main.py`
- **Puerto**: 8000
- **Responsabilidades**:
  - Enrutamiento centralizado de requests
  - Validación de JWT tokens
  - Conversión de errores HTTP
  - CORS

**Routing pattern**:
```
GET /api/v1/{service}/{path}  →  http://{service}:{port}/{path}
```

Ejemplo:
```
GET /api/v1/cursos/         →  http://cursos-service:8002/
POST /api/v1/evaluaciones/1/responder  →  http://evaluaciones-service:8003/1/responder
```

### 3. Authentication Service (FastAPI)
- **Ruta**: `services/authentication/main.py`
- **Puerto**: 8001
- **Base de datos**: MongoDB
- **Responsabilidades**:
  - Registro e login de usuarios
  - Generación de JWT tokens
  - Validación de roles (estudiante/instructor)
  - Refresh token management (Redis)

**Endpoints principales**:
- `POST /register` — Crear usuario
- `POST /login` — Obtener JWT token
- `POST /refresh` — Renovar token expirado

### 4. Cursos Service (FastAPI)
- **Ruta**: `services/cursos/main.py`
- **Puerto**: 8002
- **Base de datos**: PostgreSQL
- **Responsabilidades**:
  - Gestionar catálogo de cursos
  - Módulos y lecciones
  - Estructura jerárquica

**Endpoints principales**:
- `GET /` — Listar cursos
- `GET /{curso_id}` — Detalle de curso
- `GET /{curso_id}/modulos` — Módulos del curso
- `GET /modulos/{modulo_id}/lecciones` — Lecciones del módulo

### 5. Evaluaciones Service (FastAPI)
- **Ruta**: `services/evaluaciones/main.py`
- **Puerto**: 8003
- **Base de datos**: PostgreSQL
- **Responsabilidades**:
  - Gestionar cuestionarios
  - Auto-grading de respuestas
  - Almacenar resultados

**Endpoints principales**:
- `GET /{cuestionario_id}` — Obtener quiz (sin respuestas)
- `POST /{cuestionario_id}/responder` — Enviar respuestas y obtener score

### 6. Progreso Service (FastAPI)
- **Ruta**: `services/progreso/main.py`
- **Puerto**: 8004
- **Base de datos**: PostgreSQL
- **Responsabilidades**:
  - Tracking de progreso de estudiantes
  - Porcentaje completado por curso

**Endpoints principales**:
- `GET /estudiantes/{estudiante_id}/cursos` — Progreso del estudiante

## Flujo de Autenticación

```
1. Usuario ingresa email/password en Frontend
2. Frontend hace POST /api/v1/auth/login al Gateway
3. Gateway reenvía a http://auth-service:8001/login
4. Auth service valida credenciales contra MongoDB
5. Auth service genera JWT token
6. Frontend recibe token y lo almacena en localStorage
7. Requests subsiguientes incluyen: Authorization: Bearer {token}
8. Gateway valida JWT antes de reenviar a servicios
9. Servicios confían en el JWT validado del Gateway
```

## Databases

### MongoDB (Authentication)
- **Colección**: `users`
- **Índices**: email (unique)
- **Campos**: id, email, hashed_password, role, created_at

### PostgreSQL (Cursos, Evaluaciones, Progreso)
- **Base de datos separada** por servicio:
  - `cursos_db` — Cursos, módulos, lecciones
  - `evaluaciones_db` — Cuestionarios, preguntas, respuestas
  - `progreso_db` — Progreso del estudiante
- **Cada servicio** maneja sus propias migraciones

### Redis (Optional)
- **Uso**: Almacenar refresh tokens invalidados
- **Expiry**: TTL automático según exp claim del JWT

## Deployment

### Docker Compose
Todos los servicios se orquestan en `docker-compose.yml`:
```bash
docker-compose up --build
```

Esto levanta:
- frontend (Flask)
- api-gateway (FastAPI)
- auth-service + auth-db (MongoDB)
- cursos-service + cursos-db (PostgreSQL)
- evaluaciones-service + evaluaciones-db (PostgreSQL)
- progreso-service + progreso-db (PostgreSQL)
- redis (opcional)

### Escalabilidad Futura

Cada servicio puede:
- Escalarse horizontalmente (múltiples instancias)
- Deployarse en Kubernetes
- Tener su propio CI/CD pipeline
- Ser reemplazado sin afectar otros servicios

## Convenciones

- **Puertos**: Fijos en docker-compose.yml
- **Rutas**: `/health` en cada servicio
- **Errores**: HTTP status codes estándar
- **Datos**: JSON en request/response
- **Auth**: JWT Bearer tokens
- **Env vars**: Centralizadas en `.env`
