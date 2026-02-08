# 📘 LICITARTE - Documentación Completa

## 🎯 Descripción General

**Licitarte** es un sistema profesional para gestionar licitaciones farmacéuticas con análisis de márgenes, métricas avanzadas y seguimiento completo del proceso de cotización.

- **Versión Actual**: 1.2.0 (Web) / 1.0.0 (Desktop)
- **Tecnologías**: Python 3.11, Flask 3.0, SQLite/PostgreSQL
- **Estado**: ✅ Producción Ready
- **Arquitectura**: Dual (Web + Desktop) con código compartido

---

## 📁 Estructura del Proyecto

```
Licitarte/
├── web/                          # Aplicación Web (v1.2.0) - PRINCIPAL
│   ├── static/
│   │   ├── css/style.css        # Estilos modernizados
│   │   ├── js/                  # JavaScript modular
│   │   │   ├── dashboard.js     # Dashboard con 6 indicadores
│   │   │   ├── ingreso.js       # Nueva licitación + análisis márgenes
│   │   │   ├── gestion.js       # Gestión con diferencias vs ganador
│   │   │   ├── metricas.js      # Ranking pérdidas + diferencias promedio
│   │   │   ├── administracion.js # CRUD 11 catálogos
│   │   │   └── theme.js         # Tema claro/oscuro
│   │   └── img/Logo_licitarte.png
│   ├── templates/               # Vistas HTML
│   │   ├── base.html           # Template base con menú lateral
│   │   ├── dashboard.html      # 6 indicadores + histórico
│   │   ├── ingreso.html        # Formulario con alertas margen
│   │   ├── gestion.html        # Tabla licitaciones + detalle productos
│   │   ├── metricas.html       # Análisis competitividad
│   │   ├── administracion.html # 11 tabs de catálogos
│   │   └── ayuda.html          # Manual usuario v1.2.0
│   ├── schemas/                # Validación Pydantic
│   │   ├── licitacion_schema.py
│   │   └── __init__.py
│   ├── tests/                  # Tests pytest (28% coverage)
│   │   ├── conftest.py
│   │   ├── test_licitaciones.py
│   │   └── test_schemas.py
│   ├── utils/                  # Utilidades
│   │   ├── logger.py           # Sistema logs con rotación
│   │   └── __init__.py
│   ├── app.py                  # Aplicación Flask (78 líneas)
│   ├── config.py               # Configuración entornos
│   ├── requirements.txt        # Dependencias web
│   ├── pytest.ini              # Config pytest
│   └── .env                    # Variables entorno (no en git)
│
├── desktop/                     # Aplicación Desktop (v1.0.0) - LEGACY
│   ├── src/
│   │   └── modules/            # Módulos CustomTkinter
│   │       ├── dashboard.py
│   │       ├── ingreso.py
│   │       ├── gestion.py
│   │       └── ayuda.py
│   ├── assets/
│   │   └── Img/Logo_licitarte.png
│   ├── main.py                 # Punto entrada desktop
│   ├── Licitarte.spec          # Config PyInstaller
│   ├── build_exe.bat           # Script compilación
│   └── requirements.txt        # Dependencias desktop
│
├── shared/                      # Código Compartido
│   ├── database/
│   │   ├── migrations/         # Sistema versionado migraciones
│   │   │   ├── 001_initial_schema.sql
│   │   │   └── migrate.py      # Gestor migraciones
│   │   ├── db_manager.py       # Gestor BD (SQLite/PostgreSQL)
│   │   ├── licitaciones.db     # Base datos SQLite
│   │   └── __init__.py
│   ├── models/                 # Modelos compartidos (futuro)
│   │   └── __init__.py
│   └── __init__.py
│
├── data/                        # Datos y Backups
│   ├── Celty.xlsx              # Catálogo productos
│   ├── backups/                # Backups automáticos
│   │   ├── fase5_backup_*/
│   │   └── fase6_backup_*/
│   └── README.md
│
├── docs/                        # Documentación
│   ├── Licitarte_doc.md        # Este archivo
│   ├── FASE_4_COMPLETADA.md
│   ├── FASE_5_COMPLETADA.md
│   ├── FASE_6_COMPLETADA.md
│   └── README.md
│
├── scripts/                     # Scripts utilidad
│   ├── setup_dev.sh            # Setup desarrollo
│   ├── setup_prod.sh           # Setup producción
│   ├── backup_db.sh            # Backup BD
│   ├── migrate_db.sh           # Ejecutar migraciones
│   ├── fase5_limpieza.bat
│   └── fase6_limpieza_scripts.bat
│
├── .gitignore                   # Archivos ignorados
├── README.md                    # README principal
├── CHANGELOG.md                 # Historial cambios
├── VERSION                      # Versión actual
├── Procfile                     # Deploy Render
├── runtime.txt                  # Python version
└── docker-compose.yml           # PostgreSQL local
```

