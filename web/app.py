from flask import Flask, render_template
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import secrets

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.database.db_manager import DatabaseManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs('uploads', exist_ok=True)

# Registrar blueprints
from src.routes import register_routes
register_routes(app)

# Rutas de vistas
@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/nueva-licitacion')
def nueva_licitacion():
    return render_template('ingreso.html')

@app.route('/gestion')
def gestion():
    return render_template('gestion.html')

@app.route('/gestion-nueva')
def gestion_nueva():
    return render_template('gestion_nueva.html')

@app.route('/resultado-licitacion/<int:id>')
def resultado_licitacion(id):
    return render_template('resultado_licitacion.html')

@app.route('/polizas')
def polizas():
    return render_template('polizas.html')

@app.route('/documentacion')
def documentacion():
    return render_template('documentacion.html')

@app.route('/administracion')
def administracion():
    return render_template('administracion.html')

@app.route('/metricas')
def metricas():
    return render_template('metricas.html')

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/editar-licitacion/<int:id>')
def editar_licitacion(id):
    return render_template('editar_licitacion.html')

@app.route('/presupuesto/<int:numero>')
def ver_presupuesto(numero):
    return render_template('presupuesto.html', numero=numero)

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
