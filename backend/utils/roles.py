"""Sistema de roles y permisos"""
from functools import wraps
from flask import jsonify
from flask_login import current_user

# Roles disponibles
class Roles:
    ADMIN = 'admin'
    USER = 'user'
    VIEWER = 'viewer'

# Permisos por rol
PERMISSIONS = {
    Roles.ADMIN: ['read', 'write', 'delete', 'admin'],
    Roles.USER: ['read', 'write'],
    Roles.VIEWER: ['read']
}

def require_role(*roles):
    """Decorator para requerir roles específicos"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': 'No autorizado'}), 401
            
            user_role = getattr(current_user, 'role', Roles.ADMIN)
            
            if user_role not in roles:
                return jsonify({'error': 'Acceso denegado'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_permission(permission):
    """Decorator para requerir permiso específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': 'No autorizado'}), 401
            
            user_role = getattr(current_user, 'role', Roles.ADMIN)
            user_permissions = PERMISSIONS.get(user_role, [])
            
            if permission not in user_permissions:
                return jsonify({'error': 'Permiso denegado'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
