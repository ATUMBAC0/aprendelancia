# 📦 Documento de Entrega — Metodología Incremental

(versión integrada para MkDocs)

<!-- Contenido copiado desde DOCUMENTO_ENTREGA_INCREMENTAL.md -->

# 📦 Documento de Entrega — Metodología Incremental

Proyecto: Aprendelancia — Plataforma de Cursos Online
Fecha: 15/11/2025

Este documento resume cómo se desarrolló y validó el sistema siguiendo una metodología incremental. Incluye objetivos, entregables, evidencias y fragmentos de código clave por incremento.

---

## 🧭 Resumen por Incrementos

| Incremento | Entregable Principal | Objetivo | Evidencias requeridas |
|---|---|---|---|
| 1. Autenticación | Microservicio de autenticación (FastAPI + MongoDB) | Gestión de usuarios, registro, login, JWT | Código, endpoints activos, pruebas básicas, base MongoDB funcionando |
| 2. Microservicios dominio | Cursos, Evaluaciones, Progreso (FastAPI + Postgres) | CRUD/lectura y lógica de dominio | Código, endpoints activos, creación/lectura de datos |
| 3. API Gateway | Pasarela de API (FastAPI) | Unificación de acceso, seguridad, forwarding | Rutas genéricas GET/POST, headers y query params propagados |
| 4. Frontend | Interfaz Flask conectada a Gateway | Experiencia de usuario y consumo de APIs | Login, dashboard, cursos y progreso visibles |

---

## 1) Microservicio de Autenticación

- Tecnología: FastAPI, MongoDB, JWT (python-jose), Passlib, Redis (opcional para refresh).
- Ubicación: `services/authentication/`

### Código clave (endpoints)

```python
# services/authentication/main.py (extracto)
@app.post("/register")
def register(user: UserCreate):
    if users.find_one({"email": user.email}):
        raise HTTPException(status_code=409, detail="Email already registered")
        
    hashed = get_password_hash(user.password)
    users.insert_one({"email": user.email, "password": hashed, "role": user.role, "created_at": datetime.utcnow()})
    return {"message": "user created", "role": user.role}

@app.post("/login")
def login(form_data: UserCreate):
    user = users.find_one({"email": form_data.email})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token({"sub": str(user["_id"]), "email": user["email"], "role": user.get("role", "estudiante")})
    refresh_token = create_refresh_token({"sub": str(user["_id"]), "email": user["email"], "role": user.get("role", "estudiante")})
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@app.get("/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}
```

### Contenedor (Dockerfile)
```dockerfile
# services/authentication/Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Orquestación (docker-compose)
```yaml
# extracto de docker-compose.yml
auth-service:
  build: ./services/authentication
  container_name: auth-service
  ports:
    - "8001:8001"
  environment:
    - DATABASE_URL=mongodb://auth-db:27017/auth_db
  depends_on:
    - auth-db

auth-db:
  image: mongo:latest
  container_name: auth-db
  ports:
    - "27017:27017"
  volumes:
    - auth_data:/data/db
```

### Validación rápida
```bash
# Registro
curl -X POST http://localhost:8001/register -H 'Content-Type: application/json' \
  -d '{"email":"demo@demo.com","password":"demopass123","role":"estudiante"}'

# Login
curl -X POST http://localhost:8001/login -H 'Content-Type: application/json' \
  -d '{"email":"demo@demo.com","password":"demopass123"}'

# /me (requiere Authorization: Bearer ...)
curl http://localhost:8001/me -H "Authorization: Bearer <ACCESS_TOKEN>"
```

---

## 2) Microservicios de Dominio (Cursos, Evaluaciones, Progreso)

- Tecnología: FastAPI. En esta plantilla, los servicios exponen datos en memoria y endpoints de lectura/creación.
- Ubicación:
  - Cursos: `services/cursos/`
  - Evaluaciones: `services/evaluaciones/`
  - Progreso: `services/progreso/`

### Cursos — endpoints
```python
# services/cursos/main.py (extracto)
@app.get("/")
def list_cursos():
    return {"cursos": DATA.get("cursos", [])}

@app.get("/{curso_id}")
def get_curso(curso_id: str):
    for c in DATA.get("cursos", []):
        if c.get("id") == curso_id:
            return c
    raise HTTPException(status_code=404, detail="Curso no encontrado")

@app.post("/cursos")
def create_curso(curso: Curso):
    if any(c.get("id") == curso.id for c in DATA.get("cursos", [])):
        raise HTTPException(status_code=400, detail="Curso ya existe")
    DATA["cursos"].append(curso.dict())
    return {"message": "Curso creado", "curso": curso.dict()}
```

### Evaluaciones — endpoints
```python
# services/evaluaciones/main.py (extracto)
@app.get("/{cuestionario_id}")
def get_cuestionario(cuestionario_id: str):
    q = DATA.get("cuestionarios", {}).get(cuestionario_id)
    if not q:
        raise HTTPException(status_code=404, detail="Cuestionario no encontrado")
    # Se ocultan respuestas correctas
    safe = {"id": q["id"], "titulo": q["titulo"], "preguntas": []}
    for p in q.get("preguntas", []):
        qp = p.copy(); qp.pop("respuesta", None); safe["preguntas"].append(qp)
    return safe

@app.post("/{cuestionario_id}/responder")
def responder(cuestionario_id: str, body: Respuestas):
    # Calificación simple comparando respuestas
    ...
    return {"score": score, "correct": correct, "total": total}
