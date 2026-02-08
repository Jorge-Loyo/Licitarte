# Licitarte - Sistema de Gestión de Licitaciones Farmacéuticas

**Versión 1.1.0** - Sistema profesional para gestionar licitaciones farmacéuticas con análisis de márgenes y métricas avanzadas.

[![Versión](https://img.shields.io/badge/versión-1.1.0-blue.svg)](https://github.com/Jorge-Loyo/Licitarte)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Licencia](https://img.shields.io/badge/licencia-Propietario-red.svg)](LICENSE)

## Novedades v1.1.0

- ✨ **Análisis de Márgenes**: Alertas visuales (rojo/amarillo/verde) al cotizar productos según costo unitario
- ✨ **Métricas Avanzadas**: Módulo de métricas con ranking de causas de pérdidas y diferencias promedio
- ✨ **Motivos de Pérdida**: Catálogo configurable de motivos cuando no se adjudica
- ✨ **Diferencias vs Ganador**: Cálculo automático de diferencia en $ y % para productos no adjudicados
- ✨ **Catálogos Dinámicos**: Portales/Origen, Modalidades de Entrega, Formas de Pago, Organismos/Jurisdicción
- ✨ **Gestión de Costos**: Campo costo unitario en catálogo de productos para análisis de rentabilidad
- ✨ **Dashboard Mejorado**: 6 indicadores (unidades cotizadas/ganadas, porcentajes, totales en dinero)
- ✨ **Formato MILL**: Montos ≥1M se muestran en formato millones (ej: $200,00 MILL)
- ✨ **UI Modernizada**: Modales rediseñados, scrollbars personalizados, notificaciones custom

## Características

### Gestión Completa
- ✅ Licitaciones con datos completos (portal, modalidad, forma pago, pólizas)
- ✅ Productos con análisis de margen en tiempo real
- ✅ Catálogo Celty con costos unitarios
- ✅ Clientes con organismo/jurisdicción
- ✅ Oferentes, marcas, tipos de licitación
- ✅ Catálogos configurables (portales, modalidades, formas pago, organismos, motivos pérdida)

### Dashboard & Métricas
- ✅ 6 indicadores clave (unidades, porcentajes, dinero)
- ✅ Histórico de precios con filtros
- ✅ Productos adjudicados paginados
- ✅ Formato argentino con notación MILL

### Módulo Métricas
- ✅ Ranking de causas de pérdidas
- ✅ Diferencia promedio $ y % vs ganador
- ✅ Análisis de competitividad

### Análisis de Rentabilidad
- ✅ Alerta roja: Precio ≤ costo
- ✅ Alerta amarilla: Margen < 8%
- ✅ Alerta verde: Margen ≥ 8%
- ✅ Cálculo automático al cotizar

### Interfaz Moderna
- ✅ Modales con secciones agrupadas
- ✅ Inputs grandes (16px font, 12px padding)
- ✅ Scrollbars personalizados
- ✅ Notificaciones custom
- ✅ Tema claro/oscuro

## Tecnologías

- **Backend**: Python 3.11, Flask 3.0
- **Base de Datos**: SQLite (local) / PostgreSQL (producción)
- **Frontend**: HTML5, CSS3, JavaScript Vanilla
- **Despliegue**: Gunicorn, Render.com

## 🚀 Inicio Rápido

Licitarte tiene **2 versiones**: Desktop (CustomTkinter) y Web (Flask).

### 📦 Instalación Inicial

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/Licitarte.git
cd Licitarte

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows (Git Bash)
```

### 🌐 Ejecutar Versión WEB (Recomendado - v1.1.0)

**Opción 1: Comando directo**
```bash
cd web
pip install -r requirements.txt
python app.py
```

**Opción 2: Script automático (Windows)**
```bash
run_web.bat
```

Luego abre tu navegador en: **http://localhost:5000**

✨ **La versión web incluye todas las funcionalidades v1.1.0**: análisis de márgenes, métricas avanzadas, catálogos configurables, etc.

### 🖥️ Ejecutar Versión DESKTOP (v1.0.0)

```bash
# Instalar dependencias desktop
pip install -r requirements.txt

# Ejecutar aplicación
python main.py
```

⚠️ **Nota**: La versión desktop tiene funcionalidades básicas (v1.0.0). Para todas las características nuevas, usa la versión web.

### 🔄 Diferencias entre Versiones

| Característica | Desktop | Web |
|----------------|---------|-----|
| Interfaz | CustomTkinter (ventana nativa) | HTML/CSS/JS (navegador) |
| Versión | 1.0.0 | 1.1.0 |
| Análisis de Márgenes | ❌ | ✅ |
| Módulo Métricas | ❌ | ✅ |
| Catálogos Configurables | ❌ | ✅ |
| Diferencias vs Ganador | ❌ | ✅ |
| Dashboard 6 indicadores | ❌ | ✅ |
| Formato MILL | ❌ | ✅ |
| Multiplataforma | ✅ | ✅ |
| Requiere navegador | ❌ | ✅ |

## Estructura del Proyecto

```
Licitarte/
├── database/
│   ├── db_manager.py          # Gestor de base de datos
│   ├── licitaciones.db        # Base de datos SQLite
│   └── migrate_*.py           # Scripts de migración
├── web/
│   ├── static/
│   │   ├── css/style.css      # Estilos modernizados
│   │   ├── js/
│   │   │   ├── ingreso.js     # Nueva licitación con análisis margen
│   │   │   ├── gestion.js     # Gestión con diferencias
│   │   │   ├── dashboard.js   # Dashboard 6 indicadores
│   │   │   ├── metricas.js    # Módulo métricas
│   │   │   ├── administracion.js  # CRUD catálogos
│   │   │   └── theme.js       # Tema claro/oscuro
│   │   └── img/Logo_licitarte.png
│   ├── templates/
│   │   ├── base.html          # Template base
│   │   ├── dashboard.html     # Dashboard mejorado
│   │   ├── ingreso.html       # Formulario modernizado
│   │   ├── gestion.html       # Gestión con diferencias
│   │   ├── metricas.html      # Módulo métricas
│   │   ├── administracion.html # 9 catálogos
│   │   └── ayuda.html         # Manual actualizado
│   ├── app.py                 # Aplicación Flask
│   └── requirements.txt       # Dependencias
├── Data/Celty.xlsx            # Catálogo productos
└── README.md                  # Este archivo
```

## Módulos

### 1. Dashboard
- 6 indicadores: Unidades cotizadas/ganadas, % unidades, Total cotizado/ganado, % dinero
- Formato MILL para montos grandes
- Histórico de precios con filtros
- Productos adjudicados paginados

### 2. Nueva Licitación
- Formulario modernizado con secciones agrupadas
- Datos completos: Portal, Modalidad, Forma Pago, Póliza, Observaciones
- Selección de productos con análisis de margen en tiempo real
- Alertas visuales: Rojo (≤costo), Amarillo (<8%), Verde (≥8%)
- Auto-completado de campos según resultado
- Múltiples productos por licitación

### 3. Gestión
- Listado con Total Cotizado por licitación
- Búsqueda y filtros avanzados
- Detalle con columnas Dif. $ y Dif. % para no adjudicados
- Edición de productos con análisis de margen
- Modal modernizado con 3 secciones
- Agregar productos a licitaciones existentes

### 4. Métricas
- Ranking de causas de pérdidas con cantidad y %
- Diferencia promedio $ y % vs ganador
- Análisis de competitividad

### 5. Administración
- **Clientes**: Con organismo/jurisdicción (auto-completa en licitación)
- **Catálogo Productos**: Con costo unitario editable
- **Oferentes, Marcas, Tipos**: CRUD completo
- **Organismos/Jurisdicción**: Catálogo configurable
- **Portales/Origen**: Catálogo configurable
- **Modalidades Entrega**: Catálogo configurable
- **Formas de Pago**: Catálogo configurable
- **Motivos Pérdida**: Catálogo configurable (5 por defecto)
- Carga masiva desde Excel
- Scroll lateral en catálogo productos

### 6. Ayuda
- Manual de usuario actualizado v1.1.0
- Guías paso a paso
- Nuevas funcionalidades documentadas

## Base de Datos

### Tablas Principales
- **clientes**: nombre, razon_social, cuit, direccion, telefono, email, organismo_jurisdiccion
- **licitaciones**: numero, cliente_id, tipo_id, fecha, portal_origen, modalidad_entrega, forma_pago, requiere_poliza, monto_poliza, observaciones
- **productos**: licitacion_id, monodroga, marca, presentacion, cantidad, precio_ofertado, resultado, precio_ganador, oferente_ganador, marca_ofrecida, marca_ganadora, motivo_perdida
- **celty**: numero_registro, monodroga, marca, presentacion, laboratorio, precio_caja, precio_unitario, costo_unitario, fecha

### Catálogos Configurables
- **oferentes**, **marcas**, **tipos_licitacion**
- **portales_origen**, **modalidades_entrega**, **formas_pago**
- **organismos_jurisdiccion**, **motivos_perdida**

## Análisis de Márgenes

### Lógica de Alertas
```javascript
if (precioOfertado <= costoUnitario) {
    // ROJO: Pérdida
    margen = ((precioOfertado - costoUnitario) / costoUnitario) * 100
} else if (margen < 8%) {
    // AMARILLO: Margen bajo
} else {
    // VERDE: Margen aceptable
}
```

### Aplicación
- Nueva Licitación: Al ingresar precio ofertado
- Gestión: Al editar producto
- Requiere costo unitario cargado en catálogo

## Diferencias vs Ganador

### Cálculo Automático
```javascript
diferenciaPesos = precioOfertado - precioGanador
diferenciaPorcentaje = (diferenciaPesos / precioGanador) * 100
```

### Visualización
- Columnas Dif. $ y Dif. % en tabla de productos
- Solo para resultado "No Adjudicado"
- Formato argentino con MILL

## Formato de Moneda

### Regla MILL
```javascript
if (valor >= 1000000) {
    return (valor / 1000000).toFixed(2) + ' MILL'
} else {
    return valor.toLocaleString('es-AR')
}
```

### Ejemplos
- $200.000.000,00 → $200,00 MILL
- $850.500,50 → $850.500,50

## Seguridad

- ✓ Parametrización de consultas SQL (prevención SQL injection)
- ✓ Validación de entrada en backend
- ✓ SECRET_KEY único por entorno
- ✓ Variables de entorno para credenciales
- ✓ Manejo seguro de errores
- ✓ CSRF protection en formularios
- ✓ Sanitización de datos de usuario

## Escalabilidad

- ✓ Paginación en todas las tablas
- ✓ Índices en columnas frecuentes
- ✓ Context managers para conexiones DB
- ✓ Soporte PostgreSQL para producción
- ✓ Arquitectura modular
- ✓ Separación frontend/backend
- ✓ API REST para futuras integraciones

## Despliegue a Producción

### Variables de Entorno
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=tu-secret-key-segura
FLASK_ENV=production
PORT=5000
```

### Render.com
1. Conectar repositorio GitHub
2. Configurar variables de entorno
3. Desplegar automáticamente
4. Ejecutar migraciones si es necesario

## Mantenimiento

### Actualizar Catálogo
```bash
python -c "from database.db_manager import DatabaseManager; db = DatabaseManager(); db.cargar_catalogo_desde_excel('Data/Celty.xlsx')"
```

### Backup
```bash
# SQLite
cp database/licitaciones.db database/backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### Migraciones
```bash
cd database
python migrate_v2.py
python migrate_catalogos.py
python migrate_organismos.py
python add_motivo_perdida.py
```

## 🛠️ Solución de Problemas

### Error: "KeyError: 'total_licitaciones'"
**Solución**: Actualizar `db_manager.py` con el método `obtener_estadisticas()` completo.

### Error: "Port 5000 already in use"
**Solución**:
```bash
# Cambiar puerto
export PORT=5001  # Linux/Mac
set PORT=5001     # Windows
python app.py
```

### Error: "No module named 'flask'"
**Solución**:
```bash
cd web
pip install -r requirements.txt
```

### Base de datos no se crea
**Solución**:
```bash
mkdir database
chmod 755 database  # Linux/Mac
```ckup
```bash
# SQLite
cp database/licitaciones.db database/backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### Migraciones
```bash
cd database
python migrate_v2.py
python migrate_catalogos.py
python migrate_organismos.py
python add_motivo_perdida.py
```

## Changelog v1.1.0

### Agregado
- Módulo Métricas con ranking de pérdidas y diferencias promedio
- Análisis de márgenes con alertas visuales (rojo/amarillo/verde)
- Campo costo_unitario en catálogo de productos
- Catálogos configurables: Portales, Modalidades, Formas Pago, Organismos, Motivos Pérdida
- Columnas Dif. $ y Dif. % en productos no adjudicados
- Dashboard con 6 indicadores (unidades, porcentajes, dinero)
- Formato MILL para montos ≥1M
- Campo organismo_jurisdiccion en clientes (auto-completa en licitación)
- Campos v2.0 en licitaciones: portal_origen, modalidad_entrega, forma_pago, requiere_poliza, monto_poliza, observaciones
- Total Cotizado por licitación en Gestión
- Agregar productos a licitaciones existentes
- Notificaciones custom en lugar de alert()
- Scrollbars personalizados

### Mejorado
- Modales modernizados con secciones agrupadas
- Inputs más grandes (16px font, 12px padding)
- Formulario Nueva Licitación completamente rediseñado
- Tabla catálogo con scroll lateral y header sticky
- Lógica de resultado: Adjudicado auto-completa, No Adjudicado requiere motivo
- Marca Ofrecida por defecto "Celtyc"
- Resultado por defecto "Parcial"

### Corregido
- Múltiples archivos de base de datos consolidados
- Referencia USE_POSTGRES en endpoints
- Fecha se mantiene al editar productos del catálogo
- Excel no sobrescribe costo_unitario (solo manual)

## Licencia

Propietario - Todos los derechos reservados

## Versión

**1.1.0** - Enero 2025

## Autor

Jorge - Licitarte 2025
