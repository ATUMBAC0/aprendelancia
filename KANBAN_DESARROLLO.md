# 📊 APRENDELANCIA - Kanban de Desarrollo

## SPRINT 1: Autenticación

### 📋 To Do
- [ ] Definir esquema de usuario en MongoDB
- [ ] Configurar conexión a MongoDB
- [ ] Implementar modelo Pydantic de Usuario
- [ ] Validar emails únicos
- [ ] Implementar hashing de contraseñas

### 🔄 In Progress
- [ ] Implementar endpoint POST /register
- [ ] Implementar endpoint POST /login
- [ ] Generar JWT tokens

### ✅ Done
- [ ] Crear estructura del proyecto
- [ ] Agregar dependencias al requirements.txt
- [ ] Configurar Dockerfile

---

## SPRINT 2: Microservicios

### 📋 Cursos - To Do
- [ ] Definir modelo de Curso
- [ ] Crear tabla en PostgreSQL
- [ ] Implementar GET /cursos
- [ ] Implementar GET /cursos/{id}
- [ ] Implementar POST /cursos

### 🔄 Cursos - In Progress
- [ ] Implementar PUT /cursos/{id}
- [ ] Implementar DELETE /cursos/{id}

### ✅ Cursos - Done
- [ ] Crear estructura del servicio
- [ ] Configurar conexión a PostgreSQL

### 📋 Evaluaciones - To Do
- [ ] Definir modelo de Evaluación
- [ ] Crear tabla en PostgreSQL
- [ ] Implementar auto-grading
- [ ] Implementar POST /evaluaciones/{id}/responder

### 🔄 Evaluaciones - In Progress
- [ ] Implementar GET /evaluaciones
- [ ] Implementar GET /evaluaciones/{id}

### ✅ Evaluaciones - Done
- [ ] Crear estructura del servicio

### 📋 Progreso - To Do
- [ ] Definir modelo de Progreso
- [ ] Crear tabla en PostgreSQL
- [ ] Implementar tracking de cursos completados
- [ ] Implementar cálculo de estadísticas

### 🔄 Progreso - In Progress
- [ ] Implementar GET /progreso/estudiantes/{id}/cursos

### ✅ Progreso - Done
- [ ] Crear estructura del servicio

---

## SPRINT 3: API Gateway

### 📋 To Do
- [ ] Implementar rutas genéricas GET
- [ ] Implementar rutas genéricas POST
- [ ] Implementar CORS
- [ ] Agregar manejo de errores

### 🔄 In Progress
- [ ] Implementar healthcheck del gateway
- [ ] Agregar logging

### ✅ Done
- [ ] Crear estructura del gateway
- [ ] Configurar FastAPI

---

## SPRINT 4: Frontend

### 📋 Autenticación - To Do
- [ ] Crear página /login
- [ ] Crear página /register
- [ ] Implementar validación de formularios
- [ ] Agregar recordar contraseña

### 🔄 Autenticación - In Progress
- [ ] Integrar con API de login
- [ ] Integrar con API de registro

### ✅ Autenticación - Done
- [ ] Crear estructura del proyecto Flask

### 📋 Cursos - To Do
- [ ] Crear página /cursos
- [ ] Crear página /cursos/{id}
- [ ] Crear página /cursos/crear
- [ ] Implementar filtrado de cursos

### 🔄 Cursos - In Progress
- [ ] Integrar con API de cursos
- [ ] Agregar búsqueda

### ✅ Cursos - Done
- [ ] N/A

### 📋 Evaluaciones - To Do
- [ ] Crear página /evaluaciones
- [ ] Crear formulario de evaluación
- [ ] Implementar temporizador para evaluaciones
- [ ] Crear página de resultados

### 🔄 Evaluaciones - In Progress
- [ ] Integrar con API de evaluaciones

### ✅ Evaluaciones - Done
- [ ] N/A

### 📋 Progreso - To Do
- [ ] Crear página /progreso
- [ ] Crear dashboard de estadísticas
- [ ] Implementar gráficos
- [ ] Mostrar certificados

### 🔄 Progreso - In Progress
- [ ] Integrar con API de progreso

### ✅ Progreso - Done
- [ ] N/A

### 📋 Diseño - To Do
- [ ] Implementar responsive design
- [ ] Agregar iconos
- [ ] Mejorar paleta de colores
- [ ] Agregar animaciones

