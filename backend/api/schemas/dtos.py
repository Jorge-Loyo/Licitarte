"""Data Transfer Objects para respuestas API"""
from typing import Optional, List, Dict, Any

class LicitacionDTO:
    """DTO para licitación en listado"""
    def __init__(self, id: int, numero: str, fecha: str, cliente: str, 
                 tipo_licitacion: str, total_cotizado: float, ganancia: str,
                 oferente: Optional[str] = None, marca_ganadora: Optional[str] = None,
                 precio_ganador: Optional[float] = None, numero_presupuesto: Optional[int] = None):
        self.id = id
        self.numero = numero
        self.fecha = fecha
        self.cliente = cliente
        self.tipo_licitacion = tipo_licitacion
        self.total_cotizado = total_cotizado
        self.ganancia = ganancia
        self.oferente = oferente
        self.marca_ganadora = marca_ganadora
        self.precio_ganador = precio_ganador
        self.numero_presupuesto = numero_presupuesto
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'numero': self.numero,
            'fecha': self.fecha,
            'cliente': self.cliente or '-',
            'tipo_licitacion': self.tipo_licitacion or '-',
            'total_cotizado': self.total_cotizado,
            'ganancia': self.ganancia,
            'oferente': self.oferente,
            'marca_ganadora': self.marca_ganadora,
            'precio_ganador': self.precio_ganador,
            'numero_presupuesto': self.numero_presupuesto
        }

class LicitacionDetalleDTO:
    """DTO para detalle completo de licitación"""
    def __init__(self, id: int, numero: str, fecha: str, fecha_carga: Optional[str],
                 cliente_id: Optional[int], tipo_licitacion_id: Optional[int],
                 portal_origen: Optional[str], modalidad_entrega: Optional[str],
                 forma_pago: Optional[str], requiere_poliza: bool,
                 porcentaje_poliza: Optional[float], monto_poliza: Optional[float],
                 observaciones: Optional[str], mantenimiento_oferta: Optional[str],
                 tipo_adjudicacion: Optional[str]):
        self.id = id
        self.numero = numero
        self.fecha = fecha
        self.fecha_carga = fecha_carga
        self.cliente_id = cliente_id
        self.tipo_licitacion_id = tipo_licitacion_id
        self.portal_origen = portal_origen
        self.modalidad_entrega = modalidad_entrega
        self.forma_pago = forma_pago
        self.requiere_poliza = requiere_poliza
        self.porcentaje_poliza = porcentaje_poliza
        self.monto_poliza = monto_poliza
        self.observaciones = observaciones
        self.mantenimiento_oferta = mantenimiento_oferta
        self.tipo_adjudicacion = tipo_adjudicacion
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'numero': self.numero,
            'fecha': self.fecha,
            'fecha_carga': self.fecha_carga,
            'cliente_id': self.cliente_id,
            'tipo_licitacion_id': self.tipo_licitacion_id,
            'portal_origen': self.portal_origen,
            'modalidad_entrega': self.modalidad_entrega,
            'forma_pago': self.forma_pago,
            'requiere_poliza': self.requiere_poliza,
            'porcentaje_poliza': self.porcentaje_poliza,
            'monto_poliza': self.monto_poliza,
            'observaciones': self.observaciones,
            'mantenimiento_oferta': self.mantenimiento_oferta,
            'tipo_adjudicacion': self.tipo_adjudicacion
        }

class ResponseDTO:
    """DTO genérico para respuestas"""
    @staticmethod
    def success(data: Any = None, message: str = None) -> Dict[str, Any]:
        response = {'success': True}
        if data is not None:
            response['data'] = data
        if message:
            response['message'] = message
        return response
    
    @staticmethod
    def error(message: str, details: Any = None) -> Dict[str, Any]:
        response = {'success': False, 'error': message}
        if details:
            response['details'] = details
        return response
