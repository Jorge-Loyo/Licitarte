# Licitarte - Gestión de Licitaciones Farmacéuticas

<div align="center">

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

**Aplicación profesional de escritorio para gestionar y analizar licitaciones farmacéuticas**

</div>

---

## 📋 Descripción

Licitarte es una aplicación de escritorio moderna desarrollada en Python con CustomTkinter que permite gestionar licitaciones farmacéuticas de manera eficiente, con seguimiento de productos, análisis estadístico y consulta de históricos.

## ✨ Características Principales

- ✅ **Gestión Completa de Licitaciones**
  - Registro de licitaciones con múltiples productos
  - Edición y eliminación de registros
  - Búsqueda y filtrado en tiempo real

- 📊 **Dashboard Analítico**
  - Estadísticas en tiempo real
  - Precio promedio ponderado
  - Histórico de productos y precios
  - Tabla de productos adjudicados

- 🎨 **Interfaz Moderna**
  - Modo claro y oscuro
  - Diseño intuitivo y profesional
  - Colores: Celeste, Blanco y Negro

- 💾 **Base de Datos Local**
  - SQLite integrado
  - Sin necesidad de servidor
  - Respaldos fáciles

- 🔒 **Seguridad**
  - Validaciones robustas
  - Integridad referencial
  - Datos locales seguros

## 🚀 Instalación

### Requisitos

- Python 3.8 o superior
- Windows 10/11, macOS o Linux

### Instalación desde Código Fuente

```bash
# Clonar o descargar el repositorio
cd C:\git\Licitarte

# Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python main.py
```

### Instalación desde Ejecutable (Windows)

1. Descargar `Licitarte_v1.0_Instalador.zip`
2. Descomprimir
3. Ejecutar `Licitarte.exe` (versión portable)
   
   O usar instalador:
4. Clic derecho en `installer.bat` → Ejecutar como administrador
5. Seguir instrucciones

## 📖 Uso Rápido

### 1. Nueva Licitación

1. Ir a "➕ Nueva Licitación"
2. Completar datos de la licitación
3. Agregar productos con "+ Agregar Producto"
4. Guardar

### 2. Gestión

1. Ir a "📋 Gestión"
2. Buscar licitaciones
3. Doble clic para ver detalle
4. Editar o eliminar según necesidad

### 3. Dashboard

1. Ir a "📊 Dashboard"
2. Ver estadísticas generales
3. Buscar histórico de productos
4. Consultar productos adjudicados

### 4. Ayuda Integrada

1. Clic en "❓ Ayuda" en el menú
2. Navegar por las secciones
3. Consultar instrucciones detalladas

## 📁 Estructura del Proyecto

```
Licitarte/
├── database/
│   ├── __init__.py
│   └── db_manager.py          # Gestor de base de datos
├── modules/
│   ├── __init__.py
│   ├── ingreso.py             # Módulo de ingreso
│   ├── gestion.py             # Módulo de gestión
│   ├── dashboard.py           # Módulo de análisis
│   └── ayuda.py               # Manual integrado
├── Img/
│   └── Logo_licitarte.png     # Logo de la aplicación
├── main.py                    # Aplicación principal
├── requirements.txt           # Dependencias
├── Licitarte.spec            # Configuración PyInstaller
├── build_exe.bat             # Script para generar ejecutable
├── installer.bat             # Instalador para usuarios
├── README.md                 # Este archivo
├── MANUAL_USUARIO.md         # Manual completo
├── DISTRIBUCION.md           # Guía de distribución
└── LEEME.txt                 # Instrucciones básicas
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **CustomTkinter** - Interfaz gráfica moderna
- **SQLite3** - Base de datos local
- **Pillow** - Manejo de imágenes
- **PyInstaller** - Generación de ejecutables

## 💾 Respaldo de Datos

### Crear Respaldo

```bash
# Copiar archivo de base de datos
copy database\licitaciones.db backup\licitaciones_backup_2024-01-15.db
```

### Restaurar Respaldo

```bash
# Reemplazar base de datos actual
copy backup\licitaciones_backup_2024-01-15.db database\licitaciones.db
```

## 🔨 Generar Ejecutable

### Windows

```bash
# Método 1: Script automático
build_exe.bat

# Método 2: Manual
pip install pyinstaller
pyinstaller --clean Licitarte.spec
```

El ejecutable se generará en `dist/Licitarte.exe`

## 📊 Base de Datos

### Estructura

**Tabla: licitaciones**
- id (INTEGER PRIMARY KEY)
- numero_licitacion (TEXT UNIQUE)
- fecha (TEXT)
- laboratorio_ganador (TEXT)

**Tabla: productos**
- id (INTEGER PRIMARY KEY)
- licitacion_id (INTEGER FOREIGN KEY)
- item_producto (TEXT)
- cantidad (INTEGER)
- precio_ofertado (REAL)
- resultado (TEXT)
- precio_ganador (REAL)
- laboratorio_ganador (TEXT)

## 🔒 Seguridad

- ✅ Validación de datos de entrada
- ✅ Constraints en base de datos
- ✅ Context managers para conexiones
- ✅ Manejo de errores robusto
- ✅ Transacciones atómicas
- ✅ Prevención de SQL injection (queries parametrizadas)

## 📝 Licencia

MIT License - Ver archivo LICENSE para más detalles

## 👤 Autor

Desarrollado con ❤️ para la gestión eficiente de licitaciones farmacéuticas

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para soporte técnico o reportar problemas:

- Consultar `MANUAL_USUARIO.md` para instrucciones detalladas
- Usar la ayuda integrada en la aplicación (menú "❓ Ayuda")
- Contactar al desarrollador

## 🗺️ Roadmap

- [ ] Exportación a Excel/CSV
- [ ] Gráficos estadísticos
- [ ] Reportes PDF
- [ ] Filtros avanzados
- [ ] Importación masiva de datos
- [ ] Modo multi-usuario

## 📜 Changelog

### v1.0 (2024-01-15)

- ✅ Lanzamiento inicial
- ✅ Gestión completa de licitaciones
- ✅ Dashboard con estadísticas
- ✅ Modo claro/oscuro
- ✅ Manual de usuario integrado
- ✅ Ejecutable standalone

---

<div align="center">

**Licitarte v1.0** - Gestión Profesional de Licitaciones Farmacéuticas

</div>
