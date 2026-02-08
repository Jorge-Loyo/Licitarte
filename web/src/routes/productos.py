"""Rutas de productos"""
from flask import Blueprint, request, jsonify
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from shared.database.db_manager import DatabaseManager

bp = Blueprint('productos', __name__, url_prefix='/api/productos')
db = DatabaseManager(os.path.abspath('../shared/database/licitaciones.db'))

@bp.route('/<int:licitacion_id>', methods=['GET'])
def get_productos(licitacion_id):
    """Obtener productos de una licitación"""
    productos = db.obtener_productos_licitacion(licitacion_id)
    result = []
    for p in productos:
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
    """Crear nuevo producto"""
    data = request.json
    try:
        producto_id = db.agregar_producto(
            data['licitacion_id'],
            data['monodroga'],
            data['marca'],
            data['presentacion'],
            int(data['cantidad']),
            float(data['precio_ofertado']),
            data['resultado'],
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
        return jsonify({'success': True, 'id': producto_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    """Actualizar producto existente"""
    data = request.json
    try:
        db.actualizar_producto(
            id,
            data['monodroga'],
            data['marca'],
            data['presentacion'],
            int(data['cantidad']),
            float(data['precio_ofertado']),
            data['resultado'],
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
