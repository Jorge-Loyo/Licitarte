"""Servicio de estadísticas y métricas"""
import sys
import os
from pathlib import Path
from typing import List, Dict, Any
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from backend.database.db_manager import DatabaseManager

class EstadisticasService:
    def __init__(self):
        self.db = DatabaseManager(os.path.abspath('shared/database/licitaciones.db'))
    
    def obtener_estadisticas_generales(self) -> Dict[str, Any]:
        """Obtiene estadísticas generales del dashboard"""
        return self.db.obtener_estadisticas()
    
    def obtener_historico(self, filtro_monodroga: str = '') -> List[Dict[str, Any]]:
        """Obtiene histórico de precios con filtro opcional"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            if filtro_monodroga:
                try:
                    cursor.execute("""
                        SELECT l.numero_licitacion, t.nombre as tipo_licitacion, p.marca, p.presentacion, 
                               p.cantidad, p.precio_ofertado, l.fecha
                        FROM productos p
                        JOIN licitaciones l ON p.licitacion_id = l.id
                        LEFT JOIN tipos_licitacion t ON l.tipo_licitacion_id = t.id
                        WHERE p.resultado = 'Adjudicado' AND p.monodroga ILIKE %s
                        ORDER BY l.fecha DESC
                    """, (f'%{filtro_monodroga}%',))
                except:
                    cursor.execute("""
                        SELECT l.numero_licitacion, t.nombre as tipo_licitacion, p.marca, p.presentacion, 
                               p.cantidad, p.precio_ofertado, l.fecha
                        FROM productos p
                        JOIN licitaciones l ON p.licitacion_id = l.id
                        LEFT JOIN tipos_licitacion t ON l.tipo_licitacion_id = t.id
                        WHERE p.resultado = 'Adjudicado' AND p.monodroga LIKE ?
                        ORDER BY l.fecha DESC
                    """, (f'%{filtro_monodroga}%',))
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
        
        return [{
            'numero_licitacion': p[0], 'tipo_licitacion': p[1] or '-', 'marca': p[2],
            'presentacion': p[3], 'cantidad': p[4], 'precio': p[5], 'fecha': p[6]
        } for p in productos]
    
    def obtener_productos_adjudicados(self) -> List[Dict[str, Any]]:
        """Obtiene productos adjudicados para dashboard"""
        with self.db.get_connection() as conn:
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
        
        return [{
            'numero_licitacion': p[0], 'tipo_licitacion': p[1] or '-', 'cliente': p[2] or '-',
            'monodroga': p[3], 'marca': p[4], 'presentacion': p[5],
            'cantidad': p[6], 'precio': p[7], 'fecha': p[8]
        } for p in productos]
