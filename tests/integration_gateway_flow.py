
import requests
import time
import uuid

GATEWAY = "http://localhost:8000"


def test_gateway_integration_flow():
    ts = int(time.time())
    email = f"gw_{ts}_{uuid.uuid4().hex[:6]}@example.com"
    password = "Password123!"

    # 1) Register (via gateway)
    r = requests.post(f"{GATEWAY}/api/v1/auth/register", json={"email": email, "password": password, "role": "estudiante", "nombre": "GW", "apellido": "Test"}, timeout=5)
    # 409 means already exists (ok), accept 200/201/409
    assert r.status_code in (200, 201, 409), f"register failed: {r.status_code} {r.text}"

    # 2) Login (via gateway)
    r = requests.post(f"{GATEWAY}/api/v1/auth/login", json={"email": email, "password": password}, timeout=5)
    assert r.status_code == 200, f"login failed via gateway: {r.status_code} {r.text}"
    token = r.json().get("access_token")
    assert token, "no token returned from gateway login"
    headers = {"Authorization": f"Bearer {token}"}

    # 3) List cursos (via gateway)
    r = requests.get(f"{GATEWAY}/api/v1/cursos", timeout=5)
    assert r.status_code == 200, f"list cursos via gateway failed: {r.status_code} {r.text}"
    data = r.json()
    cursos = data.get("cursos") or []
    assert cursos, "no cursos returned via gateway"
    curso_id = cursos[0].get("id")

    # 4) Create a cuestionario (via gateway) - requires auth
    cuestionario_payload = {
        "titulo": "GW Cuestionario",
        "descripcion": "Prueba via gateway",
        "curso_id": curso_id,
        "preguntas": [
            {
                "pregunta_texto": "¿1+1?",
                "opciones": [
                    {"id": "o1", "texto": "1", "es_correcta": False},
                    {"id": "o2", "texto": "2", "es_correcta": True}
                ],
                "orden": 1
            }
        ]
    }

    r = requests.post(f"{GATEWAY}/api/v1/evaluaciones", json=cuestionario_payload, headers=headers, timeout=5)
    assert r.status_code in (200, 201), f"create cuestionario via gateway failed: {r.status_code} {r.text}"
    cuest_id = r.json().get("id")
    assert cuest_id, "no cuestionario id returned"

    # 5) Fetch cuestionario via gateway
    r = requests.get(f"{GATEWAY}/api/v1/evaluaciones/{cuest_id}", timeout=5)
    assert r.status_code == 200, f"get cuestionario via gateway failed: {r.status_code} {r.text}"
    preguntas = r.json().get("preguntas") or []
    assert preguntas, "no preguntas in cuestionario"
    pregunta_id = preguntas[0].get("id")

    # 6) Responder cuestionario via gateway (authenticated)
    respuestas = [{"pregunta_id": pregunta_id, "opcion_seleccionada_id": "o2"}]
    r = requests.post(f"{GATEWAY}/api/v1/evaluaciones/{cuest_id}/responder?estudiante_id={r.json().get('curso_id')}", json=respuestas, headers=headers, timeout=5)
    # The responder endpoint should accept the request and return a calificacion
    assert r.status_code == 200, f"responder via gateway failed: {r.status_code} {r.text}"
    resultado = r.json()
    assert "calificacion" in resultado or "respuestas_correctas" in resultado, "unexpected responder response"

    # 7) Verify progreso via gateway
    # fetch current user id via /api/v1/auth/me through gateway
    r = requests.get(f"{GATEWAY}/api/v1/auth/me", headers=headers, timeout=5)
    assert r.status_code == 200, f"/me via gateway failed: {r.status_code} {r.text}"
    estudiante_id = r.json().get("user", {}).get("id")
    assert estudiante_id, "could not obtain estudiante_id"

    r = requests.get(f"{GATEWAY}/api/v1/progreso/{estudiante_id}/cursos", headers=headers, timeout=5)
    assert r.status_code == 200, f"progreso fetch via gateway failed: {r.status_code} {r.text}"

    # If we reach here, the gateway flow worked end-to-end

