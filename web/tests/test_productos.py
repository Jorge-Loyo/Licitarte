import pytest
import json

def test_crear_producto(client, sample_licitacion):
    """Test: Crear producto válido"""
    response = client.post('/api/productos', json={
        'licitacion_id': sample_licitacion,
        'monodroga': 'Paracetamol',
        'marca': 'Genérico',
        'presentacion': '500mg x 100',
        'cantidad': 1000,
        'precio_ofertado': 10.50,
        'resultado': 'Parcial'
    })
    assert response.status_code == 201

def test_crear_producto_sin_datos(client):
    """Test: Crear producto sin datos debe fallar"""
    response = client.post('/api/productos', json={})
    assert response.status_code == 400

def test_obtener_productos_licitacion(client, sample_licitacion):
    """Test: Obtener productos de licitación"""
    response = client.get(f'/api/productos/{sample_licitacion}')
    assert response.status_code == 200
    assert isinstance(response.json, list)
