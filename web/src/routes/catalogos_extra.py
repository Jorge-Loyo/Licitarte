"""Rutas de catálogos adicionales"""
from flask import Blueprint, request, jsonify
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from shared.database.db_manager import DatabaseManager
from shared.database.connection_pool import USE_POSTGRES

bp = Blueprint('catalogos_extra', __name__, url_prefix='/api')
db = DatabaseManager()

# PORTALES ORIGEN
@bp.route('/portales-origen', methods=['GET'])
def get_portales_origen():
    portales = db.obtener_portales_origen()
    return jsonify([{'id': p[0], 'nombre': p[1]} for p in portales])

@bp.route('/portales-origen', methods=['POST'])
def crear_portal_origen():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        portal_id = db.crear_portal_origen(data['nombre'])
        return jsonify({'success': True, 'id': portal_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/portales-origen/<int:id>', methods=['PUT'])
def actualizar_portal_origen(id):
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        db.actualizar_portal_origen(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/portales-origen/<int:id>', methods=['DELETE'])
def eliminar_portal_origen(id):
    try:
        db.eliminar_portal_origen(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# MODALIDADES ENTREGA
@bp.route('/modalidades-entrega', methods=['GET'])
def get_modalidades_entrega():
    modalidades = db.obtener_modalidades_entrega()
    return jsonify([{'id': m[0], 'nombre': m[1]} for m in modalidades])

@bp.route('/modalidades-entrega', methods=['POST'])
def crear_modalidad_entrega():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        modalidad_id = db.crear_modalidad_entrega(data['nombre'])
        return jsonify({'success': True, 'id': modalidad_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/modalidades-entrega/<int:id>', methods=['PUT'])
def actualizar_modalidad_entrega(id):
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        db.actualizar_modalidad_entrega(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/modalidades-entrega/<int:id>', methods=['DELETE'])
def eliminar_modalidad_entrega(id):
    try:
        db.eliminar_modalidad_entrega(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# FORMAS PAGO
@bp.route('/formas-pago', methods=['GET'])
def get_formas_pago():
    formas = db.obtener_formas_pago()
    return jsonify([{'id': f[0], 'nombre': f[1]} for f in formas])

@bp.route('/formas-pago', methods=['POST'])
def crear_forma_pago():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        forma_id = db.crear_forma_pago(data['nombre'])
        return jsonify({'success': True, 'id': forma_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/formas-pago/<int:id>', methods=['PUT'])
def actualizar_forma_pago(id):
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        db.actualizar_forma_pago(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/formas-pago/<int:id>', methods=['DELETE'])
def eliminar_forma_pago(id):
    try:
        db.eliminar_forma_pago(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ORGANISMOS
@bp.route('/organismos', methods=['GET'])
def get_organismos():
    organismos = db.obtener_organismos()
    return jsonify([{'id': o[0], 'nombre': o[1]} for o in organismos])

@bp.route('/organismos', methods=['POST'])
def crear_organismo():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        organismo_id = db.crear_organismo(data['nombre'])
        return jsonify({'success': True, 'id': organismo_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/organismos/<int:id>', methods=['PUT'])
def actualizar_organismo(id):
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        db.actualizar_organismo(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/organismos/<int:id>', methods=['DELETE'])
def eliminar_organismo(id):
    try:
        db.eliminar_organismo(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# MOTIVOS PERDIDA
@bp.route('/motivos-perdida', methods=['GET'])
def get_motivos_perdida():
    motivos = db.obtener_motivos_perdida()
    return jsonify([{'id': m[0], 'nombre': m[1]} for m in motivos])

@bp.route('/motivos-perdida', methods=['POST'])
def crear_motivo_perdida():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        motivo_id = db.crear_motivo_perdida(data['nombre'])
        return jsonify({'success': True, 'id': motivo_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/motivos-perdida/<int:id>', methods=['PUT'])
def actualizar_motivo_perdida(id):
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        db.actualizar_motivo_perdida(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/motivos-perdida/<int:id>', methods=['DELETE'])
def eliminar_motivo_perdida(id):
    try:
        db.eliminar_motivo_perdida(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# MANTENIMIENTOS OFERTA
@bp.route('/mantenimientos-oferta', methods=['GET'])
def get_mantenimientos_oferta():
    mantenimientos = db.obtener_mantenimientos_oferta()
    return jsonify([{'id': m[0], 'nombre': m[1]} for m in mantenimientos])

@bp.route('/mantenimientos-oferta', methods=['POST'])
def crear_mantenimiento_oferta():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        mantenimiento_id = db.crear_mantenimiento_oferta(data['nombre'])
        return jsonify({'success': True, 'id': mantenimiento_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/mantenimientos-oferta/<int:id>', methods=['PUT'])
def actualizar_mantenimiento_oferta(id):
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        db.actualizar_mantenimiento_oferta(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/mantenimientos-oferta/<int:id>', methods=['DELETE'])
def eliminar_mantenimiento_oferta(id):
    try:
        db.eliminar_mantenimiento_oferta(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# RANKING Y MÉTRICAS
@bp.route('/ranking-perdidas', methods=['GET'])
def get_ranking_perdidas():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT motivo_perdida, COUNT(*) as cantidad
            FROM productos
            WHERE motivo_perdida IS NOT NULL AND motivo_perdida != ''
            GROUP BY motivo_perdida
            ORDER BY cantidad DESC
        """)
        resultados = cursor.fetchall()
    return jsonify([{'motivo': r[0], 'cantidad': r[1]} for r in resultados])

@bp.route('/diferencias-promedio', methods=['GET'])
def get_diferencias_promedio():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT AVG(precio_ofertado - precio_ganador) as dif_pesos,
                   AVG(((precio_ofertado - precio_ganador) / precio_ganador) * 100) as dif_porcentaje
            FROM productos
            WHERE resultado = 'No Adjudicado' 
              AND precio_ganador IS NOT NULL 
              AND precio_ganador > 0
        """)
        resultado = cursor.fetchone()
    
    if resultado is None:
        return jsonify({
            'diferencia_pesos': 0,
            'diferencia_porcentaje': 0
        })
    
    return jsonify({
        'diferencia_pesos': float(resultado[0]) if resultado[0] else 0,
        'diferencia_porcentaje': float(resultado[1]) if resultado[1] else 0
    })

# VERIFICACIONES
@bp.route('/licitaciones/verificar', methods=['GET'])
def verificar_licitacion():
    numero = request.args.get('numero')
    cliente_id = request.args.get('cliente_id')
    
    if not numero or not cliente_id:
        return jsonify({'existe': False})
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT COUNT(*) FROM licitaciones WHERE numero_licitacion = %s AND cliente_id = %s", (numero, int(cliente_id)))
            else:
                cursor.execute("SELECT COUNT(*) FROM licitaciones WHERE numero_licitacion = ? AND cliente_id = ?", (numero, int(cliente_id)))
            result = cursor.fetchone()
            count = result[0] if result else 0
            return jsonify({'existe': count > 0})
    except Exception as e:
        return jsonify({'existe': False, 'error': str(e)})

# LABORATORIOS
@bp.route('/laboratorios', methods=['GET'])
def get_laboratorios():
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = request.args.get('por_pagina', 50, type=int)
    
    resultado = db.obtener_laboratorios(pagina=pagina, por_pagina=por_pagina)
    
    return jsonify({
        'total': resultado['total'],
        'pagina': resultado['pagina'],
        'por_pagina': resultado['por_pagina'],
        'total_paginas': resultado['total_paginas'],
        'datos': [{'id': l[0], 'nombre': l[1], 'activo': l[2]} for l in resultado['datos']]
    })

@bp.route('/laboratorios', methods=['POST'])
def crear_laboratorio():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        laboratorio_id = db.crear_laboratorio(data['nombre'])
        return jsonify({'success': True, 'id': laboratorio_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/laboratorios/<int:id>', methods=['PUT'])
def actualizar_laboratorio(id):
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        db.actualizar_laboratorio(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/laboratorios/<int:id>', methods=['DELETE'])
def eliminar_laboratorio(id):
    try:
        db.eliminar_laboratorio(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# MONODROGAS
@bp.route('/monodrogas', methods=['GET'])
def get_monodrogas():
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = request.args.get('por_pagina', 50, type=int)
    search = request.args.get('search', '').strip()
    
    resultado = db.obtener_monodrogas(pagina=pagina, por_pagina=por_pagina, search=search)
    
    return jsonify({
        'total': resultado['total'],
        'pagina': resultado['pagina'],
        'por_pagina': resultado['por_pagina'],
        'total_paginas': resultado['total_paginas'],
        'datos': [{'id': m[0], 'nombre': m[1], 'activo': m[2]} for m in resultado['datos']]
    })

@bp.route('/monodrogas/buscar', methods=['GET'])
def buscar_monodrogas():
    q = request.args.get('q', '').strip()
    if len(q) < 3:
        return jsonify([])
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        if USE_POSTGRES:
            cursor.execute("SELECT DISTINCT nombre FROM monodrogas WHERE nombre ILIKE %s AND activo = TRUE ORDER BY nombre LIMIT 20", (f'%{q}%',))
        else:
            cursor.execute("SELECT DISTINCT nombre FROM monodrogas WHERE nombre LIKE ? AND activo = 1 ORDER BY nombre LIMIT 20", (f'%{q}%',))
        return jsonify([{'nombre': row[0]} for row in cursor.fetchall()])

@bp.route('/laboratorios/por-monodroga', methods=['GET'])
def get_laboratorios_por_monodroga():
    monodroga = request.args.get('monodroga', '').strip()
    if not monodroga:
        return jsonify([])
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        # Obtener laboratorios de la tabla laboratorios que tienen medicamentos con esa monodroga
        if USE_POSTGRES:
            cursor.execute("""
                SELECT DISTINCT l.nombre 
                FROM laboratorios l
                INNER JOIN medicamentos m ON LOWER(m.laboratorio) = LOWER(l.nombre)
                WHERE m.monodroga = %s AND l.activo = TRUE
                ORDER BY l.nombre
            """, (monodroga,))
        else:
            cursor.execute("""
                SELECT DISTINCT l.nombre 
                FROM laboratorios l
                INNER JOIN medicamentos m ON LOWER(m.laboratorio) = LOWER(l.nombre)
                WHERE m.monodroga = ? AND l.activo = 1
                ORDER BY l.nombre
            """, (monodroga,))
        return jsonify([{'nombre': row[0]} for row in cursor.fetchall() if row[0]])

@bp.route('/laboratorios/buscar', methods=['GET'])
def buscar_laboratorios():
    q = request.args.get('q', '').strip()
    monodroga = request.args.get('monodroga', '').strip()
    
    if not monodroga:
        return jsonify([])
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        if USE_POSTGRES:
            cursor.execute("""
                SELECT DISTINCT l.nombre 
                FROM laboratorios l
                WHERE l.activo = TRUE 
                  AND l.nombre ILIKE %s
                  AND EXISTS (
                      SELECT 1 FROM medicamentos m 
                      WHERE LOWER(m.laboratorio) = LOWER(l.nombre) 
                        AND LOWER(m.monodroga) = LOWER(%s)
                  )
                ORDER BY l.nombre
                LIMIT 20
            """, (f'%{q}%', monodroga))
        else:
            cursor.execute("""
                SELECT DISTINCT l.nombre 
                FROM laboratorios l
                WHERE l.activo = 1 
                  AND l.nombre LIKE ?
                  AND EXISTS (
                      SELECT 1 FROM medicamentos m 
                      WHERE LOWER(m.laboratorio) = LOWER(l.nombre) 
                        AND LOWER(m.monodroga) = LOWER(?)
                  )
                ORDER BY l.nombre
                LIMIT 20
            """, (f'%{q}%', monodroga))
        return jsonify([{'nombre': row[0]} for row in cursor.fetchall() if row[0]])

@bp.route('/marcas/por-monodroga-laboratorio', methods=['GET'])
def get_marcas_por_monodroga_laboratorio():
    monodroga = request.args.get('monodroga', '').strip()
    laboratorio = request.args.get('laboratorio', '').strip()
    if not monodroga or not laboratorio:
        return jsonify([])
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        if USE_POSTGRES:
            cursor.execute("SELECT DISTINCT marca FROM medicamentos WHERE monodroga = %s AND laboratorio = %s ORDER BY marca", (monodroga, laboratorio))
        else:
            cursor.execute("SELECT DISTINCT marca FROM medicamentos WHERE monodroga = ? AND laboratorio = ? ORDER BY marca", (monodroga, laboratorio))
        return jsonify([{'nombre': row[0]} for row in cursor.fetchall() if row[0]])

@bp.route('/monodrogas', methods=['POST'])
def crear_monodroga():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        monodroga_id = db.crear_monodroga(data['nombre'])
        return jsonify({'success': True, 'id': monodroga_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/monodrogas/<int:id>', methods=['PUT'])
def actualizar_monodroga(id):
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        db.actualizar_monodroga(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/monodrogas/<int:id>', methods=['DELETE'])
def eliminar_monodroga(id):
    try:
        db.eliminar_monodroga(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500
