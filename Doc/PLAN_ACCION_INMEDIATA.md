# ⚡ PLAN DE ACCIÓN INMEDIATA - LICITARTE

## 🎯 OBJETIVO
Implementar las mejoras más críticas en **5 días** para estabilizar el proyecto antes de continuar con desarrollo.

---

## 📅 DÍA 1: SEGURIDAD BÁSICA (2-3 horas)

### ✅ Tarea 1.1: Fijar SECRET_KEY (15 min)

**Problema:** La clave se regenera en cada reinicio, invalidando sesiones.

**Solución:**
```bash
# 1. Generar clave segura
python -c "import secrets; print(secrets.token_hex(32))"

# 2. Copiar el resultado y agregarlo a .env
echo "SECRET_KEY=tu_clave_generada_aqui" >> web/.env

# 3. Actualizar app.py
```

**Archivo:** `web/app.py`
```python
# ANTES (línea 18)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# DESPUÉS
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
if not app.config['SECRET_KEY']:
    raise ValueError("SECRET_KEY no configurada en .env")
```

### ✅ Tarea 1.2: Crear .env.example (10 min)

**Archivo:** `web/.env.example`
```bash
# Configuración de Seguridad
SECRET_KEY=genera_con_secrets_token_hex_32

# Base de Datos
DATABASE_URL=sqlite:///database/licitaciones.db
# Para producción: postgresql://user:pass@host:5432/dbname

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# Límites
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/licitarte.log
```

### ✅ Tarea 1.3: Actualizar .gitignore (5 min)

**Archivo:** `.gitignore`
```bash
# Agregar al final
# Logs
logs/
*.log

# Environment
.env
.env.local
.env.*.local

# Uploads
web/uploads/*
!web/uploads/.gitkeep
```

### ✅ Tarea 1.4: Validar Configuración (10 min)

**Crear:** `web/config.py`
```python
import os
from pathlib import Path

class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY debe estar configurada")
    
    BASE_DIR = Path(__file__).parent.parent
    DATABASE_PATH = BASE_DIR / 'database' / 'licitaciones.db'
    
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    
    ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'pdf'}

class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

**Actualizar:** `web/app.py` (líneas 1-20)
```python
from flask import Flask
from config import config
import os

