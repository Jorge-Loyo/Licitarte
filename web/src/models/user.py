"""Modelo de usuario para autenticación"""
from flask_login import UserMixin
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from shared.database.db_manager import DatabaseManager
from shared.database.connection_pool import USE_POSTGRES

db = DatabaseManager()

class User(UserMixin):
    def __init__(self, id, username, email, is_active=True):
        self.id = id
        self.username = username
        self.email = email
        self._is_active = is_active
        self.password_hash = None
    
    @property
    def is_active(self):
        return self._is_active
    
    @staticmethod
    def get(user_id):
        """Obtener usuario por ID"""
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT id, username, email, activo FROM usuarios WHERE id = %s", (user_id,))
            else:
                cursor.execute("SELECT id, username, email, activo FROM usuarios WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return User(row[0], row[1], row[2], row[3])
        return None
    
    @staticmethod
    def get_by_username(username):
        """Obtener usuario por username"""
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT id, username, email, activo, password_hash FROM usuarios WHERE username = %s", (username,))
            else:
                cursor.execute("SELECT id, username, email, activo, password_hash FROM usuarios WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                user = User(row[0], row[1], row[2], row[3])
                user.password_hash = row[4]
                return user
        return None
