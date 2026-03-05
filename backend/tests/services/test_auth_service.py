"""Tests para AuthService"""
import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from backend.api.services.auth_service import AuthService
from backend.api.models.user import User

class TestAuthService(unittest.TestCase):
    
    @patch('backend.api.services.auth_service.User.get_by_username')
    @patch('backend.api.services.auth_service.check_password_hash')
    def test_autenticar_credenciales_validas(self, mock_check_hash, mock_get_user):
        """Test autenticación con credenciales válidas"""
        # Mock usuario
        mock_user = Mock(spec=User)
        mock_user.password_hash = 'hashed_password'
        mock_user.is_active = True
        mock_get_user.return_value = mock_user
        mock_check_hash.return_value = True
        
        # Ejecutar
        user = AuthService.autenticar('testuser', 'password123')
        
        # Verificar
        self.assertIsNotNone(user)
        self.assertEqual(user, mock_user)
        mock_get_user.assert_called_once_with('testuser')
        mock_check_hash.assert_called_once_with('hashed_password', 'password123')
    
    @patch('backend.api.services.auth_service.User.get_by_username')
    def test_autenticar_usuario_no_existe(self, mock_get_user):
        """Test autenticación con usuario inexistente"""
        mock_get_user.return_value = None
        
        user = AuthService.autenticar('noexiste', 'password')
        
        self.assertIsNone(user)
    
    @patch('backend.api.services.auth_service.User.get_by_username')
    @patch('backend.api.services.auth_service.check_password_hash')
    def test_autenticar_password_incorrecta(self, mock_check_hash, mock_get_user):
        """Test autenticación con contraseña incorrecta"""
        mock_user = Mock(spec=User)
        mock_user.password_hash = 'hashed_password'
        mock_get_user.return_value = mock_user
        mock_check_hash.return_value = False
        
        user = AuthService.autenticar('testuser', 'wrongpassword')
        
        self.assertIsNone(user)
    
    @patch('backend.api.services.auth_service.User.get_by_username')
    @patch('backend.api.services.auth_service.check_password_hash')
    def test_autenticar_usuario_inactivo(self, mock_check_hash, mock_get_user):
        """Test autenticación con usuario inactivo"""
        mock_user = Mock(spec=User)
        mock_user.password_hash = 'hashed_password'
        mock_user.is_active = False
        mock_get_user.return_value = mock_user
        mock_check_hash.return_value = True
        
        user = AuthService.autenticar('testuser', 'password123')
        
        self.assertIsNone(user)
    
    def test_usuario_to_dict(self):
        """Test conversión de usuario a diccionario"""
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.username = 'testuser'
        mock_user.email = 'test@example.com'
        
        result = AuthService.usuario_to_dict(mock_user)
        
        self.assertEqual(result['id'], 1)
        self.assertEqual(result['username'], 'testuser')
        self.assertEqual(result['email'], 'test@example.com')

if __name__ == '__main__':
    unittest.main()
