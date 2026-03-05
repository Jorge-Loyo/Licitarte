"""Esquemas de validación para licitaciones"""
from pydantic import BaseModel, validator, Field
from typing import Optional, List
from datetime import datetime

class ProductoSchema(BaseModel):
    monodroga: str = Field(..., min_length=1, max_length=200)
    marca: str = Field(..., min_length=1, max_length=100)
    presentacion: str = Field(..., min_length=1, max_length=200)
    cantidad: int = Field(..., gt=0)
    precio: float = Field(..., alias='precio_ofertado', ge=0)
    resultado: str = Field(default='Parcial')
    marca_ofrecida: Optional[str] = None
    numero_renglon: Optional[str] = None
    costo_unitario: Optional[float] = Field(None, ge=0)
    margen_porcentaje: Optional[float] = None
    observaciones: Optional[str] = None
    producto_cotizar: str = Field(default='principal')
    
    @validator('resultado')
    def validar_resultado(cls, v):
        if v not in ['Adjudicado', 'Parcial', 'No Adjudicado']:
            raise ValueError('Resultado inválido')
        return v

class LicitacionCreateSchema(BaseModel):
    numero: str = Field(..., min_length=1, max_length=100)
    cliente_id: Optional[int] = None
    tipo_licitacion_id: Optional[int] = None
    fecha: str
    fecha_carga: Optional[str] = None
    portal_origen: Optional[str] = None
    modalidad_entrega: Optional[str] = None
    forma_pago: Optional[str] = None
    requiere_poliza: bool = False
    porcentaje_poliza: Optional[float] = Field(None, ge=0)
    monto_poliza: Optional[float] = Field(None, ge=0)
    observaciones: Optional[str] = None
    mantenimiento_oferta: Optional[str] = None
    productos: List[ProductoSchema] = Field(..., min_length=1)
    
    @validator('fecha')
    def validar_fecha(cls, v):
        try:
            datetime.fromisoformat(v.split()[0])
            return v
        except:
            raise ValueError('Formato de fecha inválido (YYYY-MM-DD)')
