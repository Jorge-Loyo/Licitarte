# Estructura del Proyecto - Licitarte v1.0.0

## 📁 Estructura de Directorios

```
Licitarte/
│
├── 📄 README.md                    # Documentación principal
├── 📄 CHANGELOG.md                 # Historial de cambios
├── 📄 INSTALL.md                   # Guía de instalación
├── 📄 VERSION                      # Archivo de versión (1.0.0)
├── 📄 .gitignore                   # Archivos ignorados por Git
├── 📄 .env.example                 # Plantilla de variables de entorno
├── 📄 Procfile                     # Configuración para Render.com
├── 📄 runtime.txt                  # Versión de Python para producción
├── 📄 requirements.txt             # Dependencias Python (desktop)
│
├── 📂 database/                    # Base de datos
│   ├── db_manager.py              # Gestor de base de datos (SQLite/PostgreSQL)
│   ├── licitaciones.db            # Base de datos SQLite (local, ignorado en Git)
│   └── __init__.py
│
├── 📂 web/                         # Aplicación web Flask
│   ├── app.py                     # Aplicación principal Flask
│   ├── requirements.txt           # Dependencias web
│   ├── init_production.py         # Script de inicialización producción
│   │
│   ├── 📂 static/                 # Archivos estáticos
│   │   ├── 📂 css/
│   │   │   └── style.css          # Estilos principales
│   │   ├── 📂 js/
│   │   │   ├── theme.js           # Tema claro/oscuro
│   │   │   ├── dashboard.js       # Lógica del dashboard
│   │   │   ├── ingreso.js         # Nueva licitación
│   │   │   ├── gestion.js         # Gestión de licitaciones
│   │   │   └── administracion.js  # Administración
│   │   └── 📂 img/
│   │       └── Logo_licitarte.png # Logo de la aplicación
│   │
│   ├── 📂 templates/              # Plantillas HTML
│   │   ├── base.html              # Plantilla base
│   │   ├── dashboard.html         # Dashboard
│   │   ├── ingreso.html           # Nueva licitación
│   │   ├── gestion.html           # Gestión
│   │   ├── administracion.html    # Administración
│   │   └── ayuda.html             # Manual de usuario
│   │
│   └── 📂 uploads/                # Archivos subidos (ignorado en Git)
│
├── 📂 Data/                        # Datos
│   └── Celty.xlsx                 # Catálogo de productos
│
├── 📂 Doc/                         # Documentación adicional
│   ├── DEPLOY.md                  # Guía de despliegue
│   ├── DEPLOY_RENDER.md           # Guía específica Render
│   ├── DISTRIBUCION.md            # Guía de distribución
│   └── MANUAL_USUARIO.md          # Manual de usuario detallado
│
├── 📂 modules/                     # Módulos desktop (legacy)
│   ├── __init__.py
│   ├── dashboard.py
│   ├── ingreso.py
│   ├── gestion.py
│   └── ayuda.py
│
├── 📂 Img/                         # Imágenes
│   └── Logo_licitarte.png
│
└── 📂 Licitarte_v1.0_Instalador/  # Instalador (ignorado en Git)
    └── ...
```

## 🗄️ Base de Datos

### Tablas Principales

1. **clientes**
   - Gestión de clientes
   - Campos: id, nombre, razon_social, cuit, direccion, telefono, email, activo

2. **oferentes**
   - Gestión de oferentes/laboratorios
   - Campos: id, nombre, activo

3. **marcas**
   - Gestión de marcas
   - Campos: id, nombre, activo

4. **tipos_licitacion**
   - Tipos de licitación
   - Campos: id, nombre, activo

5. **licitaciones**
   - Licitaciones principales
   - Campos: id, numero_licitacion, cliente_id, tipo_licitacion_id, fecha, oferente_ganador, marca_ganadora, precio_ganador

6. **productos**
   - Productos de cada licitación
   - Campos: id, licitacion_id, monodroga, marca, presentacion, cantidad, precio_ofertado, resultado, precio_ganador, oferente_ganador, marca_ofrecida, marca_ganadora

7. **celty**
   - Catálogo de productos Celty
   - Campos: id, numero_registro, monodroga, marca, presentacion, laboratorio, precio_caja, precio_unitario, fecha

## 🔗 Relaciones

