import pytest
import json

def test_flujo_completo_licitacion(client, sample_cliente):
    """Test: Flujo completo de crear licitación con productos"""
    # 1. Crear licitación
    lic_response = client.post('/api/licitaciones', json={
        'numero': 'TEST-001',
        'fecha': '2025-01-15',
        'cliente_id': sample_cliente,
        'productos': [{
            'monodroga': 'Ibuprofeno',
            'marca': 'Genérico',
            'presentacion': '400mg x 50',
            'cantidad': 500,
            'precio_ofertado': 15.00,
            'resultado': 'Adjudicado'
        }]
    })
    assert lic_response.status_code == 201
    lic_id = lic_response.json['id']
    
    # 2. Obtener licitación creada
    get_response = client.get(f'/api/licitaciones/{lic_id}')
    assert get_response.status_code == 200
    assert get_response.json['numero_licitacion'] == 'TEST-001'
    
    # 3. Obtener productos
    prod_response = client.get(f'/api/productos/{lic_id}')
    assert prod_response.status_code == 200
    assert len(prod_response.json) == 1
    
    # 4. Verificar estadísticas actualizadas
    stats_response = client.get('/api/estadisticas')
    assert stats_response.status_code == 200
    assert stats_response.json['total_licitaciones'] >= 1

def test_flujo_cliente_licitacion(client):
    """Test: Crear cliente y usarlo en licitación"""
    # 1. Crear cliente
    cliente_response = client.post('/api/clientes', json={
        'nombre': 'Hospital Integración',
        'razon_social': 'Hospital Integración SA',
        'organismo_jurisdiccion': 'Nacional'
    })
    assert cliente_response.status_code == 201
    cliente_id = cliente_response.json['id']
    
    # 2. Crear licitación con ese cliente
    lic_response = client.post('/api/licitaciones', json={
        'numero': 'INT-001',
        'fecha': '2025-01-20',
        'cliente_id': cliente_id,
        'productos': [{
            'monodroga': 'Amoxicilina',
            'marca': 'Test',
            'presentacion': '500mg',
            'cantidad': 100,
            'precio_ofertado': 20.00,
            'resultado': 'Parcial'
        }]
    })
    assert lic_response.status_code == 201