---

## 🗄️ Base de Datos

### Tablas Principales

#### **clientes**
```sql
id, nombre, razon_social, cuit, direccion, telefono, email, 
organismo_jurisdiccion, activo
```
- Gestión de clientes con organismo/jurisdicción
- Auto-completa organismo al seleccionar cliente en licitación

#### **licitaciones**
```sql
id, numero_licitacion, cliente_id, tipo_licitacion_id, fecha,
oferente_ganador, marca_ganadora, precio_ganador,
portal_origen, modalidad_entrega, forma_pago,
requiere_poliza, monto_poliza, observaciones,
mantenimiento_oferta, numero_presupuesto, tipo_adjudicacion
```
- Datos completos de licitación
- Campos v2.0: portal, modalidad, forma pago, póliza

#### **productos**
```sql
id, licitacion_id, monodroga, marca, presentacion, cantidad,
precio_ofertado, resultado, precio_ganador, oferente_ganador,
marca_ofrecida, marca_ganadora, motivo_perdida, numero_renglon,
costo_unitario, margen_porcentaje, observaciones, producto_cotizar
```
- Productos de cada licitación
- Análisis de margen: costo_unitario, margen_porcentaje
- Diferencias vs ganador: calculadas en frontend

#### **celty** (Catálogo)
```sql
id, numero_registro, monodroga, marca, presentacion, laboratorio,
precio_caja, precio_unitario, costo_unitario, fecha
```
- Catálogo productos Celty
- costo_unitario: editable solo manualmente (no se sobrescribe con Excel)

#### **alternativas_productos**
```sql
id, producto_id, marca, presentacion, laboratorio,
costo_unitario, margen_porcentaje, precio_ofertado, observaciones
```
- Productos alternativos por renglón

#### **ofertas_productos**
```sql
id, producto_id, oferente, laboratorio, precio
```
- Ofertas de competidores por producto

#### **presupuestos**
```sql
id, numero, licitacion_id, fecha_generacion
```
- Presupuestos generados

### Catálogos Configurables

- **oferentes**: Laboratorios oferentes
- **marcas**: Marcas de productos
- **tipos_licitacion**: Tipos de licitación
- **organismos_jurisdiccion**: Nacional, Provincial, Municipal, CABA, Privado
- **portales_origen**: Comprar, BAC, Otro
- **modalidades_entrega**: Única, Múltiple, Programada
- **formas_pago**: Contado, 30 días, 60 días
- **motivos_perdida**: Precio más alto, Marca no priorizada, etc.
- **mantenimientos_oferta**: Catálogo mantenimiento oferta

---

## 🎨 Funcionalidades Principales

### 1. Dashboard (📊)
**Archivo**: `web/templates/dashboard.html` + `web/static/js/dashboard.js`

**6 Indicadores Clave**:
- Unidades Cotizadas
- Unidades Ganadas
- % Unidades Ganadas
- Total Cotizado (formato MILL)
- Total Ganado (formato MILL)
- % Dinero Ganado

**Formato MILL**: Montos ≥ $1.000.000 → $200,00 MILL

**Histórico de Productos**:
- Búsqueda por monodroga
- Paginación (5 por página)
- Filtros avanzados

