"""Servicio de lógica de negocio para catálogos"""
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from backend.database.db_manager import DatabaseManager
from backend.validators import ClienteCreate
from backend.utils.cache import cache, clear_cache

class CatalogoService:
    def __init__(self):
        self.db = DatabaseManager(os.path.abspath('shared/database/licitaciones.db'))
    
    # CLIENTES
    @cache(ttl_seconds=300)
    def obtener_clientes(self) -> List[Dict[str, Any]]:
        clientes = self.db.obtener_clientes()
        return [{
            'id': c[0], 'nombre': c[1], 'razon_social': c[2], 'cuit': c[3],
            'direccion': c[4], 'telefono': c[5], 'email': c[6],
            'organismo_jurisdiccion': c[7] if len(c) > 7 and c[7] is not None else ''
        } for c in clientes]
    
    def crear_cliente(self, data: ClienteCreate) -> int:
        clear_cache('obtener_clientes')
        return self.db.crear_cliente(
            data.nombre, data.razon_social or '', data.cuit,
            data.direccion or '', data.telefono or '', data.email or '',
            data.organismo_jurisdiccion
        )
    
    def actualizar_cliente(self, cliente_id: int, data: Dict[str, Any]) -> None:
        clear_cache('obtener_clientes')
        self.db.actualizar_cliente(
            cliente_id, data['nombre'], data.get('razon_social', ''),
            data.get('cuit', ''), data.get('direccion', ''),
            data.get('telefono', ''), data.get('email', ''),
            data.get('organismo_jurisdiccion', '')
        )
    
    def eliminar_cliente(self, cliente_id: int) -> None:
        clear_cache('obtener_clientes')
        self.db.eliminar_cliente(cliente_id)
    
    # OFERENTES
    @cache(ttl_seconds=300)
    def obtener_oferentes(self) -> List[Dict[str, Any]]:
        oferentes = self.db.obtener_oferentes()
        return [{'id': o[0], 'nombre': o[1]} for o in oferentes]
    
    def crear_oferente(self, nombre: str) -> int:
        return self.db.crear_oferente(nombre)
    
    def actualizar_oferente(self, oferente_id: int, nombre: str) -> None:
        self.db.actualizar_oferente(oferente_id, nombre)
    
    def eliminar_oferente(self, oferente_id: int) -> None:
        self.db.eliminar_oferente(oferente_id)
    
    # MARCAS
    @cache(ttl_seconds=300)
    def obtener_marcas(self) -> List[Dict[str, Any]]:
        marcas = self.db.obtener_marcas()
        return [{'id': m[0], 'nombre': m[1]} for m in marcas]
    
    def crear_marca(self, nombre: str) -> int:
        return self.db.crear_marca(nombre)
    
    def actualizar_marca(self, marca_id: int, nombre: str) -> None:
        self.db.actualizar_marca(marca_id, nombre)
    
    def eliminar_marca(self, marca_id: int) -> None:
        self.db.eliminar_marca(marca_id)
    
    # TIPOS LICITACION
    @cache(ttl_seconds=300)
    def obtener_tipos_licitacion(self) -> List[Dict[str, Any]]:
        tipos = self.db.obtener_tipos_licitacion()
        return [{'id': t[0], 'nombre': t[1]} for t in tipos]
    
    def crear_tipo_licitacion(self, nombre: str) -> int:
        return self.db.crear_tipo_licitacion(nombre)
    
    def actualizar_tipo_licitacion(self, tipo_id: int, nombre: str) -> None:
        self.db.actualizar_tipo_licitacion(tipo_id, nombre)
    
    def eliminar_tipo_licitacion(self, tipo_id: int) -> None:
        self.db.eliminar_tipo_licitacion(tipo_id)
    
    # CATALOGO MEDICAMENTOS
    def obtener_catalogo(self, page: int = 1, per_page: int = 50, search: str = '') -> Dict[str, Any]:
        offset = (page - 1) * per_page
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            if search:
                where = "WHERE monodroga LIKE %s OR marca LIKE %s OR laboratorio LIKE %s OR CAST(cod_monodroga AS TEXT) LIKE %s"
                params = (f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%')
            else:
                where = ""
                params = ()
            
            cursor.execute(f"SELECT COUNT(*) FROM medicamentos {where}", params)
            result = cursor.fetchone()
            total = result[0] if result else 0
            
            cursor.execute(f"""
                SELECT id, numero_registro, monodroga, marca, presentacion, laboratorio, 
                       precio_caja, precio_unitario, costo_unitario, fecha, troquel, cod_ab, troquel_ean,
                       cod_monodroga, cod_laboratorio, multidosis 
                FROM medicamentos {where}
                ORDER BY monodroga LIMIT %s OFFSET %s
            """, params + (per_page, offset))
            productos = cursor.fetchall()
        
        return {
            'productos': [self._medicamento_to_dict(p) for p in productos],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }
    
    def _medicamento_to_dict(self, p: tuple) -> Dict[str, Any]:
        return {
            'id': p[0], 'numero_registro': p[1], 'monodroga': p[2], 'marca': p[3],
            'presentacion': p[4], 'laboratorio': p[5], 'precio_caja': p[6],
            'precio_unitario': p[7], 'costo_unitario': p[8], 'fecha': p[9],
            'troquel': p[10], 'cod_ab': p[11], 'troquel_ean': p[12],
            'cod_ab_estado': 'Habilitado' if p[11] == 0 else 'Deshabilitado' if p[11] == 1 else None,
            'cod_monodroga': p[13], 'cod_laboratorio': p[14], 'multidosis': p[15]
        }
