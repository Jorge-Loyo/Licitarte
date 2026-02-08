# Shared - Código Compartido

## Estructura

```
shared/
├── database/        # Gestor de base de datos
│   └── migrations/  # Scripts de migración
└── models/          # Modelos compartidos
```

## Descripción

- **database/**: Gestor de BD (SQLite/PostgreSQL)
  - db_manager.py
  - migrations/: Scripts de migración versionados

- **models/**: Modelos de datos compartidos entre web y desktop
  - licitacion.py
  - producto.py
  - cliente.py

## Imports

```python
from shared.database import DatabaseManager
from shared.models import Licitacion, Producto, Cliente
```

## Nota

Este código es utilizado por ambas aplicaciones (web y desktop).
