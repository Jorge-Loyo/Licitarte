"""Servicio para presupuestos, alternativas y ofertas"""
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from backend.database.db_manager import DatabaseManager, USE_POSTGRES

class ExtrasService:
    def __init__(self):
        self.db = DatabaseManager(os.path.abspath('shared/database/licitaciones.db'))
    
    # PRESUPUESTOS
    def obtener_siguiente_numero_presupuesto(self) -> int:
        return self.db.obtener_siguiente_numero_presupuesto()
    
    def obtener_presupuestos(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        presupuestos = self.db.obtener_presupuestos(limit, offset)
        return [{
            'numero': p[0], 'fecha': p[1], 'licitacion': p[2], 'cliente': p[3]
        } for p in presupuestos]
    
    def obtener_presupuesto_por_numero(self, numero: int) -> Optional[Dict[str, Any]]:
        return self.db.obtener_presupuesto_por_numero(numero)
    
    def crear_presupuesto(self, licitacion_id: int) -> int:
        return self.db.crear_presupuesto(licitacion_id)
    
    # ALTERNATIVAS
    def obtener_alternativas(self, producto_id: int) -> List[Dict[str, Any]]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT id, producto_id, marca, presentacion, laboratorio, costo_unitario, 
                       margen_porcentaje, precio_ofertado, observaciones
                FROM alternativas_productos WHERE producto_id = {}
            """.format('%s' if USE_POSTGRES else '?')
            
            cursor.execute(query, (producto_id,))
            alternativas = cursor.fetchall()
            
            return [{
                'id': a[0], 'producto_id': a[1], 'marca': a[2], 'presentacion': a[3],
                'laboratorio': a[4], 'costo_unitario': a[5], 'margen_porcentaje': a[6],
                'precio_ofertado': a[7], 'observaciones': a[8]
            } for a in alternativas]
    
    def crear_alternativa(self, data: Dict[str, Any]) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO alternativas_productos 
                (producto_id, marca, presentacion, laboratorio, costo_unitario, margen_porcentaje, precio_ofertado, observaciones)
                VALUES ({}, {}, {}, {}, {}, {}, {}, {})
            """.format(*(['%s'] * 8 if USE_POSTGRES else ['?'] * 8))
            
            if USE_POSTGRES:
                query += " RETURNING id"
            
            cursor.execute(query, (
                data['producto_id'], data.get('marca', ''), data.get('presentacion', ''),
                data.get('laboratorio', ''),
                float(data['costo_unitario']) if data.get('costo_unitario') else None,
                float(data['margen_porcentaje']) if data.get('margen_porcentaje') else None,
                float(data['precio_ofertado']) if data.get('precio_ofertado') else None,
                data.get('observaciones', '')
            ))
            
            if USE_POSTGRES:
                result = cursor.fetchone()
                return result[0] if result else None
            else:
                return getattr(cursor, 'lastrowid', None)
    
    def eliminar_alternativas_producto(self, producto_id: int) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = "DELETE FROM alternativas_productos WHERE producto_id = {}".format(
                '%s' if USE_POSTGRES else '?'
            )
            cursor.execute(query, (producto_id,))
    
    # OFERTAS
    def obtener_ofertas_producto(self, producto_id: int) -> List[Dict[str, Any]]:
        ofertas = self.db.obtener_ofertas_producto(producto_id)
        return [{
            'id': o[0], 'producto_id': o[1], 'oferente': o[2], 'laboratorio': o[3], 'precio': o[4]
        } for o in ofertas]
    
    def guardar_ofertas_producto(self, producto_id: int, ofertas: List[Dict[str, Any]]) -> None:
        self.db.guardar_ofertas_producto(producto_id, ofertas)
    
    # LICITACIONES RESUMEN
    def obtener_licitaciones_resumen(self) -> List[Dict[str, Any]]:
        licitaciones = self.db.obtener_licitaciones_resumen()
        return [{
            'id': l[0], 'numero': l[1], 'cliente': l[2] or '-',
            'total_productos': l[3] or 0, 'productos_ganados': l[4] or 0,
            'monto_cotizado': float(l[5]) if l[5] else 0.0,
            'monto_adjudicado': float(l[6]) if l[6] else 0.0
        } for l in licitaciones]
