# Setup Base de Datos Local

## Opción 1: PostgreSQL con Docker (RECOMENDADO)

### 1. Instalar Docker Desktop
- Descargar de https://www.docker.com/products/docker-desktop

### 2. Iniciar PostgreSQL
```bash
cd c:\git\Licitarte
docker-compose up -d
```

### 3. Instalar dependencias Python
```bash
cd web
pip install python-dotenv psycopg2-binary
```

### 4. Ejecutar migraciones (primera vez)
```bash
python -c "from database.db_manager import DatabaseManager; db = DatabaseManager(); print('Base de datos inicializada')"
```

### 5. Iniciar aplicación
```bash
python app.py
```

### Comandos útiles
```bash
# Ver logs de PostgreSQL
docker-compose logs -f postgres

# Detener PostgreSQL
docker-compose down

# Detener y eliminar datos
docker-compose down -v
```

## Opción 2: SQLite (actual)
Mantener configuración actual sin cambios.

## Ventajas PostgreSQL vs SQLite

| Característica | PostgreSQL | SQLite |
|----------------|------------|--------|
| Concurrencia | ✅ Excelente | ⚠️ Limitada |
| Transacciones | ✅ ACID completo | ⚠️ Problemas con múltiples conexiones |
| Producción | ✅ Mismo motor | ❌ Diferente |
| Backup | ✅ pg_dump | ⚠️ Copiar archivo |
| Performance | ✅ Mejor con datos grandes | ⚠️ Limitado |