**Productos Adjudicados**:
- Tabla con últimos productos ganados
- Paginación (5 por página)

### 2. Nueva Licitación (➕)
**Archivo**: `web/templates/ingreso.html` + `web/static/js/ingreso.js`

**Datos de Licitación**:
- N° Licitación, Cliente, Organismo (auto-completa)
- Tipo, Fecha, Hora Apertura
- Portal/Origen, Modalidad Entrega, Forma Pago
- Mantenimiento Oferta, Tipo Adjudicación
- Póliza: checkbox + % + monto calculado
- Observaciones

**Productos**:
- Selección de catálogo (Marca - Presentación)
- Monodroga auto-completa capitalizada
- Cantidad, Precio Ofertado
- **⚠️ ANÁLISIS DE MARGEN** (tiempo real):
  - 🔴 ROJO: Precio ≤ costo (pérdida)
  - 🟡 AMARILLO: Margen < 8% (bajo)
  - 🟢 VERDE: Margen ≥ 8% (aceptable)
- Resultado: Parcial (defecto) / Adjudicado / No Adjudicado
- Marca Ofrecida (defecto: "Celtyc")
- Oferente Ganador, Marca Ganadora, Precio Ganador
- Motivo Pérdida (si No Adjudicado)

**Lógica de Resultado**:
- **Adjudicado**: Auto-completa Oferente="Ganada", Marca=Marca Ofrecida, Precio=Precio Ofertado (campos deshabilitados)
- **No Adjudicado**: Requiere todos campos + Motivo Pérdida
- **Parcial**: Campos habilitados sin requerirlos

**Margen Total de Ganancia**:
- Costo Total, Precio Total, Margen $ y %
- Visible si hay costos unitarios

**Vista Previa Oferta**:
- Genera documento HTML con todos los datos
- Descarga PDF

### 3. Gestión (📋)
**Archivo**: `web/templates/gestion.html` + `web/static/js/gestion.js`

**Tabla Licitaciones**:
- N° Licitación, Cliente, Tipo, Fecha
- **Total Cotizado** (formato MILL)
- Presupuesto N°
- Paginación (10 por página)
- Búsqueda por N° o cliente
- Filtro por tipo

**Detalle de Licitación**:
- Modal con todos los productos
- Columnas: Monodroga, Marca-Presentación, Cantidad, Precio Oferta, Total $
- Observaciones, Ganador, Precio, Laboratorio
- **Dif. $** y **Dif. %** (solo No Adjudicado)

**Editar Producto**:
- Modal con 3 secciones:
  1. **DATOS DEL PRODUCTO**: Selección catálogo, monodroga, marca, presentación, marca ofrecida
  2. **MI OFERTA**: Cantidad, precio, resultado, análisis margen
  3. **DATOS DEL GANADOR**: Oferente, marca, precio, diferencias, motivo pérdida

**Agregar Producto**:
- Botón ➕ para agregar productos a licitación existente

**Editar Licitación**:
- Modificar datos principales

**Eliminar**:
- Elimina licitación completa con confirmación

### 4. Métricas (📈)
**Archivo**: `web/templates/metricas.html` + `web/static/js/metricas.js`

**Diferencias Promedio**:
- Diferencia Promedio $ (formato MILL)
- Diferencia Promedio %
- Solo productos No Adjudicados

**Ranking de Causas de Pérdidas**:
- Tabla ordenada por cantidad
- Columnas: #, Motivo, Cantidad, %
- Análisis de competitividad

### 5. Administración (⚙️)
**Archivo**: `web/templates/administracion.html` + `web/static/js/administracion.js`

**11 Tabs de Catálogos**:
1. **Clientes**: nombre*, organismo*, razón social*, CUIT, dirección, teléfono, email
2. **Catálogo Productos**: N° Registro, Monodroga, Marca, Presentación, Laboratorio, Precios, **Costo Unitario**, Fecha
3. **Oferentes**: CRUD + carga Excel
4. **Marcas**: CRUD + carga Excel
5. **Tipos Licitación**: CRUD + carga Excel
6. **Organismos/Jurisdicción**: CRUD
7. **Portales/Origen**: CRUD
8. **Modalidades Entrega**: CRUD
9. **Formas de Pago**: CRUD
10. **Motivos Pérdida**: CRUD
11. **Mantenimiento Oferta**: CRUD

