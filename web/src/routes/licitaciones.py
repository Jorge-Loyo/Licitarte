"""Rutas de licitaciones"""
from flask import Blueprint, request, jsonify
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from shared.database.db_manager import DatabaseManager, USE_POSTGRES

bp = Blueprint('licitaciones', __name__, url_prefix='/api/licitaciones')
db = DatabaseManager(os.path.abspath('../shared/database/licitaciones.db'))

@bp.route('', methods=['GET'])
def get_licitaciones():
    """Obtener todas las licitaciones con estadísticas"""
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.id, l.numero_licitacion, l.fecha, l.oferente_ganador, l.marca_ganadora, l.precio_ganador,
                   c.nombre as cliente, t.nombre as tipo_licitacion, l.numero_presupuesto
            FROM licitaciones l
            LEFT JOIN clientes c ON l.cliente_id = c.id
            LEFT JOIN tipos_licitacion t ON l.tipo_licitacion_id = t.id
            ORDER BY l.fecha DESC
        """)
        licitaciones = cursor.fetchall()
        
        resultado = []
        for l in licitaciones:
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT COUNT(*) as total,
                           SUM(CASE WHEN resultado = 'Adjudicado' THEN 1 ELSE 0 END) as adjudicados,
                           COALESCE(SUM(precio_ofertado * cantidad), 0) as total_cotizado
                    FROM productos WHERE licitacion_id = %s
                """, (l[0],))
            else:
                cursor.execute("""
                    SELECT COUNT(*) as total,
                           SUM(CASE WHEN resultado = 'Adjudicado' THEN 1 ELSE 0 END) as adjudicados,
                           COALESCE(SUM(precio_ofertado * cantidad), 0) as total_cotizado
                    FROM productos WHERE licitacion_id = ?
                """, (l[0],))
            stats = cursor.fetchone()
            total = stats[0] or 0
            adjudicados = stats[1] or 0
            total_cotizado = float(stats[2]) if stats[2] else 0.0
            ganancia = f"{adjudicados}/{total}" if total > 0 else "-"
            
            resultado.append({
                'id': l[0],
                'numero': l[1],
                'fecha': l[2],
                'oferente': l[3],
                'marca_ganadora': l[4],
                'precio_ganador': l[5],
                'cliente': l[6] or '-',
                'tipo_licitacion': l[7] or '-',
                'numero_presupuesto': l[8],
                'total_cotizado': total_cotizado,
                'ganancia': ganancia
            })
    
    return jsonify(resultado)

