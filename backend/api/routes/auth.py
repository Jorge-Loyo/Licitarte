"""Blueprint de autenticación - Refactorizado"""
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from backend.api.services.auth_service import AuthService
from backend.api.schemas.dtos import ResponseDTO
from backend.constants import ErrorMessages

bp = Blueprint('auth', __name__, url_prefix='/api/auth')
service = AuthService()

@bp.route('/login', methods=['POST'])
def login():
    """Login de usuario"""
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify(ResponseDTO.error('Usuario y contraseña requeridos')), 400
    
    user = service.autenticar(data['username'], data['password'])
    
    if not user:
        return jsonify(ResponseDTO.error('Credenciales inválidas')), 401
    
    login_user(user, remember=data.get('remember', False))
    return jsonify(ResponseDTO.success({'user': service.usuario_to_dict(user)})), 200

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout de usuario"""
    logout_user()
    return jsonify(ResponseDTO.success()), 200

@bp.route('/me', methods=['GET'])
@login_required
def me():
    """Obtener usuario actual"""
    return jsonify(service.usuario_to_dict(current_user)), 200

@bp.route('/check', methods=['GET'])
@login_required
def check():
    """Verificar si hay sesión activa"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': service.usuario_to_dict(current_user)
        }), 200
    return jsonify({'authenticated': False}), 200
