import pytest
import json

def test_e2e_usuario_completo(client):
    """Test E2E: Usuario crea licitación completa desde cero"""
    
    # 1. Login
    login = client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123',
        'remember': False
    })
    assert login.status_code == 200
    
    # 2. Crear cliente
    cliente = client.post('/api/clientes', json={
        'nombre': 'Hospital E2E',
        'razon_social': 'Hospital E2E SA',
        'organismo_jurisdiccion': 'Provincial'
    })
    assert cliente.status_code == 201
    cliente_id = cliente.json['id']
    
    # 3. Crear oferente
    oferente = client.post('/api/oferentes', json={'nombre': 'Lab E2E'})
    assert oferente.status_code == 201
    
    # 4. Crear licitación con productos
    licitacion = client.post('/api/licitaciones', json={
        'numero': 'E2E-001',
        'fecha': '2025-02-01',
        'cliente_id': cliente_id,
        'productos': [
            {
                'monodroga': 'Aspirina',
                'marca': 'Genérico',
                'presentacion': '100mg x 50',
                'cantidad': 1000,
                'precio_ofertado': 12.50,
                'resultado': 'Adjudicado'
            },
            {
                'monodroga': 'Omeprazol',
                'marca': 'Genérico',
                'presentacion': '20mg x 30',
                'cantidad': 500,
                'precio_ofertado': 25.00,
                'resultado': 'No Adjudicado'
            }
        ]
    })
    assert licitacion.status_code == 201
    lic_id = licitacion.json['id']
    
    # 5. Verificar licitación en listado
    listado = client.get('/api/licitaciones')
    assert listado.status_code == 200
    assert any(l['id'] == lic_id for l in listado.json)
    
    # 6. Obtener detalle
    detalle = client.get(f'/api/licitaciones/{lic_id}')
    assert detalle.status_code == 200
    assert detalle.json['numero_licitacion'] == 'E2E-001'
    
    # 7. Verificar productos
    productos = client.get(f'/api/productos/{lic_id}')
    assert productos.status_code == 200
    assert len(productos.json) == 2
    
    # 8. Verificar estadísticas actualizadas
    stats = client.get('/api/estadisticas')
    assert stats.status_code == 200
    assert stats.json['total_licitaciones'] >= 1
    assert stats.json['unidades_cotizadas'] >= 1500
    
    # 9. Logout
    logout = client.post('/api/auth/logout')
    assert logout.status_code == 200

def test_e2e_gestion_catalogos(client):
    """Test E2E: Gestión completa de catálogos"""
    
    # Login
    client.post('/api/auth/login', json={
        'username': 'admin',
        'password': 'admin123',
        'remember': False
    })
    
    # Crear portal
    portal = client.post('/api/portales-origen', json={'nombre': 'Portal E2E'})
    assert portal.status_code == 201
    
    # Crear modalidad
    modalidad = client.post('/api/modalidades-entrega', json={'nombre': 'Modalidad E2E'})
    assert modalidad.status_code == 201
    
    # Crear forma de pago
    forma = client.post('/api/formas-pago', json={'nombre': 'Forma E2E'})
    assert forma.status_code == 201
    
    # Verificar en listados
    portales = client.get('/api/portales-origen')
    assert any(p['nombre'] == 'Portal E2E' for p in portales.json)
    
    modalidades = client.get('/api/modalidades-entrega')
    assert any(m['nombre'] == 'Modalidad E2E' for m in modalidades.json)
    
    formas = client.get('/api/formas-pago')
    assert any(f['nombre'] == 'Forma E2E' for f in formas.json)
