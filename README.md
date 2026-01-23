# Licitarte - Gestión de Licitaciones Farmacéuticas

<div align="center">

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Flask](https://img.shields.io/badge/flask-3.0-red)
![License](https://img.shields.io/badge/license-MIT-orange)

**Aplicación profesional de escritorio y web para gestionar y analizar licitaciones farmacéuticas**

[Demo Web](https://licitarte.onrender.com) | [Documentación](Doc/MANUAL_USUARIO.md) | [Despliegue](Doc/DEPLOY_RENDER.md)

</div>

---

## 📋 Descripción

Licitarte es una aplicación completa (escritorio y web) desarrollada en Python que permite gestionar licitaciones farmacéuticas de manera eficiente, con seguimiento de productos, análisis estadístico y consulta de históricos.

### 🖥️ Versión Desktop
- Aplicación nativa con CustomTkinter
- Instalable en Windows/Mac/Linux
- Base de datos SQLite local

### 🌐 Versión Web
- Aplicación Flask responsive
- Accesible desde cualquier navegador
- Desplegable en Render/Heroku/AWS

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

## 🚀 Instalación y Uso

### 🖥️ Aplicación Desktop

#### Opción 1: Desde Código Fuente

```bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/licitarte.git
cd licitarte

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación desktop
python main.py
```

#### Opción 2: Ejecutable Windows

1. Descargar `Licitarte_v1.0_Instalador.zip`
2. Descomprimir
3. Ejecutar `Licitarte.exe` (portable)
4. O usar `installer.bat` como administrador

---

### 🌐 Aplicación Web

#### Ejecutar Localmente

```bash
# Desde la raíz del proyecto
cd web

# Instalar dependencias web
pip install -r requirements.txt

# Iniciar servidor
python app.py

# Abrir navegador en: http://localhost:5000
```

#### Script Rápido (Windows)

```bash
run_web.bat
```

#### Desplegar en Render

1. Subir código a GitHub
2. Crear cuenta en [Render.com](https://render.com)
3. Conectar repositorio
4. Configurar:
   - **Build Command:** `pip install -r web/requirements.txt`
   - **Start Command:** `cd web && gunicorn app:app`
5. Deploy automático

**Guía completa:** [DEPLOY_RENDER.md](Doc/DEPLOY_RENDER.md)

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
├── web/                       # 🌐 APLICACIÓN WEB
│   ├── app.py                 # Backend Flask
│   ├── requirements.txt       # Dependencias web
│   ├── static/
│   │   ├── css/style.css
│   │   ├── js/
│   │   └── img/
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── ingreso.html
│       ├── gestion.html
│       └── ayuda.html
├── Doc/
│   ├── MANUAL_USUARIO.md      # Manual completo
│   ├── DISTRIBUCION.md        # Guía distribución desktop
│   └── DEPLOY_RENDER.md       # Guía despliegue web
├── Img/
│   └── Logo_licitarte.png
├── main.py                    # 🖥️ App Desktop
├── requirements.txt           # Dependencias desktop
├── Procfile                   # Config Render
├── runtime.txt                # Python version
└── README.md
```

## 🛠️ Tecnologías Utilizadas

### Desktop
- **Python 3.8+**
- **CustomTkinter** - Interfaz gráfica moderna
- **SQLite3** - Base de datos local
- **Pillow** - Manejo de imágenes
- **PyInstaller** - Generación de ejecutables

### Web
- **Flask 3.0** - Framework web
- **Gunicorn** - Servidor WSGI
- **HTML5/CSS3/JavaScript** - Frontend
- **SQLite3** - Base de datos compartida

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

- 📖 Consultar [Manual de Usuario](Doc/MANUAL_USUARIO.md)
- 🌐 Guía de [Despliegue Web](Doc/DEPLOY_RENDER.md)
- 💻 Guía de [Distribución Desktop](Doc/DISTRIBUCION.md)
- ❓ Usar ayuda integrada en la aplicación
- 🐛 Reportar issues en GitHub

## 🌐 Demo en Línea

**URL:** https://licitarte.onrender.com

⚠️ **Nota:** Plan gratuito se duerme después de 15 min de inactividad. Primera carga puede tardar ~30 segundos.

## 🗺️ Roadmap

### v1.0 (Actual)
- ✅ Aplicación desktop completa
- ✅ Aplicación web completa
- ✅ Dashboard con estadísticas
- ✅ Modo claro/oscuro
- ✅ Manual integrado

### v1.1 (Próximo)
- [ ] Exportación a Excel/CSV
- [ ] Gráficos estadísticos
- [ ] Reportes PDF
- [ ] Filtros avanzados

### v2.0 (Futuro)
- [ ] Importación masiva de datos
- [ ] Modo multi-usuario
- [ ] API REST completa
- [ ] Aplicación móvil

## 📜 Changelog

### v1.0 (2024-01-23)

**Desktop:**
- ✅ Lanzamiento inicial
- ✅ Gestión completa de licitaciones
- ✅ Dashboard con estadísticas
- ✅ Modo claro/oscuro
- ✅ Manual de usuario integrado
- ✅ Ejecutable standalone
- ✅ Instalador/Desinstalador

**Web:**
- ✅ Aplicación Flask completa
- ✅ API REST
- ✅ Interfaz responsive
- ✅ Mismo diseño que desktop
- ✅ Desplegable en Render

---

<div align="center">

**Licitarte v1.0** - Gestión Profesional de Licitaciones Farmacéuticas

</div>
