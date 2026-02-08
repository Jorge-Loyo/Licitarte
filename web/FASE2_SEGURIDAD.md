# 🔐 FASE 2: SEGURIDAD - Implementada

## ✅ Componentes Instalados

### 1. **Flask-Login** - Autenticación de Usuarios
- Gestión de sesiones
- Protección de rutas con `@login_required`
- Usuario por defecto: `admin` / `admin123`

### 2. **Flask-Limiter** - Rate Limiting
- Límite: 200 requests/día, 50 requests/hora
- Protección contra ataques de fuerza bruta
- Headers de rate limit en respuestas

### 3. **Flask-CORS** - Cross-Origin Resource Sharing
- Configurado para localhost por defecto
- Soporta credenciales
- Configurable vía variable de entorno

### 4. **Pydantic** - Validación de Datos
- Validadores para licitaciones, productos, clientes
- Sanitización automática de inputs
- Mensajes de error descriptivos

---

## 📁 Archivos Creados

```
web/
├── security_config.py              ← Configuración de seguridad
├── migrate_usuarios.py             ← Migración tabla usuarios
├── requirements-security.txt       ← Dependencias de seguridad
├── src/
│   ├── models/
│   │   └── user.py                 ← Modelo de usuario
│   ├── routes/
│   │   └── auth.py                 ← Endpoints de autenticación
│   └── validators.py               ← Validadores Pydantic
└── templates/
    └── login.html                  ← Página de login
```

---

## 🚀 Instalación

### 1. Instalar Dependencias
```bash
cd web
pip install -r requirements-security.txt
```

### 2. Crear Tabla de Usuarios
```bash
python migrate_usuarios.py
```

### 3. Configurar Variables de Entorno (.env)
```bash
SECRET_KEY=tu-secret-key-super-segura-aqui
FLASK_ENV=development
CORS_ORIGINS=http://localhost:5000,http://127.0.0.1:5000
```

### 4. Iniciar Aplicación
```bash
python app.py
```

---

## 🔑 Endpoints de Autenticación

### POST `/api/auth/login`
```json
{
  "username": "admin",
  "password": "admin123",
  "remember": false
}
```

**Respuesta**:
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@licitarte.com"
  }
}
```

### POST `/api/auth/logout`
Requiere autenticación.

### GET `/api/auth/me`
Obtener usuario actual (requiere autenticación).

### GET `/api/auth/check`
Verificar si hay sesión activa.

---

## 🛡️ Protección de Rutas

Todas las rutas de vistas están protegidas con `@login_required`:
- `/dashboard`
- `/nueva-licitacion`
- `/gestion`
- `/administracion`
- etc.

Si no hay sesión activa, redirige a `/login`.

---

## 📊 Rate Limiting

**Límites por defecto**:
- 200 requests por día
- 50 requests por hora

**Headers de respuesta**:
```
X-RateLimit-Limit: 50
X-RateLimit-Remaining: 49
X-RateLimit-Reset: 1234567890
```

---

## ✅ Validación con Pydantic

### Ejemplo: Crear Licitación
```python
from src.validators import LicitacionCreate

@bp.route('/api/licitaciones', methods=['POST'])
def crear_licitacion():
    try:
        data = LicitacionCreate(**request.json)
        # data está validado y sanitizado
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
```

**Validaciones automáticas**:
- Campos requeridos
- Tipos de datos
- Longitud de strings
- Valores numéricos positivos
- Formato de email
- CUIT válido

---

## 🔐 Seguridad Implementada

### ✅ Autenticación
- Contraseñas hasheadas con Werkzeug
- Sesiones seguras con cookies HttpOnly
- Protección CSRF automática

### ✅ Rate Limiting
- Prevención de ataques de fuerza bruta
- Límites configurables por endpoint
- Storage en memoria (cambiar a Redis en producción)

### ✅ CORS
- Orígenes permitidos configurables
- Credenciales soportadas
- Headers seguros

### ✅ Validación
- Sanitización de inputs
- Prevención de SQL injection
- Validación de tipos y formatos

---

## 🚧 Pendiente (Fase 3)

- [ ] Manejo de errores centralizado
- [ ] Logging estructurado
- [ ] Tests de seguridad
- [ ] Roles y permisos
- [ ] 2FA (autenticación de dos factores)
- [ ] Auditoría de acciones

---

## 🔑 Credenciales por Defecto

**⚠️ CAMBIAR EN PRODUCCIÓN**

- **Usuario**: `admin`
- **Contraseña**: `admin123`
- **Email**: `admin@licitarte.com`

---

## 📝 Notas

1. **SECRET_KEY**: Generar una nueva en producción
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

2. **Rate Limiting**: Cambiar a Redis en producción
   ```python
   RATELIMIT_STORAGE_URL = "redis://localhost:6379"
   ```

3. **CORS**: Configurar orígenes permitidos en producción
   ```bash
   CORS_ORIGINS=https://tudominio.com,https://www.tudominio.com
   ```

---

**Fecha**: 2025-02-08  
**Versión**: 1.3.0  
**Estado**: ✅ Fase 2 Completada
