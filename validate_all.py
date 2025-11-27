#!/usr/bin/env python3
"""
Script integral de validación del proyecto Aprendelancia
Valida todos los servicios, bases de datos y documentación
"""

import subprocess
import sys
import time
import requests
from typing import Dict, List, Tuple

# Colores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text: str):
    """Imprime un encabezado con formato"""
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}{text:^70}{RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}\n")

def print_success(text: str):
    """Imprime mensaje de éxito"""
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text: str):
    """Imprime mensaje de error"""
    print(f"{RED}✗ {text}{RESET}")

def print_info(text: str):
    """Imprime mensaje informativo"""
    print(f"{YELLOW}ℹ {text}{RESET}")

def run_command(cmd: List[str], description: str) -> bool:
    """Ejecuta un comando y retorna si fue exitoso"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print_success(f"{description}: OK")
            return True
        else:
            print_error(f"{description}: FAILED")
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print_error(f"{description}: ERROR - {e}")
        return False

def check_docker():
    """Verifica que Docker esté instalado y funcionando"""
    print_header("VALIDACIÓN DE DOCKER")
    
    docker_ok = run_command(
        ["docker", "--version"],
        "Docker instalado"
    )
    
    compose_ok = run_command(
        ["docker-compose", "--version"],
        "Docker Compose instalado"
    )
    
    return docker_ok and compose_ok

def start_services():
    """Inicia los servicios con Docker Compose"""
    print_header("INICIANDO SERVICIOS")
    
    print_info("Deteniendo servicios previos...")
    subprocess.run(
        ["docker-compose", "down"],
        capture_output=True
    )
    
    print_info("Construyendo e iniciando servicios...")
    result = subprocess.run(
        ["docker-compose", "up", "-d", "--build"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print_success("Servicios iniciados correctamente")
        return True
    else:
        print_error("Error al iniciar servicios")
        print(result.stderr[:500])
        return False

def wait_for_service(url: str, name: str, max_attempts: int = 30) -> bool:
    """Espera a que un servicio esté disponible"""
    print_info(f"Esperando a {name}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print_success(f"{name} disponible")
                return True
        except:
            pass
        time.sleep(2)
    
    print_error(f"{name} no disponible después de {max_attempts * 2}s")
    return False

def check_services() -> Dict[str, bool]:
    """Verifica el estado de todos los servicios"""
    print_header("VERIFICACIÓN DE SERVICIOS")
    
    services = {
        "Frontend": "http://localhost:5000",
        "API Gateway": "http://localhost:8000/health",
        "Auth Service": "http://localhost:8001/health",
        "Cursos Service": "http://localhost:8002/health",
        "Evaluaciones Service": "http://localhost:8003/health",
        "Progreso Service": "http://localhost:8004/health",
    }
    
    results = {}
    
    for name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print_success(f"{name}: OK")
                results[name] = True
            else:
                print_error(f"{name}: Status {response.status_code}")
                results[name] = False
        except Exception as e:
            print_error(f"{name}: No disponible")
            results[name] = False
    
    return results

def check_databases():
    """Verifica el estado de las bases de datos"""
    print_header("VERIFICACIÓN DE BASES DE DATOS")
    
    # Verificar contenedores de bases de datos
    dbs = [
        "auth-db",
        "cursos-db",
        "evaluaciones-db",
        "progreso-db"
    ]
    
    results = {}
    
    for db in dbs:
        result = subprocess.run(
            ["docker", "ps", "--filter", f"name={db}", "--format", "{{.Status}}"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and "Up" in result.stdout:
            print_success(f"{db}: Running")
            results[db] = True
        else:
            print_error(f"{db}: Not running")
            results[db] = False
    
    return results

def test_api_endpoints():
    """Prueba endpoints básicos de la API"""
    print_header("PRUEBA DE ENDPOINTS API")
    
    endpoints = [
        ("GET", "http://localhost:8000/health", "Gateway health"),
        ("GET", "http://localhost:8000/api/v1/auth/health", "Auth through gateway"),
        ("GET", "http://localhost:8000/api/v1/cursos/health", "Cursos through gateway"),
        ("GET", "http://localhost:8000/api/v1/evaluaciones/health", "Evaluaciones through gateway"),
        ("GET", "http://localhost:8000/api/v1/progreso/health", "Progreso through gateway"),
    ]
    
    results = {}
    
    for method, url, description in endpoints:
        try:
            response = requests.request(method, url, timeout=5)
            if response.status_code == 200:
                print_success(f"{description}: OK")
                results[description] = True
            else:
                print_error(f"{description}: Status {response.status_code}")
                results[description] = False
        except Exception as e:
            print_error(f"{description}: {str(e)[:50]}")
            results[description] = False
    
    return results

def check_documentation():
    """Verifica la documentación MkDocs"""
    print_header("VERIFICACIÓN DE DOCUMENTACIÓN")
    
    import os
    
    docs_files = [
        "docs/index.md",
        "docs/architecture.md",
        "docs/setup.md",
        "docs/development.md",
        "mkdocs.yml"
    ]
    
    all_ok = True
    
    for file in docs_files:
        if os.path.exists(file):
            print_success(f"{file}: Existe")
        else:
            print_error(f"{file}: No encontrado")
            all_ok = False
    
    # Verificar que mkdocs esté instalado
    try:
        result = subprocess.run(
            ["mkdocs", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success(f"MkDocs instalado: {result.stdout.strip()}")
        else:
            print_error("MkDocs no disponible")
            all_ok = False
    except:
        print_error("MkDocs no instalado")
        all_ok = False
    
    return all_ok

def generate_report(results: Dict[str, any]):
    """Genera reporte final"""
    print_header("REPORTE FINAL")
    
    total_checks = 0
    passed_checks = 0
    
    for category, data in results.items():
        print(f"\n{YELLOW}{category}:{RESET}")
        if isinstance(data, dict):
            for item, status in data.items():
                total_checks += 1
                if status:
                    passed_checks += 1
                    print(f"  {GREEN}✓{RESET} {item}")
                else:
                    print(f"  {RED}✗{RESET} {item}")
        elif isinstance(data, bool):
            total_checks += 1
            if data:
                passed_checks += 1
                print(f"  {GREEN}✓{RESET} OK")
            else:
                print(f"  {RED}✗{RESET} FAILED")
    
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    percentage = (passed_checks / total_checks * 100) if total_checks > 0 else 0
    
    if percentage == 100:
        color = GREEN
        status = "EXCELENTE"
    elif percentage >= 80:
        color = YELLOW
        status = "BUENO"
    else:
        color = RED
        status = "REQUIERE ATENCIÓN"
    
    print(f"{color}Estado del proyecto: {status}{RESET}")
    print(f"{color}Checks pasados: {passed_checks}/{total_checks} ({percentage:.1f}%){RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}\n")
    
    return percentage >= 80

def main():
    """Función principal"""
    print_header("VALIDACIÓN INTEGRAL - PROYECTO APRENDELANCIA")
    
    results = {}
    
    # 1. Verificar Docker
    if not check_docker():
        print_error("Docker no está disponible. Abortando.")
        sys.exit(1)
    
    # 2. Iniciar servicios
    if not start_services():
        print_error("No se pudieron iniciar los servicios. Abortando.")
        sys.exit(1)
    
    # 3. Esperar a que los servicios estén listos
    print_header("ESPERANDO SERVICIOS")
    time.sleep(10)  # Dar tiempo para que inicien
    
    # 4. Verificar servicios
    results["Servicios"] = check_services()
    
    # 5. Verificar bases de datos
    results["Bases de Datos"] = check_databases()
    
    # 6. Probar endpoints
    results["Endpoints API"] = test_api_endpoints()
    
    # 7. Verificar documentación
    results["Documentación"] = check_documentation()
    
    # 8. Generar reporte
    success = generate_report(results)
    
    # Información adicional
    print_header("COMANDOS ÚTILES")
    print(f"  • Ver logs:           {YELLOW}docker-compose logs -f [servicio]{RESET}")
    print(f"  • Detener servicios:  {YELLOW}docker-compose down{RESET}")
    print(f"  • Frontend:           {YELLOW}http://localhost:5000{RESET}")
    print(f"  • API Gateway:        {YELLOW}http://localhost:8000{RESET}")
    print(f"  • Documentación:      {YELLOW}mkdocs serve -a 127.0.0.1:8080{RESET}")
    print()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
