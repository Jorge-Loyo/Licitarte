# Guía de Instalación Rápida - Licitarte v1.0.0

## 🚀 Instalación Local (Desarrollo)

### Requisitos Previos
- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Jorge-Loyo/Licitarte.git
cd Licitarte
```

2. **Crear entorno virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
cd web
pip install -r requirements.txt
```

4. **Configurar variables de entorno (opcional)**
```bash
# Copiar archivo de ejemplo
cp ../.env.example ../.env

# Editar .env con tus valores (opcional para desarrollo local)
```

5. **Ejecutar la aplicación**
```bash
python app.py
```

6. **Abrir en navegador**
```
http://localhost:5000
```

## 📦 Instalación en Producción (Render.com)

Ver [DEPLOY.md](DEPLOY.md) para instrucciones detalladas.

### Resumen Rápido

1. **Crear cuenta en Render.com**
   - https://render.com

2. **Crear PostgreSQL Database**
   - Copiar DATABASE_URL

3. **Crear Web Service**
   - Conectar repositorio GitHub
   - Build Command: `cd web && pip install -r requirements.txt`
   - Start Command: `cd web && gunicorn app:app`

4. **Configurar Variables de Entorno**
   - `DATABASE_URL`: URL de PostgreSQL
   - `SECRET_KEY`: Generar clave segura
   - `FLASK_ENV`: production

5. **Desplegar**
   - Render desplegará automáticamente

## 🗄️ Base de Datos

### Desarrollo Local
- Usa SQLite automáticamente
- Se crea en `database/licitaciones.db`
- No requiere configuración adicional

### Producción
- Usa PostgreSQL
- Requiere DATABASE_URL en variables de entorno
- Migración automática al iniciar

## 📊 Cargar Catálogo Inicial

Si tienes el archivo `Data/Celty.xlsx`:

```bash
# Desde la raíz del proyecto
python -c "from database.db_manager import DatabaseManager; db = DatabaseManager(); db.cargar_catalogo_desde_excel('Data/Celty.xlsx')"
```

O usar la interfaz web:
1. Ir a Administración
2. Tab "Catálogo Productos"
3. Clic en "📄 Cargar Excel"
4. Seleccionar archivo Celty.xlsx

## ✅ Verificar Instalación

1. **Abrir navegador en http://localhost:5000**
2. **Verificar que carga el Dashboard**
3. **Crear un cliente de prueba** (Administración > Clientes)
4. **Crear una licitación de prueba** (Nueva Licitación)
5. **Ver en Gestión** que aparece la licitación

## 🔧 Solución de Problemas

### Error: "No module named 'flask'"
```bash
pip install -r web/requirements.txt
```

### Error: "Port 5000 already in use"
```bash
# Cambiar puerto en app.py o usar variable de entorno
export PORT=5001
python app.py
```

### Error: Base de datos no se crea
```bash
# Verificar permisos de escritura en carpeta database/
mkdir database
chmod 755 database
```

## 📞 Soporte

Para problemas o consultas:
- Revisar [README.md](README.md)
- Revisar [CHANGELOG.md](CHANGELOG.md)
- Consultar manual de usuario en la aplicación (menú Ayuda)

---

**Versión**: 1.0.0  
**Fecha**: Enero 2025  
**Autor**: Jorge
