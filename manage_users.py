#!/usr/bin/env python3
"""
Script para gestionar usuarios en Aprendelancia.
Permite listar, crear y eliminar usuarios.
"""

import os
import sys
import json
from pymongo import MongoClient
from passlib.context import CryptContext
from datetime import datetime

MONGO_URL = os.getenv("AUTH_DATABASE_URL", "mongodb://auth-db:27017/auth_db")
PWD_CONTEXT = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def conectar_mongodb():
    """Conecta a MongoDB."""
    try:
        client = MongoClient(MONGO_URL)
        db = client.get_default_database()
        return db, client
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        sys.exit(1)


def listar_usuarios():
    """Lista todos los usuarios registrados."""
    db, client = conectar_mongodb()
    users = db.get_collection("users")

    print("\n" + "=" * 70)
    print("👥 USUARIOS REGISTRADOS EN APRENDELANCIA")
    print("=" * 70 + "\n")

    usuarios = list(users.find({}, {"password": 0}))

    if not usuarios:
        print("   ℹ️  No hay usuarios registrados\n")
        client.close()
        return

    for idx, user in enumerate(usuarios, 1):
        print(f"{idx}. Email: {user['email']}")
        print(f"   Nombre: {user.get('nombre', '')} {user.get('apellido', '')}")
        print(f"   Rol: {user.get('role', 'N/A')}")
        print(f"   Creado: {user.get('created_at', 'N/A')}")
        print(f"   ID: {user['_id']}\n")

    print("=" * 70 + "\n")
    print(f"   Total: {len(usuarios)} usuario(s)\n")

    client.close()


def crear_usuario():
    """Crea un nuevo usuario interactivamente."""
    db, client = conectar_mongodb()
    users = db.get_collection("users")

    print("\n" + "=" * 70)
    print("➕ CREAR NUEVO USUARIO")
    print("=" * 70 + "\n")

    # Solicitar datos
    email = input("📧 Email: ").strip()
    if not email:
        print("❌ El email no puede estar vacío\n")
        client.close()
        return

    # Verificar si existe
    if users.find_one({"email": email}):
        print(f"❌ El email {email} ya está registrado\n")
        client.close()
        return

    nombre = input("👤 Nombre: ").strip()
    apellido = input("👤 Apellido: ").strip()
    password = input("🔐 Contraseña (mín. 8 caracteres): ").strip()

    if len(password) < 8:
        print("❌ La contraseña debe tener al menos 8 caracteres\n")
        client.close()
        return

    print("\n   Roles disponibles:")
    print("   1. estudiante")
    print("   2. instructor")
    rol_choice = input("   Selecciona rol (1-2): ").strip()
    rol = "instructor" if rol_choice == "2" else "estudiante"

    # Confirmar
    print("\n📋 Resumen:")
    print(f"   Email: {email}")
    print(f"   Nombre: {nombre} {apellido}")
    print(f"   Rol: {rol}")
    confirmar = input("\n¿Crear este usuario? (s/n): ").strip().lower()

    if confirmar != "s":
        print("❌ Operación cancelada\n")
        client.close()
        return

    # Crear usuario
    try:
        hashed_password = PWD_CONTEXT.hash(password)
        user_doc = {
            "email": email,
            "password": hashed_password,
            "nombre": nombre,
            "apellido": apellido,
            "role": rol,
            "bio": "",
            "foto_url": "",
            "created_at": datetime.utcnow(),
        }
        users.insert_one(user_doc)
        print(f"\n✅ Usuario {email} creado exitosamente\n")
    except Exception as e:
        print(f"❌ Error creando usuario: {e}\n")

    client.close()


def eliminar_usuario():
    """Elimina un usuario."""
    db, client = conectar_mongodb()
    users = db.get_collection("users")

    print("\n" + "=" * 70)
    print("🗑️  ELIMINAR USUARIO")
    print("=" * 70 + "\n")

    email = input("📧 Email del usuario a eliminar: ").strip()

    user = users.find_one({"email": email})
    if not user:
        print(f"❌ Usuario {email} no encontrado\n")
        client.close()
        return

    print(f"\n   Usuario: {user['email']}")
    print(f"   Nombre: {user.get('nombre', '')} {user.get('apellido', '')}")
    confirmar = input("   ¿Eliminar este usuario? (s/n): ").strip().lower()

    if confirmar != "s":
        print("❌ Operación cancelada\n")
        client.close()
        return

    try:
        result = users.delete_one({"email": email})
        if result.deleted_count > 0:
            print(f"✅ Usuario {email} eliminado\n")
        else:
            print(f"❌ No se pudo eliminar el usuario\n")
    except Exception as e:
        print(f"❌ Error eliminando usuario: {e}\n")

    client.close()


def menu_principal():
    """Muestra el menú principal."""
    while True:
        print("\n" + "=" * 70)
        print("🔐 GESTOR DE USUARIOS - APRENDELANCIA")
        print("=" * 70)
        print("\n   1. Listar usuarios")
        print("   2. Crear nuevo usuario")
        print("   3. Eliminar usuario")
        print("   4. Salir")
        print("\n" + "=" * 70 + "\n")

        opcion = input("   Selecciona una opción (1-4): ").strip()

        if opcion == "1":
            listar_usuarios()
        elif opcion == "2":
            crear_usuario()
        elif opcion == "3":
            eliminar_usuario()
        elif opcion == "4":
            print("👋 ¡Hasta luego!\n")
            break
        else:
            print("❌ Opción no válida\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            listar_usuarios()
        elif sys.argv[1] == "create":
            crear_usuario()
        elif sys.argv[1] == "delete":
            eliminar_usuario()
        else:
            print("Uso: python3 manage_users.py [list|create|delete]")
    else:
        menu_principal()
