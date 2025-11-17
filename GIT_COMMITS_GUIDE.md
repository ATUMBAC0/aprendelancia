# 🔧 Git - Guía Práctica de Commits por Sprint

## Configuración Inicial de Git

```bash
# Configurar identidad global
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"

# Clonar repositorio
git clone https://github.com/ATUMBAC0/aprendelancia.git
cd aprendelancia

# Crear rama develop
git checkout -b develop
git push -u origin develop
```

---

## 🔵 SPRINT 1: Autenticación

### Inicio del Sprint
```bash
# Crear rama para autenticación
git checkout develop
git pull origin develop
git checkout -b feature/auth-service

# Actualizar main.py con estructura base
git add services/authentication/
git commit -m "feat: init authentication service structure

- Create authentication microservice folder
- Add main.py, models.py, database.py
- Add requirements.txt with dependencies
- Add Dockerfile for containerization"

# Actualizar modelos de usuario
git add services/authentication/models.py
git commit -m "feat(auth): add user model and database schema

- Define User pydantic model
- Add validation for email and password
- Implement unique email constraint
- Add role enum (estudiante, instructor, admin)"

# Configurar base de datos
git add services/authentication/database.py
git commit -m "feat(auth): configure mongodb connection

- Add MongoDB connection pool
- Initialize default database
- Create users collection
- Add connection error handling"

# Agregar dependencias
git add services/authentication/requirements.txt
git commit -m "build(auth): add authentication dependencies

- Add fastapi==0.104.1
- Add pymongo==4.15.4
- Add passlib[bcrypt]==1.7.4
- Add python-jose[cryptography]==3.5.0
- Add pydantic==2.5.0
- Add uvicorn==0.24.0"

# Implementar registro
git add services/authentication/main.py
git commit -m "feat(auth): implement user registration endpoint

- Create POST /register endpoint
- Add email validation
- Add password hashing with passlib
- Add duplicate email check
- Return success message with user role"

# Implementar login
git add services/authentication/main.py
git commit -m "feat(auth): implement login with JWT generation

- Create POST /login endpoint
- Add password verification
- Generate access_token (60 min expiry)
- Generate refresh_token (7 days expiry)
- Store tokens in Redis
- Return bearer token"

# Implementar refresh token
git add services/authentication/main.py
git commit -m "feat(auth): implement token refresh endpoint

- Create POST /refresh endpoint
- Validate refresh token expiry
- Generate new access token
- Maintain user claims (email, role)
- Return new access token"

# Agregar health check
git add services/authentication/main.py
git commit -m "feat(auth): add health check endpoint

- Create GET /health endpoint
- Return service status
- Check MongoDB connection
- Return response time"

# Agregar Dockerfile
git add services/authentication/Dockerfile
git commit -m "build(auth): create dockerfile for authentication service

- Use python:3.12-slim base image
- Install dependencies from requirements.txt
- Copy application code
- Expose port 8001
- Run uvicorn with hot reload"

# Integrar en docker-compose
git add docker-compose.yml
git commit -m "infra: add authentication service to docker-compose

- Add auth-service container
- Configure port 8001
- Link to MongoDB (auth-db)
- Set environment variables
- Add health checks"

# Agregar tests
git add tests/auth/test_register.py
git commit -m "test(auth): add registration endpoint tests

- Test successful registration
- Test duplicate email prevention
- Test weak password validation
- Test invalid email rejection"

git add tests/auth/test_login.py
git commit -m "test(auth): add login endpoint tests

- Test successful login
- Test JWT token generation
- Test invalid credentials
- Test token expiry"

# Documentación de variables de entorno
git add .env.example
git commit -m "docs(auth): add authentication environment variables

- Add JWT_SECRET example
- Add MongoDB connection URL
- Add Redis connection URL
- Add token expiry times"

# Mergear a develop
git add -A
git commit -m "docs(auth): finalize auth service documentation"
git push origin feature/auth-service
# Abrir Pull Request en GitHub
# Después de review y aprobación:
git checkout develop
git pull origin develop
git merge --no-ff feature/auth-service
git push origin develop
```

---

## 🔵 SPRINT 2: Microservicios

