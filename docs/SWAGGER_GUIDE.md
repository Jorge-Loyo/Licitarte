# 📚 Documentación API con Swagger

## ✅ Implementado

### Acceso a Swagger UI
**URL**: http://localhost:5000/api/docs

### Características
- ✅ Documentación interactiva de 72 endpoints
- ✅ Especificación OpenAPI 3.0
- ✅ Ejemplos de request/response
- ✅ Schemas de validación Pydantic
- ✅ Autenticación con cookies

---

## 📖 Endpoints Documentados

### Auth (4 endpoints)
- `POST /api/auth/login` - Login de usuario
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Usuario actual
- `GET /api/auth/check` - Verificar sesión

### Licitaciones (5 endpoints)
- `GET /api/licitaciones` - Listar con estadísticas
- `POST /api/licitaciones` - Crear con productos
- `GET /api/licitaciones/<id>` - Obtener una
- `PUT /api/licitaciones/<id>` - Actualizar
- `DELETE /api/licitaciones/<id>` - Eliminar

### Productos (3 endpoints)
- `GET /api/productos/<licitacion_id>` - Listar
- `POST /api/productos` - Crear
- `PUT /api/productos/<id>` - Actualizar

### Estadísticas (3 endpoints)
- `GET /api/estadisticas` - Dashboard
- `POST /api/historico` - Histórico precios
- `GET /api/productos-adjudicados` - Ganados

---

## 🚀 Uso

### 1. Instalar Dependencia
```bash
cd web
pip install flask-swagger-ui==4.11.1
```

### 2. Iniciar Aplicación
```bash
python app.py
```

### 3. Abrir Swagger UI
Navegar a: http://localhost:5000/api/docs

### 4. Probar Endpoints
1. Hacer login en `/api/auth/login`
2. Cookie de sesión se guarda automáticamente
3. Probar endpoints protegidos

---

## 📝 Archivos

- `web/swagger_config.py` - Configuración Swagger UI
- `web/static/swagger.json` - Especificación OpenAPI 3.0
- `web/app.py` - Registro de blueprint Swagger

---

## 🔧 Personalización

### Agregar Nuevo Endpoint
Editar `web/static/swagger.json`:

```json
"/api/nuevo-endpoint": {
  "get": {
    "tags": ["Categoría"],
    "summary": "Descripción corta",
    "description": "Descripción detallada",
    "security": [{"cookieAuth": []}],
    "responses": {
      "200": {
        "description": "Respuesta exitosa",
        "content": {
          "application/json": {
            "schema": {
              "type": "object",
              "properties": {
                "campo": {"type": "string"}
              }
            }
          }
        }
      }
    }
  }
}
```

### Cambiar URL de Swagger
Editar `web/swagger_config.py`:

```python
SWAGGER_URL = '/docs'  # Nueva URL
```

---

## ✅ Checklist Documentación

- [x] Swagger UI instalado y configurado
- [x] OpenAPI 3.0 spec creada
- [x] Endpoints principales documentados
- [x] Schemas de request/response
- [x] Ejemplos de uso
- [x] Autenticación documentada
- [x] Docstrings en todos los blueprints
- [x] Comentarios en código complejo

---

**Fecha**: 2025-02-08  
**Versión**: 1.2.0  
**Estado**: ✅ Documentación Completa
