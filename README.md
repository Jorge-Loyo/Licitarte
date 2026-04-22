# Licitarte - Sistema de Gestión de Licitaciones

Sistema web para gestión de licitaciones farmacéuticas con Flask y PostgreSQL.

## Estructura del Proyecto

```
Licitarte/
├── backend/              # Backend Flask
│   ├── api/             # API REST
│   │   ├── routes/      # Endpoints
│   │   ├── services/    # Lógica de negocio
│   │   ├── models/      # Modelos de datos
│   │   └── schemas/     # Validación
│   ├── database/        # Base de datos
│   ├── middleware/      # Middleware
│   ├── utils/          # Utilidades
│   ├── app.py          # Aplicación principal
│   └── config.py       # Configuración
├── frontend/           # Frontend
│   ├── static/        # CSS, JS, imágenes
│   │   ├── css/
│   │   ├── js/
│   │   │   ├── modules/  # Módulos JS
│   │   │   ├── pages/    # JS por página
│   │   │   └── shared/   # JS compartido
│   │   └── img/
│   └── templates/     # Templates HTML
│       ├── components/
│       └── pages/
├── docker/            # Docker Compose
├── data/             # Datos y backups
├── scripts/          # Scripts de utilidad
├── tests/            # Tests
└── docs/             # Documentación
```

## Requisitos

- Python 3.11+
- Docker Desktop
- PostgreSQL 15 (via Docker)

## Instalación Rápida

1. Clonar repositorio:

```bash
git clone <repo>
cd Licitarte
```

2. Iniciar aplicación:

```bash
bash start.sh

```

El script automáticamente:

- Crea entorno virtual
- Instala dependencias
- Inicia PostgreSQL en Docker
- Inicia aplicación Flask

## Configuración

Editar `.env` con tus configuraciones:

```env
DATABASE_URL=postgresql://licitarte:licitarte123@localhost:5433/licitarte_db
SECRET_KEY=tu-secret-key
FLASK_ENV=development
```

## Base de Datos

PostgreSQL corre en Docker:

- Host: localhost
- Puerto: 5433
- Usuario: licitarte
- Password: licitarte123
- Base de datos: licitarte_db

### Comandos Docker

```bash
# Iniciar BD
cd docker
docker-compose up -d

# Detener BD
docker-compose down

# Ver logs
docker-compose logs -f

# Backup
docker exec licitarte_db pg_dump -U licitarte licitarte_db > backup.sql
```

## Desarrollo

### Estructura Modular

El proyecto usa arquitectura modular:

**Backend:**

- `api/routes/` - Endpoints REST
- `api/services/` - Lógica de negocio
- `api/models/` - Modelos de datos
- `database/` - Gestión de BD

**Frontend:**

- `static/js/modules/` - Módulos reutilizables
- `static/js/pages/` - JS específico por página
- `templates/components/` - Componentes HTML

### Ejecutar Tests

```bash
pytest tests/
```

## Endpoints Principales

- `GET /` - Dashboard
- `GET /gestion` - Gestión de licitaciones
- `GET /administracion` - Administración
- `POST /api/licitaciones` - Crear licitación
- `GET /api/catalogos` - Obtener catálogos

## Tecnologías

- **Backend:** Flask, SQLAlchemy, Flask-Login
- **Frontend:** JavaScript ES6+, HTML5, CSS3
- **Base de Datos:** PostgreSQL 15
- **Contenedores:** Docker, Docker Compose

## Licencia

Propietario
