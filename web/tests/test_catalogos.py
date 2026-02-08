import pytest
import json

def test_obtener_oferentes(client):
    """Test: Obtener lista de oferentes"""
    response = client.get('/api/oferentes')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_crear_oferente(client):
    """Test: Crear oferente válido"""
    response = client.post('/api/oferentes', json={'nombre': 'Lab Test'})
    assert response.status_code == 201

def test_obtener_marcas(client):
    """Test: Obtener lista de marcas"""
    response = client.get('/api/marcas')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_crear_marca(client):
    """Test: Crear marca válida"""
    response = client.post('/api/marcas', json={'nombre': 'Marca Test'})
    assert response.status_code == 201

def test_obtener_tipos_licitacion(client):
    """Test: Obtener tipos de licitación"""
    response = client.get('/api/tipos-licitacion')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_obtener_catalogo(client):
    """Test: Obtener catálogo de productos"""
    response = client.get('/api/catalogo')
    assert response.status_code == 200
    assert isinstance(response.json, list)
