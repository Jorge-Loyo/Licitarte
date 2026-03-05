from flask import Flask, render_template, abort, send_from_directory
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from flask_login import LoginManager, login_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from markupsafe import escape

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database.db_manager import DatabaseManager, USE_POSTGRES
from backend.config import Config
from backend.api.models.user import User
from backend.utils.error_handlers import register_error_handlers
from backend.middleware.request_logging import setup_request_logging
from backend.middleware.metrics import setup_metrics
from backend.utils.logging_config import logger

template_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
static_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'shared')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config.from_object(Config)
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
CORS(app, supports_credentials=True)

# Error handlers: Manejo centralizado de errores
register_error_handlers(app)

# Request logging: Log de cada request con métricas
setup_request_logging(app)

# Metrics: Métricas de performance por endpoint
setup_metrics(app)

# Registrar blueprints
from backend.api.routes import register_routes
register_routes(app)

logger.info("Application started")

# Rutas de vistas
@app.route('/login')
def login_page():
    return render_template('modules/login/login.html')

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('modules/dashboard/dashboard.html')

@app.route('/nueva-licitacion')
@login_required
def nueva_licitacion():
    return render_template('modules/nueva-licitacion/nueva_licitacion.html')

@app.route('/gestion')
@login_required
def gestion():
    return render_template('modules/gestion/gestion.html')

@app.route('/gestion-nueva')
@login_required
def gestion_nueva():
    return render_template('modules/gestion/gestion_nueva.html')

@app.route('/resultado-licitacion/<int:id>')
@login_required
def resultado_licitacion(id):
    return render_template('modules/resultado-licitacion/resultado_licitacion.html')

@app.route('/polizas')
@login_required
def polizas():
    return render_template('modules/polizas/polizas.html')

@app.route('/documentacion')
@login_required
def documentacion():
    return render_template('modules/documentacion/documentacion.html')

@app.route('/administracion')
@login_required
def administracion():
    return render_template('modules/administracion/administracion.html')

@app.route('/metricas')
@login_required
def metricas():
    return render_template('modules/metricas/metricas.html')

@app.route('/ayuda')
@login_required
def ayuda():
    return render_template('modules/ayuda/ayuda.html')

@app.route('/editar-licitacion/<int:id>')
@login_required
def editar_licitacion(id):
    if id <= 0:
        abort(400)
    return render_template('modules/editar-licitacion/editar_licitacion.html', id=id)

@app.route('/presupuesto/<int:numero>')
@login_required
def ver_presupuesto(numero):
    if numero <= 0:
        abort(400)
    return render_template('modules/presupuesto/presupuesto.html', numero=escape(str(numero)))

@app.route('/favicon.ico')
def favicon():
    try:
        return send_from_directory(static_dir, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    except FileNotFoundError:
        return '', 204

@app.route('/shared/components/<path:filename>')
def serve_template(filename):
    return send_from_directory(os.path.join(template_dir, 'shared', 'components'), filename)

@app.route('/modules/<path:filename>')
def serve_modules(filename):
    return send_from_directory(os.path.join(template_dir, 'modules'), filename)

@app.route('/templates/<path:filename>')
def serve_templates(filename):
    return send_from_directory(os.path.join(template_dir, 'templates'), filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    is_production = os.environ.get('FLASK_ENV') == 'production'
    host = '0.0.0.0' if is_production else '127.0.0.1'
    app.run(host=host, port=port, debug=not is_production, use_reloader=False)
