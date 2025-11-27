# API de Servicios

Esta sección documenta los endpoints de la API de cada microservicio.

## API Gateway

El API Gateway actúa como punto de entrada único para todos los servicios.

**URL Base:** `http://localhost:8000`

### Endpoints del Gateway

#### Health Check
```http
GET /health
```

Retorna el estado del gateway.

**Respuesta exitosa:**
```json
{
  "status": "healthy",
  "service": "api-gateway"
}
```

#### Forwarding Pattern

El gateway redirige peticiones a los servicios usando el patrón:

```http
GET /api/v1/{service_name}/{path}
POST /api/v1/{service_name}/{path}
PUT /api/v1/{service_name}/{path}
DELETE /api/v1/{service_name}/{path}
```

**Servicios disponibles:**
- `auth` - Servicio de autenticación
- `cursos` - Servicio de cursos
- `evaluaciones` - Servicio de evaluaciones
- `progreso` - Servicio de progreso

---

## Servicio de Autenticación

**URL Base:** `http://localhost:8001`
**Via Gateway:** `http://localhost:8000/api/v1/auth`

### Endpoints

#### Health Check
```http
GET /health
```

#### Registro de Usuario
```http
POST /register
```

**Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "role": "estudiante|instructor"
}
```

#### Login
```http
POST /login
```

**Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Respuesta:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "id": "string",
    "username": "string",
    "email": "string",
    "role": "string"
  }
}
```

#### Verificar Usuario
```http
GET /users/me
```

**Headers:**
```
Authorization: Bearer {token}
```

---

## Servicio de Cursos

**URL Base:** `http://localhost:8002`
**Via Gateway:** `http://localhost:8000/api/v1/cursos`

### Endpoints

#### Health Check
```http
GET /health
```

#### Listar Cursos
```http
GET /cursos
```

**Query Parameters:**
- `instructor_id` (opcional) - Filtrar por instructor
- `activo` (opcional) - Filtrar por estado

#### Obtener Curso
```http
GET /cursos/{curso_id}
```

#### Crear Curso
```http
POST /cursos
```

**Headers:**
```
Authorization: Bearer {token}
```

**Body:**
```json
{
  "titulo": "string",
  "descripcion": "string",
  "instructor_id": "string",
  "duracion_horas": 0
}
```

#### Actualizar Curso
```http
PUT /cursos/{curso_id}
```

#### Eliminar Curso
```http
DELETE /cursos/{curso_id}
```

#### Módulos del Curso

##### Listar Módulos
```http
GET /cursos/{curso_id}/modulos
```

##### Crear Módulo
```http
POST /cursos/{curso_id}/modulos
```

**Body:**
```json
{
  "titulo": "string",
  "descripcion": "string",
  "orden": 0,
  "contenido": "string"
}
```

---

## Servicio de Evaluaciones

**URL Base:** `http://localhost:8003`
**Via Gateway:** `http://localhost:8000/api/v1/evaluaciones`

### Endpoints

#### Health Check
```http
GET /health
```

#### Listar Evaluaciones
```http
GET /evaluaciones
```

**Query Parameters:**
- `curso_id` (opcional)
- `modulo_id` (opcional)

#### Obtener Evaluación
```http
GET /evaluaciones/{evaluacion_id}
```

#### Crear Evaluación
```http
POST /evaluaciones
```

**Body:**
```json
{
  "titulo": "string",
  "descripcion": "string",
  "curso_id": "string",
  "modulo_id": "string",
  "duracion_minutos": 0,
  "puntaje_maximo": 100
}
```

#### Responder Evaluación
```http
POST /evaluaciones/{evaluacion_id}/respuestas
```

**Body:**
```json
{
  "usuario_id": "string",
  "respuestas": [
    {
      "pregunta_id": "string",
      "respuesta": "string"
    }
  ]
}
```

#### Obtener Resultado
```http
GET /evaluaciones/{evaluacion_id}/resultados/{usuario_id}
```

---

## Servicio de Progreso

**URL Base:** `http://localhost:8004`
**Via Gateway:** `http://localhost:8000/api/v1/progreso`

### Endpoints

#### Health Check
```http
GET /health
```

#### Obtener Progreso del Usuario
```http
GET /progreso/usuario/{usuario_id}
```

#### Obtener Progreso en Curso
```http
GET /progreso/usuario/{usuario_id}/curso/{curso_id}
```

#### Registrar Progreso
```http
POST /progreso
```

**Body:**
```json
{
  "usuario_id": "string",
  "curso_id": "string",
  "modulo_id": "string",
  "completado": true,
  "tiempo_minutos": 0
}
```

#### Actualizar Progreso
```http
PUT /progreso/{progreso_id}
```

#### Estadísticas
```http
GET /progreso/estadisticas/usuario/{usuario_id}
```

**Respuesta:**
```json
{
  "cursos_inscritos": 0,
  "cursos_completados": 0,
  "tiempo_total_minutos": 0,
  "promedio_evaluaciones": 0
}
```

---

## Códigos de Estado HTTP

- `200 OK` - Solicitud exitosa
- `201 Created` - Recurso creado exitosamente
- `400 Bad Request` - Datos inválidos
- `401 Unauthorized` - No autenticado
- `403 Forbidden` - No autorizado
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

## Autenticación

La mayoría de endpoints requieren autenticación mediante JWT (JSON Web Tokens).

**Header requerido:**
```
Authorization: Bearer {token}
```

El token se obtiene mediante el endpoint `/login` del servicio de autenticación.

## Formato de Errores

Los errores siguen este formato:

```json
{
  "detail": "Mensaje descriptivo del error"
}
```

## CORS

El API Gateway está configurado para aceptar peticiones de cualquier origen en desarrollo. En producción, esto debe configurarse apropiadamente.

