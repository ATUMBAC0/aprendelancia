import requests

SERVICES = {
    'auth': 'http://localhost:8001/health',
    'cursos': 'http://localhost:8002/health',
    'evaluaciones': 'http://localhost:8003/health',
    'progreso': 'http://localhost:8004/health',
}


def test_services_health():
    for name, url in SERVICES.items():
        r = requests.get(url, timeout=3)
        assert r.status_code == 200, f"{name} unhealthy: {r.status_code}"
        data = r.json()
        assert data.get('status') == 'ok', f"{name} status not ok: {data}"