**Funcionalidades**:
- Crear, Editar, Eliminar
- Carga masiva Excel (clientes, oferentes, marcas, tipos, catálogo)
- Búsqueda en tiempo real
- Scroll lateral + header sticky (catálogo)

**Catálogo Productos**:
- **Costo Unitario**: Editable solo manualmente
- Excel NO sobrescribe costo_unitario
- Fecha se mantiene al editar

### 6. Documentación (📑)
**Archivo**: `web/templates/documentacion.html` + `web/static/js/documentacion.js`

**Presupuestos Generados**:
- Tabla con N°, Licitación, Cliente, Fecha
- Búsqueda
- Paginación
- Ver/Imprimir presupuesto

### 7. Pólizas (📄)
**Archivo**: `web/templates/polizas.html`

**Estado**: 🚧 Módulo en desarrollo

**Funcionalidades Próximas**:
- Registro pólizas por licitación
- Seguimiento estados
- Alertas vencimiento
- Gestión documentos

---

## 🔧 Arquitectura Técnica

### Backend (Flask)

**app.py** (78 líneas):
```python
from flask import Flask, render_template
from src.routes import register_routes

app = Flask(__name__)
register_routes(app)  # Blueprints modulares

# Rutas de vistas (templates)
@app.route('/')
def index():
    return render_template('dashboard.html')
```

**Blueprints** (web/src/routes/):
- `licitaciones.py`: CRUD licitaciones
- `productos.py`: CRUD productos
- `clientes.py`: CRUD clientes
- `catalogos.py`: CRUD catálogos
- `estadisticas.py`: Dashboard
- `presupuestos.py`: Presupuestos
- `__init__.py`: Registro blueprints

**Validación** (web/schemas/):
- Pydantic para validación datos
- `LicitacionCreateSchema`, `ProductoSchema`

**Logging** (web/utils/logger.py):
- Sistema logs con rotación
- Archivos en `web/logs/`
- Formato: `[timestamp] LEVEL in module: message`

### Frontend

**JavaScript Modular**:
- `dashboard.js`: 6 indicadores + histórico + paginación
- `ingreso.js`: Formulario + análisis margen + vista previa
- `gestion.js`: Tabla + detalle + edición + diferencias
- `metricas.js`: Ranking + diferencias promedio
- `administracion.js`: 11 tabs CRUD + carga Excel
- `theme.js`: Tema claro/oscuro

**CSS** (web/static/css/style.css):
- Variables CSS para temas
- Scrollbars personalizados
- Modales modernizados
- Responsive design

**Notificaciones Custom**:
- Reemplazo de `alert()` nativo
- Modal estilizado
- Títulos con íconos (✓ Éxito, ✗ Error)

### Base de Datos

**db_manager.py** (shared/database/):
- Clase `DatabaseManager`
- Soporte dual: SQLite (local) / PostgreSQL (producción)
- Context managers para conexiones
- Métodos CRUD para todas las tablas
- Validaciones en backend

**Migraciones** (shared/database/migrations/):
- Sistema versionado con `migrate.py`
- Tabla `schema_migrations` para control
- Archivos SQL numerados: `001_initial_schema.sql`

**Detección Entorno**:
```python
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    USE_POSTGRES = True  # Producción
else:
    USE_POSTGRES = False  # Local SQLite
```

---

## 📊 Cálculos Clave

### Análisis de Margen
```javascript
const costoUnitario = producto.costo_unitario;
const precioOfertado = parseFloat(input.value);

if (precioOfertado <= costoUnitario) {
    // 🔴 ROJO: Pérdida
    margen = ((precioOfertado - costoUnitario) / costoUnitario) * 100;
    alerta = "PÉRDIDA";
} else {
    margen = ((precioOfertado - costoUnitario) / costoUnitario) * 100;
    if (margen < 8) {
        // 🟡 AMARILLO: Margen bajo
        alerta = "MARGEN BAJO";
    } else {
        // 🟢 VERDE: Margen aceptable
        alerta = "MARGEN ACEPTABLE";
    }
}
```