```

### Progreso — endpoints (asignación aleatoria si no hay datos)
```python
# services/progreso/main.py (extracto)
@app.get("/estudiantes/{estudiante_id}/cursos")
def progreso_estudiante(estudiante_id: str):
    existing = DATA.get("progreso", {}).get(estudiante_id)
    if not existing:
        # obtiene cursos del servicio de cursos y asigna 3 aleatorios con % de avance
        ...
        DATA["progreso"][estudiante_id] = {"cursos": cursos_asignados}
        return DATA["progreso"][estudiante_id]
    return existing
```

### Contenedores (Dockerfile)
```dockerfile
# Cursos
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8002"]
```
```dockerfile
# Evaluaciones
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8003"]
```
```dockerfile
# Progreso
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8004"]
```

### Orquestación Postgres (compose)
```yaml
# extracto de docker-compose.yml
cursos-db:
  image: postgres:latest
  environment:
    - POSTGRES_USER=user
    - POSTGRES_PASSWORD=password
    - POSTGRES_DB=cursos_db
  ports:
    - "5432:5432"
  volumes:
    - cursos_data:/var/lib/postgresql
```

---

## 3) API Gateway

- Tecnología: FastAPI con CORS y forward de rutas genéricas.
- Ubicación: `api-gateway/`

### Rutas genéricas con headers y query params
```python
# api-gateway/main.py (extracto)
@router.get("/{service_name}/{path:path}")
async def forward_get(service_name: str, path: str, request: Request):
    headers = {}
    auth = request.headers.get("Authorization")
    if auth: headers["Authorization"] = auth
    response = requests.get(f"{SERVICES[service_name]}/{path}", params=request.query_params, headers=headers)
    return response.json()

@router.post("/{service_name}/{path:path}")
async def forward_post(service_name: str, path: str, request: Request):
    headers = {}
    auth = request.headers.get("Authorization")
    if auth: headers["Authorization"] = auth
    body = None
    try: body = await request.json()
    except Exception: body = None
    response = requests.post(f"{SERVICES[service_name]}/{path}", json=body, params=request.query_params, headers=headers)
    return response.json()
```

### Contenedor (Dockerfile)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
```

### Integración en `docker-compose.yml`
```yaml
api-gateway:
  build: ./api-gateway
  environment:
    - AUTH_SERVICE_URL=http://auth-service:8001
    - CURSOS_SERVICE_URL=http://cursos-service:8002
    - EVALUACIONES_SERVICE_URL=http://evaluaciones-service:8003
    - PROGRESO_SERVICE_URL=http://progreso-service:8004
```

---

## 4) Frontend (Flask)

- Tecnología: Flask, templates Jinja2, sesión con JWT, consumo del Gateway.
- Ubicación: `frontend/`

### Ruta de login y carga de sesión
```python
# frontend/app.py (extracto)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email'); password = request.form.get('password')
        resp = _call_service('POST','auth','login', json={'email': email, 'password': password})
        if resp and 'access_token' in resp:
            session['access_token'] = resp['access_token']
            user_info = _call_service('GET','auth','me')  # devuelve {"user": {...}}
            if user_info and user_info.get('user'):
                u = user_info['user']; session['user'] = {'id': u.get('id'), 'email': u.get('email'), 'role': u.get('role','estudiante')}
            return redirect(url_for('dashboard'))
        flash('Email o contraseña incorrectos', 'error')
    return render_template('login.html')
```

### Plantilla base (navbar con rol/usuario)
```html
<!-- frontend/templates/base.html (extracto) -->
<nav>
  <a href="{{ url_for('index') }}">Inicio</a>
  {% if session.get('access_token') %}
    <a href="{{ url_for('dashboard') }}">Dashboard</a>
    <a href="{{ url_for('cursos_list') }}">Cursos</a>
    <span>Hola, {{ session.get('user', {}).get('role','Usuario').capitalize() }} ({{ session.get('user', {}).get('email','') }})</span>
    <a href="{{ url_for('logout') }}">Cerrar sesión</a>
  {% else %}
    <a href="{{ url_for('login') }}">Iniciar sesión</a>
    <a href="{{ url_for('register') }}">Registrarse</a>
  {% endif %}
</nav>
```

### Contenedor (Dockerfile)
```dockerfile
# frontend/Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["flask","run","--host=0.0.0.0","--port=5000"]
```

---

## 🚀 Ejecución del Stack

```bash
# 1) Preparar entorno
cp .env.example .env

# 2) Construir y levantar todo
docker compose up --build -d

# 3) Endpoints útiles
# Gateway Swagger:  http://localhost:8000/docs
# Frontend:         http://localhost:5000
# Auth:             http://localhost:8001/health
# Cursos:           http://localhost:8002/
# Evaluaciones:     http://localhost:8003/health
# Progreso:         http://localhost:8004/health
```

---

## ✅ Evidencias de Validación
- Health checks activos en todos los servicios (`/health`).
- Login y `/me` funcionando vía Gateway con propagación de `Authorization`.
- Dashboard del frontend mostrando cursos y progreso del usuario.
- Rutas del Gateway reenviando query params (ej. responder evaluaciones).

---

## 📎 Anexos / Recursos
- `docker-compose.yml` — Orquestación completa.
- `seed_data.py` — Script de ejemplo para poblar datos de dominio.
- `docs/` — Documentación navegable por MkDocs.

---

Este archivo es autoinclusivo y puede compartirse como documento de entrega. Para exportarlo a PDF/HTML, puedes usar MkDocs o Pandoc en tu entorno local.
