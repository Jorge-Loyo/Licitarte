"""Tests para LicitacionService"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from backend.api.services.licitacion_service import LicitacionService
from backend.validators import LicitacionCreate, ProductoCreate

class TestLicitacionService(unittest.TestCase):
    
    def setUp(self):
        """Setup antes de cada test"""
        self.service = LicitacionService()
        self.service.db = Mock()
    
    def test_obtener_todas_retorna_lista(self):
        """Test que obtener_todas retorna lista de licitaciones"""
        # Mock de datos
        mock_licitaciones = [
            (1, 'L-001', '2024-01-01', None, None, None, 'Cliente 1', 'Tipo 1', None)
        ]
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = mock_licitaciones
        mock_cursor.fetchone.return_value = (1, 1, 1000.0)
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        
        self.service.db.get_connection.return_value = mock_conn
        
        # Ejecutar
        resultado = self.service.obtener_todas()
        
        # Verificar
        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]['numero'], 'L-001')
    
    def test_crear_licitacion_retorna_id(self):
        """Test que crear retorna ID de licitación"""
        # Mock
        self.service.db.crear_licitacion.return_value = 123
        self.service._crear_productos = Mock()
        
        # Datos de prueba
        data = LicitacionCreate(
            numero='L-001',
            fecha='2024-01-01',
            productos=[]
        )
        
        # Ejecutar
        licitacion_id = self.service.crear(data)
        
        # Verificar
        self.assertEqual(licitacion_id, 123)
        self.service.db.crear_licitacion.assert_called_once()
    
    def test_obtener_por_id_no_encontrado(self):
        """Test que obtener_por_id retorna None si no existe"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        
        self.service.db.get_connection.return_value = mock_conn
        
        resultado = self.service.obtener_por_id(999)
        
        self.assertIsNone(resultado)

if __name__ == '__main__':
    unittest.main()
