"""Rutas de catálogos (clientes, oferentes, marcas, tipos, etc)"""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from shared.database.db_manager import DatabaseManager
from src.validators import ClienteCreate

bp = Blueprint('catalogos', __name__, url_prefix='/api')
db = DatabaseManager(os.path.abspath('../shared/database/licitaciones.db'))

# CLIENTES
@bp.route('/clientes', methods=['GET'])
def get_clientes():
    clientes = db.obtener_clientes()
    return jsonify([{
        'id': c[0], 'nombre': c[1], 'razon_social': c[2], 'cuit': c[3],
        'direccion': c[4], 'telefono': c[5], 'email': c[6],
        'organismo_jurisdiccion': c[7] if len(c) > 7 else ''
    } for c in clientes])

@bp.route('/clientes', methods=['POST'])
def crear_cliente():
    try:
        data = ClienteCreate(**request.json)
    except ValidationError as e:
        return jsonify({'success': False, 'error': 'Datos inválidos', 'details': e.errors()}), 400
    try:
        cliente_id = db.crear_cliente(
            data.nombre, data.razon_social or '', data.cuit or '',
            data.direccion or '', data.telefono or '', data.email or '',
            data.organismo_jurisdiccion
        )
        return jsonify({'success': True, 'id': cliente_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/clientes/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    data = request.json
    try:
        db.actualizar_cliente(id, data['nombre'], data.get('razon_social', ''), data.get('cuit', ''),
                             data.get('direccion', ''), data.get('telefono', ''), data.get('email', ''),
                             data.get('organismo_jurisdiccion', ''))
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    try:
        db.eliminar_cliente(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# OFERENTES
@bp.route('/oferentes', methods=['GET'])
def get_oferentes():
    oferentes = db.obtener_oferentes()
    return jsonify([{'id': o[0], 'nombre': o[1]} for o in oferentes])

@bp.route('/oferentes', methods=['POST'])
def crear_oferente():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        oferente_id = db.crear_oferente(data['nombre'])
        return jsonify({'success': True, 'id': oferente_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/oferentes/<int:id>', methods=['PUT'])
def actualizar_oferente(id):
    data = request.json
    try:
        db.actualizar_oferente(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/oferentes/<int:id>', methods=['DELETE'])
def eliminar_oferente(id):
    try:
        db.eliminar_oferente(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# MARCAS
@bp.route('/marcas', methods=['GET'])
def get_marcas():
    marcas = db.obtener_marcas()
    return jsonify([{'id': m[0], 'nombre': m[1]} for m in marcas])

@bp.route('/marcas', methods=['POST'])
def crear_marca():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        marca_id = db.crear_marca(data['nombre'])
        return jsonify({'success': True, 'id': marca_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/marcas/<int:id>', methods=['PUT'])
def actualizar_marca(id):
    data = request.json
    try:
        db.actualizar_marca(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/marcas/<int:id>', methods=['DELETE'])
def eliminar_marca(id):
    try:
        db.eliminar_marca(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# TIPOS LICITACION
@bp.route('/tipos-licitacion', methods=['GET'])
def get_tipos_licitacion():
    tipos = db.obtener_tipos_licitacion()
    return jsonify([{'id': t[0], 'nombre': t[1]} for t in tipos])

@bp.route('/tipos-licitacion', methods=['POST'])
def crear_tipo_licitacion():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        tipo_id = db.crear_tipo_licitacion(data['nombre'])
        return jsonify({'success': True, 'id': tipo_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/tipos-licitacion/<int:id>', methods=['PUT'])
def actualizar_tipo_licitacion(id):
    data = request.json
    try:
        db.actualizar_tipo_licitacion(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/tipos-licitacion/<int:id>', methods=['DELETE'])
def eliminar_tipo_licitacion(id):
    try:
        db.eliminar_tipo_licitacion(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CATALOGO MEDICAMENTOS
@bp.route('/catalogo', methods=['GET'])
def get_catalogo():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    search = request.args.get('search', '').strip()
    campo = request.args.get('campo', 'todos').strip()
    offset = (page - 1) * per_page
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Construir WHERE según campo
        if search:
            if campo == 'monodroga':
                where = "WHERE monodroga LIKE %s"
                params = (f'%{search}%',)
            elif campo == 'marca':
                where = "WHERE marca LIKE %s"
                params = (f'%{search}%',)
            elif campo == 'laboratorio':
                where = "WHERE laboratorio LIKE %s"
                params = (f'%{search}%',)
            else:  # todos
                where = "WHERE monodroga LIKE %s OR marca LIKE %s OR laboratorio LIKE %s"
                params = (f'%{search}%', f'%{search}%', f'%{search}%')
        else:
            where = ""
            params = ()
        
        # Contar total
        cursor.execute(f"SELECT COUNT(*) FROM medicamentos {where}", params)
        total = cursor.fetchone()[0]
        
        # Obtener página
        cursor.execute(f"""SELECT id, numero_registro, monodroga, marca, presentacion, laboratorio, 
                       precio_caja, precio_unitario, costo_unitario, fecha, troquel, cod_ab, troquel_ean,
                       cod_monodroga, cod_laboratorio, multidosis FROM medicamentos {where}
                       ORDER BY monodroga, marca, presentacion LIMIT %s OFFSET %s""",
                     params + (per_page, offset))
        productos = cursor.fetchall()
    
    return jsonify({
        'productos': [{
            'id': p[0], 'numero_registro': p[1], 'monodroga': p[2], 'marca': p[3],
            'presentacion': p[4], 'laboratorio': p[5], 'precio_caja': p[6],
            'precio_unitario': p[7], 'costo_unitario': p[8], 'fecha': p[9],
            'troquel': p[10], 'cod_ab': p[11], 'troquel_ean': p[12],
            'cod_ab_estado': 'Habilitado' if p[11] == 0 else 'Deshabilitado' if p[11] == 1 else None,
            'cod_monodroga': p[13], 'cod_laboratorio': p[14], 'multidosis': p[15]
        } for p in productos],
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    })
