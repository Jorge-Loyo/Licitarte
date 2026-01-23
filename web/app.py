from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from database.db_manager import DatabaseManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'licitarte-secret-key-2024'
db = DatabaseManager('../database/licitaciones.db')

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

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

# API Endpoints
@app.route('/api/licitaciones', methods=['GET'])
def get_licitaciones():
    licitaciones = db.obtener_licitaciones()
    return jsonify([{
        'id': l[0],
        'numero': l[1],
        'fecha': l[2],
        'laboratorio': l[3]
    } for l in licitaciones])

@app.route('/api/licitaciones', methods=['POST'])
def crear_licitacion():
    data = request.json
    try:
        licitacion_id = db.crear_licitacion(
            data['numero'],
            data['fecha'],
            data.get('laboratorio', '')
        )
        
        for producto in data.get('productos', []):
            db.agregar_producto(
                licitacion_id,
                producto['item'],
                int(producto['cantidad']),
                float(producto['precio']),
                producto['resultado'],
                None,
                producto.get('laboratorio', '')
            )
        
        return jsonify({'success': True, 'id': licitacion_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

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
        'item': p[2],
        'cantidad': p[3],
        'precio_ofertado': p[4],
        'resultado': p[5],
        'precio_ganador': p[6],
        'laboratorio': p[7]
    } for p in productos])

@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.json
    try:
        db.actualizar_producto(
            id,
            data['item'],
            int(data['cantidad']),
            float(data['precio_ofertado']),
            data['resultado'],
            float(data['precio_ganador']) if data.get('precio_ganador') else None,
            data.get('laboratorio', '')
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/estadisticas', methods=['GET'])
def get_estadisticas():
    stats = db.obtener_estadisticas()
    return jsonify(stats)

@app.route('/api/historico/<producto>', methods=['GET'])
def get_historico(producto):
    resultado = db.obtener_historico_producto(producto)
    if resultado:
        return jsonify({
            'precio': resultado[0],
            'laboratorio': resultado[1],
            'fecha': resultado[2],
            'numero_licitacion': resultado[3]
        })
    return jsonify(None)

@app.route('/api/productos-adjudicados', methods=['GET'])
def get_productos_adjudicados():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.numero_licitacion, p.item_producto, p.cantidad, p.precio_ofertado, l.fecha
            FROM productos p
            JOIN licitaciones l ON p.licitacion_id = l.id
            WHERE p.resultado = 'Adjudicado'
            ORDER BY l.fecha DESC
        """)
        productos = cursor.fetchall()
    
    return jsonify([{
        'numero_licitacion': p[0],
        'producto': p[1],
        'cantidad': p[2],
        'precio': p[3],
        'fecha': p[4]
    } for p in productos])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
