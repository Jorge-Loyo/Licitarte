"""Servicio de lógica de negocio para licitaciones"""
import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.database.db_manager import DatabaseManager

class LicitacionService:
    def __init__(self):
        self.db = DatabaseManager(os.path.abspath('shared/database/licitaciones.db'))
    
    def obtener_todas(self):
        """Obtiene todas las licitaciones con estadísticas"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT l.id, l.numero_licitacion, l.fecha, l.oferente_ganador, l.marca_ganadora, l.precio_ganador,
                       c.nombre as cliente, t.nombre as tipo_licitacion, l.numero_presupuesto
                FROM licitaciones l
                LEFT JOIN clientes c ON l.cliente_id = c.id
                LEFT JOIN tipos_licitacion t ON l.tipo_licitacion_id = t.id
                ORDER BY l.fecha DESC
            """)
            return cursor.fetchall()
    
    def crear(self, data):
        """Crea una nueva licitación con productos"""
        licitacion_id = self.db.crear_licitacion(
            data['numero'], data['fecha'], '', '', None,
            data.get('cliente_id'), data.get('tipo_licitacion_id'),
            data.get('portal_origen', ''), data.get('modalidad_entrega', ''),
            data.get('forma_pago', ''), data.get('requiere_poliza', False),
            data.get('monto_poliza'), data.get('observaciones', ''),
            data.get('mantenimiento_oferta', '')
        )
        
        for producto in data.get('productos', []):
            self.db.agregar_producto(
                licitacion_id, producto['monodroga'], producto['marca'],
                producto['presentacion'], producto['cantidad'], producto['precio'],
                producto['resultado'], producto.get('precio_ganador'),
                producto.get('oferente_ganador', ''), producto.get('marca_ofrecida', ''),
                producto.get('marca_ganadora', ''), producto.get('motivo_perdida', ''),
                producto.get('numero_renglon', ''), producto.get('costo_unitario'),
                producto.get('margen_porcentaje'), producto.get('observaciones', ''),
                producto.get('producto_cotizar', 'principal')
            )
        
        return {'id': licitacion_id}
