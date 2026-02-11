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

from shared.database.db_manager import DatabaseManager
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
login_manager.login_view = 'login_page'  # type: ignore

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
