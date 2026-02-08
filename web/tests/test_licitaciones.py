import pytest
import json

def test_obtener_licitaciones(client):
    """Test: Obtener lista de licitaciones"""
    response = client.get('/api/licitaciones')
    assert response.status_code == 200
    result = json.loads(response.data)
    assert isinstance(result, list)

def test_crear_licitacion_sin_datos(client):
    """Test: Crear licitación sin datos debe fallar"""
    response = client.post(
        '/api/licitaciones',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400

def test_obtener_estadisticas(client):
    """Test: Obtener estadísticas del dashboard"""
    response = client.get('/api/estadisticas')
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'total_licitaciones' in result
    assert 'unidades_cotizadas' in result

def test_obtener_clientes(client):
    """Test: Obtener lista de clientes"""
    response = client.get('/api/clientes')
    assert response.status_code == 200
    result = json.loads(response.data)
    assert isinstance(result, list)

def test_crear_cliente_sin_nombre(client):
    """Test: Crear cliente sin nombre debe fallar"""
    response = client.post(
        '/api/clientes',
        data=json.dumps({'nombre': ''}),
        content_type='application/json'
    )
    assert response.status_code == 400
