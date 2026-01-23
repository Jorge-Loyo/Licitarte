# Guía de Despliegue a Producción - Licitarte

## Preparación

### 1. Variables de Entorno
Configurar en Render.com o servidor:

```bash
DATABASE_URL=postgresql://usuario:password@host:5432/licitarte
SECRET_KEY=generar-con-secrets-token-hex-32
FLASK_ENV=production
PORT=5000
```

### 2. Base de Datos PostgreSQL
- Crear base de datos PostgreSQL en Render o servicio externo
- Copiar DATABASE_URL completo

## Despliegue en Render.com

### Paso 1: Crear Web Service
1. Conectar repositorio GitHub
2. Configurar:
   - **Build Command**: `cd web && pip install -r requirements.txt`
   - **Start Command**: `cd web && gunicorn app:app`
   - **Environment**: Python 3.11

### Paso 2: Configurar Variables de Entorno
En Render Dashboard > Environment:
- `DATABASE_URL`: URL de PostgreSQL
- `SECRET_KEY`: Clave secreta generada
- `FLASK_ENV`: production

### Paso 3: Inicializar Base de Datos
Después del primer despliegue, ejecutar en Shell de Render:
```bash
cd web
python init_production.py
```

### Paso 4: Cargar Catálogo (Opcional)
Si necesitas cargar el catálogo Celty:
1. Subir archivo `Data/Celty.xlsx` al repositorio
2. Ejecutar script de inicialización

## Despliegue Manual (VPS/Servidor)

### 1. Instalar Dependencias
```bash
cd Licitarte/web
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno
```bash
export DATABASE_URL="postgresql://..."
export SECRET_KEY="tu-clave-secreta"
export FLASK_ENV="production"
```

### 3. Inicializar Base de Datos
```bash
python init_production.py
```

### 4. Ejecutar con Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 5. Configurar Nginx (Recomendado)
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Seguridad

### Checklist de Seguridad
- ✓ SECRET_KEY único y seguro
- ✓ DEBUG=False en producción
- ✓ HTTPS habilitado
- ✓ Base de datos con contraseña fuerte
- ✓ Backups automáticos configurados
- ✓ Variables de entorno protegidas

### Backups
Configurar backups automáticos de PostgreSQL:
- Render: Automático en planes pagos
- Manual: `pg_dump` diario

## Mantenimiento

### Actualizar Catálogo
```bash
# Subir nuevo Celty.xlsx
# Ejecutar en servidor:
python -c "from database.db_manager import DatabaseManager; db = DatabaseManager(); db.cargar_catalogo_desde_excel('../Data/Celty.xlsx')"
```

### Monitoreo
- Logs: Render Dashboard o `/var/log/`
- Errores: Revisar logs de aplicación
- Performance: Monitorear uso de base de datos

## Troubleshooting

### Error: "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Error: "DATABASE_URL not set"
Verificar variables de entorno en Render Dashboard

### Error: "Permission denied"
Verificar permisos de archivos y directorios

## Contacto y Soporte
Para problemas o consultas, revisar logs y documentación.