### Tarea 2.1: Servicio de Cursos
```bash
git checkout develop
git pull origin develop
git checkout -b feature/cursos-service

# Estructura base
git add services/cursos/
git commit -m "feat(cursos): init cursos service structure

- Create cursos microservice folder
- Add main.py, models.py, database_sql.py
- Add requirements.txt with postgresql dependencies
- Add Dockerfile"

# Modelos de datos
git add services/cursos/models.py
git commit -m "feat(cursos): define curso data models

- Create Curso model with all fields
- Add validation for curso data
- Implement categoria enum
- Add timestamps (created_at, updated_at)"

# Conexión a base de datos
git add services/cursos/database_sql.py
git commit -m "feat(cursos): configure postgresql connection

- Setup SQLAlchemy connection pool
- Create cursos table schema
- Add migration support
- Implement connection error handling"

# CRUD endpoints
git add services/cursos/main.py
git commit -m "feat(cursos): implement curso CRUD endpoints

- GET /cursos - list all courses
- GET /cursos/{id} - get course by id
- POST /cursos - create new course (instructor)
- PUT /cursos/{id} - update course
- DELETE /cursos/{id} - delete course
- GET /health - health check"

# Dockerfile
git add services/cursos/Dockerfile
git commit -m "build(cursos): create dockerfile for cursos service"

# Integrar en docker-compose
git add docker-compose.yml
git commit -m "infra: add cursos service to docker-compose"

# Tests
git add tests/cursos/
git commit -m "test(cursos): add CRUD endpoint tests"

# Mergear
git push origin feature/cursos-service
# PR, review, merge a develop
```

### Tarea 2.2: Servicio de Evaluaciones
```bash
git checkout develop
git pull origin develop
git checkout -b feature/evaluaciones-service

# Estructura base
git add services/evaluaciones/
git commit -m "feat(evaluaciones): init evaluaciones service structure"

# Modelos con auto-grading
git add services/evaluaciones/models.py
git commit -m "feat(evaluaciones): define evaluation models with grading

- Create Evaluacion model
- Define Pregunta model with question types
- Implement Respuesta model
- Add auto-grading logic for multiple choice
- Add punto calculation"

# Base de datos
git add services/evaluaciones/database_sql.py
git commit -m "feat(evaluaciones): configure postgresql for evaluations"

# CRUD endpoints
git add services/evaluaciones/main.py
git commit -m "feat(evaluaciones): implement evaluation CRUD endpoints"

# Auto-grading
git add services/evaluaciones/main.py
git commit -m "feat(evaluaciones): implement automatic grading system

- Auto-grade multiple choice questions
- Calculate total score
- Store results with timestamp
- Return immediate feedback"

# Dockerfile
git add services/evaluaciones/Dockerfile
git commit -m "build(evaluaciones): create dockerfile for evaluaciones"

# Integrar en docker-compose
git add docker-compose.yml
git commit -m "infra: add evaluaciones service to docker-compose"

# Tests
git add tests/evaluaciones/
git commit -m "test(evaluaciones): add evaluation endpoint tests"

# Mergear
git push origin feature/evaluaciones-service
```

### Tarea 2.3: Servicio de Progreso
```bash
git checkout develop
git pull origin develop
git checkout -b feature/progreso-service

# Estructura base
git add services/progreso/
git commit -m "feat(progreso): init progreso service structure"

# Modelos de progreso
git add services/progreso/models.py
git commit -m "feat(progreso): define progress tracking models

- Create EstudianteProgreso model
- Define CursoCompletado model
- Add progress percentage calculation
- Implement statistics models"

# Base de datos
git add services/progreso/database_sql.py
git commit -m "feat(progreso): configure postgresql for progress tracking"

# Endpoints de progreso
git add services/progreso/main.py
git commit -m "feat(progreso): implement progress tracking endpoints

- GET /progreso/estudiantes/{id}/cursos - progress per course
- GET /progreso/estudiantes/{id}/evaluaciones - grades
- POST /progreso/estudiantes/{id}/marcar-completado - mark course done
- GET /progreso/estadisticas - global statistics"

# Dockerfile
git add services/progreso/Dockerfile
git commit -m "build(progreso): create dockerfile for progreso service"

# Integrar en docker-compose
git add docker-compose.yml
git commit -m "infra: add progreso service to docker-compose"

# Tests
git add tests/progreso/
git commit -m "test(progreso): add progress tracking tests"

# Mergear
git push origin feature/progreso-service
```

---

## 🔵 SPRINT 3: API Gateway

```bash
git checkout develop
git pull origin develop
git checkout -b feature/api-gateway

# Estructura base
git add api-gateway/
git commit -m "feat(gateway): init api gateway structure

- Create api-gateway folder
- Add main.py, requirements.txt
- Configure FastAPI app"

# Dependencias
git add api-gateway/requirements.txt
git commit -m "build(gateway): add gateway dependencies

- Add fastapi==0.104.1
- Add httpx==0.25.0
- Add python-dotenv==1.2.0
- Add uvicorn==0.24.0"

# Rutas genéricas
git add api-gateway/main.py
git commit -m "feat(gateway): implement generic routing for all services

- Create router for /api/v1/{service}/{path}
- Implement GET request forwarding
- Implement POST request forwarding
- Implement PUT request forwarding
- Implement DELETE request forwarding"

# CORS
git add api-gateway/main.py
git commit -m "feat(gateway): add cors middleware support

- Enable CORS for frontend origin
- Allow credentials
- Set allowed headers and methods"

# Health monitoring
git add api-gateway/main.py
git commit -m "feat(gateway): implement service health monitoring

- GET /health returns gateway status
- Check connection to all services
- Return service availability
- Track response times"

# Dockerfile
git add api-gateway/Dockerfile
git commit -m "build(gateway): create dockerfile for api gateway"

# Integrar en docker-compose
git add docker-compose.yml
git commit -m "infra: add api gateway to docker-compose

- Configure port 8000
- Link to all microservices
- Set environment variables"

# Tests
git add tests/gateway/
git commit -m "test(gateway): add gateway routing integration tests"

# Documentación
git add docs/API_REFERENCE.md
git commit -m "docs: add API reference documentation

- Document all endpoints
- Add request/response examples
- Add authentication requirements"

# Mergear
git push origin feature/api-gateway
```

