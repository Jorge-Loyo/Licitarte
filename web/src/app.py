"""Aplicación Flask Licitarte - Refactorizada v1.3.0"""
from flask import Flask, render_template
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.routes import register_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs('uploads', exist_ok=True)

# Registrar blueprints
register_routes(app)

# Rutas de vistas (templates)
@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/')
def index():
    return render_template('dashboard.html')

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
