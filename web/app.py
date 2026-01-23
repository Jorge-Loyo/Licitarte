from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from database.db_manager import DatabaseManager
from werkzeug.utils import secure_filename

import os
import secrets

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = DatabaseManager('../database/licitaciones.db')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/administracion')
def administracion():
    return render_template('administracion.html')

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

# API Endpoints
@app.route('/api/catalogo', methods=['GET'])
def get_catalogo():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, numero_registro, monodroga, marca, presentacion, laboratorio, precio_caja, precio_unitario, fecha FROM celty ORDER BY monodroga, marca, presentacion")
        productos = cursor.fetchall()
    return jsonify([{
        'id': p[0],
        'numero_registro': p[1],
        'monodroga': p[2],
        'marca': p[3],
        'presentacion': p[4],
        'laboratorio': p[5],
        'precio_caja': p[6],
        'precio_unitario': p[7],
        'fecha': p[8]
    } for p in productos])

@app.route('/api/licitaciones', methods=['GET'])
def get_licitaciones():
    licitaciones = db.obtener_licitaciones()
    return jsonify([{
        'id': l[0],
        'numero': l[1],
        'cliente_id': l[2],
        'fecha': l[3],
        'oferente': l[4],
        'marca_ganadora': l[5],
        'precio_ganador': l[6]
    } for l in licitaciones])

@app.route('/api/licitaciones', methods=['POST'])
def crear_licitacion():
    data = request.json
    if not data:
        return jsonify({'success': False, 'error': 'No se recibieron datos'}), 400
    
    try:
        if not data.get('numero') or not data.get('fecha'):
            return jsonify({'success': False, 'error': 'Número y fecha son obligatorios'}), 400
        
        licitacion_id = db.crear_licitacion(
            data['numero'],
            data['fecha'],
            data.get('oferente', ''),
            data.get('marca_ganadora', ''),
            float(data['precio_ganador']) if data.get('precio_ganador') else None,
            int(data['cliente_id']) if data.get('cliente_id') else None
        )
        
        for producto in data.get('productos', []):
            db.agregar_producto(
                licitacion_id,
                producto['monodroga'],
                producto['marca'],
                producto['presentacion'],
                int(producto['cantidad']),
                float(producto['precio']),
                producto['resultado'],
                None,
                '',
                producto.get('marca_ofrecida', '')
            )
        
        return jsonify({'success': True, 'id': licitacion_id})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@app.route('/api/licitaciones/<int:id>', methods=['DELETE'])
def eliminar_licitacion(id):
    try:
        db.eliminar_licitacion(id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/productos/<int:licitacion_id>', methods=['GET'])
def get_productos(licitacion_id):
    productos = db.obtener_productos_licitacion(licitacion_id)
    return jsonify([{
        'id': p[0],
        'licitacion_id': p[1],
        'monodroga': p[2],
        'marca': p[3],
        'presentacion': p[4],
        'cantidad': p[5],
        'precio_ofertado': p[6],
        'resultado': p[7],
        'precio_ganador': p[8],
        'oferente': p[9],
        'marca_ofrecida': p[10]
    } for p in productos])

@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.json
    try:
        db.actualizar_producto(
            id,
            data['monodroga'],
            data['marca'],
            data['presentacion'],
            int(data['cantidad']),
            float(data['precio_ofertado']),
            data['resultado'],
            float(data['precio_ganador']) if data.get('precio_ganador') else None,
            data.get('oferente', ''),
            data.get('marca_ofrecida', '')
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/estadisticas', methods=['GET'])
def get_estadisticas():
    stats = db.obtener_estadisticas()
    return jsonify(stats)

@app.route('/api/historico', methods=['POST'])
def get_historico():
    data = request.json
    resultado = db.obtener_historico_producto(data['monodroga'], data['marca'], data['presentacion'])
    if resultado:
        return jsonify({
            'precio': resultado[0],
            'oferente': resultado[1],
            'marca_ofrecida': resultado[2],
            'fecha': resultado[3],
            'numero_licitacion': resultado[4]
        })
    return jsonify(None)

@app.route('/api/productos-adjudicados', methods=['GET'])
def get_productos_adjudicados():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.numero_licitacion, p.monodroga, p.marca, p.presentacion, p.cantidad, p.precio_ofertado, l.fecha
            FROM productos p
            JOIN licitaciones l ON p.licitacion_id = l.id
            WHERE p.resultado = 'Adjudicado'
            ORDER BY l.fecha DESC
        """)
        productos = cursor.fetchall()
    
    return jsonify([{
        'numero_licitacion': p[0],
        'monodroga': p[1],
        'marca': p[2],
        'presentacion': p[3],
        'cantidad': p[4],
        'precio': p[5],
        'fecha': p[6]
    } for p in productos])

# API Clientes
@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    clientes = db.obtener_clientes()
    return jsonify([{
        'id': c[0],
        'nombre': c[1],
        'razon_social': c[2],
        'cuit': c[3],
        'direccion': c[4],
        'telefono': c[5],
        'email': c[6]
    } for c in clientes])

@app.route('/api/clientes', methods=['POST'])
def crear_cliente():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    
    try:
        cliente_id = db.crear_cliente(
            data['nombre'],
            data.get('razon_social', ''),
            data.get('cuit', ''),
            data.get('direccion', ''),
            data.get('telefono', ''),
            data.get('email', '')
        )
        return jsonify({'success': True, 'id': cliente_id})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@app.route('/api/clientes/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    data = request.json
    try:
        db.actualizar_cliente(
            id,
            data['nombre'],
            data.get('razon_social', ''),
            data.get('cuit', ''),
            data.get('direccion', ''),
            data.get('telefono', ''),
            data.get('email', '')
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    try:
        db.eliminar_cliente(id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/cargar-catalogo', methods=['POST'])
def cargar_catalogo():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No se envió archivo'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No se seleccionó archivo'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Solo se permiten archivos .xlsx o .xls'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        result = db.cargar_catalogo_desde_excel(filepath)
        
        os.remove(filepath)
        
        if result:
            return jsonify({'success': True, 'message': 'Catálogo cargado exitosamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al procesar el archivo'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