@bp.route('', methods=['POST'])
def crear_licitacion():
    """Crear nueva licitación con productos"""
    data = request.json
    if not data:
        return jsonify({'success': False, 'error': 'No se recibieron datos'}), 400
    
    try:
        if not data.get('numero') or not data.get('fecha'):
            return jsonify({'success': False, 'error': 'Número y fecha son obligatorios'}), 400
        
        licitacion_id = db.crear_licitacion(
            data['numero'],
            data['fecha'],
            '',
            '',
            None,
            int(data['cliente_id']) if data.get('cliente_id') else None,
            int(data['tipo_licitacion_id']) if data.get('tipo_licitacion_id') else None,
            data.get('portal_origen', ''),
            data.get('modalidad_entrega', ''),
            data.get('forma_pago', ''),
            data.get('requiere_poliza', False),
            float(data['monto_poliza']) if data.get('monto_poliza') else None,
            data.get('observaciones', ''),
            data.get('mantenimiento_oferta', '')
        )
        
        for producto in data.get('productos', []):
            producto_id = db.agregar_producto(
                licitacion_id,
                producto['monodroga'],
                producto['marca'],
                producto['presentacion'],
                int(producto['cantidad']),
                float(producto['precio']),
                producto['resultado'],
                float(producto['precio_ganador']) if producto.get('precio_ganador') else None,
                producto.get('oferente_ganador', ''),
                producto.get('marca_ofrecida', ''),
                producto.get('marca_ganadora', ''),
                producto.get('motivo_perdida', ''),
                producto.get('numero_renglon', ''),
                float(producto['costo_unitario']) if producto.get('costo_unitario') else None,
                float(producto['margen_porcentaje']) if producto.get('margen_porcentaje') else None,
                producto.get('observaciones', ''),
                producto.get('producto_cotizar', 'principal')
            )
            
            for alternativa in producto.get('alternativas', []):
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    if USE_POSTGRES:
                        cursor.execute("""
                            INSERT INTO alternativas_productos 
                            (producto_id, marca, presentacion, laboratorio, costo_unitario, margen_porcentaje, precio_ofertado, observaciones)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            producto_id,
                            alternativa.get('marca', ''),
                            alternativa.get('presentacion', ''),
                            alternativa.get('laboratorio', ''),
                            float(alternativa['costo_unitario']) if alternativa.get('costo_unitario') else None,
                            float(alternativa['margen_porcentaje']) if alternativa.get('margen_porcentaje') else None,
                            float(alternativa['precio_ofertado']) if alternativa.get('precio_ofertado') else None,
                            alternativa.get('observaciones', '')
                        ))
                    else:
                        cursor.execute("""
                            INSERT INTO alternativas_productos 
                            (producto_id, marca, presentacion, laboratorio, costo_unitario, margen_porcentaje, precio_ofertado, observaciones)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            producto_id,
                            alternativa.get('marca', ''),
                            alternativa.get('presentacion', ''),
                            alternativa.get('laboratorio', ''),
                            float(alternativa['costo_unitario']) if alternativa.get('costo_unitario') else None,
                            float(alternativa['margen_porcentaje']) if alternativa.get('margen_porcentaje') else None,
                            float(alternativa['precio_ofertado']) if alternativa.get('precio_ofertado') else None,
                            alternativa.get('observaciones', '')
                        ))
        
        return jsonify({'success': True, 'id': licitacion_id}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@bp.route('/<int:id>', methods=['GET'])
def get_licitacion(id):
    """Obtener una licitación específica"""
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT l.numero_licitacion, c.nombre as cliente
                    FROM licitaciones l
                    LEFT JOIN clientes c ON l.cliente_id = c.id
                    WHERE l.id = %s
                """, (id,))
            else:
                cursor.execute("""
                    SELECT l.numero_licitacion, c.nombre as cliente
                    FROM licitaciones l
                    LEFT JOIN clientes c ON l.cliente_id = c.id
                    WHERE l.id = ?
                """, (id,))
            row = cursor.fetchone()
            if row:
                return jsonify({'numero': row[0], 'cliente': row[1] or '-'})
            return jsonify({'error': 'No encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['PUT'])
def actualizar_licitacion(id):
    """Actualizar licitación existente"""
    data = request.json
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    UPDATE licitaciones 
                    SET numero_licitacion=%s, fecha=%s, cliente_id=%s, tipo_licitacion_id=%s,
                        portal_origen=%s, modalidad_entrega=%s, forma_pago=%s,
                        requiere_poliza=%s, monto_poliza=%s, observaciones=%s, mantenimiento_oferta=%s,
                        tipo_adjudicacion=%s
                    WHERE id=%s
                """, (
                    data['numero'],
                    data['fecha'],
                    int(data['cliente_id']) if data.get('cliente_id') else None,
                    int(data['tipo_licitacion_id']) if data.get('tipo_licitacion_id') else None,
                    data.get('portal_origen', ''),
                    data.get('modalidad_entrega', ''),
                    data.get('forma_pago', ''),
                    data.get('requiere_poliza', False),
                    float(data['monto_poliza']) if data.get('monto_poliza') else None,
                    data.get('observaciones', ''),
                    data.get('mantenimiento_oferta', ''),
                    data.get('tipo_adjudicacion', 'Parcial'),
                    id
                ))
            else:
                cursor.execute("""
                    UPDATE licitaciones 
                    SET numero_licitacion=?, fecha=?, cliente_id=?, tipo_licitacion_id=?,
                        portal_origen=?, modalidad_entrega=?, forma_pago=?,
                        requiere_poliza=?, monto_poliza=?, observaciones=?, mantenimiento_oferta=?,
                        tipo_adjudicacion=?
                    WHERE id=?
                """, (
                    data['numero'],
                    data['fecha'],
                    int(data['cliente_id']) if data.get('cliente_id') else None,
                    int(data['tipo_licitacion_id']) if data.get('tipo_licitacion_id') else None,
                    data.get('portal_origen', ''),
                    data.get('modalidad_entrega', ''),
                    data.get('forma_pago', ''),
                    data.get('requiere_poliza', False),
                    float(data['monto_poliza']) if data.get('monto_poliza') else None,
                    data.get('observaciones', ''),
                    data.get('mantenimiento_oferta', ''),
                    data.get('tipo_adjudicacion', 'Parcial'),
                    id
                ))
        
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['DELETE'])
def eliminar_licitacion(id):
    """Eliminar licitación"""
    try:
        db.eliminar_licitacion(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500
