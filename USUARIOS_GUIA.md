# 👥 Guía de Gestión de Usuarios - Aprendelancia

## 📋 Tabla de Contenidos
1. [Ver usuarios registrados](#ver-usuarios-registrados)
2. [Crear nuevo usuario](#crear-nuevo-usuario)
3. [Eliminar usuario](#eliminar-usuario)
4. [Pasos rápidos](#pasos-rápidos)

---

## Ver usuarios registrados

### Opción 1: Desde MongoDB (terminal)
```bash
docker-compose exec auth-db mongosh auth_db
# Dentro de mongosh:
db.users.find({}, {password: 0}).pretty()
```

### Opción 2: Con script Python (recomendado)
```bash
# Listar usuarios
docker cp manage_users.py authentication:/app/
docker-compose exec authentication python3 /app/manage_users.py list
```

### Opción 3: Menú interactivo
```bash
docker-compose exec authentication python3 /app/manage_users.py
```

---

## Crear nuevo usuario

### Opción 1: Desde el formulario web
1. Ve a: **http://localhost:5000/register**
2. Completa el formulario:
   - Email
   - Contraseña (mínimo 8 caracteres)
   - Nombre completo
   - Rol (estudiante o instructor)
3. Haz clic en "Registrarse"

### Opción 2: Vía API POST (curl)
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nuevo@gmail.com",
    "password": "password123",
    "nombre": "Juan",
    "apellido": "Pérez",
    "role": "estudiante"
  }'
```

**Respuesta exitosa:**
```json
{
  "message": "user created",
  "role": "estudiante"
}
```

### Opción 3: Vía API POST (Python)
```bash
python3 << 'EOF'
import requests

url = "http://localhost:8000/api/v1/auth/register"
datos = {
    "email": "nuevo@gmail.com",
    "password": "password123",
    "nombre": "Juan",
    "apellido": "Pérez",
    "role": "estudiante"
}

response = requests.post(url, json=datos)
print(f"Status: {response.status_code}")
print(response.json())
EOF
```

### Opción 4: Menú interactivo (script Python)
```bash
docker cp manage_users.py authentication:/app/
docker-compose exec authentication python3 /app/manage_users.py
# Selecciona opción 2
```

---

## Eliminar usuario

### Opción 1: Desde MongoDB
```bash
docker-compose exec auth-db mongosh auth_db
# Dentro de mongosh:
db.users.deleteOne({email: "usuario@gmail.com"})
```

### Opción 2: Menú interactivo
```bash
docker-compose exec authentication python3 /app/manage_users.py
# Selecciona opción 3
```

---

## Pasos rápidos

### ⚡ Crear múltiples usuarios rápidamente
```bash
python3 create_users.py  # Usa los usuarios predefinidos
```

**Usuarios predefinidos creados:**
- admin@gmail.com (instructor) - password: admin123
- instructor1@gmail.com (instructor) - password: password123
- instructor2@gmail.com (instructor) - password: password123
- estudiante1@gmail.com (estudiante) - password: password123
- estudiante2@gmail.com (estudiante) - password: password123
- estudiante3@gmail.com (estudiante) - password: password123

### 🔑 Probar login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@gmail.com",
    "password": "admin123",
    "role": "instructor"
  }'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "refresh_token": "eyJhbGci..."
}
```

### 📱 Acceder desde el frontend
1. Ve a: **http://localhost:5000/login**
2. Ingresa credenciales:
   - Email: admin@gmail.com
   - Password: admin123
3. Haz clic en "Iniciar sesión"

---

## 📊 Estructura de datos del usuario

```json
{
  "_id": "ObjectId",
  "email": "usuario@gmail.com",
  "password": "hash_pbkdf2_sha256",
  "nombre": "Juan",
  "apellido": "Pérez",
  "role": "estudiante",
  "bio": "",
  "foto_url": "",
  "created_at": "2025-11-15T21:14:34.966Z"
}
```

### Roles disponibles:
- **estudiante** - Acceso limitado a cursos y evaluaciones
- **instructor** - Acceso completo para crear y gestionar cursos

---

## ⚠️ Validaciones

- **Email:** Debe ser único y válido
- **Contraseña:** Mínimo 8 caracteres
- **Rol:** Solo "estudiante" e "instructor"
- **Nombre y Apellido:** Campos opcionales

---

## 🔗 Endpoints disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Crear nuevo usuario |
| POST | `/api/v1/auth/login` | Iniciar sesión |
| POST | `/api/v1/auth/refresh` | Renovar token |
| GET | `/api/v1/auth/health` | Verificar salud del servicio |

---

## 💡 Tips

- El password se hashea automáticamente con PBKDF2-SHA256
- Los tokens JWT expiran en 60 minutos (access_token)
- El refresh_token es válido por 7 días
- Usa el `access_token` para acceder a endpoints protegidos

---

## 🆘 Solución de problemas

### Error: "Email already registered"
- El email ya existe en la base de datos
- Usa otro email o elimina el usuario anterior

### Error: "Password must be at least 8 characters long"
- La contraseña es demasiado corta
- Usa al menos 8 caracteres

### Error: "Incorrect email or password"
- Email o contraseña incorrectos al hacer login
- Verifica que el usuario esté creado
- Verifica la contraseña correcta

### Error: "Role must be 'estudiante', 'instructor', or 'admin'"
- El rol no es válido
- Usa solo "estudiante" o "instructor"

---

**Última actualización:** 15 de Noviembre de 2025
