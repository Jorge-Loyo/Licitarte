"""Rutas de presupuestos, alternativas, ofertas y exportación"""
from flask import Blueprint, request, jsonify, send_file
import sys
import os
from pathlib import Path
from io import BytesIO

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from shared.database.db_manager import DatabaseManager, USE_POSTGRES

bp = Blueprint('extras', __name__, url_prefix='/api')
db = DatabaseManager(os.path.abspath('../shared/database/licitaciones.db'))

# PRESUPUESTOS
@bp.route('/presupuestos/siguiente-numero', methods=['GET'])
def get_siguiente_numero_presupuesto():
    try:
        numero = db.obtener_siguiente_numero_presupuesto()
        return jsonify({'numero': numero})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/presupuestos', methods=['GET'])
def get_presupuestos():
    try:
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        presupuestos = db.obtener_presupuestos(limit, offset)
        return jsonify([{
            'numero': p[0], 'fecha': p[1], 'licitacion': p[2], 'cliente': p[3]
        } for p in presupuestos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/presupuestos/<int:numero>', methods=['GET'])
def get_presupuesto(numero):
    try:
        presupuesto = db.obtener_presupuesto_por_numero(numero)
        if presupuesto:
            return jsonify({'success': True, 'data': presupuesto})
        return jsonify({'success': False, 'error': 'Presupuesto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/presupuestos/crear', methods=['POST'])
def crear_presupuesto():
    data = request.json
    if not data or not data.get('licitacion_id'):
        return jsonify({'success': False, 'error': 'licitacion_id es obligatorio'}), 400
    
    try:
        numero = db.crear_presupuesto(data['licitacion_id'])
        return jsonify({'success': True, 'numero': numero})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ALTERNATIVAS
@bp.route('/alternativas/<int:producto_id>', methods=['GET'])
def get_alternativas(producto_id):
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT id, producto_id, marca, presentacion, laboratorio, costo_unitario, 
                           margen_porcentaje, precio_ofertado, observaciones
                    FROM alternativas_productos WHERE producto_id = %s
                """, (producto_id,))
            else:
                cursor.execute("""
                    SELECT id, producto_id, marca, presentacion, laboratorio, costo_unitario, 
                           margen_porcentaje, precio_ofertado, observaciones
                    FROM alternativas_productos WHERE producto_id = ?
                """, (producto_id,))
            alternativas = cursor.fetchall()
            return jsonify([{
                'id': a[0], 'producto_id': a[1], 'marca': a[2], 'presentacion': a[3],
                'laboratorio': a[4], 'costo_unitario': a[5], 'margen_porcentaje': a[6],
                'precio_ofertado': a[7], 'observaciones': a[8]
            } for a in alternativas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/alternativas', methods=['POST'])
def crear_alternativa():
    data = request.json
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    INSERT INTO alternativas_productos 
                    (producto_id, marca, presentacion, laboratorio, costo_unitario, margen_porcentaje, precio_ofertado, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                """, (
                    data['producto_id'], data.get('marca', ''), data.get('presentacion', ''),
                    data.get('laboratorio', ''),
                    float(data['costo_unitario']) if data.get('costo_unitario') else None,
                    float(data['margen_porcentaje']) if data.get('margen_porcentaje') else None,
                    float(data['precio_ofertado']) if data.get('precio_ofertado') else None,
                    data.get('observaciones', '')
                ))
                alt_id = cursor.fetchone()[0]
            else:
                cursor.execute("""
                    INSERT INTO alternativas_productos 
                    (producto_id, marca, presentacion, laboratorio, costo_unitario, margen_porcentaje, precio_ofertado, observaciones)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data['producto_id'], data.get('marca', ''), data.get('presentacion', ''),
                    data.get('laboratorio', ''),
                    float(data['costo_unitario']) if data.get('costo_unitario') else None,
                    float(data['margen_porcentaje']) if data.get('margen_porcentaje') else None,
                    float(data['precio_ofertado']) if data.get('precio_ofertado') else None,
                    data.get('observaciones', '')
                ))
                alt_id = cursor.lastrowid
            return jsonify({'success': True, 'id': alt_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/alternativas/<int:producto_id>', methods=['DELETE'])
def eliminar_alternativas_producto(producto_id):
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("DELETE FROM alternativas_productos WHERE producto_id = %s", (producto_id,))
            else:
                cursor.execute("DELETE FROM alternativas_productos WHERE producto_id = ?", (producto_id,))
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# OFERTAS
@bp.route('/ofertas/<int:producto_id>', methods=['GET'])
def get_ofertas_producto(producto_id):
    try:
        ofertas = db.obtener_ofertas_producto(producto_id)
        return jsonify([{
            'id': o[0], 'producto_id': o[1], 'oferente': o[2], 'laboratorio': o[3], 'precio': o[4]
        } for o in ofertas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/ofertas/<int:producto_id>', methods=['POST'])
def guardar_ofertas_producto(producto_id):
    data = request.json
    try:
        ofertas = data.get('ofertas', [])
        db.guardar_ofertas_producto(producto_id, ofertas)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# LICITACIONES DETALLE Y RESUMEN
@bp.route('/licitaciones/<int:id>/detalle', methods=['GET'])
def get_licitacion_detalle(id):
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT l.id, l.numero_licitacion, l.fecha, l.cliente_id, l.tipo_licitacion_id,
                           l.portal_origen, l.modalidad_entrega, l.forma_pago, l.requiere_poliza,
                           l.monto_poliza, l.observaciones, l.mantenimiento_oferta, l.tipo_adjudicacion
                    FROM licitaciones l WHERE l.id = %s
                """, (id,))
            else:
                cursor.execute("""
                    SELECT l.id, l.numero_licitacion, l.fecha, l.cliente_id, l.tipo_licitacion_id,
                           l.portal_origen, l.modalidad_entrega, l.forma_pago, l.requiere_poliza,
                           l.monto_poliza, l.observaciones, l.mantenimiento_oferta, l.tipo_adjudicacion
                    FROM licitaciones l WHERE l.id = ?
                """, (id,))
            
            row = cursor.fetchone()
            if not row:
                return jsonify({'success': False, 'error': 'Licitación no encontrada'}), 404
            
            porcentaje_poliza = None
            if row[8] and row[9]:
                if USE_POSTGRES:
                    cursor.execute("SELECT COALESCE(SUM(precio_ofertado * cantidad), 0) FROM productos WHERE licitacion_id = %s", (id,))
                else:
                    cursor.execute("SELECT COALESCE(SUM(precio_ofertado * cantidad), 0) FROM productos WHERE licitacion_id = ?", (id,))
                total = cursor.fetchone()[0]
                if total > 0:
                    porcentaje_poliza = (float(row[9]) / float(total)) * 100
            
            return jsonify({
                'id': row[0], 'numero': row[1], 'fecha': row[2], 'cliente_id': row[3],
                'tipo_licitacion_id': row[4], 'portal_origen': row[5], 'modalidad_entrega': row[6],
                'forma_pago': row[7], 'requiere_poliza': row[8], 'monto_poliza': row[9],
                'porcentaje_poliza': porcentaje_poliza, 'observaciones': row[10],
                'mantenimiento_oferta': row[11], 'tipo_adjudicacion': row[12] if len(row) > 12 and row[12] else 'Parcial'
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/licitaciones-resumen', methods=['GET'])
def get_licitaciones_resumen():
    try:
        licitaciones = db.obtener_licitaciones_resumen()
        return jsonify([{
            'id': l[0], 'numero': l[1], 'cliente': l[2] or '-',
            'total_productos': l[3] or 0, 'productos_ganados': l[4] or 0,
            'monto_cotizado': float(l[5]) if l[5] else 0.0,
            'monto_adjudicado': float(l[6]) if l[6] else 0.0
        } for l in licitaciones])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# EXPORTAR EXCEL
@bp.route('/licitaciones/<int:id>/exportar-excel', methods=['GET'])
def exportar_licitacion_excel(id):
    try:
        import pandas as pd
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT numero_licitacion FROM licitaciones WHERE id = %s", (id,))
            else:
                cursor.execute("SELECT numero_licitacion FROM licitaciones WHERE id = ?", (id,))
            licitacion = cursor.fetchone()
            if not licitacion:
                return jsonify({'error': 'Licitación no encontrada'}), 404
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT p.id, p.monodroga, p.marca, p.presentacion, p.cantidad, p.precio_ofertado,
                           p.resultado, p.precio_ganador, p.oferente_ganador, c.laboratorio
                    FROM productos p
                    LEFT JOIN medicamentos c ON LOWER(TRIM(p.monodroga)) = LOWER(TRIM(c.monodroga))
                                      AND LOWER(TRIM(p.marca)) = LOWER(TRIM(c.marca))
                                      AND LOWER(TRIM(p.presentacion)) = LOWER(TRIM(c.presentacion))
                    WHERE p.licitacion_id = %s
                """, (id,))
            else:
                cursor.execute("""
                    SELECT p.id, p.monodroga, p.marca, p.presentacion, p.cantidad, p.precio_ofertado,
                           p.resultado, p.precio_ganador, p.oferente_ganador, c.laboratorio
                    FROM productos p
                    LEFT JOIN medicamentos c ON LOWER(TRIM(p.monodroga)) = LOWER(TRIM(c.monodroga))
                                      AND LOWER(TRIM(p.marca)) = LOWER(TRIM(c.marca))
                                      AND LOWER(TRIM(p.presentacion)) = LOWER(TRIM(c.presentacion))
                    WHERE p.licitacion_id = ?
                """, (id,))
            productos = cursor.fetchall()
        
        data = []
        for p in productos:
            row = {
                'Monodroga': p[1], 'Laboratorio': p[9] or '',
                'Marca - Presentacion': f"{p[2]} - {p[3]}",
                'Cantidad': p[4], 'Precio': p[5]
            }
            
            ofertas = db.obtener_ofertas_producto(p[0])
            for idx, oferta in enumerate(ofertas, 1):
                row[f'Oferente{idx}'] = oferta[2]
                row[f'Precio{idx}'] = oferta[4]
                row[f'Laboratorio {idx}'] = oferta[3]
            
            if p[6] == 'Adjudicado':
                row['Ganador'] = 'Celtyc'
                row['Precio Ganador'] = p[5]
            elif p[6] == 'No Adjudicado' and p[8]:
                row['Ganador'] = p[8]
                row['Precio Ganador'] = p[7]
            else:
                row['Ganador'] = '-'
                row['Precio Ganador'] = '-'
            
            data.append(row)
        
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Licitación')
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'licitacion_{licitacion[0]}.xlsx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
