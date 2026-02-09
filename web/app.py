from flask import Flask, render_template
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import secrets
from flask_login import LoginManager, login_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))

# Log de inicio para debugging en Render
print("="*50)
print("INICIANDO APLICACIÓN LICITARTE")
print("="*50)

from shared.database.db_manager import DatabaseManager

# Verificar y cargar datos iniciales si es necesario
try:
    db = DatabaseManager()
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM medicamentos")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("⚠ Base de datos vacía, cargando datos iniciales...")
            import tarfile
            seed_file = Path(__file__).parent.parent / "Data" / "medicamentos_seed.sql.gz"
            print(f"Buscando archivo: {seed_file}")
            print(f"Archivo existe: {seed_file.exists()}")
            
            if seed_file.exists():
                with tarfile.open(seed_file, 'r:gz') as tar:
                    for member in tar.getmembers():
                        if member.name.endswith('.sql'):
                            f = tar.extractfile(member)
                            sql_content = f.read().decode('utf-8')
                            break
                
                # Filtrar solo INSERT statements (excluir comentarios)
                lines = sql_content.split('\n')
                statements = []
                current_statement = []
                
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('--'):
                        continue
                    if line.startswith('INSERT INTO'):
                        if current_statement:
                            statements.append(' '.join(current_statement))
                        current_statement = [line]
                    elif current_statement:
                        current_statement.append(line)
                        if line.endswith(';'):
                            statements.append(' '.join(current_statement))
                            current_statement = []
                
                total = len(statements)
                print(f"Ejecutando {total} INSERT statements...")
                
                # Usar autocommit para evitar transacciones abortadas
                conn.autocommit = True
                success_count = 0
                
                for i, statement in enumerate(statements):
                    try:
                        cursor.execute(statement.rstrip(';'))
                        success_count += 1
                        if (i + 1) % 1000 == 0:
                            print(f"Procesado {i+1}/{total}... ({success_count} exitosos)")
                    except Exception as e:
                        if i < 3:
                            print(f"Error {i}: {str(e)[:100]}")
                        continue
                
                conn.autocommit = False
                cursor.execute("SELECT COUNT(*) FROM medicamentos")
                count = cursor.fetchone()[0]
                print(f"✓ Cargados {count} medicamentos exitosamente")
            else:
                print("✗ Archivo de seed no encontrado")
        else:
            print(f"✓ Base de datos conectada: {count} medicamentos en catálogo")
except Exception as e:
    print(f"✗ Error en inicialización de BD: {e}")
    import traceback
    traceback.print_exc()
from security_config import SecurityConfig
from src.models.user import User
from src.utils.error_handlers import register_error_handlers
from src.middleware.request_logging import setup_request_logging
from src.utils.logging_config import logger
from swagger_config import swaggerui_blueprint, SWAGGER_URL

app = Flask(__name__)
app.config.from_object(SecurityConfig)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs('uploads', exist_ok=True)

# Flask-Login: Manejo de sesiones y autenticación
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

@login_manager.user_loader
def load_user(user_id):
    """Cargar usuario por ID para Flask-Login."""
    return User.get(user_id)

# Flask-Limiter: Rate limiting (200/día, 50/hora)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"  # Cambiar a Redis en producción
)

# Flask-CORS: Cross-Origin Resource Sharing
CORS(app, origins=SecurityConfig.CORS_ORIGINS, supports_credentials=True)

# Swagger UI: Documentación interactiva de API
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Error handlers: Manejo centralizado de errores
register_error_handlers(app)

# Request logging: Log de cada request con métricas
setup_request_logging(app)

# Registrar blueprints: 7 módulos con 72 endpoints
from src.routes import register_routes
register_routes(app)

logger.info("Application started")
print("✓ Aplicación Flask iniciada correctamente")
print("="*50)

# Rutas de vistas
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/nueva-licitacion')
@login_required
def nueva_licitacion():
    return render_template('ingreso.html')

@app.route('/gestion')
@login_required
def gestion():
    return render_template('gestion.html')

@app.route('/gestion-nueva')
@login_required
def gestion_nueva():
    return render_template('gestion_nueva.html')

@app.route('/resultado-licitacion/<int:id>')
@login_required
def resultado_licitacion(id):
    return render_template('resultado_licitacion.html')

@app.route('/polizas')
@login_required
def polizas():
    return render_template('polizas.html')

@app.route('/documentacion')
@login_required
def documentacion():
    return render_template('documentacion.html')

@app.route('/administracion')
@login_required
def administracion():
    return render_template('administracion.html')

@app.route('/metricas')
@login_required
def metricas():
    return render_template('metricas.html')

@app.route('/ayuda')
@login_required
def ayuda():
    return render_template('ayuda.html')

@app.route('/editar-licitacion/<int:id>')
@login_required
def editar_licitacion(id):
    return render_template('editar_licitacion.html')

@app.route('/presupuesto/<int:numero>')
@login_required
def ver_presupuesto(numero):
    return render_template('presupuesto.html', numero=numero)

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
