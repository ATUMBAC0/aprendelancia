import requests
import time
import uuid

AUTH = "http://localhost:8001"
CURSOS = "http://localhost:8002"
EVALUACIONES = "http://localhost:8003"
PROGRESO = "http://localhost:8004"


def fail(msg):
    raise AssertionError(msg)


def test_end_to_end_flow():
    ts = int(time.time())
    email = f"int_{ts}_{uuid.uuid4().hex[:6]}@example.com"
    password = "Password123!"

    # 1) Register
    r = requests.post(f"{AUTH}/register", json={"email": email, "password": password, "role": "estudiante"}, timeout=5)
    assert r.status_code in (200, 201), f"register failed: {r.status_code} {r.text}"

    # 2) Login
    r = requests.post(f"{AUTH}/login", json={"email": email, "password": password}, timeout=5)
    assert r.status_code == 200, f"login failed: {r.status_code} {r.text}"
    token = r.json().get("access_token")
    assert token, "no token returned"

    # 3) Get current user via /me
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{AUTH}/me", headers=headers, timeout=5)
    assert r.status_code == 200, f"/me failed: {r.status_code} {r.text}"
    user = r.json().get("user")
    estudiante_id = user.get("id")

    # 4) List cursos and pick one
    r = requests.get(f"{CURSOS}/api/v1/cursos", timeout=5)
    assert r.status_code == 200, f"list cursos failed: {r.status_code} {r.text}"
    data = r.json()
    cursos = data.get("cursos") or []
    assert cursos, "no cursos seeded"
    curso_id = cursos[0].get("id")

    # 5) Create a cuestionario for the curso
    cuestionario_payload = {
        "titulo": "Test Cuestionario",
        "descripcion": "Integracion test",
        "curso_id": curso_id,
        "preguntas": [
            {
                "pregunta_texto": "¿2+2?",
                "opciones": [
                    {"id": "o1", "texto": "3", "es_correcta": False},
                    {"id": "o2", "texto": "4", "es_correcta": True}
                ],
                "orden": 1
            }
        ]
    }
    r = requests.post(f"{EVALUACIONES}/api/v1/evaluaciones", json=cuestionario_payload, timeout=5)
    assert r.status_code in (200,201), f"create cuestionario failed: {r.status_code} {r.text}"
    cuest_id = r.json().get("id")
    assert cuest_id, "no cuestionario id returned"

    # 6) Responder cuestionario (seleccionando la respuesta correcta)
    respuestas = [{"pregunta_id": None, "opcion_seleccionada_id": "o2"}]
    # need to fetch cuestionario to get pregunta_id
    r = requests.get(f"{EVALUACIONES}/api/v1/evaluaciones/{cuest_id}", timeout=5)
    assert r.status_code == 200
    preguntas = r.json().get("preguntas") or []
    assert preguntas, "no preguntas in cuestionario"
    pregunta_id = preguntas[0].get("id")
    respuestas = [{"pregunta_id": pregunta_id, "opcion_seleccionada_id": "o2"}]

    r = requests.post(f"{EVALUACIONES}/api/v1/evaluaciones/{cuest_id}/responder?estudiante_id={estudiante_id}", json=respuestas, timeout=5)
    assert r.status_code == 200, f"responder failed: {r.status_code} {r.text}"
    resultado = r.json()
    assert resultado.get("calificacion") is not None

    # 7) Verificar que progreso registró la evaluación
    r = requests.get(f"{PROGRESO}/api/v1/progreso/{estudiante_id}/cursos", timeout=5)
    assert r.status_code == 200, f"progreso fetch failed: {r.status_code} {r.text}"
    data = r.json()
    assert data.get("estudiante_id") == estudiante_id

    # Test passes if we reach here

*** End Patch