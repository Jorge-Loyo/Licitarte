"""Blueprint de productos.

Maneja CRUD de productos asociados a licitaciones:
- GET /api/productos/<licitacion_id>: Lista productos de una licitación
- POST /api/productos: Crear producto nuevo
- PUT /api/productos/<id>: Actualizar producto existente

Validación: Usa Pydantic (ProductoCreate) para validar datos.
Campos: monodroga, marca, presentación, cantidad, precio, resultado,
        marca_ofrecida, costo_unitario, margen_porcentaje, observaciones.
"""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from shared.database.db_manager import DatabaseManager
from src.validators import ProductoCreate

bp = Blueprint('productos', __name__, url_prefix='/api/productos')
db = DatabaseManager(os.path.abspath('../shared/database/licitaciones.db'))

@bp.route('/<int:licitacion_id>', methods=['GET'])
def get_productos(licitacion_id):
    """Obtener productos de una licitación.
    
    Args:
        licitacion_id: ID de la licitación
    
    Returns:
        JSON: Lista de productos con todos los campos:
            - Básicos: monodroga, marca, presentación, cantidad, precio
            - Resultado: resultado, precio_ganador, oferente_ganador
            - Análisis: costo_unitario, margen_porcentaje
            - Extras: marca_ofrecida, marca_ganadora, motivo_perdida
    
    Nota: Maneja tuplas de longitud variable (compatibilidad con
    versiones antiguas de BD que no tenían todos los campos).
    """
    productos = db.obtener_productos_licitacion(licitacion_id)
    result = []
    for p in productos:
        # Construir dict con manejo de campos opcionales
        # (compatibilidad con esquemas antiguos)
        producto_dict = {
            'id': p[0],
            'licitacion_id': p[1],
            'monodroga': p[2],
            'marca': p[3],
            'presentacion': p[4],
            'cantidad': p[5],
            'precio_ofertado': p[6],
            'resultado': p[7],
            'precio_ganador': p[8],
            'oferente_ganador': p[9],
            'marca_ofrecida': p[10],
            'marca_ganadora': p[11] if len(p) > 11 else '',
            'motivo_perdida': p[12] if len(p) > 12 else '',
            'numero_renglon': p[13] if len(p) > 13 else '',
            'costo_unitario': p[14] if len(p) > 14 else None,
            'margen_porcentaje': p[15] if len(p) > 15 else None,
            'observaciones': p[16] if len(p) > 16 else '',
            'producto_cotizar': p[17] if len(p) > 17 else 'principal'
        }
        result.append(producto_dict)
    return jsonify(result)

@bp.route('', methods=['POST'])
def crear_producto():
    """Crear nuevo producto.
    
    Validación Pydantic:
        - ProductoCreate valida estructura y tipos
        - cantidad > 0, precio >= 0
        - resultado in ['Adjudicado', 'Parcial', 'No Adjudicado']
    
    Returns:
        201: {'success': True, 'id': <producto_id>}
        400: {'success': False, 'error': str, 'details': []}
    """
    try:
        # Validar que request.json no sea None
        if not request.json:
            return jsonify({'success': False, 'error': 'Request body no puede estar vacío'}), 400
        # Validar con Pydantic
        data = ProductoCreate(**request.json)
    except ValidationError as e:
        return jsonify({'success': False, 'error': 'Datos inválidos', 'details': e.errors()}), 400
    
    try:
        producto_id = db.agregar_producto(
            data.licitacion_id,
            data.monodroga,
            data.marca,
            data.presentacion,
            data.cantidad,
            data.precio,
            data.resultado,
            None,
            '',
            data.marca_ofrecida or '',
            '',
            '',
            data.numero_renglon or '',
            data.costo_unitario,
            data.margen_porcentaje,
            data.observaciones or '',
            data.producto_cotizar or 'principal'
        )
        return jsonify({'success': True, 'id': producto_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    """Actualizar producto existente.
    
    Args:
        id: ID del producto a actualizar
    
    Body: Todos los campos del producto (monodroga, marca, etc.)
    
    Conversiones:
        - cantidad: int
        - precio_ofertado, precio_ganador: float (nullable)
        - costo_unitario, margen_porcentaje: float (nullable)
    
    Returns:
        200: {'success': True}
        500: {'error': str}
    """
    data = request.json
    if not data:
        return jsonify({'success': False, 'error': 'Request body no puede estar vacío'}), 400
    
    try:
        db.actualizar_producto(
            id,
            data.get('monodroga'),
            data.get('marca'),
            data.get('presentacion'),
            int(data['cantidad']) if data.get('cantidad') else 0,
            float(data['precio_ofertado']) if data.get('precio_ofertado') else 0,
            data.get('resultado', 'Parcial'),
            float(data['precio_ganador']) if data.get('precio_ganador') else None,
            data.get('oferente', ''),
            data.get('marca_ofrecida', ''),
            data.get('marca_ganadora', ''),
            data.get('motivo_perdida', ''),
            data.get('numero_renglon', ''),
            float(data['costo_unitario']) if data.get('costo_unitario') else None,
            float(data['margen_porcentaje']) if data.get('margen_porcentaje') else None,
            data.get('observaciones', ''),
            data.get('producto_cotizar', 'principal')
        )
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
