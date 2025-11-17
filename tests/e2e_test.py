#!/usr/bin/env python3
"""E2E smoke test (minimal) for cursos-online.

Flow:
 - register a test user via API Gateway
 - login and get access_token
 - fetch frontend /client HTML and ensure courses are listed
 - visit a course detail page on the frontend
 - fetch lessons via gateway and create an inscripción using the gateway with the token
 - fetch the inscripción and assert a tutor was assigned

Requirements: Python 3, requests
"""
import requests
import re
import sys
import time
from uuid import uuid4

FRONTEND = "http://localhost:5000"
GATEWAY = "http://localhost:8000"


def fail(msg, code=1):
    print("ERROR:", msg)
    sys.exit(code)


def main():
    ts = int(time.time())
    email = f"e2e_{ts}_{uuid4().hex[:6]}@example.com"
    password = "password123"

    print("1) Registering user", email)
    r = requests.post(
        f"{GATEWAY}/api/v1/auth/register",
        json={"email": email, "password": password, "role": "estudiante"},
        timeout=5
    )
    if r.status_code not in (200, 201):
        fail(f"register failed: {r.status_code} {r.text}")
    print("  registered")

    print("2) Logging in")
    r = requests.post(
        f"{GATEWAY}/api/v1/auth/login",
        json={"email": email, "password": password},
        timeout=5
    )
    if r.status_code != 200:
        fail(f"login failed: {r.status_code} {r.text}")

    token = r.json().get("access_token")
    if not token:
        fail("no access_token returned")
    headers = {"Authorization": f"Bearer {token}"}
    print("  got token")

    print("3) Load frontend /client and check course list")
    r = requests.get(f"{FRONTEND}/client", timeout=5)
    if r.status_code != 200:
        fail(f"frontend /client failed: {r.status_code}")

    html = r.text

    # simple check for known courses (change names to your real ones)
    if not re.search(r"Python Básico|Curso Django|Machine Learning", html, re.I):
        fail("course names not found in frontend HTML")
    print("  frontend shows courses")

    # extract first course link
    m = re.search(r'href="(/courses/[^"]+)"', html)
    if not m:
        fail("could not find course link in frontend HTML")

    course_path = m.group(1)
    course_id = course_path.split('/')[-1]
    print(f"  using course: {course_id}")

    print("4) Fetch course detail page (frontend)")
    r = requests.get(f"{FRONTEND}{course_path}", timeout=5)
    if r.status_code != 200:
        fail(f"course detail page failed: {r.status_code}")
    print("  ok")

    print("5) Fetch lessons via gateway")
    r = requests.get(f"{GATEWAY}/api/v1/cursos/{course_id}/lecciones", timeout=5)
    if r.status_code != 200:
        fail(f"lessons fetch failed: {r.status_code} {r.text}")

    data = r.json()

    # Support formats {"lecciones": [...]} or raw list
    if isinstance(data, dict):
        lessons = data.get("lecciones") or data.get("items") or []
    elif isinstance(data, list):
        lessons = data
    else:
        lessons = []

    if not lessons:
        fail("lessons list is empty")

    lesson = lessons[0]
    lesson_id = lesson.get('id') if isinstance(lesson, dict) else lesson
    print(f"  course has {len(lessons)} lessons, picking {lesson_id}")

    print("6) Create inscripción via gateway (authenticated)")
    payload = {
        "curso_id": course_id,
        "estudiante_email": email,
        "items": [{"leccion_id": lesson_id}],
    }

    # Fixed the duplicated path bug & adapted to cursos
    r = requests.post(
        f"{GATEWAY}/api/v1/inscripciones",
        json=payload,
        headers=headers,
        timeout=5
    )
    if r.status_code not in (200, 201):
        fail(f"create inscripción failed: {r.status_code} {r.text}")

    inscripcion = r.json()
    inscripcion_id = inscripcion.get("id")
    if not inscripcion_id:
        fail("no inscripción id returned")

    print(f"  created inscripción {inscripcion_id}")

    print("7) Fetch the inscripción and verify tutor assigned")
    r = requests.get(
        f"{GATEWAY}/api/v1/inscripciones/{inscripcion_id}",
        headers=headers,
        timeout=5
    )
    if r.status_code != 200:
        fail(f"get inscripción failed: {r.status_code} {r.text}")

    data = r.json()
    if not data.get("tutor"):
        fail("no tutor assigned to inscripción")

    print("  tutor assigned:", data.get("tutor"))
    print("E2E test passed ✅")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        fail(str(e))