### Diferencias vs Ganador
```javascript
const diferenciaPesos = precioOfertado - precioGanador;
const diferenciaPorcentaje = (diferenciaPesos / precioGanador) * 100;
```

### Formato MILL
```javascript
function formatearMontoMILL(valor) {
    if (valor >= 1000000) {
        return '$' + (valor / 1000000).toFixed(2).replace('.', ',') + ' MILL';
    }
    return '$' + valor.toLocaleString('es-AR', {minimumFractionDigits: 2});
}
```

### Total Cotizado
```sql
SELECT SUM(precio_ofertado * cantidad) 
FROM productos 
WHERE licitacion_id = ?
```

### Estadísticas Dashboard
```python
def obtener_estadisticas():
    unidades_cotizadas = SUM(cantidad)
    unidades_ganadas = SUM(cantidad WHERE resultado='Adjudicado')
    porcentaje_unidades = (unidades_ganadas / unidades_cotizadas) * 100
    
    total_cotizado = SUM(precio_ofertado * cantidad)
    total_ganado = SUM(precio_ofertado * cantidad WHERE resultado='Adjudicado')
    porcentaje_dinero = (total_ganado / total_cotizado) * 100
```

---

## 🚀 Flujo de Trabajo

### 1. Nueva Licitación
```
Usuario → Ingreso → Selecciona Cliente → Auto-completa Organismo
       → Completa datos licitación (portal, modalidad, forma pago, póliza)
       → Agrega productos del catálogo
       → Sistema calcula margen en tiempo real
       → Alerta visual según margen (rojo/amarillo/verde)
       → Selecciona resultado (Adjudicado/Parcial/No Adjudicado)
       → Si Adjudicado: auto-completa ganador
       → Si No Adjudicado: requiere motivo pérdida
       → Vista previa oferta
       → Guardar → BD
```

### 2. Gestión de Licitación
```
Usuario → Gestión → Busca/Filtra licitación
       → Ver Detalle → Modal con productos
       → Editar Producto → Modal 3 secciones
       → Modifica datos → Sistema recalcula margen
       → Si No Adjudicado: calcula diferencias vs ganador
       → Guardar → BD → Actualiza tabla
```

### 3. Análisis de Métricas
```
Usuario → Métricas → Sistema consulta BD
       → Calcula diferencias promedio ($ y %)
       → Genera ranking motivos pérdida
       → Ordena por cantidad descendente
       → Calcula porcentajes
       → Muestra tabla con análisis
```

### 4. Administración de Catálogos
```
Usuario → Administración → Selecciona tab
       → Crear/Editar/Eliminar registro
       → O carga Excel masiva
       → Sistema valida datos
       → Guarda en BD
       → Actualiza tabla
```

---

## 🔐 Seguridad

### Backend
- ✅ Parametrización consultas SQL (prevención SQL injection)
- ✅ Validación entrada con Pydantic
- ✅ SECRET_KEY único por entorno
- ✅ Variables entorno para credenciales
- ✅ Manejo seguro errores con try-catch
- ✅ CSRF protection en formularios
- ✅ Sanitización datos usuario

### Base de Datos
- ✅ Foreign keys habilitadas
- ✅ Constraints en columnas (CHECK, UNIQUE, NOT NULL)
- ✅ Índices en columnas frecuentes
- ✅ Transacciones con rollback
- ✅ Context managers para conexiones

### Archivos Sensibles (.gitignore)
```
.env
.env.local
.env.production
web/.env
*.db
*.db-journal
logs/
uploads/
```

---

## 📈 Métricas del Proyecto

### Código
- **app.py**: 78 líneas (reducido de 1500+)
- **Blueprints**: 8 archivos modulares
- **JavaScript**: 6 archivos modulares
- **Templates**: 11 archivos HTML
- **Tests**: 28% coverage (9/9 passing)

