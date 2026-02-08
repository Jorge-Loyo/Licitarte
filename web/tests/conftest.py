import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app
from database.db_manager import DatabaseManager

@pytest.fixture
def app():
    """Fixture de la aplicación Flask"""
    flask_app.config['TESTING'] = True
    yield flask_app

@pytest.fixture
def client(app):
    """Cliente de prueba"""
    return app.test_client()

@pytest.fixture
def db():
    """Base de datos de prueba en memoria"""
    db = DatabaseManager(':memory:')
    yield db

@pytest.fixture
def sample_cliente(db):
    """Cliente de ejemplo para tests"""
    cliente_id = db.crear_cliente(
        nombre='Hospital Test',
        razon_social='Hospital Test SA',
        cuit='20-12345678-9',
        direccion='Calle Falsa 123',
        telefono='1234-5678',
        email='test@hospital.com',
        organismo_jurisdiccion='Provincial'
    )
    return cliente_id
