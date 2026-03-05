"""Rutas de carga masiva Excel"""
from flask import Blueprint, request, jsonify, current_app
import sys
import os
from pathlib import Path
from werkzeug.utils import secure_filename

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from backend.database.db_manager import DatabaseManager, USE_POSTGRES

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
    if not file.filename or file.filename == '':
        return jsonify({'success': False, 'error': 'No se seleccionó archivo'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Solo se permiten archivos .xlsx o .xls'}), 400
    
    try:
        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({'success': False, 'error': 'Nombre de archivo inválido'}), 400
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        def generate():
            import pandas as pd
            try:
                df = pd.read_excel(filepath)
                total_rows = len(df)
                batch_size = 1000
                
                yield f'data: {{"progress": 0, "total": {total_rows}, "message": "Iniciando carga..."}}\n\n'
                
                for batch_start in range(0, total_rows, batch_size):
                    batch_end = min(batch_start + batch_size, total_rows)
                    df_batch = df.iloc[batch_start:batch_end]
                    
                    with db.get_connection() as conn:
                        cursor = conn.cursor()
                        for _, row in df_batch.iterrows():
                            try:
                                numero_registro = str(row.get('N de Registro', '')) if pd.notna(row.get('N de Registro')) else ''
                                if not numero_registro or numero_registro == 'nan':
                                    continue
                                    
                                troquel = str(row.get('Troquel', '')) if pd.notna(row.get('Troquel')) else None
                                cod_ab = int(row.get('Cod AB')) if pd.notna(row.get('Cod AB')) and row.get('Cod AB') else None
                                troquel_ean = str(row.get('Troquel.1', '')) if pd.notna(row.get('Troquel.1')) else None
                                cod_monodroga = int(row.get('Cod Monodroga')) if pd.notna(row.get('Cod Monodroga')) and row.get('Cod Monodroga') else None
                                monodroga_excel = str(row.get('Monodroga', '')) if pd.notna(row.get('Monodroga')) else ''
                                cod_laboratorio = int(row.get('Cod Laboratorio')) if pd.notna(row.get('Cod Laboratorio')) and row.get('Cod Laboratorio') else None
                                laboratorio_excel = str(row.get('Laboratorio', '')) if pd.notna(row.get('Laboratorio')) else ''
                                marca = str(row.get('Marca', '')) if pd.notna(row.get('Marca')) else ''
                                presentacion = str(row.get('Presentacion', '')) if pd.notna(row.get('Presentacion')) else ''
                                multidosis = int(row.get('Multidosis')) if pd.notna(row.get('Multidosis')) and row.get('Multidosis') else None
                                precio_caja = float(row.get('Precio x caja', 0)) if pd.notna(row.get('Precio x caja')) else None
                                precio_unitario = float(row.get('Precio unitario', 0)) if pd.notna(row.get('Precio unitario')) else None
                                
                                fecha_raw = row.get('Fecha')
                                if pd.notna(fecha_raw):
                                    if isinstance(fecha_raw, str):
                                        fecha = fecha_raw.split()[0] if ' ' in fecha_raw else fecha_raw
                                    else:
                                        fecha = fecha_raw.strftime('%d/%m/%Y')
                                else:
                                    fecha = ''
                                
                                monodroga_final = monodroga_excel.strip()
                                if monodroga_excel and monodroga_excel.strip():
                                    if USE_POSTGRES:
                                        cursor.execute("INSERT INTO monodrogas (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING", (monodroga_excel.strip(),))
                                        cursor.execute("SELECT nombre FROM monodrogas WHERE LOWER(nombre) = LOWER(%s)", (monodroga_excel.strip(),))
                                    else:
                                        cursor.execute("INSERT OR IGNORE INTO monodrogas (nombre) VALUES (?)", (monodroga_excel.strip(),))
                                        cursor.execute("SELECT nombre FROM monodrogas WHERE LOWER(nombre) = LOWER(?)", (monodroga_excel.strip(),))
                                    result = cursor.fetchone()
                                    if result:
                                        monodroga_final = result[0]
                                
                                laboratorio_final = laboratorio_excel.strip()
                                if laboratorio_excel and laboratorio_excel.strip():
                                    if USE_POSTGRES:
                                        cursor.execute("INSERT INTO laboratorios (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING", (laboratorio_excel.strip(),))
                                        cursor.execute("SELECT nombre FROM laboratorios WHERE LOWER(nombre) = LOWER(%s)", (laboratorio_excel.strip(),))
                                    else:
                                        cursor.execute("INSERT OR IGNORE INTO laboratorios (nombre) VALUES (?)", (laboratorio_excel.strip(),))
                                        cursor.execute("SELECT nombre FROM laboratorios WHERE LOWER(nombre) = LOWER(?)", (laboratorio_excel.strip(),))
                                    result = cursor.fetchone()
                                    if result:
                                        laboratorio_final = result[0]
                                
                                if USE_POSTGRES:
                                    cursor.execute("""
                                        INSERT INTO medicamentos (numero_registro, troquel, cod_ab, troquel_ean, cod_monodroga,
                                        monodroga, cod_laboratorio, laboratorio, marca, presentacion, multidosis,
                                        precio_caja, precio_unitario, fecha) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        ON CONFLICT (numero_registro) DO UPDATE SET
                                            troquel = EXCLUDED.troquel, cod_ab = EXCLUDED.cod_ab,
                                            troquel_ean = EXCLUDED.troquel_ean, cod_monodroga = EXCLUDED.cod_monodroga,
                                            monodroga = EXCLUDED.monodroga, cod_laboratorio = EXCLUDED.cod_laboratorio,
                                            laboratorio = EXCLUDED.laboratorio, marca = EXCLUDED.marca,
                                            presentacion = EXCLUDED.presentacion, multidosis = EXCLUDED.multidosis,
                                            precio_caja = EXCLUDED.precio_caja, precio_unitario = EXCLUDED.precio_unitario,
                                            fecha = EXCLUDED.fecha
                                    """, (numero_registro, troquel, cod_ab, troquel_ean, cod_monodroga, monodroga_final,
                                          cod_laboratorio, laboratorio_final, marca, presentacion, multidosis,
                                          precio_caja, precio_unitario, fecha))
                                else:
                                    cursor.execute("""
                                        INSERT OR REPLACE INTO medicamentos (numero_registro, troquel, cod_ab, troquel_ean,
                                        cod_monodroga, monodroga, cod_laboratorio, laboratorio, marca, presentacion,
                                        multidosis, precio_caja, precio_unitario, fecha) 
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    """, (numero_registro, troquel, cod_ab, troquel_ean, cod_monodroga, monodroga_final,
                                          cod_laboratorio, laboratorio_final, marca, presentacion, multidosis,
                                          precio_caja, precio_unitario, fecha))
                            except Exception as e:
                                current_app.logger.warning(f"Error procesando fila: {str(e)}")
                        conn.commit()
                    
                    yield f'data: {{"progress": {batch_end}, "total": {total_rows}, "message": "Procesado lote {batch_start}-{batch_end} de {total_rows}"}}\n\n'
                
                yield f'data: {{"progress": {total_rows}, "total": {total_rows}, "message": "Completado", "done": true}}\n\n'
            except Exception as e:
                yield f'data: {{"error": "{str(e)}"}}\n\n'
            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)
        
        return current_app.response_class(generate(), mimetype='text/event-stream')
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
                    data.get('numero_registro'), data.get('monodroga', ''), data.get('marca', ''),
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
                    data.get('numero_registro'), data.get('monodroga', ''), data.get('marca', ''),
                    data.get('presentacion', ''), data.get('laboratorio', ''),
                    float(data['precio_caja']) if data.get('precio_caja') else None,
                    float(data['precio_unitario']) if data.get('precio_unitario') else None,
                    float(data['costo_unitario']) if data.get('costo_unitario') else None,
                    data.get('fecha', ''), data.get('troquel', ''), data.get('cod_ab'),
                    data.get('troquel_ean', ''), data.get('cod_monodroga'),
                    data.get('cod_laboratorio'), data.get('multidosis')
                ))
            conn.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/catalogo/<int:id>', methods=['PUT'])
