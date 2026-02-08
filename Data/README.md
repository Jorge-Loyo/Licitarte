# Data - Datos

## Estructura

```
data/
├── Celty.xlsx           # Catálogo de productos farmacéuticos
└── backups/             # Backups de base de datos
```

## Descripción

- **Celty.xlsx**: Catálogo de referencia de productos
  - Número de registro
  - Monodroga
  - Marca
  - Presentación
  - Laboratorio
  - Precios
  - Costos

- **backups/**: Backups automáticos de la BD
  - SQLite: backup_YYYYMMDD.db
  - PostgreSQL: backup_YYYYMMDD.sql

## Nota

Esta carpeta NO se sube a Git (excepto Celty.xlsx).