### 🔄 Diseño - In Progress
- [ ] Hacer navegación más intuitiva

### ✅ Diseño - Done
- [ ] Crear base.html

---

## SPRINT 5: Testing & Deploy

### 📋 To Do
- [ ] Escribir tests unitarios
- [ ] Escribir tests de integración
- [ ] Configurar CI/CD
- [ ] Crear coverage report

### 🔄 In Progress
- [ ] Documentar API endpoints
- [ ] Crear guías de usuario

### ✅ Done
- [ ] N/A

---

## 📈 Burndown Chart (Estimado)

```
Sprint 1: Autenticación
100% |  ╲
  80% |    ╲
  60% |      ╲
  40% |        ╲
  20% |          ╲
   0% |____________╲___
        1  2  3  4  5  Días

Sprint 2: Microservicios
100% |    ╲
  80% |      ╲
  60% |        ╲
  40% |          ╲
  20% |            ╲
   0% |______________╲___
        1  2  3  4  5  6  7  Días

Sprint 3: API Gateway
100% |  ╲
  80% |    ╲
  60% |      ╲
  40% |        ╲
  20% |          ╲
   0% |____________╲___
        1  2  3  4  5  Días

Sprint 4: Frontend
100% |      ╲
  80% |        ╲
  60% |          ╲
  40% |            ╲
  20% |              ╲
   0% |________________╲___
        1  2  3  4  5  6  7  Días

Sprint 5: Testing & Deploy
100% |  ╲
  80% |    ╲
  60% |      ╲
  40% |        ╲
  20% |          ╲
   0% |____________╲___
        1  2  3  4  Días
```

---

## 🎯 Métricas de Éxito por Sprint

### Sprint 1: Autenticación
- ✅ Al menos 2 usuarios creados exitosamente
- ✅ Login generando JWT válidos
- ✅ Todos los tests pasando
- ✅ API disponible en http://localhost:8001

### Sprint 2: Microservicios
- ✅ Mínimo 5 cursos en base de datos
- ✅ Mínimo 3 evaluaciones disponibles
- ✅ Progreso tracked correctamente
- ✅ APIs disponibles en puertos 8002, 8003, 8004

### Sprint 3: API Gateway
- ✅ Todas las rutas forwardeadas correctamente
- ✅ CORS permitiendo requests del frontend
- ✅ Health check respondiendo en < 100ms
- ✅ API disponible en http://localhost:8000

### Sprint 4: Frontend
- ✅ Todas las páginas cargan sin errores
- ✅ Validación client-side funcionando
- ✅ Responsive en móvil, tablet, desktop
- ✅ Frontend disponible en http://localhost:5000

### Sprint 5: Testing & Deploy
- ✅ Coverage > 80%
- ✅ Todos los tests pasando
- ✅ Documentación completa
- ✅ Stack completo deployable con docker-compose

---

## 🔄 Flujo de Trabajo por Sprint

### Inicio de Sprint
1. Revisar checklist de sprint anterior
2. Estimar tareas en story points
3. Asignar tareas al equipo
4. Crear ramas Git para cada feature

### Durante el Sprint
1. Daily standup (15 min)
2. Mover tareas en Kanban
3. Code review en PRs
4. Hacer commits descriptivos

### Fin de Sprint
1. Completar todas las tareas
2. Merge a rama main
3. Testing integral
4. Demo a stakeholders
5. Retrospectiva

---

## 🔀 Ramas Git Recomendadas

```
main (producción)
 ├── develop (desarrollo)
 │    ├── feature/auth-register
 │    ├── feature/auth-login
 │    ├── feature/cursos-crud
 │    ├── feature/evaluaciones-crud
 │    ├── feature/progreso-tracking
 │    ├── feature/gateway-routing
 │    ├── feature/frontend-login
 │    ├── feature/frontend-cursos
 │    └── feature/frontend-evaluaciones
 └── hotfix/bug-fix
```

### Convención de ramas
```
feature/{nombre}      # Nueva funcionalidad
bugfix/{nombre}       # Corrección de bugs
hotfix/{nombre}       # Fixes urgentes en main
refactor/{nombre}     # Refactorización
docs/{nombre}         # Cambios en documentación
```

---

**Última actualización:** 15 de Noviembre de 2025
