# Licitarte - Sistema de Gestión de Licitaciones Farmacéuticas

**Versión 1.0.0** - Sistema profesional para gestionar licitaciones farmacéuticas con catálogo integrado de productos Celty.

[![Versión](https://img.shields.io/badge/versión-1.0.0-blue.svg)](https://github.com/Jorge-Loyo/Licitarte)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Licencia](https://img.shields.io/badge/licencia-Propietario-red.svg)](LICENSE)

## Características

- ✅ Gestión completa de licitaciones y productos
- ✅ Catálogo integrado de productos farmacéuticos Celty
- ✅ Gestión de clientes (CRUD completo)
- ✅ Gestión de oferentes (CRUD completo)
- ✅ Gestión de marcas (CRUD completo)
- ✅ Gestión de tipos de licitación (CRUD completo)
- ✅ Dashboard con estadísticas en tiempo real
- ✅ Histórico de precios con filtros avanzados
- ✅ Interfaz web responsive
- ✅ Soporte SQLite (local) y PostgreSQL (producción)
- ✅ Formato argentino de precios (punto miles, coma decimal)
- ✅ Carga masiva desde Excel (clientes, oferentes, marcas, tipos, catálogo)
- ✅ Paginación en todas las tablas

## Tecnologías

- **Backend**: Python 3.11, Flask
- **Base de Datos**: SQLite / PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Despliegue**: Gunicorn, Render.com

## Instalación Local

### Requisitos
- Python 3.11+
- pip

### Pasos

1. **Clonar repositorio**
```bash
git clone https://github.com/tu-usuario/Licitarte.git
cd Licitarte
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Instalar dependencias**
```bash
cd web
pip install -r requirements.txt
```

4. **Ejecutar aplicación**
```bash
python app.py
```

5. **Abrir navegador**
```
http://localhost:5000
```

## Estructura del Proyecto

```
Licitarte/
├── database/
│   ├── db_manager.py          # Gestor de base de datos
│   └── licitaciones.db        # Base de datos SQLite (local)
├── web/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css      # Estilos
│   │   ├── js/
│   │   │   ├── ingreso.js     # Nueva licitación
│   │   │   ├── gestion.js     # Gestión
│   │   │   ├── dashboard.js   # Dashboard
│   │   │   ├── administracion.js  # Administración
│   │   │   └── theme.js       # Tema claro/oscuro
│   │   └── img/
│   │       └── Logo_licitarte.png
│   ├── templates/
│   │   ├── base.html          # Template base
│   │   ├── dashboard.html     # Dashboard
│   │   ├── ingreso.html       # Nueva licitación
│   │   ├── gestion.html       # Gestión
│   │   ├── administracion.html # Administración
│   │   └── ayuda.html         # Manual de usuario
│   ├── app.py                 # Aplicación Flask
│   ├── requirements.txt       # Dependencias
│   └── init_production.py     # Script de inicialización
├── Data/
│   └── Celty.xlsx             # Catálogo de productos
├── .env.example               # Ejemplo de variables de entorno
├── .gitignore                 # Archivos ignorados
├── Procfile                   # Configuración Render
├── runtime.txt                # Versión Python
├── DEPLOY.md                  # Guía de despliegue
└── README.md                  # Este archivo
```

## Módulos

### 1. Dashboard
- Estadísticas en tiempo real (total licitaciones, ganadas, unidades, precio promedio)
- Productos adjudicados con paginación
- Histórico de precios con búsqueda y filtros
- Filtros por monodroga

### 2. Nueva Licitación
- Datos de licitación (N°, Cliente, Tipo, Fecha)
- Selección de cliente desde lista desplegable
- Selección de tipo de licitación
- Selección de productos desde catálogo Celty (Marca - Presentación)
- Auto-completado de monodroga capitalizada
- Auto-completado de marca ofrecida desde laboratorio
- Campos: Oferente Ganador, Marca Ganadora, Precio Ganador
- Múltiples productos por licitación
- Agregar nuevos oferentes/marcas/tipos sobre la marcha

### 3. Gestión
- Listar todas las licitaciones con paginación (10 por página)
- Buscar por N° o oferente
- Filtrar por tipo de licitación
- Columna "Ganancia" muestra items adjudicados/total (ej: 3/5)
- Ver detalle completo de productos
- Editar licitación (N°, Cliente, Tipo, Fecha)
- Editar productos (monodroga, marca, presentación, cantidad, precios, resultado, oferente, marca ganadora, marca ofrecida)
- Eliminar licitaciones

### 4. Administración
- **Clientes**: CRUD completo (nombre, razón social, CUIT, dirección, teléfono, email)
- **Oferentes**: CRUD completo con carga masiva desde Excel
- **Marcas**: CRUD completo con carga masiva desde Excel
- **Tipos de Licitación**: CRUD completo con carga masiva desde Excel
- **Catálogo Celty**: Visualización completa con búsqueda (N° Registro, Monodroga, Marca, Presentación, Laboratorio, Precio Caja, Precio Unitario, Fecha)
- **Carga Masiva**: Importar desde Excel para todas las entidades
- **Formato de Precios**: Argentino (punto miles, coma decimal)

### 5. Ayuda
- Manual de usuario completo actualizado
- Guías paso a paso para cada módulo
- Consejos y buenas prácticas
- Documentación de nuevas funcionalidades

## Base de Datos

### Tablas

#### clientes
- id, nombre, razon_social, cuit, direccion, telefono, email, activo

#### oferentes
- id, nombre, activo

#### marcas
- id, nombre, activo

#### tipos_licitacion
- id, nombre, activo

#### licitaciones
- id, numero_licitacion, cliente_id, tipo_licitacion_id, fecha, oferente_ganador, marca_ganadora, precio_ganador

#### productos
- id, licitacion_id, monodroga, marca, presentacion, cantidad, precio_ofertado, resultado, precio_ganador, oferente_ganador, marca_ofrecida, marca_ganadora

#### celty (catálogo)
- id, numero_registro, monodroga, marca, presentacion, laboratorio, precio_caja, precio_unitario, fecha

## Despliegue a Producción

Ver [DEPLOY.md](DEPLOY.md) para instrucciones detalladas.

### Resumen
1. Configurar PostgreSQL
2. Configurar variables de entorno
3. Desplegar en Render.com
4. Ejecutar script de inicialización

## Seguridad

- ✓ SECRET_KEY único por entorno
- ✓ Validación de datos de entrada
- ✓ Manejo seguro de errores
- ✓ Protección contra SQL injection (parametrización)
- ✓ Variables de entorno para credenciales

## Mantenimiento

### Actualizar Catálogo
```bash
python -c "from database.db_manager import DatabaseManager; db = DatabaseManager(); db.cargar_catalogo_desde_excel('Data/Celty.xlsx')"
```

### Backup Base de Datos
```bash
# SQLite
cp database/licitaciones.db database/backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

## Licencia

Propietario - Todos los derechos reservados

## Versión

**1.0.0** - Enero 2025

Ver [CHANGELOG.md](CHANGELOG.md) para historial completo de cambios.

## Autor

Jorge - Licitarte 2025

## Enlaces Útiles

- [Guía de Instalación](INSTALL.md)
- [Guía de Despliegue](DEPLOY.md)
- [Historial de Cambios](CHANGELOG.md)
- [Manual de Usuario](web/templates/ayuda.html) (disponible en la aplicación)
