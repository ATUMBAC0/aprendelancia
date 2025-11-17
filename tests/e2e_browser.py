#!/usr/bin/env python3
"""
Lightweight E2E scripted test that simulates browser interaction via requests.Session.
Flow:
 - register a user via API Gateway
 - login via the frontend (/login form) so the frontend sets session cookie with access_token
 - load frontend /client, pick a course link
 - fetch lessons via frontend proxy
 - POST to frontend /api/inscripciones (AJAX proxy) with session cookie
 - poll /api/inscripcion/<id> to check estado and tutor asignado
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
    email = f"e2e_user_{ts}_{uuid4().hex[:6]}@example.com"
    password = "password123"

    print("Registering user", email)
    r = requests.post(
        f"{GATEWAY}/api/v1/auth/register",
        json={"email": email, "password": password, "role": "estudiante"},
        timeout=5
    )
    if r.status_code not in (200, 201):
        fail(f"register failed: {r.status_code} {r.text}")
    print("Registered")

    sess = requests.Session()

    # Perform frontend login
    print("Logging in via frontend /login")
    login_page = sess.get(f"{FRONTEND}/login", timeout=5)
    if login_page.status_code != 200:
        fail(f"could not load frontend login page: {login_page.status_code}")

    r = sess.post(
        f"{FRONTEND}/login",
        data={"email": email, "password": password},
        timeout=5,
        allow_redirects=True
    )

    # Validate session
    home = sess.get(f"{FRONTEND}/home", timeout=5)
    if home.status_code != 200:
        print("Warning: could not access /home after login (status)", home.status_code)

    print("Fetching frontend /client")
    r = sess.get(f"{FRONTEND}/client", timeout=5)
    if r.status_code != 200:
        fail(f"frontend /client failed: {r.status_code}")

    html = r.text

    # Buscar enlace de curso en HTML
    m = re.search(r'href="(/courses/[^\"]+)"', html)
    if not m:
        fail("could not find course link in frontend HTML")

    course_path = m.group(1)
    course_id = course_path.split('/')[-1]
    print("Using course", course_id)

    print("Fetching lessons via frontend proxy")
    r = sess.get(f"{FRONTEND}/api/cursos/{course_id}/lecciones", timeout=5)
    if r.status_code != 200:
        fail(f"lesson fetch failed: {r.status_code} {r.text}")

    data = r.json()
    lessons = data.get('lecciones') if isinstance(data, dict) else data

    if not lessons:
        fail("lecciones vacías")

    first_lesson = lessons[0]
    lesson_id = first_lesson.get('id')