def actualizar_producto_catalogo(id):
    data = request.json
    if not data:
        return jsonify({'success': False, 'error': 'Request body no puede estar vacío'}), 400
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    UPDATE medicamentos SET numero_registro=%s, monodroga=%s, marca=%s, presentacion=%s, 
                    laboratorio=%s, precio_caja=%s, precio_unitario=%s, costo_unitario=%s, fecha=%s, 
                    troquel=%s, cod_ab=%s, troquel_ean=%s, cod_monodroga=%s, cod_laboratorio=%s, multidosis=%s WHERE id=%s
                """, (
                    data.get('numero_registro'), data.get('monodroga', ''), data.get('marca', ''),
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
                    data.get('numero_registro'), data.get('monodroga', ''), data.get('marca', ''),
                    data.get('presentacion', ''), data.get('laboratorio', ''),
                    float(data['precio_caja']) if data.get('precio_caja') else None,
                    float(data['precio_unitario']) if data.get('precio_unitario') else None,
                    float(data['costo_unitario']) if data.get('costo_unitario') else None,
                    data.get('fecha', ''), data.get('troquel', ''), data.get('cod_ab'),
                    data.get('troquel_ean', ''), data.get('cod_monodroga'),
                    data.get('cod_laboratorio'), data.get('multidosis'), id
                ))
            conn.commit()
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
            except Exception:
                current_app.logger.warning("Error procesando cliente")
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
            except Exception:
                current_app.logger.warning("Error procesando oferente")
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
            except Exception:
                current_app.logger.warning("Error procesando marca")
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
            except Exception:
                current_app.logger.warning("Error procesando tipo licitacion")
        return jsonify({'success': True, 'message': f'{count} tipos cargados'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# MONODROGAS
@bp.route('/cargar-monodrogas', methods=['POST'])
def cargar_monodrogas():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No se envió archivo'}), 400
    
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Solo se permiten archivos .xlsx o .xls'}), 400
    
    try:
        import pandas as pd
        df = pd.read_excel(file)
        count = 0
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            for _, row in df.iterrows():
                try:
                    id_monodroga = int(row.get('ID', row.get('id', row.get('Cod Monodroga', 0))))
                    descripcion = str(row.get('Descripcion', row.get('descripcion', row.get('Monodroga', ''))))
                    
                    if id_monodroga and descripcion:
                        if USE_POSTGRES:
                            cursor.execute(
                                "INSERT INTO monodrogas (id, nombre) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
                                (id_monodroga, descripcion.strip())
                            )
                        else:
                            cursor.execute(
                                "INSERT OR IGNORE INTO monodrogas (id, nombre) VALUES (?, ?)",
                                (id_monodroga, descripcion.strip())
                            )
                        count += 1
                except Exception:
                    current_app.logger.warning("Error procesando monodroga")
            conn.commit()
        
        return jsonify({'success': True, 'message': f'{count} monodrogas cargadas'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# LABORATORIOS
@bp.route('/cargar-laboratorios', methods=['POST'])
def cargar_laboratorios():
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
                # Buscar ID
                id_laboratorio = None
                for col in ['ID', 'id', 'Id', 'Cod Laboratorio', 'cod_laboratorio']:
                    if col in df.columns and pd.notna(row.get(col)):
                        id_laboratorio = int(row.get(col)) if row.get(col) else None
                        break
                
                # Buscar Descripción
                descripcion = None
                for col in ['Descripcion', 'descripcion', 'Descripción', 'Laboratorio', 'laboratorio', 'Nombre', 'nombre']:
                    if col in df.columns and pd.notna(row.get(col)):
                        descripcion = str(row.get(col))
                        break
                
                if id_laboratorio and descripcion:
                    with db.get_connection() as conn:
                        cursor = conn.cursor()
                        if USE_POSTGRES:
                            cursor.execute(
                                "INSERT INTO laboratorios (id, nombre) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING",
                                (id_laboratorio, descripcion.strip())
                            )
                        else:
                            cursor.execute(
                                "INSERT OR IGNORE INTO laboratorios (id, nombre) VALUES (?, ?)",
                                (id_laboratorio, descripcion.strip())
                            )
                        conn.commit()
                    count += 1
            except Exception as e:
                print(f"Error en fila ID={id_laboratorio}: {e}")
                continue
        
        return jsonify({'success': True, 'message': f'{count} laboratorios cargados'})
    except Exception as e:
        print(f"Error general: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