---

## 🔵 SPRINT 4: Frontend

```bash
git checkout develop
git pull origin develop
git checkout -b feature/frontend-complete

# Estructura base
git add frontend/
git commit -m "feat(frontend): init flask application structure

- Create frontend folder with Flask app
- Add templates, static folders
- Configure app.py"

# Dependencias
git add frontend/requirements.txt
git commit -m "build(frontend): add flask dependencies

- Add flask==3.0.0
- Add requests==2.31.0
- Add python-dotenv==1.2.0"

# Base de templates
git add frontend/templates/base.html
git commit -m "feat(frontend): add base html template

- Create responsive layout
- Add navigation bar
- Include CSS/JS references"

# Página de login
git add frontend/templates/login.html
git commit -m "feat(frontend): create login page

- Add email and password inputs
- Add form validation
- Add submit button
- Add register link"

git add frontend/app.py
git commit -m "feat(frontend): implement login endpoint

- Create POST /login handler
- Call auth API
- Store JWT token in session
- Redirect to dashboard"

# Página de registro
git add frontend/templates/register.html
git commit -m "feat(frontend): create registration page

- Add form with all required fields
- Add role selection
- Add password confirmation
- Add submit button"

git add frontend/app.py
git commit -m "feat(frontend): implement registration endpoint

- Create POST /register handler
- Call auth API
- Validate form data
- Handle registration errors"

# Dashboard
git add frontend/templates/dashboard.html
git commit -m "feat(frontend): create dashboard page

- Show welcome message
- Display user information
- Add links to main sections
- Add logout button"

# Página de cursos
git add frontend/templates/cursos.html
git commit -m "feat(frontend): create courses listing page

- Display all available courses
- Add course cards with info
- Add enroll button
- Add search/filter"

git add frontend/templates/curso_detalle.html
git commit -m "feat(frontend): create course detail page

- Show course information
- List course content
- Display instructor info
- Add progress bar"

git add frontend/templates/curso_crear.html
git commit -m "feat(frontend): create course creation form

- Add form for course details
- Add rich text editor for description
- Add category selector
- Add publish button (instructor only)"

git add frontend/app.py
git commit -m "feat(frontend): implement courses endpoints

- GET /cursos - list courses
- GET /cursos/{id} - course detail
- POST /cursos/crear - create course (instructor)
- POST /cursos/{id}/enrollar - enroll in course"

# Página de evaluaciones
git add frontend/templates/evaluaciones.html
git commit -m "feat(frontend): create evaluations listing page

- Display available evaluations
- Show evaluation info
- Add take test button
- Show past results"

git add frontend/templates/evaluacion_realizar.html
git commit -m "feat(frontend): create evaluation form

- Display questions one by one
- Add timer for evaluation
- Show question progress
- Prevent backwards navigation"

git add frontend/templates/resultados.html
git commit -m "feat(frontend): create results page

- Show evaluation score
- Display correct/incorrect answers
- Show answer explanations
- Option to review evaluation"

git add frontend/app.py
git commit -m "feat(frontend): implement evaluation endpoints

- GET /evaluaciones - list evaluations
- GET /evaluaciones/{id} - start evaluation
- POST /evaluaciones/{id}/submit - submit answers
- GET /resultados/{id} - view results"

# Página de progreso
git add frontend/templates/progreso.html
git commit -m "feat(frontend): create progress tracking page

- Show enrolled courses
- Display progress bars
- Show estimated completion
- List achievements"

git add frontend/templates/estadisticas.html
git commit -m "feat(frontend): create statistics dashboard

- Show learning statistics
- Display charts and graphs
- Show performance metrics
- Compare with averages"

git add frontend/app.py
git commit -m "feat(frontend): implement progress endpoints

- GET /progreso - student progress
- GET /estadisticas - statistics dashboard
- GET /certificados - earned certificates"

# Styling
git add frontend/static/style.css
git commit -m "style(frontend): add complete styling

- Create consistent color scheme
- Add responsive breakpoints
- Style all form elements
- Add hover effects and transitions"

git add frontend/static/responsive.css
git commit -m "style(frontend): add responsive design

- Mobile-first approach
- Tablet breakpoints
- Desktop optimizations
- Print styles"

# JavaScript
git add frontend/static/js/validation.js
git commit -m "feat(frontend): add client-side validation

- Validate email format
- Check password strength
- Validate required fields
- Show validation messages"

git add frontend/static/js/timer.js
git commit -m "feat(frontend): add evaluation timer

- Display countdown timer
- Warn when time is running out
- Auto-submit when time expires"

git add frontend/static/chart.js
git commit -m "feat(frontend): add chart library for statistics

- Include Chart.js library
- Create progress charts
- Create performance graphs
- Create achievement visualizations"

# Dockerfile
git add frontend/Dockerfile
git commit -m "build(frontend): create dockerfile for frontend

- Use python:3.12-slim base
- Install dependencies
- Copy application code
- Expose port 5000"

# Integrar en docker-compose
git add docker-compose.yml
git commit -m "infra: add frontend service to docker-compose

- Configure port 5000
- Link to api-gateway
- Set environment variables"

# Mergear
git push origin feature/frontend-complete
```

