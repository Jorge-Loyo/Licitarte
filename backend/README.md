# Backend - Licitarte

## Estructura Modular

```
backend/
├── api/
│   ├── models/          # Modelos de datos (User, etc.)
│   ├── routes/          # Blueprints Flask (solo validación + llamada a service)
│   ├── schemas/         # Pydantic schemas + DTOs
│   └── services/        # Lógica de negocio
├── database/            # Gestión de BD + migraciones
├── middleware/          # Request logging, auth, etc.
├── utils/               # Logging + error handlers
├── app.py              # Entry point
├── config.py           # Configuración
├── constants.py        # Constantes del sistema
└── validators.py       # Validaciones Pydantic
```

## Principios de Arquitectura

### 1. Separación de Responsabilidades

**Routes (Controladores):**
- Validación de entrada (Pydantic)
- Llamada a service
- Manejo de respuestas HTTP
- NO contiene lógica de negocio

**Services (Lógica de Negocio):**
- Toda la lógica de negocio
- Interacción con base de datos
- Transformación de datos
- Cálculos y validaciones complejas

**DTOs (Data Transfer Objects):**
- Estructuran respuestas API
- Consistencia en formato de datos
- Fácil serialización

### 2. Constantes Centralizadas

Archivo `constants.py` contiene:
- Estados de productos
- Tipos de adjudicación
- Límites del sistema
- Mensajes de error

### 3. Validaciones con Pydantic

- Validación automática de entrada
- Type hints
- Mensajes de error claros
- Usa constantes para valores permitidos

## Ejemplo de Uso

### Route (Controlador)
```python
@bp.route('', methods=['POST'])
@login_required
def crear_licitacion():
    if not request.json:
        return jsonify(ResponseDTO.error(ErrorMessages.REQUEST_VACIO)), 400
    
    try:
        data = LicitacionCreate(**request.json)
    except ValidationError as e:
        return jsonify(ResponseDTO.error(ErrorMessages.DATOS_INVALIDOS, e.errors())), 400
    
    try:
        licitacion_id = service.crear(data)
        return jsonify(ResponseDTO.success({'id': licitacion_id})), 201
    except Exception as e:
        return jsonify(ResponseDTO.error(ErrorMessages.ERROR_INTERNO)), 500
```

### Service (Lógica de Negocio)
```python
def crear(self, data: LicitacionCreate) -> int:
    licitacion_id = self.db.crear_licitacion(...)
    self._crear_productos(licitacion_id, data.productos)
    return licitacion_id

def _crear_productos(self, licitacion_id: int, productos: List) -> None:
    for producto in productos:
        producto_id = self.db.agregar_producto(...)
        for alternativa in producto.alternativas:
            self._crear_alternativa(producto_id, alternativa)
```

### DTO (Respuesta)
```python
class LicitacionDTO:
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'numero': self.numero,
            'fecha': self.fecha,
            'cliente': self.cliente or '-',
            'total_cotizado': self.total_cotizado
        }
```

## Refactorización Completada

### ✅ Licitaciones
- ✅ Service completo con toda la lógica
- ✅ Routes simplificadas (90 líneas vs 300+)
- ✅ DTOs para respuestas
- ✅ Usa constantes

### ⚠️ Pendiente (otros módulos)
- [ ] Productos service
- [ ] Catálogos service
- [ ] Estadísticas service
- [ ] Auth service

## Constantes Disponibles

```python
from backend.constants import EstadoProducto, TipoAdjudicacion, ErrorMessages

# Estados
EstadoProducto.PARCIAL
EstadoProducto.ADJUDICADO
EstadoProducto.NO_ADJUDICADO

# Tipos
TipoAdjudicacion.PARCIAL
TipoAdjudicacion.TOTAL

# Mensajes
ErrorMessages.DATOS_INVALIDOS
ErrorMessages.NO_ENCONTRADO
ErrorMessages.ERROR_INTERNO
```

## DTOs Disponibles

```python
from backend.api.schemas.dtos import ResponseDTO, LicitacionDTO

# Respuesta exitosa
ResponseDTO.success(data={'id': 123})

# Respuesta con error
ResponseDTO.error('Mensaje de error', details={...})

# DTO de licitación
dto = LicitacionDTO(id=1, numero='L-001', ...)
dto.to_dict()
```

## Próximos Pasos

1. **Crear services para otros módulos:**
   - ProductoService
   - CatalogoService
   - EstadisticaService
   - AuthService

2. **Agregar tests:**
   - Unit tests para services
   - Integration tests para routes

3. **Documentación API:**
   - Swagger/OpenAPI
   - Ejemplos de uso

4. **Optimizaciones:**
   - Caché de consultas frecuentes
   - Paginación en listados
   - Índices en BD
