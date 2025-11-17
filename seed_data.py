#!/usr/bin/env python3
"""
Script para poblar las bases de datos con cursos de Ingeniería en Sistemas,
evaluaciones y progreso de estudiantes.
"""

import requests
import random
from datetime import datetime

# URLs de los microservicios
BASE_CURSOS = "http://localhost:8002"
BASE_EVALUACIONES = "http://localhost:8003"
BASE_PROGRESO = "http://localhost:8004"

# Cursos de Ingeniería en Sistemas
CURSOS = [
    {
        "id": "ing-sys-001",
        "titulo": "Fundamentos de Programación",
        "descripcion": "Introducción a la programación con Python. Variables, estructuras de control, funciones y OOP.",
        "instructor_id": "instructor1@gmail.com",
        "duracion_horas": 60,
        "rating": round(random.uniform(4.2, 5.0), 1),
        "nivel": "Básico"
    },
    {
        "id": "ing-sys-002",
        "titulo": "Estructuras de Datos y Algoritmos",
        "descripcion": "Arrays, listas enlazadas, árboles, grafos, algoritmos de ordenamiento y búsqueda.",
        "instructor_id": "instructor1@gmail.com",
        "duracion_horas": 80,
        "rating": round(random.uniform(4.0, 4.9), 1),
        "nivel": "Intermedio"
    },
    {
        "id": "ing-sys-003",
        "titulo": "Bases de Datos Relacionales",
        "descripcion": "SQL, diseño de bases de datos, normalización, PostgreSQL y MySQL.",
        "instructor_id": "instructor2@gmail.com",
        "duracion_horas": 50,
        "rating": round(random.uniform(4.3, 5.0), 1),
        "nivel": "Intermedio"
    },
    {
        "id": "ing-sys-004",
        "titulo": "Desarrollo Web Full Stack",
        "descripcion": "HTML, CSS, JavaScript, React, Node.js, APIs RESTful y despliegue.",
        "instructor_id": "instructor2@gmail.com",
        "duracion_horas": 120,
        "rating": round(random.uniform(4.4, 5.0), 1),
        "nivel": "Avanzado"
    },
    {
        "id": "ing-sys-005",
        "titulo": "Arquitectura de Software",
        "descripcion": "Patrones de diseño, microservicios, arquitecturas limpias y principios SOLID.",
        "instructor_id": "instructor1@gmail.com",
        "duracion_horas": 70,
        "rating": round(random.uniform(4.5, 5.0), 1),
        "nivel": "Avanzado"
    },
    {
        "id": "ing-sys-006",
        "titulo": "Sistemas Operativos",
        "descripcion": "Procesos, threads, gestión de memoria, sistemas de archivos, Linux.",
        "instructor_id": "instructor2@gmail.com",
        "duracion_horas": 65,
        "rating": round(random.uniform(4.1, 4.8), 1),
        "nivel": "Intermedio"
    },
    {
        "id": "ing-sys-007",
        "titulo": "Redes de Computadoras",
        "descripcion": "Protocolos TCP/IP, DNS, HTTP, routing, switching y seguridad en redes.",
        "instructor_id": "instructor1@gmail.com",
        "duracion_horas": 55,
        "rating": round(random.uniform(4.2, 4.9), 1),
        "nivel": "Intermedio"
    },
    {
        "id": "ing-sys-008",
        "titulo": "Inteligencia Artificial",
        "descripcion": "Machine Learning, redes neuronales, NLP, computer vision con Python y TensorFlow.",
        "instructor_id": "instructor2@gmail.com",
        "duracion_horas": 100,
        "rating": round(random.uniform(4.6, 5.0), 1),
        "nivel": "Avanzado"
    },
    {
        "id": "ing-sys-009",
        "titulo": "Seguridad Informática",
        "descripcion": "Criptografía, pentesting, análisis de vulnerabilidades, ethical hacking.",
        "instructor_id": "instructor1@gmail.com",
        "duracion_horas": 75,
        "rating": round(random.uniform(4.3, 4.9), 1),
        "nivel": "Avanzado"
    },
    {
        "id": "ing-sys-010",
        "titulo": "Cloud Computing y DevOps",
        "descripcion": "AWS, Docker, Kubernetes, CI/CD, infraestructura como código.",
        "instructor_id": "instructor2@gmail.com",
        "duracion_horas": 90,
        "rating": round(random.uniform(4.4, 5.0), 1),
        "nivel": "Avanzado"
    }
]

# Evaluaciones para cada curso
EVALUACIONES_TEMPLATE = [
    {
        "tipo": "cuestionario",
        "preguntas": 10,
        "duracion_minutos": 30,
        "puntos_totales": 100
    },
    {
        "tipo": "proyecto",
        "descripcion": "Proyecto práctico final",
        "puntos_totales": 100
    }
]

# Estudiantes (de los usuarios creados)
ESTUDIANTES = [
    "estudiante1@gmail.com",
    "estudiante2@gmail.com",
    "estudiante3@gmail.com"
]


