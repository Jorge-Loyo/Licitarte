from pydantic import BaseModel, field_validator, Field
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
    
    @field_validator('resultado')
    @classmethod
    def validar_resultado(cls, v: str) -> str:
        if v not in ['Adjudicado', 'Parcial', 'No Adjudicado']:
            raise ValueError('Resultado debe ser: Adjudicado, Parcial o No Adjudicado')
        return v

class LicitacionCreateSchema(BaseModel):
    numero: str = Field(..., min_length=1, max_length=100)
    cliente_id: Optional[int] = None
    tipo_licitacion_id: Optional[int] = None
    fecha: str
    portal_origen: Optional[str] = None
    modalidad_entrega: Optional[str] = None
    forma_pago: Optional[str] = None
    requiere_poliza: bool = False
    monto_poliza: Optional[float] = Field(None, ge=0)
    observaciones: Optional[str] = None
    mantenimiento_oferta: Optional[str] = None
    productos: List[ProductoSchema] = Field(..., min_length=1)
    
    @field_validator('fecha')
    @classmethod
    def validar_fecha(cls, v: str) -> str:
        try:
            datetime.strptime(v.split()[0], '%Y-%m-%d')
            return v
        except Exception:
            raise ValueError('Formato de fecha inválido (YYYY-MM-DD)')
    
    @field_validator('productos')
    @classmethod
    def validar_renglones_unicos(cls, v: List[ProductoSchema]) -> List[ProductoSchema]:
        renglones = [p.numero_renglon for p in v if p.numero_renglon]
        if len(renglones) != len(set(renglones)):
            raise ValueError('Números de renglón duplicados')
        return v