app = Flask(__name__)
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Resto del código...
```

---

## 📅 DÍA 2: LOGGING (2-3 horas)

### ✅ Tarea 2.1: Configurar Logger (30 min)

**Crear:** `web/utils/logger.py`
```python
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(name='licitarte'):
    """Configura logger con rotación de archivos"""
    
    # Crear directorio de logs
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Configurar logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    # Handler para archivo (rotación cada 10MB, mantener 5 backups)
    file_handler = RotatingFileHandler(
        log_dir / 'licitarte.log',
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    
    # Agregar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Logger global
logger = setup_logger()
```

### ✅ Tarea 2.2: Implementar en Endpoints Críticos (1 hora)

**Actualizar:** `web/app.py`
```python
from utils.logger import logger

# Ejemplo en crear_licitacion
@app.route('/api/licitaciones', methods=['POST'])
def crear_licitacion():
    data = request.json
    logger.info(f"Creando licitación: {data.get('numero', 'SIN_NUMERO')}")
    
    if not data:
        logger.warning("Intento de crear licitación sin datos")
        return jsonify({'success': False, 'error': 'No se recibieron datos'}), 400
    
    try:
        # ... código existente ...
        logger.info(f"Licitación {licitacion_id} creada exitosamente")
        return jsonify({'success': True, 'id': licitacion_id})
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400
    
    except Exception as e:
        logger.exception(f"Error inesperado creando licitación: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500
```

### ✅ Tarea 2.3: Logging en Base de Datos (30 min)

**Actualizar:** `database/db_manager.py`
```python
import logging

logger = logging.getLogger('licitarte')

class DatabaseManager:
    def crear_licitacion(self, numero, fecha, ...):
        logger.info(f"DB: Creando licitación {numero}")
        
        if not numero or not fecha:
            logger.error("DB: Intento de crear licitación sin número o fecha")
            raise ValueError("Número y fecha son obligatorios")
        
        try:
            with self.get_connection() as conn:
                # ... código existente ...
                logger.info(f"DB: Licitación {numero} creada con ID {licitacion_id}")
                return licitacion_id
        except Exception as e:
            logger.exception(f"DB: Error creando licitación {numero}: {str(e)}")
            raise
```

---

## 📅 DÍA 3: TESTING BÁSICO (3-4 horas)

### ✅ Tarea 3.1: Configurar Pytest (20 min)

```bash
# Instalar dependencias
cd web
pip install pytest pytest-cov pytest-flask faker

# Crear pytest.ini
```

**Crear:** `pytest.ini`
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --cov=app
    --cov-report=html
    --cov-report=term-missing
```

### ✅ Tarea 3.2: Crear Fixtures (30 min)

**Crear:** `tests/conftest.py`
```python
import pytest
import sys
import os

# Agregar path del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app
from database.db_manager import DatabaseManager

@pytest.fixture
def app():
    """Fixture de la aplicación Flask"""
    flask_app.config['TESTING'] = True
    flask_app.config['DATABASE'] = ':memory:'  # SQLite en memoria
    yield flask_app

@pytest.fixture
def client(app):
    """Cliente de prueba"""
    return app.test_client()

@pytest.fixture
def db():
    """Base de datos de prueba"""
    db = DatabaseManager(':memory:')
    yield db

@pytest.fixture
def sample_cliente(db):
    """Cliente de ejemplo"""
    cliente_id = db.crear_cliente(
        nombre='Hospital Test',
        razon_social='Hospital Test SA',
        cuit='20-12345678-9',
        direccion='Calle Falsa 123',
        telefono='1234-5678',
        email='test@hospital.com',
        organismo_jurisdiccion='Provincial'
    )
    return cliente_id
```

### ✅ Tarea 3.3: Primer Test (1 hora)

**Crear:** `tests/test_licitaciones.py`
```python
import pytest
import json

def test_crear_licitacion_exitoso(client, sample_cliente):
    """Test: Crear licitación con datos válidos"""
    data = {
        'numero': 'LIC-2025-001',
        'cliente_id': sample_cliente,
        'tipo_licitacion_id': None,
        'fecha': '2025-01-15 10:00',
        'portal_origen': 'Comprar',
        'modalidad_entrega': 'Única',
        'forma_pago': 'Contado',
        'requiere_poliza': False,
        'monto_poliza': None,
        'observaciones': 'Test',
        'mantenimiento_oferta': '',
        'productos': [
            {
                'monodroga': 'Paracetamol',
                'marca': 'Genérico',
                'presentacion': '500mg x 20',
                'cantidad': 100,
                'precio': 10.50,
                'resultado': 'Parcial',
                'marca_ofrecida': 'Laboratorio Test',
                'numero_renglon': '1',
                'costo_unitario': 8.00,
                'margen_porcentaje': 31.25,
                'observaciones': '',
                'producto_cotizar': 'principal',
                'alternativas': []
            }
        ]
    }
    
    response = client.post(
        '/api/licitaciones',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result['success'] == True
    assert 'id' in result

def test_crear_licitacion_sin_numero(client):
    """Test: Crear licitación sin número debe fallar"""
    data = {
        'numero': '',
        'fecha': '2025-01-15',
        'productos': []
    }
    
    response = client.post(
        '/api/licitaciones',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    result = json.loads(response.data)
    assert result['success'] == False

def test_obtener_licitaciones(client):
    """Test: Obtener lista de licitaciones"""
    response = client.get('/api/licitaciones')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert isinstance(result, list)
```

### ✅ Tarea 3.4: Ejecutar Tests (10 min)

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov

# Generar reporte HTML
pytest --cov --cov-report=html
# Ver en: htmlcov/index.html
```

---

## 📅 DÍA 4: VALIDACIONES BACKEND (3-4 horas)

### ✅ Tarea 4.1: Instalar Pydantic (5 min)

```bash
pip install pydantic
```

### ✅ Tarea 4.2: Crear Schemas (1 hora)

**Crear:** `web/schemas/licitacion_schema.py`
```python
from pydantic import BaseModel, validator, Field
from typing import Optional, List
from datetime import datetime

class ProductoSchema(BaseModel):
    """Schema para validar productos"""
    monodroga: str = Field(..., min_length=1, max_length=200)
    marca: str = Field(..., min_length=1, max_length=100)
    presentacion: str = Field(..., min_length=1, max_length=200)
    cantidad: int = Field(..., gt=0)
    precio: float = Field(..., alias='precio_ofertado', ge=0)
    resultado: str = Field(default='Parcial')
    marca_ofrecida: Optional[str] = None
    numero_renglon: Optional[str] = None
    costo_unitario: Optional[float] = Field(None, ge=0)
    margen_porcentaje: Optional[float] = None
    observaciones: Optional[str] = None
    producto_cotizar: str = Field(default='principal')
    
    @validator('resultado')
    def validar_resultado(cls, v):
        if v not in ['Adjudicado', 'Parcial', 'No Adjudicado']:
            raise ValueError('Resultado inválido')
        return v
    
    @validator('precio')
    def validar_precio_vs_costo(cls, v, values):
        if 'costo_unitario' in values and values['costo_unitario']:
            if v < values['costo_unitario']:
                # Solo advertencia, no error
                pass
        return v

class LicitacionCreateSchema(BaseModel):
    """Schema para crear licitación"""
    numero: str = Field(..., min_length=1, max_length=100)
    cliente_id: Optional[int] = None
    tipo_licitacion_id: Optional[int] = None
    fecha: str
    portal_origen: Optional[str] = None
    modalidad_entrega: Optional[str] = None
    forma_pago: Optional[str] = None
    requiere_poliza: bool = False
    monto_poliza: Optional[float] = Field(None, ge=0)
    observaciones: Optional[str] = None
    mantenimiento_oferta: Optional[str] = None
    productos: List[ProductoSchema] = Field(..., min_items=1)
    
    @validator('fecha')
    def validar_fecha(cls, v):
        try:
            # Intentar parsear fecha
            datetime.strptime(v.split()[0], '%Y-%m-%d')
            return v
        except:
            raise ValueError('Formato de fecha inválido (YYYY-MM-DD)')
    
    @validator('productos')
    def validar_renglones_unicos(cls, v):
        renglones = [p.numero_renglon for p in v if p.numero_renglon]
        if len(renglones) != len(set(renglones)):
            raise ValueError('Números de renglón duplicados')
        return v
```

### ✅ Tarea 4.3: Implementar Validación (1 hora)

**Actualizar:** `web/app.py`
```python
from schemas.licitacion_schema import LicitacionCreateSchema
from pydantic import ValidationError

@app.route('/api/licitaciones', methods=['POST'])
def crear_licitacion():
    try:
        # Validar con Pydantic
        schema = LicitacionCreateSchema(**request.json)
        
        logger.info(f"Creando licitación: {schema.numero}")
        
        # Convertir a dict para DB
        data = schema.dict()
        
        licitacion_id = db.crear_licitacion(
            data['numero'],
            data['fecha'],
            '',
            '',
            None,
            data.get('cliente_id'),
            data.get('tipo_licitacion_id'),
            data.get('portal_origen', ''),
            data.get('modalidad_entrega', ''),
            data.get('forma_pago', ''),
            data.get('requiere_poliza', False),
            data.get('monto_poliza'),
            data.get('observaciones', ''),
            data.get('mantenimiento_oferta', '')
        )
        
        # Agregar productos
        for producto in data['productos']:
            db.agregar_producto(
                licitacion_id,
                producto['monodroga'],
                producto['marca'],
                producto['presentacion'],
                producto['cantidad'],
                producto['precio'],
                producto['resultado'],
                None,
                '',
                producto.get('marca_ofrecida', ''),
                '',
                '',
                producto.get('numero_renglon', ''),
                producto.get('costo_unitario'),
                producto.get('margen_porcentaje'),
                producto.get('observaciones', ''),
                producto.get('producto_cotizar', 'principal')
            )
        
        logger.info(f"Licitación {licitacion_id} creada exitosamente")
        return jsonify({'success': True, 'id': licitacion_id})
    
    except ValidationError as e:
        logger.warning(f"Validación fallida: {e.errors()}")
        return jsonify({
            'success': False,
            'error': 'Datos inválidos',
            'details': e.errors()
        }), 400
    
    except Exception as e:
        logger.exception(f"Error inesperado: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno'}), 500
```

---

## 📅 DÍA 5: MIGRACIONES (3-4 horas)

### ✅ Tarea 5.1: Crear Sistema de Migraciones (1 hora)

**Crear:** `database/migrations/migrate.py`
```python
import sqlite3
import os
from pathlib import Path

class MigrationManager:
    """Gestor de migraciones de base de datos"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.migrations_dir = Path(__file__).parent
        
    def init_migrations_table(self):
        """Crea tabla de control de migraciones"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def get_applied_migrations(self):
        """Obtiene migraciones ya aplicadas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT version FROM schema_migrations ORDER BY version')
        versions = [row[0] for row in cursor.fetchall()]
        conn.close()
        return versions
    
    def get_pending_migrations(self):
        """Obtiene migraciones pendientes"""
        applied = set(self.get_applied_migrations())
        all_migrations = sorted([
            int(f.stem.split('_')[0])
            for f in self.migrations_dir.glob('*.sql')
        ])
        return [v for v in all_migrations if v not in applied]
    
    def apply_migration(self, version):
        """Aplica una migración específica"""
        migration_file = self.migrations_dir / f"{version:03d}_*.sql"
        files = list(self.migrations_dir.glob(f"{version:03d}_*.sql"))
        
        if not files:
            raise FileNotFoundError(f"Migración {version} no encontrada")
        
        with open(files[0], 'r', encoding='utf-8') as f:
            sql = f.read()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Ejecutar migración
            cursor.executescript(sql)
            
            # Registrar como aplicada
            cursor.execute(
                'INSERT INTO schema_migrations (version) VALUES (?)',
                (version,)
            )
            
            conn.commit()
            print(f"✓ Migración {version} aplicada")
        
        except Exception as e:
            conn.rollback()
            print(f"✗ Error en migración {version}: {e}")
            raise
        
        finally:
            conn.close()
    
    def migrate(self):
        """Aplica todas las migraciones pendientes"""
        self.init_migrations_table()
        pending = self.get_pending_migrations()
        
        if not pending:
            print("✓ Base de datos actualizada")
            return
        
        print(f"Aplicando {len(pending)} migraciones...")
        for version in pending:
            self.apply_migration(version)
        
        print("✓ Todas las migraciones aplicadas")

if __name__ == '__main__':
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else '../licitaciones.db'
    manager = MigrationManager(db_path)
    manager.migrate()
```

### ✅ Tarea 5.2: Extraer Schema Actual (30 min)

**Crear:** `database/migrations/001_initial_schema.sql`
```sql
-- Migración inicial: Schema base de Licitarte
-- Versión: 1.0.0
-- Fecha: 2025-01-15

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    razon_social TEXT,
    cuit TEXT,
    direccion TEXT,
    telefono TEXT,
    email TEXT,
    organismo_jurisdiccion TEXT,
    activo INTEGER DEFAULT 1
);

-- Tabla de tipos de licitación
CREATE TABLE IF NOT EXISTS tipos_licitacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    activo INTEGER DEFAULT 1
);

-- Tabla de licitaciones
CREATE TABLE IF NOT EXISTS licitaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_licitacion TEXT UNIQUE NOT NULL,
    cliente_id INTEGER,
    tipo_licitacion_id INTEGER,
    fecha TEXT NOT NULL,
    oferente_ganador TEXT,
    marca_ganadora TEXT,
    precio_ganador REAL,
    portal_origen TEXT,
    modalidad_entrega TEXT,
    forma_pago TEXT,
    requiere_poliza INTEGER DEFAULT 0,
    monto_poliza REAL,
    observaciones TEXT,
    mantenimiento_oferta TEXT,
    numero_presupuesto INTEGER,
    tipo_adjudicacion TEXT DEFAULT 'Parcial',
    CHECK(length(numero_licitacion) > 0),
    FOREIGN KEY (cliente_id) REFERENCES clientes (id),
    FOREIGN KEY (tipo_licitacion_id) REFERENCES tipos_licitacion (id)
);

-- Tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    licitacion_id INTEGER NOT NULL,
    monodroga TEXT NOT NULL,
    marca TEXT NOT NULL,
    presentacion TEXT NOT NULL,
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    precio_ofertado REAL NOT NULL CHECK(precio_ofertado >= 0),
    resultado TEXT NOT NULL CHECK(resultado IN ('Adjudicado', 'Parcial', 'No Adjudicado')),
    precio_ganador REAL CHECK(precio_ganador >= 0),
    oferente_ganador TEXT,
    marca_ofrecida TEXT,
    marca_ganadora TEXT,
    motivo_perdida TEXT,
    numero_renglon TEXT,
    costo_unitario REAL,
    margen_porcentaje REAL,
    observaciones TEXT,
    producto_cotizar TEXT DEFAULT 'principal',
    FOREIGN KEY (licitacion_id) REFERENCES licitaciones (id) ON DELETE CASCADE
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_licitacion_numero ON licitaciones(numero_licitacion);
CREATE INDEX IF NOT EXISTS idx_licitacion_cliente ON licitaciones(cliente_id);
CREATE INDEX IF NOT EXISTS idx_producto_licitacion ON productos(licitacion_id);
CREATE INDEX IF NOT EXISTS idx_producto_resultado ON productos(resultado);
```

### ✅ Tarea 5.3: Ejecutar Migraciones (10 min)

```bash
# Ejecutar migraciones
cd database/migrations
python migrate.py ../licitaciones.db

# Verificar
sqlite3 ../licitaciones.db "SELECT * FROM schema_migrations;"
```

---

## 📊 RESUMEN DE 5 DÍAS

### Logros Alcanzados
- ✅ SECRET_KEY fija y segura
- ✅ Configuración centralizada
- ✅ Logging estructurado
- ✅ Tests básicos funcionando
- ✅ Validaciones backend con Pydantic
- ✅ Sistema de migraciones versionado

### Métricas
- **Seguridad:** 4/10 → 7/10
- **Mantenibilidad:** 5/10 → 7/10
- **Testabilidad:** 1/10 → 5/10
- **Confianza:** 3/10 → 7/10

### Próximos Pasos (Semana 2)
1. Aumentar cobertura de tests a 30%
2. Refactorizar endpoint más complejo
3. Implementar rate limiting
4. Documentar API con Swagger

---

## 🚀 COMANDOS RÁPIDOS

### Setup Inicial
```bash
# Clonar y configurar
git clone <repo>
cd Licitarte/web

# Instalar dependencias
pip install -r requirements.txt
pip install pytest pytest-cov pydantic

# Configurar
cp .env.example .env
# Editar .env con tu SECRET_KEY

# Ejecutar migraciones
cd ../database/migrations
python migrate.py ../licitaciones.db

# Ejecutar tests
cd ../../web
pytest

# Iniciar aplicación
python app.py
```

### Desarrollo Diario
```bash
# Antes de empezar
git pull
pytest  # Verificar que todo funciona

# Después de cambios
pytest  # Verificar que no rompiste nada
git add .
git commit -m "feat: descripción del cambio"
git push
```

---

## ✅ CHECKLIST DE VERIFICACIÓN

Marca cuando completes cada tarea:

### Día 1: Seguridad
- [ ] SECRET_KEY generada y en .env
- [ ] .env.example creado
- [ ] config.py implementado
- [ ] .gitignore actualizado
- [ ] Aplicación inicia sin errores

### Día 2: Logging
- [ ] logger.py creado
- [ ] Logging en 5+ endpoints
- [ ] Logging en db_manager
- [ ] Logs se guardan en logs/licitarte.log
- [ ] Logs visibles en consola

### Día 3: Testing
- [ ] pytest instalado
- [ ] conftest.py con fixtures
- [ ] 3+ tests escritos
- [ ] Tests pasan exitosamente
- [ ] Reporte de cobertura generado

### Día 4: Validaciones
- [ ] Pydantic instalado
- [ ] licitacion_schema.py creado
- [ ] Validación en crear_licitacion
- [ ] Errores de validación retornan 400
- [ ] Tests actualizados

### Día 5: Migraciones
- [ ] migrate.py creado
- [ ] 001_initial_schema.sql creado
- [ ] Migraciones ejecutadas
- [ ] Tabla schema_migrations existe
- [ ] DB funciona correctamente

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "SECRET_KEY no configurada"
```bash
# Verificar que .env existe
ls web/.env

# Verificar contenido
cat web/.env | grep SECRET_KEY

# Regenerar si es necesario
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" >> web/.env
```

### Error: "No module named 'pydantic'"
```bash
pip install pydantic
```

### Tests fallan
```bash
# Verificar que estás en el directorio correcto
cd web

# Reinstalar dependencias
pip install -r requirements.txt
pip install pytest pytest-cov

# Ejecutar con más detalle
pytest -v
```

### Migraciones no se aplican
```bash
# Verificar que el archivo existe
ls database/migrations/001_initial_schema.sql

# Ejecutar manualmente
cd database/migrations
python migrate.py ../licitaciones.db
```

---

## 📞 SIGUIENTE PASO

**Después de completar estos 5 días, revisa:**
- `REPORTE_ANALISIS_TECNICO.md` - Para ver todos los problemas
- `OPCIONES_DE_CAMINOS.md` - Para decidir el rumbo a largo plazo

**¿Necesitas ayuda?** Pregunta específicamente sobre cualquier tarea.

---

**Generado por:** Amazon Q Developer  
**Fecha:** Enero 2025  
**Versión:** 1.0
