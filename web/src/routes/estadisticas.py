"""Rutas de estadísticas y métricas"""
from flask import Blueprint, request, jsonify
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from shared.database.db_manager import DatabaseManager

bp = Blueprint('estadisticas', __name__, url_prefix='/api')
db = DatabaseManager(os.path.abspath('../shared/database/licitaciones.db'))

@bp.route('/estadisticas', methods=['GET'])
def get_estadisticas():
    """Obtener estadísticas generales del dashboard"""
    stats = db.obtener_estadisticas()
    return jsonify(stats)

@bp.route('/historico', methods=['POST'])
def get_historico():
    """Obtener histórico de precios con filtros"""
    data = request.json or {}
    filtro = data.get('monodroga', '')
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        if filtro:
            try:
                cursor.execute("""
                    SELECT l.numero_licitacion, t.nombre as tipo_licitacion, p.marca, p.presentacion, 
                           p.cantidad, p.precio_ofertado, l.fecha
                    FROM productos p
                    JOIN licitaciones l ON p.licitacion_id = l.id
                    LEFT JOIN tipos_licitacion t ON l.tipo_licitacion_id = t.id
                    WHERE p.resultado = 'Adjudicado' AND p.monodroga ILIKE %s
                    ORDER BY l.fecha DESC
                """, (f'%{filtro}%',))
            except:
                cursor.execute("""
                    SELECT l.numero_licitacion, t.nombre as tipo_licitacion, p.marca, p.presentacion, 
                           p.cantidad, p.precio_ofertado, l.fecha
                    FROM productos p
                    JOIN licitaciones l ON p.licitacion_id = l.id
                    LEFT JOIN tipos_licitacion t ON l.tipo_licitacion_id = t.id
                    WHERE p.resultado = 'Adjudicado' AND p.monodroga LIKE ?
                    ORDER BY l.fecha DESC
                """, (f'%{filtro}%',))
        else:
            cursor.execute("""
                SELECT l.numero_licitacion, t.nombre as tipo_licitacion, p.marca, p.presentacion, 
                       p.cantidad, p.precio_ofertado, l.fecha
                FROM productos p
                JOIN licitaciones l ON p.licitacion_id = l.id
                LEFT JOIN tipos_licitacion t ON l.tipo_licitacion_id = t.id
                WHERE p.resultado = 'Adjudicado'
                ORDER BY l.fecha DESC
            """)
        productos = cursor.fetchall()
    
    return jsonify([{
        'numero_licitacion': p[0], 'tipo_licitacion': p[1] or '-', 'marca': p[2],
        'presentacion': p[3], 'cantidad': p[4], 'precio': p[5], 'fecha': p[6]
    } for p in productos])

@bp.route('/productos-adjudicados', methods=['GET'])
def get_productos_adjudicados():
    """Obtener productos adjudicados para dashboard"""
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.numero_licitacion, t.nombre as tipo_licitacion, c.nombre as cliente, 
                   p.monodroga, p.marca, p.presentacion, p.cantidad, p.precio_ofertado, l.fecha
            FROM productos p
            JOIN licitaciones l ON p.licitacion_id = l.id
            LEFT JOIN clientes c ON l.cliente_id = c.id
            LEFT JOIN tipos_licitacion t ON l.tipo_licitacion_id = t.id
            WHERE p.resultado = 'Adjudicado'
            ORDER BY l.fecha DESC
        """)
        productos = cursor.fetchall()
    
    return jsonify([{
        'numero_licitacion': p[0], 'tipo_licitacion': p[1] or '-', 'cliente': p[2] or '-',
        'monodroga': p[3], 'marca': p[4], 'presentacion': p[5],
        'cantidad': p[6], 'precio': p[7], 'fecha': p[8]
    } for p in productos])