```
clientes (1) ──────> (N) licitaciones
tipos_licitacion (1) ──> (N) licitaciones
licitaciones (1) ────> (N) productos
```

## 🚀 Endpoints API

### Licitaciones
- `GET /api/licitaciones` - Listar todas
- `POST /api/licitaciones` - Crear nueva
- `PUT /api/licitaciones/<id>` - Actualizar
- `DELETE /api/licitaciones/<id>` - Eliminar

### Productos
- `GET /api/productos/<licitacion_id>` - Listar por licitación
- `PUT /api/productos/<id>` - Actualizar producto

### Clientes
- `GET /api/clientes` - Listar todos
- `POST /api/clientes` - Crear nuevo
- `PUT /api/clientes/<id>` - Actualizar
- `DELETE /api/clientes/<id>` - Eliminar

### Oferentes
- `GET /api/oferentes` - Listar todos
- `POST /api/oferentes` - Crear nuevo
- `PUT /api/oferentes/<id>` - Actualizar
- `DELETE /api/oferentes/<id>` - Eliminar

### Marcas
- `GET /api/marcas` - Listar todas
- `POST /api/marcas` - Crear nueva
- `PUT /api/marcas/<id>` - Actualizar
- `DELETE /api/marcas/<id>` - Eliminar

### Tipos de Licitación
- `GET /api/tipos-licitacion` - Listar todos
- `POST /api/tipos-licitacion` - Crear nuevo
- `PUT /api/tipos-licitacion/<id>` - Actualizar
- `DELETE /api/tipos-licitacion/<id>` - Eliminar

### Catálogo
- `GET /api/catalogo` - Listar productos Celty
- `POST /api/catalogo` - Agregar producto

### Estadísticas
- `GET /api/estadisticas` - Estadísticas generales
- `POST /api/historico` - Histórico de precios
- `GET /api/productos-adjudicados` - Productos ganados

### Carga Masiva
- `POST /api/cargar-catalogo` - Cargar catálogo desde Excel
- `POST /api/cargar-clientes` - Cargar clientes desde Excel
- `POST /api/cargar-oferentes` - Cargar oferentes desde Excel
- `POST /api/cargar-marcas` - Cargar marcas desde Excel
- `POST /api/cargar-tipos-licitacion` - Cargar tipos desde Excel

## 🎨 Temas

- **Modo Oscuro** (por defecto)
- **Modo Claro** (toggle en sidebar)

## 📊 Paginación

- **Gestión**: 10 items por página
- **Dashboard - Productos Adjudicados**: 5 items por página
- **Dashboard - Histórico**: 5 items por página

## 🔒 Seguridad

- Validación de entrada en backend
- Parametrización de queries SQL (prevención SQL injection)
- SECRET_KEY único por entorno
- Variables de entorno para credenciales
- HTTPS en producción (Render.com)

## 🌐 Despliegue

### Desarrollo Local
- SQLite
- Flask development server
- Puerto 5000

### Producción (Render.com)
- PostgreSQL
- Gunicorn WSGI server
- Puerto configurable (variable PORT)
- Migración automática de base de datos

## 📦 Dependencias Principales

### Web (web/requirements.txt)
- Flask 3.0.0
- gunicorn 21.2.0
- psycopg2-binary 2.9.9
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- python-dotenv 1.0.0

### Desktop (requirements.txt - legacy)
- customtkinter 5.2.1
- Pillow >= 10.0.0
- pandas >= 2.0.0
- openpyxl >= 3.1.0

## 🔄 Flujo de Trabajo

1. **Usuario accede a la aplicación**
2. **Dashboard**: Ve estadísticas generales
3. **Nueva Licitación**: Crea licitación con productos
4. **Gestión**: Edita/elimina licitaciones
5. **Administración**: Gestiona catálogos y maestros
6. **Ayuda**: Consulta manual de usuario

## 📈 Escalabilidad

### Preparado para:
- ✅ Múltiples usuarios concurrentes
- ✅ Miles de licitaciones
- ✅ Catálogo extenso de productos
- ✅ Exportación de datos (futuro)
- ✅ Reportes personalizados (futuro)
- ✅ API REST para integraciones (futuro)

---

**Versión**: 1.0.0  
**Fecha**: Enero 2025  
**Autor**: Jorge
