#!/usr/bin/env python3
"""
Script para validar la estructura y contenido de la documentación
"""

import os
from pathlib import Path

# Colores
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text: str):
    print(f"\n{BLUE}{'=' * 70}{RESET}")
    print(f"{BLUE}{text:^70}{RESET}")
    print(f"{BLUE}{'=' * 70}{RESET}\n")

def print_success(text: str):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text: str):
    print(f"{RED}✗ {text}{RESET}")

def print_info(text: str):
    print(f"{YELLOW}ℹ {text}{RESET}")

def check_file_exists(filepath: str, description: str):
    """Verifica que un archivo exista"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print_success(f"{description}: {size} bytes")
        return True
    else:
        print_error(f"{description}: NO ENCONTRADO")
        return False

def validate_docs():
    """Valida todos los archivos de documentación"""
    print_header("VALIDACIÓN DE DOCUMENTACIÓN")
    
    docs_dir = "docs"
    
    # Archivos principales
    main_docs = {
        f"{docs_dir}/index.md": "Página de inicio",
        f"{docs_dir}/architecture.md": "Arquitectura del sistema",
        f"{docs_dir}/setup.md": "Guía de instalación",
        f"{docs_dir}/development.md": "Guía de desarrollo",
        f"{docs_dir}/api.md": "Referencia de API",
        f"{docs_dir}/entrega.md": "Documento de entrega",
        f"{docs_dir}/INCREMENTAL.md": "Flujo incremental",
        f"{docs_dir}/GIT_COMMITS_GUIDE.md": "Guía de commits",
        "mkdocs.yml": "Configuración MkDocs",
    }
    
    results = {}
    
    print(f"\n{YELLOW}Archivos principales:{RESET}")
    for filepath, description in main_docs.items():
        results[filepath] = check_file_exists(filepath, description)
    
    # Verificar contenido mínimo
    print(f"\n{YELLOW}Verificación de contenido:{RESET}")
    
    content_checks = {
        f"{docs_dir}/index.md": ["Aprendelancia", "microservicios"],
        f"{docs_dir}/architecture.md": ["API Gateway", "Frontend"],
        f"{docs_dir}/setup.md": ["Docker", "docker-compose"],
        f"{docs_dir}/development.md": ["pytest", "tests"],
        f"{docs_dir}/api.md": ["endpoints", "Authentication"],
        f"{docs_dir}/entrega.md": ["Incremento", "Evidencias"],
        f"{docs_dir}/GIT_COMMITS_GUIDE.md": ["git commit", "Sprint"],
    }
    
    for filepath, keywords in content_checks.items():
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                missing = [kw for kw in keywords if kw.lower() not in content]
                if not missing:
                    print_success(f"{os.path.basename(filepath)}: Contiene palabras clave")
                else:
                    print_error(f"{os.path.basename(filepath)}: Faltan keywords: {missing}")
        else:
            print_error(f"{os.path.basename(filepath)}: Archivo no existe")
    
    # Verificar mkdocs.yml
    print(f"\n{YELLOW}Configuración MkDocs:{RESET}")
    
    if os.path.exists("mkdocs.yml"):
        with open("mkdocs.yml", 'r', encoding='utf-8') as f:
            mkdocs_content = f.read()
            
            checks = {
                "site_name": "Nombre del sitio",
                "theme": "Tema configurado",
                "nav": "Navegación configurada",
                "plugins": "Plugins configurados",
                "markdown_extensions": "Extensiones Markdown",
            }
            
            for key, desc in checks.items():
                if key in mkdocs_content:
                    print_success(f"{desc}")
                else:
                    print_error(f"{desc}: No encontrado")
    
    # Estadísticas
    print_header("ESTADÍSTICAS")
    
    total_docs = len([f for f in Path(docs_dir).glob("*.md")])
    total_size = sum(f.stat().st_size for f in Path(docs_dir).glob("*.md"))
    
    print(f"{BLUE}Total de archivos .md:{RESET} {total_docs}")
    print(f"{BLUE}Tamaño total:{RESET} {total_size:,} bytes ({total_size/1024:.2f} KB)")
    
    # Listar todos los archivos
    print(f"\n{YELLOW}Archivos en docs/:{RESET}")
    for file in sorted(Path(docs_dir).glob("*")):
        if file.is_file():
            size = file.stat().st_size
            print(f"  • {file.name}: {size:,} bytes")
    
    # Verificar enlaces
    print(f"\n{YELLOW}Verificación de enlaces internos:{RESET}")
    
    if os.path.exists(f"{docs_dir}/index.md"):
        with open(f"{docs_dir}/index.md", 'r', encoding='utf-8') as f:
            content = f.read()
            links = [
                "architecture.md",
                "setup.md",
                "api.md",
                "development.md",
            ]
            
            for link in links:
                if link in content:
                    print_success(f"Enlace a {link}")
                else:
                    print_info(f"Enlace a {link} no encontrado en index.md")
    
    # Resumen final
    print_header("RESUMEN")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"{BLUE}Archivos encontrados:{RESET} {passed}/{total} ({percentage:.1f}%)")
    
    if percentage == 100:
        print(f"\n{GREEN}✓ Toda la documentación está presente y válida{RESET}")
        return True
    else:
        print(f"\n{YELLOW}⚠ Algunos archivos de documentación faltan o tienen problemas{RESET}")
        return False

def main():
    """Función principal"""
    print_header("VALIDADOR DE DOCUMENTACIÓN - APRENDELANCIA")
    
    if not os.path.exists("docs"):
        print_error("Directorio 'docs/' no encontrado")
        return False
    
    result = validate_docs()
    
    print(f"\n{BLUE}Comandos útiles:{RESET}")
    print(f"  • Ver docs:     {YELLOW}./serve_docs.sh{RESET}")
    print(f"  • O manual:     {YELLOW}mkdocs serve -a 127.0.0.1:8090{RESET}")
    print(f"  • Build docs:   {YELLOW}mkdocs build{RESET}")
    print()
    
    return result

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
