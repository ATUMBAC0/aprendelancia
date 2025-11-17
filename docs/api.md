# API Reference

## Base URL

- **Docker**: `http://localhost:8000` (Gateway)
- **Local**: `http://127.0.0.1:8000` (Gateway)
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Routing Pattern

All requests go through the API Gateway using:

```
/api/v1/{service_name}/{path}
```

Ejemplos:
- `GET /api/v1/cursos/` → `http://cursos-service:8002/`
- `POST /api/v1/auth/login` → `http://auth-service:8001/login`
- `GET /api/v1/progreso/estudiantes/123/cursos` → `http://progreso-service:8004/estudiantes/123/cursos`

---

## Authentication Service

**Direct URL**: `http://localhost:8001` (or via gateway: `/api/v1/auth`)

### POST /register

Crear nuevo usuario.

**Request**:
```json
{
  "email": "juan@example.com",
  "password": "MySecurePassword123",
  "nombre": "Juan Pérez",
  "role": "estudiante"
}
```

**Response** (201):
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "juan@example.com",
  "nombre": "Juan Pérez",
  "role": "estudiante"
}
```

**Errores**:
- `400` — Email ya existe o campos inválidos
- `422` — Validación fallida

### POST /login

Obtener JWT token.

**Request**:
```json
{
  "email": "juan@example.com",
  "password": "MySecurePassword123"
}
```

**Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Errores**:
- `401` — Email/password incorrecto
- `404` — Usuario no existe

### POST /refresh

Renovar access token expirado.

**Header**:
```
Authorization: Bearer {refresh_token}
```

**Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### GET /health

Health check.

**Response** (200):
```json
{
  "status": "ok"
}
```

---

## Cursos Service

**Direct URL**: `http://localhost:8002` (or via gateway: `/api/v1/cursos`)

### GET /

Listar todos los cursos.

**Query Parameters**:
- `skip` — Offset (default: 0)
- `limit` — Límite de resultados (default: 100)

**Response** (200):
```json
{
  "cursos": [
    {
      "id": "curso1",
      "titulo": "Python Básico",
      "descripcion": "Aprende Python desde cero",
      "duracion_horas": 40,
      "nivel": "principiante"
    },
    {
      "id": "curso2",
      "titulo": "Web Development",
      "descripcion": "HTML, CSS, JavaScript",
      "duracion_horas": 60,
      "nivel": "intermedio"
    }
  ]
}
```

### GET /{curso_id}

Obtener detalle de un curso.

**Response** (200):
```json
{
  "id": "curso1",
  "titulo": "Python Básico",
  "descripcion": "Aprende Python desde cero",
  "duracion_horas": 40,
  "nivel": "principiante",
  "instructor": "Dr. García"
}
```

**Errores**:
- `404` — Curso no existe

### GET /{curso_id}/modulos

Obtener módulos de un curso.

**Response** (200):
```json
{
  "modulos": [
    {
      "id": "mod1",
      "titulo": "Fundamentos",
      "descripcion": "Variables, tipos de datos",
      "orden": 1
    },
    {
      "id": "mod2",
      "titulo": "Control de Flujo",
      "descripcion": "If, for, while",
      "orden": 2
    }
  ]
}
```

### GET /modulos/{modulo_id}/lecciones

Obtener lecciones de un módulo.

**Response** (200):
```json
{
  "lecciones": [
    {
      "id": "lec1",
      "titulo": "Variables",
      "duracion_minutos": 30,
      "orden": 1
    },
    {
      "id": "lec2",
      "titulo": "Tipos de datos",
      "duracion_minutos": 45,
      "orden": 2
    }
  ]
}
```

### GET /health

**Response** (200):
```json
{
  "status": "ok"
}
```

---

## Evaluaciones Service

**Direct URL**: `http://localhost:8003` (or via gateway: `/api/v1/evaluaciones`)

### GET /{cuestionario_id}

Obtener cuestionario (sin respuestas correctas).

**Response** (200):
```json
{
  "id": "c1",
  "titulo": "Quiz Python Básico",
  "descripcion": "Evalúa tu conocimiento de Python",
  "duracion_minutos": 30,
  "preguntas": [
    {
      "id": "p1",
      "tipo": "opcion",
      "texto": "¿Cuál es la función para imprimir en Python?",
      "opciones": [
        "imprimir()",
        "print()",
        "mostrar()",
        "echo()"
      ]
    },
    {
      "id": "p2",
      "tipo": "opcion",
      "texto": "¿Cuánto es 2 + 2?",
      "opciones": ["3", "4", "5", "6"]
    }
  ]
}
```

### POST /{cuestionario_id}/responder

Enviar respuestas y obtener score automático.

**Request**:
```json
{
  "respuestas": {
    "p1": 1,
    "p2": 1
  }
}
```

(Los índices son 0-based para las opciones)

**Response** (200):
```json
{
  "cuestionario_id": "c1",
  "score": 100.0,
  "correct": 2,
  "total": 2,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Errores**:
- `400` — Respuestas inválidas
- `404` — Cuestionario no existe

### GET /health

**Response** (200):
```json
{
  "status": "ok"
}
```

---

## Progreso Service

**Direct URL**: `http://localhost:8004` (or via gateway: `/api/v1/progreso`)

### GET /estudiantes/{estudiante_id}/cursos

Obtener progreso del estudiante en todos sus cursos.

**Response** (200):
```json
{
  "estudiante_id": "est1",
  "cursos": [
    {
      "curso_id": "curso1",
      "titulo": "Python Básico",
      "completado_pct": 45,
      "horas_completadas": 18,
      "horas_totales": 40
    },
    {
      "curso_id": "curso2",
      "titulo": "Web Development",
      "completado_pct": 0,
      "horas_completadas": 0,
      "horas_totales": 60
    }
  ]
}
```

### GET /estudiantes/{estudiante_id}/cursos/{curso_id}

Obtener progreso detallado en un curso específico.

**Response** (200):
```json
{
  "curso_id": "curso1",
  "titulo": "Python Básico",
  "completado_pct": 45,
  "modulos": [
    {
      "modulo_id": "mod1",
      "titulo": "Fundamentos",
      "completado_pct": 100,
      "lecciones": [
        {
          "leccion_id": "lec1",
          "titulo": "Variables",
          "completada": true
        }
      ]
    }
  ]
}
```

### GET /health

**Response** (200):
```json
{
  "status": "ok"
}
```

---

## Gateway Health

### GET /health

Health check general del Gateway.

**Response** (200):
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Error Responses

Todos los endpoints retornan errores en este formato:

```json
{
  "detail": "Mensaje de error descriptivo"
}
```

**Códigos HTTP comunes**:
- `200` — OK
- `201` — Creado
- `400` — Bad Request (datos inválidos)
- `401` — Unauthorized (JWT inválido/expirado)
- `403` — Forbidden (no tienes permisos)
- `404` — Not Found
- `500` — Internal Server Error

---

## Autenticación

Incluir el JWT en todas las requests autenticadas:

```bash
curl -H "Authorization: Bearer {access_token}" \
  http://localhost:8000/api/v1/cursos/
```

El Gateway valida el token antes de reenviar a los servicios.

