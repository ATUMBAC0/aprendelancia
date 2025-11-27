# Configuración

## Requisitos Previos

- **Docker** y **Docker Compose** (recomendado)
- O **Python 3.8+**, **PostgreSQL**, **MongoDB**, **Redis** (para local)
- **Git**

## Opción 1: Docker Compose (Recomendado)

### Paso 1: Clonar el repositorio

```bash
git clone <repo-url>
cd aprendelancia
```

### Paso 2: Configurar variables de entorno

```bash
cp .env.example .env
```

Revisar y ajustar `.env` si es necesario.

### Paso 3: Levantar los servicios

```bash
docker-compose up --build
```

Esto toma unos minutos en la primera ejecución. Verás algo como:

```
auth-service_1         | Uvicorn running on http://0.0.0.0:8001
cursos-service_1       | Uvicorn running on http://0.0.0.0:8002
evaluaciones-service_1 | Uvicorn running on http://0.0.0.0:8003
progreso-service_1     | Uvicorn running on http://0.0.0.0:8004
api-gateway_1          | Uvicorn running on http://0.0.0.0:8000
frontend_1             | Running on http://0.0.0.0:5000
```

### Paso 4: Acceder a la plataforma

- **Frontend**: http://localhost:5000
- **Gateway API Docs**: http://localhost:8000/docs
- **Gateway Redoc**: http://localhost:8000/redoc

### Paso 5: Probar

```bash
# Health check
curl http://localhost:8000/api/v1/auth/health
curl http://localhost:8000/api/v1/cursos/health
```

---

## Opción 2: Local (Sin Docker)

### Paso 1: Crear virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate  # Windows
```

### Paso 2: Instalar dependencias

```bash
# Instalaciones comunes
pip install --upgrade pip setuptools

# Services
for service in authentication cursos evaluaciones progreso; do
  pip install -r services/$service/requirements.txt
done

# Gateway y Frontend
pip install -r api-gateway/requirements.txt
pip install -r frontend/requirements.txt
```

### Paso 3: Configurar bases de datos

#### PostgreSQL

```bash
# macOS
brew install postgresql

# Linux (Debian/Ubuntu)
sudo apt-get install postgresql postgresql-contrib

# Crear bases de datos
createdb cursos_db
createdb evaluaciones_db
createdb progreso_db

# Verificar
psql -l | grep -E "cursos_db|evaluaciones_db|progreso_db"
```

#### MongoDB

```bash
# macOS
brew install mongodb-community

# Linux (Debian/Ubuntu)
sudo apt-get install -y mongodb

# Iniciar servicio
brew services start mongodb-community  # macOS
sudo systemctl start mongod  # Linux
```

#### Redis

```bash
# macOS
brew install redis

# Linux
sudo apt-get install redis-server

# Iniciar
brew services start redis  # macOS
sudo systemctl start redis-server  # Linux
```

### Paso 4: Configurar .env

```bash
cp .env.example .env
```

Actualizar con URLs locales:

```
API_GATEWAY_URL=http://127.0.0.1:8000
AUTH_DATABASE_URL=mongodb://127.0.0.1:27017/auth_db
REDIS_URL=redis://127.0.0.1:6379/0
CURSOS_DATABASE_URL=postgresql://localhost/cursos_db
EVALUACIONES_DATABASE_URL=postgresql://localhost/evaluaciones_db
PROGRESO_DATABASE_URL=postgresql://localhost/progreso_db
```

### Paso 5: Ejecutar servicios

Abrir **5 terminales diferentes**:

**Terminal 1: Cursos Service**
```bash
cd services/cursos
uvicorn main:app --reload --host 127.0.0.1 --port 8002
```

**Terminal 2: Evaluaciones Service**
```bash
cd services/evaluaciones
uvicorn main:app --reload --host 127.0.0.1 --port 8003
```

**Terminal 3: Progreso Service**
```bash
cd services/progreso
uvicorn main:app --reload --host 127.0.0.1 --port 8004
```

**Terminal 4: API Gateway**
```bash
uvicorn api_gateway.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 5: Frontend**
```bash
cd frontend
python app.py
```

### Acceder

- Frontend: http://127.0.0.1:5000
- Gateway: http://127.0.0.1:8000/docs

---

## Troubleshooting

### Docker: "Port already in use"

```bash
# Ver qué está usando los puertos
lsof -i :5000
lsof -i :8000

# Matar proceso
kill -9 <PID>

# O cambiar puertos en docker-compose.yml
```

### PostgreSQL: "Connection refused"

```bash
# Verificar que PostgreSQL está corriendo
brew services list  # macOS
systemctl status postgresql  # Linux

# Crear DBs si no existen
createdb cursos_db
createdb evaluaciones_db
createdb progreso_db
```

### MongoDB: "Connection refused"

```bash
# Verificar conexión
mongo --eval "db.version()"

# Iniciar si no corre
brew services start mongodb-community  # macOS
```

### Redis: "Connection refused"

```bash
# Verificar
redis-cli ping

# Iniciar
brew services start redis  # macOS
```

### "Module not found" errors

```bash
# Reinstalar dependencias
pip install -r services/<service>/requirements.txt --force-reinstall

# O completamente
python3 -m venv .venv
source .venv/bin/activate
pip install -r common/requirements.txt  # Si existe
for service in authentication cursos evaluaciones progreso; do
  pip install -r services/$service/requirements.txt
done
```

---

## Comandos Útiles

### Docker Compose

```bash
# Levantar en background
docker-compose up -d --build

# Ver logs de un servicio
docker-compose logs -f cursos-service

# Ver logs de todos
docker-compose logs -f

# Parar servicios
docker-compose down

# Parar y eliminar volúmenes (⚠️ pierde datos)
docker-compose down -v

# Rebuild de una imagen
docker-compose build --no-cache auth-service

# Ejecutar comando en contenedor
docker-compose exec cursos-service bash
```

### Local Development

```bash
# Tests
pytest tests/test_health.py -v

# Lint
flake8 services/cursos/ api-gateway/ frontend/

# Syntax check
python -m py_compile services/cursos/main.py

# Build docs
mkdocs serve  # http://127.0.0.1:8000/docs/
```

---

## Variables de Entorno

Ver `.env.example` para la lista completa. Principales:

```
API_GATEWAY_URL=http://localhost:8000           # URL del gateway (usado por Frontend)
AUTH_DATABASE_URL=mongodb://...                 # Connection string MongoDB
REDIS_URL=redis://...                           # Redis URL
JWT_SECRET=<random-long-string>                 # Clave secreta JWT
CURSOS_DATABASE_URL=postgresql://...            # DB Cursos
EVALUACIONES_DATABASE_URL=postgresql://...      # DB Evaluaciones
PROGRESO_DATABASE_URL=postgresql://...          # DB Progreso
FLASK_SECRET=<random-string>                    # Clave secreta Flask
```

Generar secrets seguros:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
