# Web - Código Fuente

## Estructura

```
src/
├── routes/          # Endpoints API
├── models/          # Modelos de datos
├── services/        # Lógica de negocio
└── utils/           # Utilidades
```

## Descripción

- **routes/**: Endpoints REST de la aplicación
- **models/**: Modelos de datos específicos de web
- **services/**: Lógica de negocio y servicios
- **utils/**: Funciones auxiliares (logger, validators, etc)

## Imports

```python
from src.routes import licitaciones
from src.services import LicitacionService
from src.utils import logger
```
