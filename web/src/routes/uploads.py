"""Rutas de carga masiva Excel"""
from flask import Blueprint, request, jsonify, current_app
import sys
import os
from pathlib import Path
from werkzeug.utils import secure_filename

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from shared.database.db_manager import DatabaseManager, USE_POSTGRES

bp = Blueprint('uploads', __name__, url_prefix='/api')
db = DatabaseManager(os.path.abspath('../shared/database/licitaciones.db'))

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# CATÁLOGO
@bp.route('/cargar-catalogo', methods=['POST'])
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
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        result = db.cargar_catalogo_desde_excel(filepath)
        os.remove(filepath)
        
        if result:
            return jsonify({'success': True, 'message': 'Catálogo cargado exitosamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al procesar el archivo'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# CATÁLOGO CRUD
@bp.route('/catalogo', methods=['POST'])
def crear_producto_catalogo():
    data = request.json
    if not data or not data.get('numero_registro'):
        return jsonify({'success': False, 'error': 'Número de registro es obligatorio'}), 400
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    INSERT INTO medicamentos (numero_registro, monodroga, marca, presentacion, laboratorio, 
                    precio_caja, precio_unitario, costo_unitario, fecha, troquel, cod_ab, troquel_ean, 
                    cod_monodroga, cod_laboratorio, multidosis)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    data['numero_registro'], data.get('monodroga', ''), data.get('marca', ''),
                    data.get('presentacion', ''), data.get('laboratorio', ''),
                    float(data['precio_caja']) if data.get('precio_caja') else None,
                    float(data['precio_unitario']) if data.get('precio_unitario') else None,
                    float(data['costo_unitario']) if data.get('costo_unitario') else None,
                    data.get('fecha', ''), data.get('troquel', ''), data.get('cod_ab'),
                    data.get('troquel_ean', ''), data.get('cod_monodroga'),
                    data.get('cod_laboratorio'), data.get('multidosis')
                ))
            else:
                cursor.execute("""
                    INSERT INTO medicamentos (numero_registro, monodroga, marca, presentacion, laboratorio, 
                    precio_caja, precio_unitario, costo_unitario, fecha, troquel, cod_ab, troquel_ean, 
                    cod_monodroga, cod_laboratorio, multidosis)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data['numero_registro'], data.get('monodroga', ''), data.get('marca', ''),
                    data.get('presentacion', ''), data.get('laboratorio', ''),
                    float(data['precio_caja']) if data.get('precio_caja') else None,
                    float(data['precio_unitario']) if data.get('precio_unitario') else None,
                    float(data['costo_unitario']) if data.get('costo_unitario') else None,
                    data.get('fecha', ''), data.get('troquel', ''), data.get('cod_ab'),
                    data.get('troquel_ean', ''), data.get('cod_monodroga'),
                    data.get('cod_laboratorio'), data.get('multidosis')
                ))
        return jsonify({'success': True}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/catalogo/<int:id>', methods=['PUT'])
def actualizar_producto_catalogo(id):
    data = request.json
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    UPDATE medicamentos SET numero_registro=%s, monodroga=%s, marca=%s, presentacion=%s, 
                    laboratorio=%s, precio_caja=%s, precio_unitario=%s, costo_unitario=%s, fecha=%s, 
                    troquel=%s, cod_ab=%s, troquel_ean=%s, cod_monodroga=%s, cod_laboratorio=%s, multidosis=%s WHERE id=%s
                """, (
                    data['numero_registro'], data.get('monodroga', ''), data.get('marca', ''),
                    data.get('presentacion', ''), data.get('laboratorio', ''),
                    float(data['precio_caja']) if data.get('precio_caja') else None,
                    float(data['precio_unitario']) if data.get('precio_unitario') else None,
                    float(data['costo_unitario']) if data.get('costo_unitario') else None,
                    data.get('fecha', ''), data.get('troquel', ''), data.get('cod_ab'),
                    data.get('troquel_ean', ''), data.get('cod_monodroga'),
                    data.get('cod_laboratorio'), data.get('multidosis'), id
                ))
            else:
                cursor.execute("""
                    UPDATE medicamentos SET numero_registro=?, monodroga=?, marca=?, presentacion=?, 
                    laboratorio=?, precio_caja=?, precio_unitario=?, costo_unitario=?, fecha=?, 
                    troquel=?, cod_ab=?, troquel_ean=?, cod_monodroga=?, cod_laboratorio=?, multidosis=? WHERE id=?
                """, (
                    data['numero_registro'], data.get('monodroga', ''), data.get('marca', ''),
                    data.get('presentacion', ''), data.get('laboratorio', ''),
                    float(data['precio_caja']) if data.get('precio_caja') else None,
                    float(data['precio_unitario']) if data.get('precio_unitario') else None,
                    float(data['costo_unitario']) if data.get('costo_unitario') else None,
                    data.get('fecha', ''), data.get('troquel', ''), data.get('cod_ab'),
                    data.get('troquel_ean', ''), data.get('cod_monodroga'),
                    data.get('cod_laboratorio'), data.get('multidosis'), id
                ))
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CLIENTES
@bp.route('/cargar-clientes', methods=['POST'])
def cargar_clientes():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No se envió archivo'}), 400
    
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Solo se permiten archivos .xlsx o .xls'}), 400
    
    try:
        import pandas as pd
        df = pd.read_excel(file)
        count = 0
        for _, row in df.iterrows():
            try:
                db.crear_cliente(
                    str(row.get('nombre', row.get('Nombre', ''))),
                    str(row.get('razon_social', row.get('Razon Social', ''))),
                    str(row.get('cuit', row.get('CUIT', ''))),
                    str(row.get('direccion', row.get('Direccion', ''))),
                    str(row.get('telefono', row.get('Telefono', ''))),
                    str(row.get('email', row.get('Email', ''))),
                    str(row.get('organismo_jurisdiccion', row.get('Organismo', '')))
                )
                count += 1
            except:
                continue
        return jsonify({'success': True, 'message': f'{count} clientes cargados'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# OFERENTES
@bp.route('/cargar-oferentes', methods=['POST'])
def cargar_oferentes():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No se envió archivo'}), 400
    
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Solo se permiten archivos .xlsx o .xls'}), 400
    
    try:
        import pandas as pd
        df = pd.read_excel(file)
        count = 0
        for _, row in df.iterrows():
            try:
                db.crear_oferente(str(row.get('nombre', row.get('Nombre', ''))))
                count += 1
            except:
                continue
        return jsonify({'success': True, 'message': f'{count} oferentes cargados'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# MARCAS
@bp.route('/cargar-marcas', methods=['POST'])
def cargar_marcas():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No se envió archivo'}), 400
    
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Solo se permiten archivos .xlsx o .xls'}), 400
    
    try:
        import pandas as pd
        df = pd.read_excel(file)
        count = 0
        for _, row in df.iterrows():
            try:
                db.crear_marca(str(row.get('nombre', row.get('Nombre', ''))))
                count += 1
            except:
                continue
        return jsonify({'success': True, 'message': f'{count} marcas cargadas'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# TIPOS LICITACIÓN
@bp.route('/cargar-tipos-licitacion', methods=['POST'])
def cargar_tipos_licitacion():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No se envió archivo'}), 400
    
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Solo se permiten archivos .xlsx o .xls'}), 400
    
    try:
        import pandas as pd
        df = pd.read_excel(file)
        count = 0
        for _, row in df.iterrows():
            try:
                db.crear_tipo_licitacion(str(row.get('nombre', row.get('Nombre', ''))))
                count += 1
            except:
                continue
        return jsonify({'success': True, 'message': f'{count} tipos cargados'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
