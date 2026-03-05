"""Constantes del sistema"""

# Estados de productos
class EstadoProducto:
    PARCIAL = 'Parcial'
    ADJUDICADO = 'Adjudicado'
    NO_ADJUDICADO = 'No Adjudicado'
    
    @classmethod
    def valores(cls):
        return [cls.PARCIAL, cls.ADJUDICADO, cls.NO_ADJUDICADO]

# Tipos de adjudicación
class TipoAdjudicacion:
    PARCIAL = 'Parcial'
    TOTAL = 'Total'
    
    @classmethod
    def valores(cls):
        return [cls.PARCIAL, cls.TOTAL]

# Producto a cotizar
class ProductoCotizar:
    PRINCIPAL = 'principal'
    ALTERNATIVA = 'alternativa'
    
    @classmethod
    def valores(cls):
        return [cls.PRINCIPAL, cls.ALTERNATIVA]

# Límites
class Limites:
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    MAX_FILES = 10
    ITEMS_PER_PAGE = 10
    MAX_ITEMS_PER_PAGE = 100

# Mensajes de error
class ErrorMessages:
    DATOS_INVALIDOS = 'Datos inválidos'
    NO_ENCONTRADO = 'Recurso no encontrado'
    ERROR_INTERNO = 'Error interno del servidor'
    REQUEST_VACIO = 'Request body no puede estar vacío'
    NUMERO_REQUERIDO = 'Número de licitación es requerido'
    MONTO_POLIZA_INVALIDO = 'Monto de póliza debe ser mayor a 0 si requiere póliza'
