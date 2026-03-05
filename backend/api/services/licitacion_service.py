"""Servicio de lógica de negocio para licitaciones"""
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from backend.database.db_manager import DatabaseManager, USE_POSTGRES
from backend.api.schemas.dtos import LicitacionDTO, LicitacionDetalleDTO
from backend.validators import LicitacionCreate
from backend.utils.logging_config import logger

class LicitacionService:
    def __init__(self):
        self.db = DatabaseManager(os.path.abspath('shared/database/licitaciones.db'))
    
    def obtener_todas(self) -> List[Dict[str, Any]]:
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
            licitaciones = cursor.fetchall()
            
            resultado = []
            for l in licitaciones:
                stats = self._obtener_estadisticas_productos(l[0])
                
                dto = LicitacionDTO(
                    id=l[0],
                    numero=l[1],
                    fecha=l[2],
                    oferente=l[3],
                    marca_ganadora=l[4],
                    precio_ganador=l[5],
                    cliente=l[6],
                    tipo_licitacion=l[7],
                    numero_presupuesto=l[8],
                    total_cotizado=stats['total_cotizado'],
                    ganancia=stats['ganancia']
                )
                resultado.append(dto.to_dict())
            
            return resultado
    
    def _obtener_estadisticas_productos(self, licitacion_id: int) -> Dict[str, Any]:
        """Obtiene estadísticas de productos de una licitación"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN resultado = 'Adjudicado' THEN 1 ELSE 0 END) as adjudicados,
                       COALESCE(SUM(precio_ofertado * cantidad), 0) as total_cotizado
                FROM productos WHERE licitacion_id = {}
            """.format('%s' if USE_POSTGRES else '?')
            
            cursor.execute(query, (licitacion_id,))
            stats = cursor.fetchone()
            
            if stats:
                total = stats[0] or 0
                adjudicados = stats[1] or 0
                total_cotizado = float(stats[2]) if stats[2] else 0.0
            else:
                total = 0
                adjudicados = 0
                total_cotizado = 0.0
            
            ganancia = f"{adjudicados}/{total}" if total > 0 else "-"
            
            return {
                'total': total,
                'adjudicados': adjudicados,
                'total_cotizado': total_cotizado,
                'ganancia': ganancia
            }
    
    def obtener_por_id(self, licitacion_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene una licitación por ID"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT l.numero_licitacion, c.nombre as cliente
                FROM licitaciones l
                LEFT JOIN clientes c ON l.cliente_id = c.id
                WHERE l.id = {}
            """.format('%s' if USE_POSTGRES else '?')
            
            cursor.execute(query, (licitacion_id,))
            row = cursor.fetchone()
            
            if row:
                return {'numero': row[0], 'cliente': row[1] or '-'}
            return None
    
    def obtener_detalle(self, licitacion_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene detalle completo de licitación"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT l.id, l.numero_licitacion, l.fecha, l.fecha_carga, l.cliente_id, l.tipo_licitacion_id,
                       l.portal_origen, l.modalidad_entrega, l.forma_pago, l.requiere_poliza, 
                       l.porcentaje_poliza, l.monto_poliza, l.observaciones, l.mantenimiento_oferta, l.tipo_adjudicacion
                FROM licitaciones l
                WHERE l.id = {}
            """.format('%s' if USE_POSTGRES else '?')
            
            cursor.execute(query, (licitacion_id,))
            row = cursor.fetchone()
            
            if row:
                dto = LicitacionDetalleDTO(
                    id=row[0], numero=row[1], fecha=row[2], fecha_carga=row[3],
                    cliente_id=row[4], tipo_licitacion_id=row[5], portal_origen=row[6],
                    modalidad_entrega=row[7], forma_pago=row[8], requiere_poliza=row[9],
                    porcentaje_poliza=row[10], monto_poliza=row[11], observaciones=row[12],
                    mantenimiento_oferta=row[13], tipo_adjudicacion=row[14]
                )
                return dto.to_dict()
            return None
    
    def crear(self, data: LicitacionCreate) -> int:
        """Crea una nueva licitación con productos (con transacción)"""
        logger.info(f"Creando licitación: {data.numero}")
        with self.db.get_connection() as conn:
            try:
                licitacion_id = self.db.crear_licitacion(
                    data.numero, data.fecha, '', '', None,
                    data.cliente_id, data.tipo_licitacion_id,
                    data.portal_origen or '', data.modalidad_entrega or '',
                    data.forma_pago or '', data.requiere_poliza,
                    data.porcentaje_poliza, data.monto_poliza,
                    data.observaciones or '', data.mantenimiento_oferta or '',
                    data.fecha_carga
                )
                
                self._crear_productos(licitacion_id, data.productos)
                
                conn.commit()
                logger.info(f"Licitación creada exitosamente: ID={licitacion_id}")
                return licitacion_id
            except Exception as e:
                conn.rollback()
                logger.error(f"Error creando licitación {data.numero}: {e}")
                raise e
    
    def _crear_productos(self, licitacion_id: int, productos: List) -> None:
        """Crea productos y alternativas de una licitación"""
        for producto in productos:
            producto_id = self.db.agregar_producto(
                licitacion_id,
                producto.monodroga,
                producto.marca,
                producto.presentacion,
                producto.cantidad,
                producto.precio,
                producto.resultado,
                None, '', 
                producto.marca_ofrecida or '', '', '',
                producto.numero_renglon or '',
                producto.costo_unitario,
                producto.margen_porcentaje,
                producto.observaciones or '',
                producto.producto_cotizar
            )
            
            for alternativa in getattr(producto, 'alternativas', []):
                self._crear_alternativa(producto_id, alternativa)
    
    def _crear_alternativa(self, producto_id: int, alternativa: Dict[str, Any]) -> None:
        """Crea una alternativa de producto"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO alternativas_productos 
                (producto_id, marca, presentacion, laboratorio, costo_unitario, margen_porcentaje, precio_ofertado, observaciones)
                VALUES ({}, {}, {}, {}, {}, {}, {}, {})
            """.format(*(['%s'] * 8 if USE_POSTGRES else ['?'] * 8))
            
            cursor.execute(query, (
                producto_id,
                alternativa.get('marca', ''),
                alternativa.get('presentacion', ''),
                alternativa.get('laboratorio', ''),
                float(alternativa['costo_unitario']) if alternativa.get('costo_unitario') else None,
                float(alternativa['margen_porcentaje']) if alternativa.get('margen_porcentaje') else None,
                float(alternativa['precio_ofertado']) if alternativa.get('precio_ofertado') else None,
                alternativa.get('observaciones', '')
            ))
    
    def actualizar(self, licitacion_id: int, data: Dict[str, Any]) -> None:
        """Actualiza una licitación existente"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            query = """
                UPDATE licitaciones 
                SET numero_licitacion={0}, fecha={0}, cliente_id={0}, tipo_licitacion_id={0},
                    portal_origen={0}, modalidad_entrega={0}, forma_pago={0},
                    requiere_poliza={0}, porcentaje_poliza={0}, monto_poliza={0}, observaciones={0}, 
                    mantenimiento_oferta={0}, tipo_adjudicacion={0}
                WHERE id={0}
            """.format('%s' if USE_POSTGRES else '?')
            
            cursor.execute(query, (
                data.get('numero'),
                data.get('fecha'),
                int(data['cliente_id']) if data.get('cliente_id') else None,
                int(data['tipo_licitacion_id']) if data.get('tipo_licitacion_id') else None,
                data.get('portal_origen', ''),
                data.get('modalidad_entrega', ''),
                data.get('forma_pago', ''),
                data.get('requiere_poliza', False),
                float(data['porcentaje_poliza']) if data.get('porcentaje_poliza') else None,
                float(data['monto_poliza']) if data.get('monto_poliza') else None,
                data.get('observaciones', ''),
                data.get('mantenimiento_oferta', ''),
                data.get('tipo_adjudicacion', 'Parcial'),
                licitacion_id
            ))
    
    def eliminar(self, licitacion_id: int) -> None:
        """Elimina una licitación"""
        logger.info(f"Eliminando licitación: ID={licitacion_id}")
        self.db.eliminar_licitacion(licitacion_id)
        logger.info(f"Licitación eliminada: ID={licitacion_id}")
