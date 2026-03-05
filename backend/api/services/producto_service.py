"""Servicio de lógica de negocio para productos"""
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from backend.database.db_manager import DatabaseManager
from backend.validators import ProductoCreate

class ProductoService:
    def __init__(self):
        self.db = DatabaseManager(os.path.abspath('shared/database/licitaciones.db'))
    
    def obtener_por_licitacion(self, licitacion_id: int) -> List[Dict[str, Any]]:
        """Obtiene productos de una licitación"""
        productos = self.db.obtener_productos_licitacion(licitacion_id)
        return [self._producto_to_dict(p) for p in productos]
    
    def _producto_to_dict(self, p: tuple) -> Dict[str, Any]:
        """Convierte tupla de producto a diccionario"""
        return {
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
    
    def crear(self, data: ProductoCreate) -> int:
        """Crea un nuevo producto"""
        return self.db.agregar_producto(
            data.licitacion_id,
            data.monodroga,
            data.marca,
            data.presentacion,
            data.cantidad,
            data.precio,
            data.resultado,
            None, '',
            data.marca_ofrecida or '', '', '',
            data.numero_renglon or '',
            data.costo_unitario,
            data.margen_porcentaje,
            data.observaciones or '',
            data.producto_cotizar or 'principal'
        )
    
    def actualizar(self, producto_id: int, data: Dict[str, Any]) -> None:
        """Actualiza un producto existente"""
        self.db.actualizar_producto(
            producto_id,
            data.get('monodroga'),
            data.get('marca'),
            data.get('presentacion'),
            int(data['cantidad']) if data.get('cantidad') else 0,
            float(data['precio_ofertado']) if data.get('precio_ofertado') else 0,
            data.get('resultado', 'Parcial'),
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
