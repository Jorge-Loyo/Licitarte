"""Tests para endpoints de licitaciones"""
import pytest
import json

def test_get_licitaciones(client):
    """Test: Obtener lista de licitaciones"""
    response = client.get('/api/licitaciones')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)

def test_crear_licitacion_sin_numero(client):
    """Test: Crear licitación sin número debe fallar"""
    data = {'numero': '', 'fecha': '2025-01-15', 'productos': []}
    response = client.post('/api/licitaciones', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400

def test_obtener_estadisticas(client):
    """Test: Obtener estadísticas"""
    response = client.get('/api/estadisticas')
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'total_licitaciones' in result
