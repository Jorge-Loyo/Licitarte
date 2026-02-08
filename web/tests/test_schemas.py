import pytest
from pydantic import ValidationError
from schemas.licitacion_schema import LicitacionCreateSchema, ProductoSchema

def test_producto_schema_valido():
    """Test: ProductoSchema con datos válidos"""
    data = {
        'monodroga': 'Paracetamol',
        'marca': 'Genérico',
        'presentacion': '500mg x 20',
        'cantidad': 100,
        'precio_ofertado': 10.50
    }
    producto = ProductoSchema(**data)
    assert producto.monodroga == 'Paracetamol'
    assert producto.cantidad == 100

def test_producto_schema_cantidad_negativa():
    """Test: ProductoSchema con cantidad negativa debe fallar"""
    data = {
        'monodroga': 'Paracetamol',
        'marca': 'Genérico',
        'presentacion': '500mg x 20',
        'cantidad': -10,
        'precio_ofertado': 10.50
    }
    with pytest.raises(ValidationError):
        ProductoSchema(**data)

def test_licitacion_schema_valida():
    """Test: LicitacionCreateSchema con datos válidos"""
    data = {
        'numero': 'LIC-2025-001',
        'fecha': '2025-01-15 10:00',
        'productos': [
            {
                'monodroga': 'Paracetamol',
                'marca': 'Genérico',
                'presentacion': '500mg x 20',
                'cantidad': 100,
                'precio_ofertado': 10.50
            }
        ]
    }
    licitacion = LicitacionCreateSchema(**data)
    assert licitacion.numero == 'LIC-2025-001'
    assert len(licitacion.productos) == 1

def test_licitacion_schema_sin_productos():
    """Test: LicitacionCreateSchema sin productos debe fallar"""
    data = {
        'numero': 'LIC-2025-001',
        'fecha': '2025-01-15',
        'productos': []
    }
    with pytest.raises(ValidationError):
        LicitacionCreateSchema(**data)
