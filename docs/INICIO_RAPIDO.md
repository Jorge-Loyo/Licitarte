# 🚀 Inicio Rápido - Licitarte con Docker

## Requisitos
- Docker Desktop instalado
- Python 3.11
- Git

## Pasos

### 1. Iniciar PostgreSQL con Docker
```bash
cd C:\git\Licitarte
docker-compose up -d
```

Esto inicia PostgreSQL en:
- Host: localhost
- Puerto: 5432
- Usuario: licitarte
- Password: licitarte123
- Base de datos: licitarte_db

### 2. Configurar Variables de Entorno
```bash
cd web
copy .env.example .env
```

Edita `.env` si necesitas cambiar credenciales.

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar Migraciones
```bash
cd ..
python shared/database/run_migrations.py
```

### 5. Iniciar Aplicación
```bash
cd web
python app.py
```

Abre: http://localhost:5000

## Comandos Útiles

### Ver logs de PostgreSQL
```bash
docker logs licitarte_db
```

### Detener PostgreSQL
```bash
docker-compose down
```

### Reiniciar PostgreSQL
```bash
docker-compose restart
```

### Conectar a PostgreSQL
```bash
docker exec -it licitarte_db psql -U licitarte -d licitarte_db
```

## Solución de Problemas

### Error: "DATABASE_URL no configurado"
- Verifica que `.env` existe en `web/`
- Verifica que Docker está corriendo: `docker ps`

### Error: "No se pudo conectar a PostgreSQL"
- Inicia Docker: `docker-compose up -d`
- Espera 5 segundos para que PostgreSQL inicie
- Verifica puerto 5432 libre: `netstat -an | findstr 5432`

### Puerto 5432 ocupado
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "5433:5432"  # Usar 5433 en lugar de 5432

# Actualizar DATABASE_URL en .env
DATABASE_URL=postgresql://licitarte:licitarte123@localhost:5433/licitarte_db
```