---

## 🔵 SPRINT 5: Testing & Deploy

```bash
git checkout develop
git pull origin develop
git checkout -b feature/testing-and-docs

# Tests unitarios
git add tests/unit/
git commit -m "test: add comprehensive unit tests

- Test auth logic
- Test models validation
- Test database operations
- Target coverage > 80%"

# Tests de integración
git add tests/integration/
git commit -m "test: add integration tests

- Test end-to-end workflows
- Test API communication
- Test database persistence
- Test error handling"

# Tests de UI
git add tests/ui/
git commit -m "test: add UI/frontend tests

- Test page rendering
- Test form validation
- Test navigation
- Test responsive design"

# CI/CD
git add .github/workflows/
git commit -m "ci: add github actions workflow

- Run tests on every push
- Generate coverage report
- Build docker images
- Check code quality"

# README
git add README.md
git commit -m "docs: add project README

- Add project description
- Include quick start guide
- Add technology stack
- Include screenshots"

# Setup guide
git add docs/SETUP.md
git commit -m "docs: add setup instructions

- Prerequisites
- Installation steps
- Running docker-compose
- Troubleshooting"

# API Reference
git add docs/API_REFERENCE.md
git commit -m "docs: add complete API reference

- Document all endpoints
- Include request/response examples
- Add authentication info
- Add error codes"

# Architecture
git add docs/ARCHITECTURE.md
git commit -m "docs: add architecture documentation

- System design overview
- Component interactions
- Database schema
- Deployment diagram"

# Deployment guide
git add DEPLOY.md
git commit -m "ops: add deployment instructions

- Production setup
- Environment configuration
- Database backup procedures
- Monitoring setup"

# Environment template
git add .env.example
git commit -m "infra: add complete environment variables template

- All service configurations
- Database connections
- Security settings
- API keys"

# Coverage report
git add coverage/
git commit -m "ci: generate coverage report

- Achieve > 80% coverage
- Identify untested code
- Add missing tests"

# Final merge
git push origin feature/testing-and-docs
# PR, review, merge a develop

# Crear release
git checkout main
git pull origin main
git merge --no-ff develop
git tag -a v1.0 -m "Release version 1.0"
git push origin main --tags
```

---

## 📊 Flujo de Trabajo Estándar

### Para cada feature
```bash
# 1. Crear rama
git checkout develop
git pull origin develop
git checkout -b feature/nombre-descriptivo

# 2. Hacer cambios y commits
git add archivos
git commit -m "tipo(scope): descripción"

# 3. Push a GitHub
git push origin feature/nombre-descriptivo

# 4. Crear Pull Request
# Ir a GitHub y abrir PR

# 5. Después de aprobación, mergear
git checkout develop
git pull origin develop
git merge --no-ff feature/nombre-descriptivo
git push origin develop

# 6. Eliminar rama local
git branch -d feature/nombre-descriptivo
```

---

## 🔍 Comandos Útiles

```bash
# Ver estado
git status

# Ver historial
git log --oneline

# Ver diferencias
git diff

# Deshacer cambios
git checkout -- archivo
git reset HEAD archivo

# Ver ramas
git branch -a

# Cambiar entre ramas
git checkout nombre-rama

# Stash (guardar cambios temporalmente)
git stash
git stash pop

# Ver remotes
git remote -v

# Actualizar main branch
git fetch origin main
git rebase origin/main

# Squash commits
git rebase -i HEAD~3

# Cherry-pick (aplicar commit específico)
git cherry-pick hash-commit
```

---

**Última actualización:** 15 de Noviembre de 2025
