"""Validadores Pydantic para API"""
from pydantic import BaseModel, validator, Field
from typing import Optional, List
from datetime import datetime

class LicitacionCreate(BaseModel):
    numero: str = Field(..., min_length=1, max_length=100)
    fecha: str
    cliente_id: Optional[int] = None
    tipo_licitacion_id: Optional[int] = None
    portal_origen: Optional[str] = Field(None, max_length=100)
    modalidad_entrega: Optional[str] = Field(None, max_length=100)
    forma_pago: Optional[str] = Field(None, max_length=100)
    requiere_poliza: bool = False
    monto_poliza: Optional[float] = None
    observaciones: Optional[str] = None
    mantenimiento_oferta: Optional[str] = Field(None, max_length=100)
    
    @validator('numero')
    def numero_valido(cls, v):
        if not v or not v.strip():
            raise ValueError('Número de licitación no puede estar vacío')
        return v.strip()
    
    @validator('monto_poliza')
    def monto_poliza_valido(cls, v, values):
        if values.get('requiere_poliza') and (v is None or v <= 0):
            raise ValueError('Monto de póliza debe ser mayor a 0 si requiere póliza')
        return v

class ProductoCreate(BaseModel):
    monodroga: str = Field(..., min_length=1, max_length=200)
    marca: str = Field(..., min_length=1, max_length=200)
    presentacion: str = Field(..., min_length=1, max_length=200)
    cantidad: int = Field(..., gt=0)
    precio: float = Field(..., gt=0)
    resultado: str = Field(default='Parcial')
    marca_ofrecida: Optional[str] = Field(None, max_length=200)
    numero_renglon: Optional[str] = Field(None, max_length=50)
    costo_unitario: Optional[float] = Field(None, ge=0)
    margen_porcentaje: Optional[float] = None
    observaciones: Optional[str] = None
    
    @validator('resultado')
    def resultado_valido(cls, v):
        if v not in ['Parcial', 'Adjudicado', 'No Adjudicado']:
            raise ValueError('Resultado debe ser: Parcial, Adjudicado o No Adjudicado')
        return v

class ClienteCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200)
    razon_social: Optional[str] = Field(None, max_length=200)
    cuit: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=300)
    telefono: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    organismo_jurisdiccion: str = Field(..., min_length=1, max_length=100)
    
    @validator('email')
    def email_valido(cls, v):
        if v and '@' not in v:
            raise ValueError('Email inválido')
        return v
    
    @validator('cuit')
    def cuit_valido(cls, v):
        if v and not v.replace('-', '').isdigit():
            raise ValueError('CUIT debe contener solo números y guiones')
        return v

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    remember: bool = False