### Base de Datos
- **Tablas**: 18 (9 principales + 9 catálogos)
- **Índices**: 8 optimizados
- **Migraciones**: Sistema versionado

### Funcionalidades
- **Módulos**: 7 principales
- **Catálogos**: 11 configurables
- **Indicadores**: 6 en dashboard
- **Alertas**: 3 niveles de margen

---

## 🛠️ Desarrollo

### Setup Local
```bash
# Web
cd web
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python app.py

# Desktop
cd desktop
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Variables de Entorno (web/.env)
```bash
SECRET_KEY=tu-secret-key-segura
DATABASE_URL=postgresql://user:pass@host:5432/db  # Producción
FLASK_ENV=development  # o production
PORT=5000
```

### Migraciones
```bash
cd shared/database/migrations
python migrate.py ../licitaciones.db
```

### Tests
```bash
cd web
pytest
pytest --cov=. --cov-report=html
```

### Backup
```bash
bash scripts/backup_db.sh
```

---

## 🚢 Despliegue

### Render.com (Producción)
1. Conectar repositorio GitHub
2. Configurar variables entorno:
   - `DATABASE_URL`: PostgreSQL URL
   - `SECRET_KEY`: Clave segura
   - `FLASK_ENV`: production
3. Deploy automático desde main
4. Ejecutar migraciones si necesario

### Docker (PostgreSQL Local)
```bash
docker-compose up -d
bash scripts/setup_postgres.bat
```

---

## 📝 Convenciones

### Código
- **Python**: PEP 8
- **JavaScript**: camelCase para variables, PascalCase para clases
- **SQL**: snake_case para tablas y columnas
- **Archivos**: snake_case.py, kebab-case.js

### Git
- **Commits**: Español, descriptivos
- **Branches**: feature/nombre, fix/nombre
- **Tags**: v1.2.0

### Base de Datos
- **IDs**: INTEGER PRIMARY KEY AUTOINCREMENT (SQLite) / SERIAL (PostgreSQL)
- **Fechas**: TEXT formato ISO 8601 (YYYY-MM-DD HH:MM:SS)
- **Montos**: REAL (2 decimales)
- **Booleanos**: INTEGER 0/1 (SQLite) / BOOLEAN (PostgreSQL)

---

## 🔄 Próximas Funcionalidades

### Módulo Pólizas (v1.3.0)
- Registro pólizas por licitación
- Seguimiento estados
- Alertas vencimiento
- Gestión documentos

### Reportes Avanzados (v1.4.0)
- Exportación Excel/PDF
- Gráficos interactivos
- Análisis tendencias
- Comparativas temporales

### Notificaciones (v1.5.0)
- Email automático
- Recordatorios vencimientos
- Alertas márgenes bajos

---

## 📞 Soporte

### Logs
- **Ubicación**: `web/logs/licitarte.log`
- **Rotación**: 10MB por archivo, 5 backups
- **Formato**: `[timestamp] LEVEL in module: message`

### Backups
- **Automáticos**: `data/backups/`
- **Manual**: `bash scripts/backup_db.sh`
- **Restauración**: Reemplazar `shared/database/licitaciones.db`

### Rollback
- **Fase 5**: `data/backups/fase5_backup_*/`
- **Fase 6**: `data/backups/fase6_backup_*/`

---

## ✅ Checklist Comprensión

- [ ] Entiendo la estructura dual (web + desktop)
- [ ] Conozco las 18 tablas de la BD
- [ ] Comprendo el análisis de márgenes (rojo/amarillo/verde)
- [ ] Sé cómo funcionan las diferencias vs ganador
- [ ] Entiendo el formato MILL (≥1M)
- [ ] Conozco los 11 catálogos configurables
- [ ] Comprendo el flujo de nueva licitación
- [ ] Sé cómo funciona el sistema de migraciones
- [ ] Entiendo la arquitectura con blueprints
- [ ] Conozco las validaciones con Pydantic

---

**Última actualización**: 2025-01-26  
**Versión documento**: 1.0  
**Autor**: Licitarte Team
