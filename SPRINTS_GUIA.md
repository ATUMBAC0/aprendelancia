# 🚀 APRENDELANCIA - Guía de Desarrollo por Sprints (Metodología Incremental)

## 📋 Contenido
1. [Visión del Proyecto](#visión-del-proyecto)
2. [Arquitectura](#arquitectura)
3. [Sprints Planificados](#sprints-planificados)
4. [Instrucciones por Sprint](#instrucciones-por-sprint)
5. [Commits Recomendados](#commits-recomendados)
6. [Checklist de Completitud](#checklist-de-completitud)

---

## 🎯 Visión del Proyecto

**Aprendelancia** es una plataforma de educación en línea que permite:
- Estudiantes: Tomar cursos, realizar evaluaciones y ver su progreso
- Instructores: Crear y gestionar cursos, crear evaluaciones
- Administradores: Gestionar usuarios y contenido

**Stack Tecnológico:**
- Backend: FastAPI (Python)
- Base de Datos: MongoDB (Autenticación), PostgreSQL (Servicios)
- Cache: Redis
- Frontend: Flask
- Orquestación: Docker Compose

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Flask)                         │
│                      http://localhost:5000                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (FastAPI)                      │
│                      http://localhost:8000                      │
│  Rutas: /api/v1/{servicio}/{endpoint}                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        ↓                     ↓                     ↓
   ┌─────────┐          ┌──────────┐          ┌──────────┐
   │  AUTH   │          │ CURSOS   │          │ EVALUA.. │
   │ Service │          │ Service  │          │ Service  │
   │  :8001  │          │  :8002   │          │  :8003   │
   └─────────┘          └──────────┘          └──────────┘
        ↓                     ↓                     ↓
   ┌─────────┐          ┌──────────┐          ┌──────────┐
   │ MongoDB │          │ PostgreSQL│         │PostgreSQL│
   │ auth-db │          │ cursos-db │         │ eval-db  │
   └─────────┘          └──────────┘          └──────────┘
        ↓
   ┌─────────┐
   │ PROGRESO│
   │ Service │
   │  :8004  │
   └─────────┘
        ↓
   ┌─────────┐
   │PostgreSQL
   │prog-db  │
   └─────────┘
```

---

## 📅 Sprints Planificados

| Sprint | Duración | Componentes | Objetivo |
|--------|----------|-------------|----------|
| **Sprint 1** | 2-3 días | Autenticación | Implementar sistema de login/registro |
| **Sprint 2** | 3-4 días | Microservicios (Cursos, Evaluaciones, Progreso) | APIs CRUD funcionales |
| **Sprint 3** | 2-3 días | API Gateway | Enrutamiento centralizado |
| **Sprint 4** | 3-4 días | Frontend | Interfaz web completa |
| **Sprint 5** | 1-2 días | Testing & Deploy | QA y documentación |

---

## 🔧 Instrucciones por Sprint

### 📍 SPRINT 1: Microservicio de Autenticación (2-3 días)

#### Objetivo
Implementar autenticación segura con JWT y OAuth

#### Tareas

**Tarea 1.1: Configurar estructura base**
```bash
# 1. Crear estructura del proyecto
mkdir -p services/authentication
cd services/authentication

# 2. Crear archivos necesarios
touch main.py requirements.txt models.py database.py Dockerfile
```

**Commits recomendados:**
```bash
git add services/authentication/
git commit -m "feat: init authentication service structure"
```

**Tarea 1.2: Implementar modelos y BD**
```bash
# 1. Editar models.py - Definir esquema de usuarios
# 2. Editar database.py - Conexión a MongoDB
# 3. Editar requirements.txt - Agregar dependencias
```

**Dependencias a instalar:**
```
fastapi==0.104.1
uvicorn==0.24.0
pymongo==4.15.4
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.5.0
pydantic==2.5.0
python-dotenv==1.2.0
email-validator==2.3.0
redis==7.0.1
```

**Commits recomendados:**
```bash
git add services/authentication/models.py
git commit -m "feat(auth): add user model and database schema"

git add services/authentication/database.py
git commit -m "feat(auth): configure mongodb connection"

git add services/authentication/requirements.txt
git commit -m "build(auth): add dependencies"
```

**Tarea 1.3: Implementar endpoints de autenticación**
```bash
# Endpoints a implementar en main.py:
# POST   /register     - Crear nuevo usuario
# POST   /login        - Obtener JWT token
# POST   /refresh      - Renovar token
# GET    /health       - Verificar salud
# GET    /users        - Listar usuarios (admin)
```

**Commits recomendados:**
```bash
git add services/authentication/main.py
git commit -m "feat(auth): implement register endpoint"

git add services/authentication/main.py
git commit -m "feat(auth): implement login and JWT generation"

git add services/authentication/main.py
git commit -m "feat(auth): implement token refresh endpoint"

git add services/authentication/main.py
git commit -m "feat(auth): implement health check endpoint"
```

**Tarea 1.4: Crear Dockerfile y docker-compose entry**
```bash
# 1. Editar Dockerfile
# 2. Agregar servicio a docker-compose.yml
```

**Commits recomendados:**
```bash
git add services/authentication/Dockerfile
git commit -m "build(auth): create dockerfile for authentication service"

git add docker-compose.yml
git commit -m "infra: add authentication service to docker-compose"
```

**Tarea 1.5: Testing local**
```bash
# Probar endpoints
curl -X POST http://localhost:8001/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'

curl -X POST http://localhost:8001/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'
```

**Commits recomendados:**
```bash
git add tests/auth/
git commit -m "test(auth): add integration tests for auth endpoints"

git add .env.example
git commit -m "docs(auth): add environment variables documentation"
```

---

### 📍 SPRINT 2: Microservicios de Negocio (3-4 días)

#### Objetivo
Implementar 3 microservicios CRUD: Cursos, Evaluaciones, Progreso

#### Estructura para cada servicio
```
services/{nombre}/
├── main.py              # Endpoints FastAPI
├── models.py            # Modelos de datos
├── database_sql.py      # Conexión PostgreSQL
├── requirements.txt     # Dependencias
└── Dockerfile          # Containerización
```

#### Tarea 2.1: Microservicio de Cursos (1 día)

**Endpoints a implementar:**
```
GET    /cursos                  - Listar todos los cursos
GET    /cursos/{id}            - Obtener curso por ID
POST   /cursos                  - Crear nuevo curso (instructor)
PUT    /cursos/{id}            - Actualizar curso (instructor)
DELETE /cursos/{id}            - Eliminar curso (instructor)
GET    /health                 - Health check
```

**Commits recomendados:**
```bash
git add services/cursos/
git commit -m "feat(cursos): init cursos service structure"

git add services/cursos/models.py
git commit -m "feat(cursos): define curso data models"

git add services/cursos/database_sql.py
git commit -m "feat(cursos): configure postgresql connection"

git add services/cursos/main.py
git commit -m "feat(cursos): implement CRUD endpoints for cursos"

git add services/cursos/Dockerfile
git commit -m "build(cursos): create dockerfile"

git add docker-compose.yml
git commit -m "infra: add cursos service to docker-compose"
```

#### Tarea 2.2: Microservicio de Evaluaciones (1 día)

**Endpoints a implementar:**
```
GET    /evaluaciones                    - Listar evaluaciones
GET    /evaluaciones/{id}              - Obtener evaluación
POST   /evaluaciones                    - Crear evaluación (instructor)
POST   /evaluaciones/{id}/responder    - Responder evaluación (estudiante)
GET    /evaluaciones/{id}/resultados  - Ver resultados
DELETE /evaluaciones/{id}              - Eliminar evaluación
GET    /health                         - Health check
```

**Commits recomendados:**
```bash
git add services/evaluaciones/
git commit -m "feat(evaluaciones): init evaluaciones service"

git add services/evaluaciones/models.py
git commit -m "feat(evaluaciones): define evaluation models"

git add services/evaluaciones/main.py
git commit -m "feat(evaluaciones): implement evaluation CRUD"

git add services/evaluaciones/main.py
git commit -m "feat(evaluaciones): implement auto-grading for evaluations"

git add services/evaluaciones/Dockerfile
git commit -m "build(evaluaciones): create dockerfile"

git add docker-compose.yml
git commit -m "infra: add evaluaciones service to docker-compose"
```

#### Tarea 2.3: Microservicio de Progreso (1 día)

**Endpoints a implementar:**
```
GET    /progreso/estudiantes/{id}/cursos              - Ver progreso en cursos
GET    /progreso/estudiantes/{id}/evaluaciones        - Ver calificaciones
POST   /progreso/estudiantes/{id}/marcar-completado  - Marcar curso completado
GET    /progreso/estadisticas                         - Estadísticas globales
GET    /health                                        - Health check
```

**Commits recomendados:**
```bash
git add services/progreso/
git commit -m "feat(progreso): init progreso service"

git add services/progreso/models.py
git commit -m "feat(progreso): define progress models"

git add services/progreso/main.py
git commit -m "feat(progreso): implement progress tracking endpoints"

git add services/progreso/Dockerfile
git commit -m "build(progreso): create dockerfile"

git add docker-compose.yml
git commit -m "infra: add progreso service to docker-compose"
```

#### Tarea 2.4: Actualizar docker-compose y testing

**Commits recomendados:**
```bash
git add docker-compose.yml
git commit -m "infra: configure all microservices in docker-compose"

git add tests/services/
git commit -m "test(services): add integration tests for all microservices"

git add .env.example
git commit -m "docs: add database urls for all services"
```

---

### 📍 SPRINT 3: API Gateway (2-3 días)

#### Objetivo
Implementar enrutador centralizado para todos los microservicios

#### Tarea 3.1: Estructura base del Gateway

**Commits recomendados:**
```bash
git add api-gateway/
git commit -m "feat(gateway): init api gateway structure"

git add api-gateway/requirements.txt
git commit -m "build(gateway): add gateway dependencies"
```

#### Tarea 3.2: Implementar rutas genéricas

**Endpoints a implementar:**
```
GET    /api/v1/{servicio}/{path:path}   - Enrutar GET a servicio
POST   /api/v1/{servicio}/{path:path}   - Enrutar POST a servicio
PUT    /api/v1/{servicio}/{path:path}   - Enrutar PUT a servicio
DELETE /api/v1/{servicio}/{path:path}   - Enrutar DELETE a servicio
GET    /health                          - Health check gateway
GET    /docs                            - Swagger documentation
```

**Commits recomendados:**
```bash
git add api-gateway/main.py
git commit -m "feat(gateway): implement generic routing for all services"

git add api-gateway/main.py
git commit -m "feat(gateway): add cors middleware support"

git add api-gateway/main.py
git commit -m "feat(gateway): implement service health monitoring"

git add api-gateway/Dockerfile
git commit -m "build(gateway): create dockerfile for gateway"

git add docker-compose.yml
git commit -m "infra: add api gateway to docker-compose"
```

#### Tarea 3.3: Testing e integración

**Commits recomendados:**
```bash
git add tests/gateway/
git commit -m "test(gateway): add integration tests for gateway routing"

git add docs/API_REFERENCE.md
git commit -m "docs: add API reference documentation"
```

---

### 📍 SPRINT 4: Frontend (3-4 días)

#### Objetivo
Desarrollar interfaz web completa para la plataforma

#### Tarea 4.1: Estructura y configuración (0.5 días)

**Commits recomendados:**
```bash
git add frontend/
git commit -m "feat(frontend): init flask application structure"

git add frontend/requirements.txt
git commit -m "build(frontend): add flask dependencies"

git add frontend/app.py
git commit -m "feat(frontend): configure flask app and routes"

git add frontend/static/
git commit -m "feat(frontend): add static assets (css, js)"

git add frontend/templates/
git commit -m "feat(frontend): add base template"
```

#### Tarea 4.2: Páginas de autenticación (1 día)

**Páginas a crear:**
- /login - Formulario de login
- /register - Formulario de registro
- /dashboard - Dashboard principal (protegido)

**Commits recomendados:**
```bash
git add frontend/templates/login.html
git commit -m "feat(frontend): create login page"

git add frontend/templates/register.html
git commit -m "feat(frontend): create registration page"

git add frontend/app.py
git commit -m "feat(frontend): implement login endpoint"

git add frontend/app.py
git commit -m "feat(frontend): implement registration endpoint"

git add frontend/templates/dashboard.html
git commit -m "feat(frontend): create dashboard page"
```

#### Tarea 4.3: Páginas de cursos (1 día)

**Páginas a crear:**
- /cursos - Listar cursos disponibles
- /cursos/{id} - Detalle del curso
- /cursos/crear - Crear nuevo curso (instructor)

**Commits recomendados:**
```bash
git add frontend/templates/cursos.html
git commit -m "feat(frontend): create courses listing page"

git add frontend/templates/curso_detalle.html
git commit -m "feat(frontend): create course detail page"

git add frontend/templates/curso_crear.html
git commit -m "feat(frontend): create course creation form"

git add frontend/app.py
git commit -m "feat(frontend): implement courses endpoints"

git add frontend/static/style.css
git commit -m "style(frontend): add courses styling"
```

#### Tarea 4.4: Páginas de evaluaciones (0.75 días)

**Páginas a crear:**
- /evaluaciones - Listar evaluaciones
- /evaluaciones/{id} - Realizar evaluación
- /resultados - Ver resultados de evaluaciones

**Commits recomendados:**
```bash
git add frontend/templates/evaluaciones.html
git commit -m "feat(frontend): create evaluations listing page"

git add frontend/templates/evaluacion_realizar.html
git commit -m "feat(frontend): create evaluation form"

git add frontend/templates/resultados.html
git commit -m "feat(frontend): create results page"

git add frontend/app.py
git commit -m "feat(frontend): implement evaluation endpoints"
```

#### Tarea 4.5: Páginas de progreso (0.75 días)

**Páginas a crear:**
- /progreso - Ver progreso personal
- /estadisticas - Estadísticas globales

**Commits recomendados:**
```bash
git add frontend/templates/progreso.html
git commit -m "feat(frontend): create progress tracking page"

git add frontend/templates/estadisticas.html
git commit -m "feat(frontend): create statistics dashboard"

git add frontend/app.py
git commit -m "feat(frontend): implement progress endpoints"

git add frontend/static/chart.js
git commit -m "feat(frontend): add chart library for statistics"
```

#### Tarea 4.6: Styling y UX (0.5 días)

**Commits recomendados:**
```bash
git add frontend/static/style.css
git commit -m "style(frontend): enhance overall styling"

git add frontend/static/responsive.css
git commit -m "style(frontend): add responsive design"

git add frontend/templates/base.html
git commit -m "feat(frontend): improve base template navigation"

git add frontend/static/js/
git commit -m "feat(frontend): add client-side validation"
```

#### Tarea 4.7: Dockerfile y docker-compose

**Commits recomendados:**
```bash
git add frontend/Dockerfile
git commit -m "build(frontend): create dockerfile for frontend"

git add docker-compose.yml
git commit -m "infra: add frontend service to docker-compose"
```

---

### 📍 SPRINT 5: Testing, Deploy y Documentación (1-2 días)

#### Tarea 5.1: Testing integral

**Commits recomendados:**
```bash
git add tests/
git commit -m "test: add comprehensive integration tests"

git add tests/conftest.py
git commit -m "test: configure pytest fixtures"

git add .github/workflows/
git commit -m "ci: add github actions workflow"
```

#### Tarea 5.2: Documentación

**Commits recomendados:**
```bash
git add README.md
git commit -m "docs: add project readme"

git add docs/SETUP.md
git commit -m "docs: add setup instructions"

git add docs/API_REFERENCE.md
git commit -m "docs: add api reference"

git add docs/ARCHITECTURE.md
git commit -m "docs: add architecture documentation"
```

#### Tarea 5.3: Deployment

**Commits recomendados:**
```bash
git add docker-compose.yml
git commit -m "infra: final docker-compose configuration"

git add .env.example
git commit -m "infra: add environment variables template"

git add DEPLOY.md
git commit -m "ops: add deployment instructions"
```

---

## 📝 Commits Recomendados - Resumen Completo

### Patrón de commits
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Tipos de commits
- **feat**: Nueva funcionalidad
- **fix**: Corrección de bugs
- **docs**: Cambios en documentación
- **style**: Cambios de formato/estilo
- **refactor**: Refactorización de código
- **test**: Agregar o modificar tests
- **build**: Cambios en build/dependencias
- **infra**: Cambios en infraestructura
- **ci**: Cambios en CI/CD

### Ejemplo de commit
```bash
git commit -m "feat(auth): implement jwt token generation

- Add token creation for authenticated users
- Implement refresh token mechanism
- Add token expiration handling

Closes #42"
```

---

## ✅ Checklist de Completitud

### Sprint 1: Autenticación
- [ ] Estructura del proyecto creada
- [ ] Modelos de usuario definidos
- [ ] MongoDB conectado
- [ ] Endpoint /register funcional
- [ ] Endpoint /login funcional
- [ ] JWT token generación
- [ ] Endpoint /refresh funcional
- [ ] Tests unitarios pasando
- [ ] Dockerfile creado
- [ ] docker-compose entry configurado
- [ ] Variables de entorno documentadas

### Sprint 2: Microservicios
- [ ] Servicio Cursos: CRUD completo
- [ ] Servicio Evaluaciones: CRUD + auto-grading
- [ ] Servicio Progreso: endpoints de tracking
- [ ] PostgreSQL configurado para cada servicio
- [ ] Tests de integración pasando
- [ ] Health checks implementados
- [ ] Dockerfiles creados
- [ ] docker-compose actualizado
- [ ] Variables de entorno documentadas

### Sprint 3: API Gateway
- [ ] Rutas genéricas implementadas
- [ ] CORS habilitado
- [ ] Error handling implementado
- [ ] Logging configurado
- [ ] Health monitoring funcional
- [ ] Tests de routing pasando
- [ ] Dockerfile creado
- [ ] docker-compose actualizado

### Sprint 4: Frontend
- [ ] Página de login funcional
- [ ] Página de registro funcional
- [ ] Dashboard con información del usuario
- [ ] Página de cursos con listado
- [ ] Página de detalles de curso
- [ ] Formulario de crear curso
- [ ] Página de evaluaciones
- [ ] Formulario de realizar evaluación
- [ ] Página de progreso
- [ ] Dashboard de estadísticas
- [ ] Responsive design implementado
- [ ] Validación client-side
- [ ] Styling completo
- [ ] Tests de UI
- [ ] Dockerfile creado
- [ ] docker-compose actualizado

### Sprint 5: Finalización
- [ ] Tests de integración completos
- [ ] Coverage > 80%
- [ ] README actualizado
- [ ] API Reference documentada
- [ ] Architecture docs creada
- [ ] Setup instructions documentadas
- [ ] Deploy procedures documentadas
- [ ] CI/CD pipeline configurado
- [ ] Environment variables template
- [ ] Todo en git

---

## 🚀 Comandos Útiles

### Ejecutar todo el stack
```bash
docker-compose up -d
```

### Ver logs de un servicio
```bash
docker-compose logs -f {servicio}
```

### Ejecutar tests
```bash
pytest tests/ -v
```

### Hacer commit
```bash
git add .
git commit -m "feat: description"
git push origin main
```

### Ver estado de git
```bash
git status
git log --oneline
```

---

## 📚 Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)
- [JWT Introduction](https://jwt.io/introduction)

---

**Proyecto:** Aprendelancia  
**Última actualización:** 15 de Noviembre de 2025  
**Versión:** 1.0