def create_cursos():
    """Crear cursos en el servicio de cursos"""
    print("\n" + "="*60)
    print("📚 CREANDO CURSOS DE INGENIERÍA EN SISTEMAS")
    print("="*60 + "\n")
    
    created = 0
    for curso in CURSOS:
        try:
            response = requests.post(f"{BASE_CURSOS}/cursos", json=curso, timeout=5)
            if response.status_code in [200, 201]:
                print(f"✅ Curso creado: {curso['titulo']} (Rating: {curso['rating']}/5.0)")
                created += 1
            else:
                print(f"⚠️  Error al crear {curso['titulo']}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error conectando al servicio de cursos: {e}")
            break
    
    print(f"\n📊 RESUMEN: {created}/{len(CURSOS)} cursos creados")
    return created


def create_evaluaciones():
    """Crear evaluaciones para cada curso"""
    print("\n" + "="*60)
    print("📝 CREANDO EVALUACIONES")
    print("="*60 + "\n")
    
    created = 0
    for curso in CURSOS:
        for idx, eval_template in enumerate(EVALUACIONES_TEMPLATE):
            evaluacion = {
                "id": f"{curso['id']}-eval-{idx+1}",
                "curso_id": curso['id'],
                "titulo": f"Evaluación {idx+1}: {curso['titulo']}",
                **eval_template
            }
            
            try:
                response = requests.post(f"{BASE_EVALUACIONES}/evaluaciones", json=evaluacion, timeout=5)
                if response.status_code in [200, 201]:
                    print(f"✅ Evaluación creada: {evaluacion['titulo']}")
                    created += 1
                else:
                    print(f"⚠️  Error: {response.status_code}")
            except Exception as e:
                print(f"❌ Error: {e}")
                break
    
    print(f"\n📊 RESUMEN: {created} evaluaciones creadas")
    return created


def create_progreso():
    """Crear progreso aleatorio para estudiantes en cursos"""
    print("\n" + "="*60)
    print("📈 CREANDO PROGRESO DE ESTUDIANTES")
    print("="*60 + "\n")
    
    created = 0
    for estudiante in ESTUDIANTES:
        print(f"\n👤 Estudiante: {estudiante}")
        
        # Cada estudiante tiene progreso en 3-6 cursos aleatorios
        num_cursos = random.randint(3, 6)
        cursos_asignados = random.sample(CURSOS, num_cursos)
        
        for curso in cursos_asignados:
            progreso = {
                "estudiante_id": estudiante,
                "curso_id": curso['id'],
                "completado_pct": random.randint(20, 100),
                "tiempo_invertido_horas": random.randint(5, curso['duracion_horas']),
                "ultima_leccion": f"leccion-{random.randint(1, 10)}",
                "fecha_inicio": "2024-09-01",
                "fecha_ultima_actividad": datetime.now().strftime("%Y-%m-%d")
            }
            
            # Crear calificaciones aleatorias si el curso está avanzado
            if progreso['completado_pct'] > 50:
                calificacion = round(random.uniform(70, 100), 1)
                progreso['calificacion'] = calificacion
                estado = "✅" if calificacion >= 70 else "❌"
                print(f"  {estado} {curso['titulo']}: {progreso['completado_pct']}% | Nota: {calificacion}/100")
            else:
                print(f"  ⏳ {curso['titulo']}: {progreso['completado_pct']}% | En progreso")
            
            try:
                response = requests.post(f"{BASE_PROGRESO}/progreso", json=progreso, timeout=5)
                if response.status_code in [200, 201]:
                    created += 1
            except Exception as e:
                print(f"❌ Error: {e}")
                break
    
    print(f"\n📊 RESUMEN: {created} registros de progreso creados")
    return created


def main():
    print("\n" + "="*60)
    print("🚀 INICIANDO POBLACIÓN DE DATOS")
    print("="*60)
    
    # Verificar que los servicios estén disponibles
    services = {
        "Cursos": BASE_CURSOS,
        "Evaluaciones": BASE_EVALUACIONES,
        "Progreso": BASE_PROGRESO
    }
    
    print("\n🔍 Verificando servicios...")
    all_ok = True
    for name, url in services.items():
        try:
            response = requests.get(f"{url}/health", timeout=2)
            if response.status_code == 200:
                print(f"  ✅ {name}: OK")
            else:
                print(f"  ⚠️  {name}: Respuesta {response.status_code}")
                all_ok = False
        except Exception as e:
            print(f"  ❌ {name}: No disponible ({e})")
            all_ok = False
    
    if not all_ok:
        print("\n⚠️  ADVERTENCIA: Algunos servicios no están disponibles.")
        print("Los datos se crearán solo en los servicios activos.\n")
    
    # Poblar datos
    cursos_created = create_cursos()
    evals_created = create_evaluaciones()
    progreso_created = create_progreso()
    
    # Resumen final
    print("\n" + "="*60)
    print(" POBLACIÓN DE DATOS COMPLETADA")
    print("="*60)
    print(f"   Cursos: {cursos_created}")
    print(f"   Evaluaciones: {evals_created}")
    print(f"   Registros de progreso: {progreso_created}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
