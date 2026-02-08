"""Blueprint de autenticación.

Maneja login/logout y verificación de sesión:
- POST /api/auth/login: Autenticar usuario
- POST /api/auth/logout: Cerrar sesión (requiere login)
- GET /api/auth/me: Obtener usuario actual (requiere login)
- GET /api/auth/check: Verificar si hay sesión activa

Seguridad:
    - Contraseñas hasheadas con Werkzeug
    - Flask-Login para manejo de sesiones
    - Cookies HttpOnly y Secure en producción
"""
from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
def login():
    """Login de usuario.
    
    Body:
        username: str (requerido)
        password: str (requerido)
        remember: bool (opcional, default False)
    
    Proceso:
        1. Validar que username y password existan
        2. Buscar usuario en BD
        3. Verificar hash de contraseña
        4. Verificar que usuario esté activo
        5. Crear sesión con Flask-Login
    
    Returns:
        200: {'success': True, 'user': {id, username, email}}
        400: Datos faltantes
        401: Credenciales inválidas
        403: Usuario inactivo
    """
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'success': False, 'error': 'Usuario y contraseña requeridos'}), 400
    
    # Buscar usuario por username
    user = User.get_by_username(data['username'])
    
    # Verificar usuario existe y contraseña es correcta
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'success': False, 'error': 'Credenciales inválidas'}), 401
    
    # Verificar usuario activo
    if not user.is_active:
        return jsonify({'success': False, 'error': 'Usuario inactivo'}), 403
    
    # Crear sesión (cookie HttpOnly)
    login_user(user, remember=data.get('remember', False))
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout de usuario.
    
    Requiere: Sesión activa (@login_required)
    
    Proceso: Destruye sesión con Flask-Login
    
    Returns:
        200: {'success': True}
    """
    logout_user()
    return jsonify({'success': True})

@bp.route('/me', methods=['GET'])
@login_required
def me():
    """Obtener usuario actual.
    
    Requiere: Sesión activa (@login_required)
    
    Returns:
        200: {id, username, email}
    """
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email
    })

@bp.route('/check', methods=['GET'])
def check():
    """Verificar si hay sesión activa.
    
    No requiere login (endpoint público).
    
    Returns:
        200: {'authenticated': bool, 'user': {...} | null}
    
    Uso: Frontend verifica sesión al cargar app.
    """
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email
            }
        })
    return jsonify({'authenticated': False})
