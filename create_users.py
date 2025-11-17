#!/usr/bin/env python3
"""
Script para crear usuarios en la plataforma Aprendelancia.
Uso: python3 create_users.py
"""

import os
import sys
from pymongo import MongoClient
from passlib.context import CryptContext
from datetime import datetime

# Configuración
MONGO_URL = os.getenv("AUTH_DATABASE_URL", "mongodb://auth-db:27017/auth_db")
PWD_CONTEXT = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Usuarios predefinidos
USUARIOS_PREDEFINIDOS = [
    {
        "email": "admin@gmail.com",
        "password": "admin123",
        "nombre": "Admin User",
        "apellido": "Sistema",
        "role": "instructor",
    },
    {
        "email": "instructor1@gmail.com",
        "password": "password123",
        "nombre": "Juan",
        "apellido": "Pérez",
        "role": "instructor",
    },
    {
        "email": "instructor2@gmail.com",
        "password": "password123",
        "nombre": "María",
        "apellido": "González",
        "role": "instructor",
    },
    {
        "email": "estudiante1@gmail.com",
        "password": "password123",
        "nombre": "Carlos",
        "apellido": "López",
        "role": "estudiante",
    },
    {
        "email": "estudiante2@gmail.com",
        "password": "password123",
        "nombre": "Ana",
        "apellido": "Martínez",
        "role": "estudiante",
    },
    {
        "email": "estudiante3@gmail.com",
        "password": "password123",
        "nombre": "Roberto",
        "apellido": "Rodríguez",
        "role": "estudiante",
    },
]


def conectar_mongodb():
    """Conecta a MongoDB."""
    try:
        client = MongoClient(MONGO_URL)
        db = client.get_default_database()
        return db, client
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        sys.exit(1)


def crear_usuarios():
    """Crea los usuarios predefinidos en la base de datos."""
    db, client = conectar_mongodb()
    users = db.get_collection("users")

    # Asegurar que existe índice único en email
    try:
        users.create_index("email", unique=True)
    except Exception:
        pass

    print("\n" + "=" * 60)
    print("🔐 CREANDO USUARIOS EN APRENDELANCIA")
    print("=" * 60 + "\n")

    creados = 0
    saltados = 0

    for usuario_data in USUARIOS_PREDEFINIDOS:
        email = usuario_data["email"]
        password = usuario_data["password"]

        # Verificar si el usuario ya existe
        if users.find_one({"email": email}):
            print(f"⏭️  Saltando {email} (ya existe)")
            saltados += 1
            continue

        # Hashear la contraseña
        hashed_password = PWD_CONTEXT.hash(password)

        # Crear documento del usuario
        user_doc = {
            "email": email,
            "password": hashed_password,
            "nombre": usuario_data.get("nombre", ""),
            "apellido": usuario_data.get("apellido", ""),
            "role": usuario_data.get("role", "estudiante"),
            "bio": "",
            "foto_url": "",
            "created_at": datetime.utcnow(),
        }

        try:
            users.insert_one(user_doc)
            print(
                f"✅ Usuario creado: {email} (rol: {usuario_data['role']}, pwd: {password})"
            )
            creados += 1
        except Exception as e:
            print(f"❌ Error creando {email}: {e}")

    print("\n" + "=" * 60)
    print(f"📊 RESUMEN: {creados} creados, {saltados} saltados")
    print("=" * 60 + "\n")

    # Mostrar todos los usuarios
    print("👥 Usuarios disponibles:")
    print("-" * 60)
    for user in users.find({}, {"password": 0}):
        user_id = user.pop("_id")
        print(f"  • {user['email']} (rol: {user['role']})")

    client.close()


if __name__ == "__main__":
    crear_usuarios()
