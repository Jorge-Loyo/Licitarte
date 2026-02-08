# 🛡️ FASE 3: MANEJO DE ERRORES Y LOGGING - Implementada

## ✅ Componentes Implementados

### 1. **Logging Estructurado**
- Logs en formato JSON para análisis
- Logs en texto plano para lectura humana
- Rotación automática (10MB, 5 backups)
- Niveles: INFO, WARNING, ERROR
- Metadata: request_id, user_id, timestamp

### 2. **Manejadores de Errores Centralizados**
- ValidationError (Pydantic) → 400
- Bad Request → 400
- Unauthorized → 401
- Forbidden → 403
- Not Found → 404
- Rate Limit → 429
- Internal Error → 500
- Excepciones no manejadas → 500

### 3. **Request Logging Middleware**
- Log de cada request entrante
- Tiempo de respuesta en ms
- Request ID único por request
- User ID si está autenticado
- Headers con X-Request-ID

---

## 📁 Archivos Creados

```
web/
├── src/
│   ├── utils/
│   │   ├── logging_config.py       ← Sistema de logging
│   │   └── error_handlers.py       ← Manejadores de errores
│   ├── middleware/
│   │   └── request_logging.py      ← Middleware de logging
│   └── validators.py                ← Validadores Pydantic
├── logs/                            ← Directorio de logs (auto-creado)
│   ├── app.log                      ← Logs en texto
│   └── app.json.log                 ← Logs en JSON
└── EJEMPLO_VALIDACION.py            ← Ejemplo de uso
```

---

## 📊 Formato de Logs

### Logs JSON (app.json.log)
```json
{
  "timestamp": "2025-02-08T18:30:45.123456",
  "level": "INFO",
  "logger": "licitarte",
  "message": "Request completed: POST /api/licitaciones",
  "module": "request_logging",
  "function": "after_request",
  "line": 25,
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "method": "POST",
  "path": "/api/licitaciones",
  "status_code": 201,
  "elapsed_ms": 45.23,
  "user_id": 1
}
```

### Logs Texto (app.log)
```
[2025-02-08 18:30:45,123] INFO in request_logging: Request completed: POST /api/licitaciones
[2025-02-08 18:30:46,456] ERROR in licitaciones: Error creating licitacion: Database error
```

---

## 🔍 Uso del Logger

### En cualquier módulo:
```python
from src.utils.logging_config import logger

# Info
logger.info("Usuario creado", extra={'user_id': 123})

# Warning
logger.warning("Intento de acceso no autorizado")

# Error con traceback
try:
    # código
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
```

---

## 🛡️ Manejo de Errores

### Automático
Todos los errores son capturados y loggeados automáticamente:

```python
@bp.route('/api/licitaciones', methods=['POST'])
def crear_licitacion():
    # Si hay ValidationError → 400 automático
    # Si hay Exception → 500 automático
    # Todo se loggea automáticamente
    pass
```

### Manual (recomendado)
```python
from pydantic import ValidationError
from src.utils.logging_config import logger

@bp.route('/api/licitaciones', methods=['POST'])
def crear_licitacion():
    try:
        data = LicitacionCreate(**request.json)
        # lógica
        logger.info(f"Licitacion created: {id}")
        return jsonify({'success': True}), 201
    except ValidationError as e:
        logger.warning(f"Validation error: {e.errors()}")
        return jsonify({'error': 'Datos inválidos', 'details': e.errors()}), 400
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return jsonify({'error': 'Error interno'}), 500
```

---

## 📈 Respuestas de Error Estandarizadas

### Validación (400)
```json
{
  "success": false,
  "error": "Datos inválidos",
  "details": [
    {
      "loc": ["numero"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### No autorizado (401)
```json
{
  "success": false,
  "error": "No autorizado"
}
```

### Rate limit (429)
```json
{
  "success": false,
  "error": "Demasiadas solicitudes. Intente más tarde."
}
```

### Error interno (500)
```json
{
  "success": false,
  "error": "Error interno del servidor"
}
```

---

## 🔧 Headers de Respuesta

Todas las respuestas incluyen:
```
X-Request-ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
X-RateLimit-Limit: 50
X-RateLimit-Remaining: 49
X-RateLimit-Reset: 1234567890
```

---

## 📊 Análisis de Logs

### Buscar errores:
```bash
grep "ERROR" logs/app.log
```

### Analizar JSON:
```bash
cat logs/app.json.log | jq '.level == "ERROR"'
```

### Requests lentos (>1000ms):
```bash
cat logs/app.json.log | jq 'select(.elapsed_ms > 1000)'
```

### Por usuario:
```bash
cat logs/app.json.log | jq 'select(.user_id == 1)'
```

---

## 🚀 Ventajas

### ✅ Debugging
- Request ID para rastrear requests completos
- Stack traces completos en logs
- Metadata contextual (user, endpoint, tiempo)

### ✅ Monitoreo
- Logs estructurados para herramientas (ELK, Splunk)
- Métricas de performance (elapsed_ms)
- Detección de patrones de error

### ✅ Seguridad
- Log de intentos de acceso no autorizado
- Rate limiting loggeado
- Auditoría de acciones

### ✅ Producción
- Rotación automática de logs
- No expone detalles internos al cliente
- Errores consistentes y profesionales

---

## 🔄 Rotación de Logs

**Automática**:
- Cada archivo: máximo 10MB
- Mantiene 5 backups
- Archivos antiguos: app.log.1, app.log.2, etc.

**Manual**:
```bash
# Limpiar logs antiguos
rm logs/app.log.*
rm logs/app.json.log.*
```

---

## 📝 Próximos Pasos (Fase 4)

- [ ] Integrar con servicio externo (Sentry, Datadog)
- [ ] Alertas automáticas por email
- [ ] Dashboard de métricas
- [ ] Tests de manejo de errores
- [ ] Documentación de errores para frontend

---

## 💡 Recomendaciones

1. **Producción**: Enviar logs a servicio externo (Sentry, CloudWatch)
2. **Desarrollo**: Revisar logs/app.log regularmente
3. **Debugging**: Usar X-Request-ID para rastrear requests
4. **Monitoreo**: Configurar alertas para errores 500

---

**Fecha**: 2025-02-08  
**Versión**: 1.3.0  
**Estado**: ✅ Fase 3 Completada
