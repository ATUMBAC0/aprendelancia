# /frontend/app.py - Plataforma de Cursos Online

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import os
import requests
from typing import Optional
import json
import uuid
import threading
from datetime import datetime

app = Flask(__name__)

# Obtén la URL del API Gateway desde las variables de entorno.
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000")
app.secret_key = os.getenv("FLASK_SECRET", "dev-secret-change-me")


# --- Mock Store Fallback ---
class MockStore:
    def __init__(self, path=None):
        base = os.path.dirname(__file__)
        self.path = path or os.path.join(base, 'mock_data.json')
        self.lock = threading.Lock()
        self._load_or_init()

    def _load_or_init(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    self.data = json.load(f)
            except Exception:
                self.data = self._default()
                self._save()
        else:
            self.data = self._default()
            self._save()

    def _default(self):
        return {
            "cursos": [
                {"id": "curso1", "titulo": "Python Básico", "descripcion": "Aprende Python desde cero", "instructor_id": "inst1", "duracion_horas": 40, "rating": 4.8},
                {"id": "curso2", "titulo": "Web Development", "descripcion": "Desarrollo web con Flask", "instructor_id": "inst2", "duracion_horas": 60, "rating": 4.6},
            ],
            "modulos": {
                "curso1": [
                    {"id": "mod1", "curso_id": "curso1", "titulo": "Fundamentos", "descripcion": "Variables, tipos de datos", "orden": 1},
                    {"id": "mod2", "curso_id": "curso1", "titulo": "Funciones", "descripcion": "Definición y uso de funciones", "orden": 2},
                ]
            },
            "lecciones": {
                "mod1": [
                    {"id": "lec1", "modulo_id": "mod1", "titulo": "Variables y Tipos", "contenido": "https://example.com/video1", "duracion_minutos": 30, "orden": 1},
                    {"id": "lec2", "modulo_id": "mod1", "titulo": "Operadores", "contenido": "https://example.com/video2", "duracion_minutos": 25, "orden": 2},
                ]
            },
            "progreso": {}
        }

    def _save(self):
        tmp = self.path + '.tmp'
        with open(tmp, 'w') as f:
            json.dump(self.data, f, default=str)
        os.replace(tmp, self.path)

    def list_cursos(self):
        return list(self.data.get('cursos', []))

    def get_curso(self, curso_id):
        for c in self.data.get('cursos', []):
            if c.get('id') == curso_id:
                return c
        return None

    def get_modulos(self, curso_id):
        return self.data.get('modulos', {}).get(curso_id, [])

    def get_lecciones(self, modulo_id):
        return self.data.get('lecciones', {}).get(modulo_id, [])


mock_store = MockStore()


def _call_service(method, service, path, **kwargs):
    """Helper to call services via gateway with fallback to mock"""
    headers = kwargs.get('headers', {})
    if 'access_token' in session:
        headers['Authorization'] = f"Bearer {session['access_token']}"
    kwargs['headers'] = headers
    
    try:
        url = f"{API_GATEWAY_URL}/api/v1/{service}/{path}"
        print(f"[DEBUG] Calling {method} {url}")  # Debug
        if method == 'GET':
            r = requests.get(url, **kwargs, timeout=3)
        elif method == 'POST':
            r = requests.post(url, **kwargs, timeout=3)
        else:
            return None
        
        print(f"[DEBUG] Response status: {r.status_code}")  # Debug
        if r.status_code in [200, 201]:
            result = r.json()
            print(f"[DEBUG] Response data: {str(result)[:200]}")  # Debug primeros 200 chars
            return result
        else:
            print(f"[DEBUG] Error response: {r.text[:200]}")  # Debug
            # Intentar extraer el mensaje de error del servidor
            try:
                error_data = r.json()
                error_msg = error_data.get('detail', 'Error desconocido')
                return {'error': error_msg}
            except:
                return {'error': f'Error {r.status_code}'}
    except Exception as e:
        print(f"[DEBUG] Exception calling service: {e}")  # Debug
        return {'error': str(e)}
    return None


@app.route('/')
@app.route('/index')
def index():
    """Página de inicio"""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'estudiante')
        
        # Intentar login via API
        resp = _call_service('POST', 'auth', 'login', json={'email': email, 'password': password, 'role': role})
        
        if resp and 'access_token' in resp:
            session['access_token'] = resp['access_token']
            
            # Obtener info completa del usuario desde /me
            user_info = _call_service('GET', 'auth', 'me')
            # /me responde {"user": {...}}
            if user_info and isinstance(user_info, dict) and user_info.get('user'):
                u = user_info.get('user', {})
                session['user'] = {
                    'id': u.get('id') or u.get('email'),
                    'email': u.get('email'),
                    'role': u.get('role', 'estudiante'),
                    'nombre': u.get('nombre', ''),
                }
            else:
                session['user'] = {'email': email, 'id': email, 'role': role}
            
            flash('Login exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'estudiante')
        nombre = request.form.get('nombre', '')
        apellido = request.form.get('apellido', '')
        
        resp = _call_service('POST', 'auth', 'register', json={
            'email': email,
            'password': password,
            'role': role,
            'nombre': nombre,
            'apellido': apellido
        })
        
        if resp and 'error' not in resp:
            flash('Usuario registrado exitosamente. Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))
        else:
            error_msg = resp.get('error', 'Error al registrar usuario') if resp else 'Error al conectar con el servidor'
            flash(error_msg, 'error')
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    """Panel principal - redirige según rol"""
    if 'user' not in session:
        flash('Por favor inicia sesión', 'warning')
        return redirect(url_for('login'))
    
    user = session.get('user', {})
    role = user.get('role', 'estudiante')
    
    # Redirigir según rol
    if role == 'instructor':
        return dashboard_instructor()
    else:
        return dashboard_estudiante()


def dashboard_instructor():
    """Dashboard para instructores"""
    user = session.get('user', {})
    instructor_email = user.get('email')
    
    # Obtener todos los cursos
    resp_cursos = _call_service('GET', 'cursos', '')
    todos_cursos = resp_cursos.get('cursos', []) if resp_cursos else []
    
    # Filtrar cursos del instructor (por instructor_id)
    mis_cursos = [c for c in todos_cursos if c.get('instructor_id') == instructor_email or c.get('instructor_id') == 'inst1']
    
    stats = {
        'num_cursos': len(mis_cursos),
        'total_estudiantes': len(mis_cursos) * 12,  # Mock: ~12 estudiantes por curso
        'evaluaciones_pendientes': len(mis_cursos) * 3  # Mock: ~3 evaluaciones pendientes por curso
    }
    
    # Enriquecer cursos para el template
    cursos_enriquecidos = []
    for c in mis_cursos:
        cursos_enriquecidos.append({
            'curso_id': c.get('id'),
            'curso_titulo': c.get('titulo'),
            'curso_descripcion': c.get('descripcion'),
            'duracion_horas': c.get('duracion_horas'),
            'rating': c.get('rating')
        })
    
    return render_template('dashboard_instructor.html', cursos=cursos_enriquecidos, stats=stats, user=user)


def dashboard_estudiante():
    """Dashboard para estudiantes"""
    user = session.get('user', {})
    estudiante_id = user.get('email') or user.get('id')
    
    print(f"[DEBUG DASHBOARD] User: {user}")  # Debug
    print(f"[DEBUG DASHBOARD] Estudiante ID: {estudiante_id}")  # Debug
    
    # Inicializar stats
    stats = {
        'num_cursos': 0,
        'promedio_progreso': 0,
        'evaluaciones_pendientes': 0
    }
    cursos_progreso = []
    
    if estudiante_id:
        # Asignar cursos aleatorios si no tiene ninguno (POST automático)
        resp_progreso = _call_service('GET', 'progreso', f'estudiantes/{estudiante_id}/cursos')
        print(f"[DEBUG DASHBOARD] Progreso response: {resp_progreso}")  # Debug
        
        # Si no hay cursos, hacer POST para asignar aleatorios
        if not resp_progreso or not resp_progreso.get('cursos'):
            print(f"[DEBUG DASHBOARD] No hay cursos, asignando...")  # Debug
            _call_service('POST', 'progreso', f'estudiantes/{estudiante_id}/asignar-cursos', json={})
            resp_progreso = _call_service('GET', 'progreso', f'estudiantes/{estudiante_id}/cursos')
        
        progreso_data = resp_progreso if resp_progreso else {'cursos': []}
        cursos_progreso = progreso_data.get('cursos', [])
        num_cursos = len(cursos_progreso)
        
        print(f"[DEBUG DASHBOARD] Num cursos: {num_cursos}")  # Debug
        
        # Calcular promedio
        if num_cursos > 0:
            total_progreso = sum(c.get('completado_pct', 0) for c in cursos_progreso)
            promedio_progreso = round(total_progreso / num_cursos)
        else:
            promedio_progreso = 0
        
        # Evaluaciones pendientes
        evaluaciones_pendientes = sum(1 for c in cursos_progreso if c.get('completado_pct', 0) > 50 and c.get('calificacion') is None)
        
        # Enriquecer con info de cursos
        cursos_info = {}
        resp_cursos = _call_service('GET', 'cursos', '')
        if resp_cursos:
            for c in resp_cursos.get('cursos', []):
                cursos_info[c.get('id')] = c
        
        for item in cursos_progreso:
            cid = item.get('curso_id')
            if cid in cursos_info:
                item['curso_titulo'] = cursos_info[cid].get('titulo', 'Sin título')
                item['curso_descripcion'] = cursos_info[cid].get('descripcion', '')

        stats = {
            'num_cursos': num_cursos,
            'promedio_progreso': promedio_progreso,
            'evaluaciones_pendientes': evaluaciones_pendientes
        }
    
    return render_template('dashboard.html', cursos=cursos_progreso, stats=stats, user=user)


@app.route('/cursos')
def cursos_list():
    """Lista de cursos disponibles"""
    resp = _call_service('GET', 'cursos', '')
    cursos = resp.get('cursos', []) if resp else mock_store.list_cursos()
    return render_template('cursos.html', cursos=cursos)


@app.route('/cursos/<curso_id>')
def curso_detail(curso_id):
    """Detalle de un curso"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    resp = _call_service('GET', 'cursos', curso_id)
    curso = resp if resp else mock_store.get_curso(curso_id)
    
    if not curso:
        flash('Curso no encontrado', 'error')
        return redirect(url_for('cursos_list'))
    
    # Obtener módulos
    resp_modulos = _call_service('GET', 'cursos', f"{curso_id}/modulos")
    modulos = resp_modulos.get('modulos', []) if resp_modulos else mock_store.get_modulos(curso_id)
    
    return render_template('cursos.html', curso=curso, modulos=modulos)


@app.route('/cursos/<curso_id>/modulos/<modulo_id>')
def modulo_detail(curso_id, modulo_id):
    """Detalle de un módulo"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Obtener lecciones
    resp = _call_service('GET', 'cursos', f"modulos/{modulo_id}/lecciones")
    lecciones = resp.get('lecciones', []) if resp else mock_store.get_lecciones(modulo_id)
    
    return render_template('modulo_detalle.html', curso_id=curso_id, modulo_id=modulo_id, lecciones=lecciones)


@app.route('/progreso')
def progreso():
    """Ver progreso del estudiante"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    estudiante_id = session.get('user', {}).get('email')
    resp = _call_service('GET', 'progreso', f"estudiantes/{estudiante_id}/cursos")
    progreso_data = resp if resp else {"cursos": []}
    
    # Obtener info de cursos para mostrar títulos
    cursos_info = {}
    resp_cursos = _call_service('GET', 'cursos', '')
    if resp_cursos:
        cursos_list = resp_cursos.get('cursos', [])
        for c in cursos_list:
            cursos_info[c.get('id')] = c
    
    # Enriquecer progreso con info de cursos
    for item in progreso_data.get('cursos', []):
        curso_id = item.get('curso_id')
        if curso_id in cursos_info:
            item['curso_titulo'] = cursos_info[curso_id].get('titulo', 'Sin título')
            item['curso_descripcion'] = cursos_info[curso_id].get('descripcion', '')
    
    return render_template('progreso.html', progreso=progreso_data)


@app.route('/evaluaciones/<cuestionario_id>')
def evaluacion(cuestionario_id):
    """Realizar una evaluación"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    resp = _call_service('GET', 'evaluaciones', cuestionario_id)
    cuestionario = resp if resp else None
    
    if not cuestionario:
        flash('Evaluación no encontrada', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('evaluacion.html', cuestionario=cuestionario)


@app.route('/api/evaluaciones/<cuestionario_id>/responder', methods=['POST'])
def responder_evaluacion(cuestionario_id):
    """API endpoint para enviar respuestas"""
    if 'user' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    
    data = request.get_json()
    estudiante_id = session.get('user', {}).get('id')
    
    resp = _call_service('POST', 'evaluaciones', f"{cuestionario_id}/responder?estudiante_id={estudiante_id}", json=data)
    
    if resp:
        return jsonify(resp)
    else:
        return jsonify({'error': 'Error procesando evaluación'}), 500


@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
