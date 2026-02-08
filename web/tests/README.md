# Tests - Licitarte

## Cobertura Actual: 80%+

### Estructura de Tests

```
tests/
├── conftest.py              # Fixtures compartidos
├── test_licitaciones.py     # Tests unitarios licitaciones
├── test_productos.py        # Tests unitarios productos
├── test_catalogos.py        # Tests unitarios catálogos
├── test_security.py         # Tests de seguridad
├── test_integration.py      # Tests de integración
└── test_e2e.py             # Tests end-to-end
```

## Ejecutar Tests

### Todos los tests
```bash
cd web
pytest
```

### Con coverage
```bash
pytest --cov=. --cov-report=html --cov-report=term
```

### Solo tests específicos
```bash
pytest tests/test_licitaciones.py
pytest tests/test_security.py -v
```

### Tests E2E
```bash
pytest tests/test_e2e.py -v
```

## CI/CD

GitHub Actions ejecuta automáticamente:
- Tests en cada push a main/develop
- Coverage mínimo 80%
- Linting con flake8

Ver: `.github/workflows/ci.yml`

## Fixtures Disponibles

- `app`: Aplicación Flask en modo testing
- `client`: Cliente HTTP para tests
- `db`: Base de datos en memoria
- `sample_cliente`: Cliente de prueba
- `sample_licitacion`: Licitación de prueba
