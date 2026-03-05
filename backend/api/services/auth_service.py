"""Servicio de autenticación"""
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from werkzeug.security import check_password_hash
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from backend.api.models.user import User

class AuthService:
    
    @staticmethod
    def autenticar(username: str, password: str) -> Optional[User]:
        """Autentica un usuario por username y password"""
        user = User.get_by_username(username)
        
        if not user or not user.password_hash:
            return None
        
        if not check_password_hash(user.password_hash, password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    @staticmethod
    def usuario_to_dict(user: User) -> Dict[str, Any]:
        """Convierte usuario a diccionario"""
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
