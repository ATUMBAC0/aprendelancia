#!/usr/bin/env python3
"""
Script de prueba para verificar login y registro desde el frontend
"""
import requests

FRONTEND_URL = "http://localhost:5000"

def test_login():
    """Prueba el flujo de login"""
    print("🔍 Probando login...")
    
    # Crear sesión para mantener cookies
    session = requests.Session()
    
    # Hacer POST al login
    response = session.post(
        f"{FRONTEND_URL}/login",
        data={
            "email": "estudiante@test.com",
            "password": "password123"
        },
        allow_redirects=False
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 302:  # Redirect
        print(f"✅ Login exitoso - redirigiendo a: {response.headers.get('Location')}")
        
        # Seguir el redirect
        dashboard_response = session.get(f"{FRONTEND_URL}{response.headers.get('Location')}")
        print(f"Dashboard status: {dashboard_response.status_code}")
        
        if dashboard_response.status_code == 200:
            print("✅ Dashboard cargado correctamente")
            return True
    else:
        print(f"❌ Login falló - Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return False

def test_register():
    """Prueba el flujo de registro"""
    print("\n🔍 Probando registro...")
    
    # Crear sesión
    session = requests.Session()
    
    # Intentar registrar nuevo usuario
    import random
    random_email = f"test{random.randint(1000, 9999)}@example.com"
    
    response = session.post(
        f"{FRONTEND_URL}/register",
        data={
            "email": random_email,
            "password": "password123",
            "nombre": "Usuario",
            "apellido": "Prueba",
            "role": "estudiante"
        },
        allow_redirects=False
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 302:  # Redirect to login
        print(f"✅ Registro exitoso - redirigiendo a: {response.headers.get('Location')}")
        print(f"Usuario creado: {random_email}")
        return True
    else:
        print(f"❌ Registro falló - Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return False

def main():
    print("=" * 60)
    print("Pruebas de Login y Registro - Frontend")
    print("=" * 60)
    
    # Probar login
    login_ok = test_login()
    
    # Probar registro
    register_ok = test_register()
    
    print("\n" + "=" * 60)
    print("Resumen:")
    print(f"  Login: {'✅ PASS' if login_ok else '❌ FAIL'}")
    print(f"  Registro: {'✅ PASS' if register_ok else '❌ FAIL'}")
    print("=" * 60)

if __name__ == "__main__":
    main()
