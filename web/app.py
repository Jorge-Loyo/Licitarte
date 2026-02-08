from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

sys.path.insert(0, os.path.abspath('..'))
from database.db_manager import DatabaseManager, USE_POSTGRES
from werkzeug.utils import secure_filename

import secrets

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = DatabaseManager(os.path.abspath('../database/licitaciones.db'))

# Ejecutar migraciones v1.1.0 automáticamente
if USE_POSTGRES:
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute("ALTER TABLE celty ADD COLUMN costo_unitario REAL")
                conn.commit()
            except:
                pass
            
            try:
                cursor.execute("CREATE TABLE portales_origen (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Comprar', 'BAC', 'Otro']:
                    cursor.execute("INSERT INTO portales_origen (nombre) VALUES (%s)", (v,))
                conn.commit()
            except:
                pass
            
            try:
                cursor.execute("CREATE TABLE modalidades_entrega (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Única', 'Múltiple', 'Programada']:
                    cursor.execute("INSERT INTO modalidades_entrega (nombre) VALUES (%s)", (v,))
                conn.commit()
            except:
                pass
            
            try:
                cursor.execute("CREATE TABLE formas_pago (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Contado', '30 días', '60 días']:
                    cursor.execute("INSERT INTO formas_pago (nombre) VALUES (%s)", (v,))
                conn.commit()
            except:
                pass
            
            try:
                cursor.execute("CREATE TABLE organismos_jurisdiccion (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Nacional', 'Provincial', 'Municipal', 'CABA', 'Privado']:
                    cursor.execute("INSERT INTO organismos_jurisdiccion (nombre) VALUES (%s)", (v,))
                conn.commit()
            except:
                pass
            
            try:
                cursor.execute("CREATE TABLE motivos_perdida (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Precio más alto', 'Marca no priorizada', 'No cumplía especificación', 'Error administrativo', 'Otro']:
                    cursor.execute("INSERT INTO motivos_perdida (nombre) VALUES (%s)", (v,))
                conn.commit()
            except:
                pass
            
            for col in ['portal_origen', 'modalidad_entrega', 'forma_pago', 'observaciones']:
                try:
                    cursor.execute(f"ALTER TABLE licitaciones ADD COLUMN {col} TEXT")
                    conn.commit()
                except:
                    pass
            
            try:
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN requiere_poliza BOOLEAN")
                conn.commit()
            except:
                pass
            
            try:
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN monto_poliza REAL")
                conn.commit()
            except:
                pass
            
            try:
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN tipo_licitacion_id INTEGER")
                conn.commit()
            except:
                pass
            
            try:
                cursor.execute("ALTER TABLE clientes ADD COLUMN organismo_jurisdiccion TEXT")
                conn.commit()
            except:
                pass
            
            try:
                cursor.execute("ALTER TABLE productos ADD COLUMN motivo_perdida TEXT")
                conn.commit()
            except:
                pass
            
            try:
                cursor.execute("ALTER TABLE productos ADD COLUMN producto_cotizar TEXT DEFAULT 'principal'")
                conn.commit()
            except:
                pass
    except Exception:
        pass

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

# API Endpoints
@app.route('/api/catalogo', methods=['GET'])
def get_catalogo():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, numero_registro, monodroga, marca, presentacion, laboratorio, precio_caja, precio_unitario, costo_unitario, fecha FROM celty ORDER BY monodroga, marca, presentacion")
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
        'costo_unitario': p[8],
        'fecha': p[9]
    } for p in productos])

@app.route('/api/catalogo', methods=['POST'])
def crear_producto_catalogo():
    data = request.json
    if not data or not data.get('numero_registro'):
        return jsonify({'success': False, 'error': 'Número de registro es obligatorio'}), 400
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    INSERT INTO celty (numero_registro, monodroga, marca, presentacion, laboratorio, precio_caja, precio_unitario, costo_unitario, fecha)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    data['numero_registro'],
                    data.get('monodroga', ''),
                    data.get('marca', ''),
                    data.get('presentacion', ''),
                    data.get('laboratorio', ''),
                    float(data['precio_caja']) if data.get('precio_caja') else None,
                    float(data['precio_unitario']) if data.get('precio_unitario') else None,
                    float(data['costo_unitario']) if data.get('costo_unitario') else None,
                    data.get('fecha', '')
                ))
            else:
                cursor.execute("""
                    INSERT INTO celty (numero_registro, monodroga, marca, presentacion, laboratorio, precio_caja, precio_unitario, costo_unitario, fecha)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data['numero_registro'],
                    data.get('monodroga', ''),
                    data.get('marca', ''),
                    data.get('presentacion', ''),
                    data.get('laboratorio', ''),
                    float(data['precio_caja']) if data.get('precio_caja') else None,
                    float(data['precio_unitario']) if data.get('precio_unitario') else None,
                    float(data['costo_unitario']) if data.get('costo_unitario') else None,
                    data.get('fecha', '')
                ))
        return jsonify({'success': True}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/catalogo/<int:id>', methods=['PUT'])
def actualizar_producto_catalogo(id):
    data = request.json
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    UPDATE celty SET numero_registro=%s, monodroga=%s, marca=%s, presentacion=%s, 
                    laboratorio=%s, precio_caja=%s, precio_unitario=%s, costo_unitario=%s, fecha=%s WHERE id=%s
                """, (
                    data['numero_registro'],
                    data.get('monodroga', ''),
                    data.get('marca', ''),
                    data.get('presentacion', ''),
                    data.get('laboratorio', ''),
                    float(data['precio_caja']) if data.get('precio_caja') else None,
                    float(data['precio_unitario']) if data.get('precio_unitario') else None,
                    float(data['costo_unitario']) if data.get('costo_unitario') else None,
                    data.get('fecha', ''),
                    id
                ))
            else:
                cursor.execute("""
                    UPDATE celty SET numero_registro=?, monodroga=?, marca=?, presentacion=?, 
                    laboratorio=?, precio_caja=?, precio_unitario=?, costo_unitario=?, fecha=? WHERE id=?
                """, (
                    data['numero_registro'],
                    data.get('monodroga', ''),
                    data.get('marca', ''),
                    data.get('presentacion', ''),
                    data.get('laboratorio', ''),
                    float(data['precio_caja']) if data.get('precio_caja') else None,
                    float(data['precio_unitario']) if data.get('precio_unitario') else None,
                    float(data['costo_unitario']) if data.get('costo_unitario') else None,
                    data.get('fecha', ''),
                    id
                ))
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/licitaciones', methods=['GET'])
def get_licitaciones():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.id, l.numero_licitacion, l.fecha, l.oferente_ganador, l.marca_ganadora, l.precio_ganador,
                   c.nombre as cliente, t.nombre as tipo_licitacion, l.numero_presupuesto
            FROM licitaciones l
            LEFT JOIN clientes c ON l.cliente_id = c.id
            LEFT JOIN tipos_licitacion t ON l.tipo_licitacion_id = t.id
            ORDER BY l.fecha DESC
        """)
        licitaciones = cursor.fetchall()
        
        # Calcular ganancia y total cotizado para cada licitación
        resultado = []
        for l in licitaciones:
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT COUNT(*) as total,
                           SUM(CASE WHEN resultado = 'Adjudicado' THEN 1 ELSE 0 END) as adjudicados,
                           COALESCE(SUM(precio_ofertado * cantidad), 0) as total_cotizado
                    FROM productos WHERE licitacion_id = %s
                """, (l[0],))
            else:
                cursor.execute("""
                    SELECT COUNT(*) as total,
                           SUM(CASE WHEN resultado = 'Adjudicado' THEN 1 ELSE 0 END) as adjudicados,
                           COALESCE(SUM(precio_ofertado * cantidad), 0) as total_cotizado
                    FROM productos WHERE licitacion_id = ?
                """, (l[0],))
            stats = cursor.fetchone()
            total = stats[0] or 0
            adjudicados = stats[1] or 0
            total_cotizado = float(stats[2]) if stats[2] else 0.0
            ganancia = f"{adjudicados}/{total}" if total > 0 else "-"
            
            resultado.append({
                'id': l[0],
                'numero': l[1],
                'fecha': l[2],
                'oferente': l[3],
                'marca_ganadora': l[4],
                'precio_ganador': l[5],
                'cliente': l[6] or '-',
                'tipo_licitacion': l[7] or '-',
                'numero_presupuesto': l[8],
                'total_cotizado': total_cotizado,
                'ganancia': ganancia
            })
    
    return jsonify(resultado)

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
            '',
            '',
            None,
            int(data['cliente_id']) if data.get('cliente_id') else None,
            int(data['tipo_licitacion_id']) if data.get('tipo_licitacion_id') else None,
            data.get('portal_origen', ''),
            data.get('modalidad_entrega', ''),
            data.get('forma_pago', ''),
            data.get('requiere_poliza', False),
            float(data['monto_poliza']) if data.get('monto_poliza') else None,
            data.get('observaciones', ''),
            data.get('mantenimiento_oferta', '')
        )
        
        for producto in data.get('productos', []):
            producto_id = db.agregar_producto(
                licitacion_id,
                producto['monodroga'],
                producto['marca'],
                producto['presentacion'],
                int(producto['cantidad']),
                float(producto['precio']),
                producto['resultado'],
                float(producto['precio_ganador']) if producto.get('precio_ganador') else None,
                producto.get('oferente_ganador', ''),
                producto.get('marca_ofrecida', ''),
                producto.get('marca_ganadora', ''),
                producto.get('motivo_perdida', ''),
                producto.get('numero_renglon', ''),
                float(producto['costo_unitario']) if producto.get('costo_unitario') else None,
                float(producto['margen_porcentaje']) if producto.get('margen_porcentaje') else None,
                producto.get('observaciones', ''),
                producto.get('producto_cotizar', 'principal')
            )
            
            for alternativa in producto.get('alternativas', []):
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    if USE_POSTGRES:
                        cursor.execute("""
                            INSERT INTO alternativas_productos 
                            (producto_id, marca, presentacion, laboratorio, costo_unitario, margen_porcentaje, precio_ofertado, observaciones)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            producto_id,
                            alternativa.get('marca', ''),
                            alternativa.get('presentacion', ''),
                            alternativa.get('laboratorio', ''),
                            float(alternativa['costo_unitario']) if alternativa.get('costo_unitario') else None,
                            float(alternativa['margen_porcentaje']) if alternativa.get('margen_porcentaje') else None,
                            float(alternativa['precio_ofertado']) if alternativa.get('precio_ofertado') else None,
                            alternativa.get('observaciones', '')
                        ))
                    else:
                        cursor.execute("""
                            INSERT INTO alternativas_productos 
                            (producto_id, marca, presentacion, laboratorio, costo_unitario, margen_porcentaje, precio_ofertado, observaciones)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            producto_id,
                            alternativa.get('marca', ''),
                            alternativa.get('presentacion', ''),
                            alternativa.get('laboratorio', ''),
                            float(alternativa['costo_unitario']) if alternativa.get('costo_unitario') else None,
                            float(alternativa['margen_porcentaje']) if alternativa.get('margen_porcentaje') else None,
                            float(alternativa['precio_ofertado']) if alternativa.get('precio_ofertado') else None,
                            alternativa.get('observaciones', '')
                        ))
        
        return jsonify({'success': True, 'id': licitacion_id}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@app.route('/api/licitaciones/<int:id>', methods=['DELETE'])
def eliminar_licitacion(id):
    try:
        db.eliminar_licitacion(id)
        return '', 204
    except Exception as e:
        print(f"ERROR eliminando licitación {id}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/licitaciones/<int:id>', methods=['GET'])
def get_licitacion(id):
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT l.numero_licitacion, c.nombre as cliente
                    FROM licitaciones l
                    LEFT JOIN clientes c ON l.cliente_id = c.id
                    WHERE l.id = %s
                """, (id,))
            else:
                cursor.execute("""
                    SELECT l.numero_licitacion, c.nombre as cliente
                    FROM licitaciones l
                    LEFT JOIN clientes c ON l.cliente_id = c.id
                    WHERE l.id = ?
                """, (id,))
            row = cursor.fetchone()
            if row:
                return jsonify({'numero': row[0], 'cliente': row[1] or '-'})
            return jsonify({'error': 'No encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/licitaciones/<int:id>', methods=['PUT'])
def actualizar_licitacion(id):
    data = request.json
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    UPDATE licitaciones 
                    SET numero_licitacion=%s, fecha=%s, cliente_id=%s, tipo_licitacion_id=%s,
                        portal_origen=%s, modalidad_entrega=%s, forma_pago=%s,
                        requiere_poliza=%s, monto_poliza=%s, observaciones=%s, mantenimiento_oferta=%s,
                        tipo_adjudicacion=%s
                    WHERE id=%s
                """, (
                    data['numero'],
                    data['fecha'],
                    int(data['cliente_id']) if data.get('cliente_id') else None,
                    int(data['tipo_licitacion_id']) if data.get('tipo_licitacion_id') else None,
                    data.get('portal_origen', ''),
                    data.get('modalidad_entrega', ''),
                    data.get('forma_pago', ''),
                    data.get('requiere_poliza', False),
                    float(data['monto_poliza']) if data.get('monto_poliza') else None,
                    data.get('observaciones', ''),
                    data.get('mantenimiento_oferta', ''),
                    data.get('tipo_adjudicacion', 'Parcial'),
                    id
                ))
            else:
                cursor.execute("""
                    UPDATE licitaciones 
                    SET numero_licitacion=?, fecha=?, cliente_id=?, tipo_licitacion_id=?,
                        portal_origen=?, modalidad_entrega=?, forma_pago=?,
                        requiere_poliza=?, monto_poliza=?, observaciones=?, mantenimiento_oferta=?,
                        tipo_adjudicacion=?
                    WHERE id=?
                """, (
                    data['numero'],
                    data['fecha'],
                    int(data['cliente_id']) if data.get('cliente_id') else None,
                    int(data['tipo_licitacion_id']) if data.get('tipo_licitacion_id') else None,
                    data.get('portal_origen', ''),
                    data.get('modalidad_entrega', ''),
                    data.get('forma_pago', ''),
                    data.get('requiere_poliza', False),
                    float(data['monto_poliza']) if data.get('monto_poliza') else None,
                    data.get('observaciones', ''),
                    data.get('mantenimiento_oferta', ''),
                    data.get('tipo_adjudicacion', 'Parcial'),
                    id
                ))
        
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/productos/<int:licitacion_id>', methods=['GET'])
def get_productos(licitacion_id):
    productos = db.obtener_productos_licitacion(licitacion_id)
    result = []
    for p in productos:
        producto_dict = {
            'id': p[0],
            'licitacion_id': p[1],
            'monodroga': p[2],
            'marca': p[3],
            'presentacion': p[4],
            'cantidad': p[5],
            'precio_ofertado': p[6],
            'resultado': p[7],
            'precio_ganador': p[8],
            'oferente_ganador': p[9],  # Cambiar de 'oferente' a 'oferente_ganador'
            'marca_ofrecida': p[10],
            'marca_ganadora': p[11] if len(p) > 11 else '',
            'motivo_perdida': p[12] if len(p) > 12 else '',
            'numero_renglon': p[13] if len(p) > 13 else '',
            'costo_unitario': p[14] if len(p) > 14 else None,
            'margen_porcentaje': p[15] if len(p) > 15 else None,
            'observaciones': p[16] if len(p) > 16 else '',
            'producto_cotizar': p[17] if len(p) > 17 else 'principal'
        }
        result.append(producto_dict)
    return jsonify(result)

@app.route('/api/productos', methods=['POST'])
def crear_producto():
    data = request.json
    try:
        producto_id = db.agregar_producto(
            data['licitacion_id'],
            data['monodroga'],
            data['marca'],
            data['presentacion'],
            int(data['cantidad']),
            float(data['precio_ofertado']),
            data['resultado'],
            float(data['precio_ganador']) if data.get('precio_ganador') else None,
            data.get('oferente', ''),
            data.get('marca_ofrecida', ''),
            data.get('marca_ganadora', ''),
            data.get('motivo_perdida', ''),
            data.get('numero_renglon', ''),
            float(data['costo_unitario']) if data.get('costo_unitario') else None,
            float(data['margen_porcentaje']) if data.get('margen_porcentaje') else None,
            data.get('observaciones', ''),
            data.get('producto_cotizar', 'principal')
        )
        return jsonify({'success': True, 'id': producto_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

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
            data.get('marca_ofrecida', ''),
            data.get('marca_ganadora', ''),
            data.get('motivo_perdida', ''),
            data.get('numero_renglon', ''),
            float(data['costo_unitario']) if data.get('costo_unitario') else None,
            float(data['margen_porcentaje']) if data.get('margen_porcentaje') else None,
            data.get('observaciones', ''),
            data.get('producto_cotizar', 'principal')
        )
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estadisticas', methods=['GET'])
def get_estadisticas():
    stats = db.obtener_estadisticas()
    return jsonify(stats)

@app.route('/api/historico', methods=['POST'])
def get_historico():
    data = request.json
    filtro = data.get('monodroga', '')
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        if filtro:
            if db.USE_POSTGRES:
                cursor.execute("""
                    SELECT l.numero_licitacion, t.nombre as tipo_licitacion, p.marca, p.presentacion, 
                           p.cantidad, p.precio_ofertado, l.fecha
                    FROM productos p
                    JOIN licitaciones l ON p.licitacion_id = l.id
                    LEFT JOIN tipos_licitacion t ON l.tipo_licitacion_id = t.id
                    WHERE p.resultado = 'Adjudicado'
                      AND p.monodroga ILIKE %s
                    ORDER BY l.fecha DESC
                """, (f'%{filtro}%',))
            else:
                cursor.execute("""
                    SELECT l.numero_licitacion, t.nombre as tipo_licitacion, p.marca, p.presentacion, 
                           p.cantidad, p.precio_ofertado, l.fecha
                    FROM productos p
                    JOIN licitaciones l ON p.licitacion_id = l.id
                    LEFT JOIN tipos_licitacion t ON l.tipo_licitacion_id = t.id
                    WHERE p.resultado = 'Adjudicado'
                      AND p.monodroga LIKE ?
                    ORDER BY l.fecha DESC
                """, (f'%{filtro}%',))
        else:
            cursor.execute("""
                SELECT l.numero_licitacion, t.nombre as tipo_licitacion, p.marca, p.presentacion, 
                       p.cantidad, p.precio_ofertado, l.fecha
                FROM productos p
                JOIN licitaciones l ON p.licitacion_id = l.id
                LEFT JOIN tipos_licitacion t ON l.tipo_licitacion_id = t.id
                WHERE p.resultado = 'Adjudicado'
                ORDER BY l.fecha DESC
            """)
        
        productos = cursor.fetchall()
    
    return jsonify([{
        'numero_licitacion': p[0],
        'tipo_licitacion': p[1] or '-',
        'marca': p[2],
        'presentacion': p[3],
        'cantidad': p[4],
        'precio': p[5],
        'fecha': p[6]
    } for p in productos])

@app.route('/api/productos-adjudicados', methods=['GET'])
def get_productos_adjudicados():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.numero_licitacion, t.nombre as tipo_licitacion, c.nombre as cliente, 
                   p.monodroga, p.marca, p.presentacion, p.cantidad, p.precio_ofertado, l.fecha
            FROM productos p
            JOIN licitaciones l ON p.licitacion_id = l.id
            LEFT JOIN clientes c ON l.cliente_id = c.id
            LEFT JOIN tipos_licitacion t ON l.tipo_licitacion_id = t.id
            WHERE p.resultado = 'Adjudicado'
            ORDER BY l.fecha DESC
        """)
        productos = cursor.fetchall()
    
    return jsonify([{
        'numero_licitacion': p[0],
        'tipo_licitacion': p[1] or '-',
        'cliente': p[2] or '-',
        'monodroga': p[3],
        'marca': p[4],
        'presentacion': p[5],
        'cantidad': p[6],
        'precio': p[7],
        'fecha': p[8]
    } for p in productos])

# API Clientes
@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    clientes = db.obtener_clientes()
    result = [{
        'id': c[0],
        'nombre': c[1],
        'razon_social': c[2],
        'cuit': c[3],
        'direccion': c[4],
        'telefono': c[5],
        'email': c[6],
        'organismo_jurisdiccion': c[7] if len(c) > 7 else ''
    } for c in clientes]
    return jsonify(result)

@app.route('/api/clientes', methods=['POST'])
def crear_cliente():
    data = request.json
    
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    
    if not data.get('organismo_jurisdiccion'):
        return jsonify({'success': False, 'error': 'Organismo/Jurisdicción es obligatorio'}), 400
    
    try:
        cliente_id = db.crear_cliente(
            data['nombre'],
            data.get('razon_social', ''),
            data.get('cuit', ''),
            data.get('direccion', ''),
            data.get('telefono', ''),
            data.get('email', ''),
            data.get('organismo_jurisdiccion', '')
        )
        return jsonify({'success': True, 'id': cliente_id}), 201
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
            data.get('email', ''),
            data.get('organismo_jurisdiccion', '')
        )
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    try:
        db.eliminar_cliente(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Oferentes
@app.route('/api/oferentes', methods=['GET'])
def get_oferentes():
    oferentes = db.obtener_oferentes()
    return jsonify([{'id': o[0], 'nombre': o[1]} for o in oferentes])

@app.route('/api/oferentes', methods=['POST'])
def crear_oferente():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        oferente_id = db.crear_oferente(data['nombre'])
        return jsonify({'success': True, 'id': oferente_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/oferentes/<int:id>', methods=['PUT'])
def actualizar_oferente(id):
    data = request.json
    try:
        db.actualizar_oferente(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/oferentes/<int:id>', methods=['DELETE'])
def eliminar_oferente(id):
    try:
        db.eliminar_oferente(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Marcas
@app.route('/api/marcas', methods=['GET'])
def get_marcas():
    marcas = db.obtener_marcas()
    return jsonify([{'id': m[0], 'nombre': m[1]} for m in marcas])

@app.route('/api/marcas', methods=['POST'])
def crear_marca():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        marca_id = db.crear_marca(data['nombre'])
        return jsonify({'success': True, 'id': marca_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/marcas/<int:id>', methods=['PUT'])
def actualizar_marca(id):
    data = request.json
    try:
        db.actualizar_marca(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/marcas/<int:id>', methods=['DELETE'])
def eliminar_marca(id):
    try:
        db.eliminar_marca(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Tipos de Licitación
@app.route('/api/tipos-licitacion', methods=['GET'])
def get_tipos_licitacion():
    tipos = db.obtener_tipos_licitacion()
    return jsonify([{'id': t[0], 'nombre': t[1]} for t in tipos])

@app.route('/api/tipos-licitacion', methods=['POST'])
def crear_tipo_licitacion():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        tipo_id = db.crear_tipo_licitacion(data['nombre'])
        return jsonify({'success': True, 'id': tipo_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/tipos-licitacion/<int:id>', methods=['PUT'])
def actualizar_tipo_licitacion(id):
    data = request.json
    try:
        db.actualizar_tipo_licitacion(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tipos-licitacion/<int:id>', methods=['DELETE'])
def eliminar_tipo_licitacion(id):
    try:
        db.eliminar_tipo_licitacion(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@app.route('/api/cargar-clientes', methods=['POST'])
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

@app.route('/api/cargar-oferentes', methods=['POST'])
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

@app.route('/api/cargar-marcas', methods=['POST'])
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

@app.route('/api/cargar-tipos-licitacion', methods=['POST'])
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

# API Portales Origen
@app.route('/api/portales-origen', methods=['GET'])
def get_portales_origen():
    portales = db.obtener_portales_origen()
    return jsonify([{'id': p[0], 'nombre': p[1]} for p in portales])

@app.route('/api/portales-origen', methods=['POST'])
def crear_portal_origen():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        portal_id = db.crear_portal_origen(data['nombre'])
        return jsonify({'success': True, 'id': portal_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/portales-origen/<int:id>', methods=['PUT'])
def actualizar_portal_origen(id):
    data = request.json
    try:
        db.actualizar_portal_origen(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/portales-origen/<int:id>', methods=['DELETE'])
def eliminar_portal_origen(id):
    try:
        db.eliminar_portal_origen(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Modalidades Entrega
@app.route('/api/modalidades-entrega', methods=['GET'])
def get_modalidades_entrega():
    modalidades = db.obtener_modalidades_entrega()
    return jsonify([{'id': m[0], 'nombre': m[1]} for m in modalidades])

@app.route('/api/modalidades-entrega', methods=['POST'])
def crear_modalidad_entrega():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        modalidad_id = db.crear_modalidad_entrega(data['nombre'])
        return jsonify({'success': True, 'id': modalidad_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/modalidades-entrega/<int:id>', methods=['PUT'])
def actualizar_modalidad_entrega(id):
    data = request.json
    try:
        db.actualizar_modalidad_entrega(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modalidades-entrega/<int:id>', methods=['DELETE'])
def eliminar_modalidad_entrega(id):
    try:
        db.eliminar_modalidad_entrega(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Formas Pago
@app.route('/api/formas-pago', methods=['GET'])
def get_formas_pago():
    formas = db.obtener_formas_pago()
    return jsonify([{'id': f[0], 'nombre': f[1]} for f in formas])

@app.route('/api/formas-pago', methods=['POST'])
def crear_forma_pago():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        forma_id = db.crear_forma_pago(data['nombre'])
        return jsonify({'success': True, 'id': forma_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/formas-pago/<int:id>', methods=['PUT'])
def actualizar_forma_pago(id):
    data = request.json
    try:
        db.actualizar_forma_pago(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/formas-pago/<int:id>', methods=['DELETE'])
def eliminar_forma_pago(id):
    try:
        db.eliminar_forma_pago(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Organismos Jurisdiccion
@app.route('/api/organismos', methods=['GET'])
def get_organismos():
    organismos = db.obtener_organismos()
    return jsonify([{'id': o[0], 'nombre': o[1]} for o in organismos])

@app.route('/api/organismos', methods=['POST'])
def crear_organismo():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        organismo_id = db.crear_organismo(data['nombre'])
        return jsonify({'success': True, 'id': organismo_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/organismos/<int:id>', methods=['PUT'])
def actualizar_organismo(id):
    data = request.json
    try:
        db.actualizar_organismo(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/organismos/<int:id>', methods=['DELETE'])
def eliminar_organismo(id):
    try:
        db.eliminar_organismo(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Motivos Perdida
@app.route('/api/motivos-perdida', methods=['GET'])
def get_motivos_perdida():
    motivos = db.obtener_motivos_perdida()
    return jsonify([{'id': m[0], 'nombre': m[1]} for m in motivos])

@app.route('/api/motivos-perdida', methods=['POST'])
def crear_motivo_perdida():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        motivo_id = db.crear_motivo_perdida(data['nombre'])
        return jsonify({'success': True, 'id': motivo_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/motivos-perdida/<int:id>', methods=['PUT'])
def actualizar_motivo_perdida(id):
    data = request.json
    try:
        db.actualizar_motivo_perdida(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/motivos-perdida/<int:id>', methods=['DELETE'])
def eliminar_motivo_perdida(id):
    try:
        db.eliminar_motivo_perdida(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ranking-perdidas', methods=['GET'])
def get_ranking_perdidas():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT motivo_perdida, COUNT(*) as cantidad
            FROM productos
            WHERE motivo_perdida IS NOT NULL AND motivo_perdida != ''
            GROUP BY motivo_perdida
            ORDER BY cantidad DESC
        """)
        resultados = cursor.fetchall()
    return jsonify([{'motivo': r[0], 'cantidad': r[1]} for r in resultados])

@app.route('/api/diferencias-promedio', methods=['GET'])
def get_diferencias_promedio():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT AVG(precio_ofertado - precio_ganador) as dif_pesos,
                   AVG(((precio_ofertado - precio_ganador) / precio_ganador) * 100) as dif_porcentaje
            FROM productos
            WHERE resultado = 'No Adjudicado' 
              AND precio_ganador IS NOT NULL 
              AND precio_ganador > 0
        """)
        resultado = cursor.fetchone()
    return jsonify({
        'diferencia_pesos': float(resultado[0]) if resultado[0] else 0,
        'diferencia_porcentaje': float(resultado[1]) if resultado[1] else 0
    })

@app.route('/api/licitaciones/verificar', methods=['GET'])
def verificar_licitacion():
    numero = request.args.get('numero')
    cliente_id = request.args.get('cliente_id')
    
    if not numero or not cliente_id:
        return jsonify({'existe': False})
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT COUNT(*) FROM licitaciones WHERE numero_licitacion = %s AND cliente_id = %s", (numero, int(cliente_id)))
            else:
                cursor.execute("SELECT COUNT(*) FROM licitaciones WHERE numero_licitacion = ? AND cliente_id = ?", (numero, int(cliente_id)))
            count = cursor.fetchone()[0]
            return jsonify({'existe': count > 0})
    except Exception as e:
        return jsonify({'existe': False, 'error': str(e)})

# API Mantenimientos Oferta
@app.route('/api/mantenimientos-oferta', methods=['GET'])
def get_mantenimientos_oferta():
    mantenimientos = db.obtener_mantenimientos_oferta()
    return jsonify([{'id': m[0], 'nombre': m[1]} for m in mantenimientos])

@app.route('/api/mantenimientos-oferta', methods=['POST'])
def crear_mantenimiento_oferta():
    data = request.json
    if not data or not data.get('nombre'):
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    try:
        mantenimiento_id = db.crear_mantenimiento_oferta(data['nombre'])
        return jsonify({'success': True, 'id': mantenimiento_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/mantenimientos-oferta/<int:id>', methods=['PUT'])
def actualizar_mantenimiento_oferta(id):
    data = request.json
    try:
        db.actualizar_mantenimiento_oferta(id, data['nombre'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mantenimientos-oferta/<int:id>', methods=['DELETE'])
def eliminar_mantenimiento_oferta(id):
    try:
        db.eliminar_mantenimiento_oferta(id)
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Presupuestos
@app.route('/api/presupuestos/siguiente-numero', methods=['GET'])
def get_siguiente_numero_presupuesto():
    try:
        numero = db.obtener_siguiente_numero_presupuesto()
        return jsonify({'numero': numero})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/presupuestos', methods=['GET'])
def get_presupuestos():
    try:
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        presupuestos = db.obtener_presupuestos(limit, offset)
        return jsonify([{
            'numero': p[0],
            'fecha': p[1],
            'licitacion': p[2],
            'cliente': p[3]
        } for p in presupuestos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/presupuestos/<int:numero>', methods=['GET'])
def get_presupuesto(numero):
    try:
        presupuesto = db.obtener_presupuesto_por_numero(numero)
        if presupuesto:
            return jsonify({'success': True, 'data': presupuesto})
        return jsonify({'success': False, 'error': 'Presupuesto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/presupuesto/<int:numero>')
def ver_presupuesto(numero):
    return render_template('presupuesto.html', numero=numero)

@app.route('/api/presupuestos/crear', methods=['POST'])
def crear_presupuesto():
    data = request.json
    if not data or not data.get('licitacion_id'):
        return jsonify({'success': False, 'error': 'licitacion_id es obligatorio'}), 400
    
    try:
        numero = db.crear_presupuesto(data['licitacion_id'])
        return jsonify({'success': True, 'numero': numero})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/licitaciones/<int:id>/detalle', methods=['GET'])
def get_licitacion_detalle(id):
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT l.id, l.numero_licitacion, l.fecha, l.cliente_id, l.tipo_licitacion_id,
                           l.portal_origen, l.modalidad_entrega, l.forma_pago, l.requiere_poliza,
                           l.monto_poliza, l.observaciones, l.mantenimiento_oferta, l.tipo_adjudicacion
                    FROM licitaciones l
                    WHERE l.id = %s
                """, (id,))
            else:
                cursor.execute("""
                    SELECT l.id, l.numero_licitacion, l.fecha, l.cliente_id, l.tipo_licitacion_id,
                           l.portal_origen, l.modalidad_entrega, l.forma_pago, l.requiere_poliza,
                           l.monto_poliza, l.observaciones, l.mantenimiento_oferta, l.tipo_adjudicacion
                    FROM licitaciones l
                    WHERE l.id = ?
                """, (id,))
            
            row = cursor.fetchone()
            if not row:
                return jsonify({'success': False, 'error': 'Licitación no encontrada'}), 404
            
            # Calcular porcentaje de póliza si existe
            porcentaje_poliza = None
            if row[8] and row[9]:  # requiere_poliza y monto_poliza
                # Obtener total cotizado
                if USE_POSTGRES:
                    cursor.execute("SELECT COALESCE(SUM(precio_ofertado * cantidad), 0) FROM productos WHERE licitacion_id = %s", (id,))
                else:
                    cursor.execute("SELECT COALESCE(SUM(precio_ofertado * cantidad), 0) FROM productos WHERE licitacion_id = ?", (id,))
                total = cursor.fetchone()[0]
                if total > 0:
                    porcentaje_poliza = (float(row[9]) / float(total)) * 100
            
            return jsonify({
                'id': row[0],
                'numero': row[1],
                'fecha': row[2],
                'cliente_id': row[3],
                'tipo_licitacion_id': row[4],
                'portal_origen': row[5],
                'modalidad_entrega': row[6],
                'forma_pago': row[7],
                'requiere_poliza': row[8],
                'monto_poliza': row[9],
                'porcentaje_poliza': porcentaje_poliza,
                'observaciones': row[10],
                'mantenimiento_oferta': row[11],
                'tipo_adjudicacion': row[12] if len(row) > 12 and row[12] else 'Parcial'
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/editar-licitacion/<int:id>')
def editar_licitacion(id):
    return render_template('editar_licitacion.html')

@app.route('/api/alternativas/<int:producto_id>', methods=['GET'])
def get_alternativas(producto_id):
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT id, producto_id, marca, presentacion, laboratorio, costo_unitario, 
                           margen_porcentaje, precio_ofertado, observaciones
                    FROM alternativas_productos WHERE producto_id = %s
                """, (producto_id,))
            else:
                cursor.execute("""
                    SELECT id, producto_id, marca, presentacion, laboratorio, costo_unitario, 
                           margen_porcentaje, precio_ofertado, observaciones
                    FROM alternativas_productos WHERE producto_id = ?
                """, (producto_id,))
            alternativas = cursor.fetchall()
            return jsonify([{
                'id': a[0],
                'producto_id': a[1],
                'marca': a[2],
                'presentacion': a[3],
                'laboratorio': a[4],
                'costo_unitario': a[5],
                'margen_porcentaje': a[6],
                'precio_ofertado': a[7],
                'observaciones': a[8]
            } for a in alternativas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/alternativas', methods=['POST'])
def crear_alternativa():
    data = request.json
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    INSERT INTO alternativas_productos 
                    (producto_id, marca, presentacion, laboratorio, costo_unitario, margen_porcentaje, precio_ofertado, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                """, (
                    data['producto_id'],
                    data.get('marca', ''),
                    data.get('presentacion', ''),
                    data.get('laboratorio', ''),
                    float(data['costo_unitario']) if data.get('costo_unitario') else None,
                    float(data['margen_porcentaje']) if data.get('margen_porcentaje') else None,
                    float(data['precio_ofertado']) if data.get('precio_ofertado') else None,
                    data.get('observaciones', '')
                ))
                alt_id = cursor.fetchone()[0]
            else:
                cursor.execute("""
                    INSERT INTO alternativas_productos 
                    (producto_id, marca, presentacion, laboratorio, costo_unitario, margen_porcentaje, precio_ofertado, observaciones)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data['producto_id'],
                    data.get('marca', ''),
                    data.get('presentacion', ''),
                    data.get('laboratorio', ''),
                    float(data['costo_unitario']) if data.get('costo_unitario') else None,
                    float(data['margen_porcentaje']) if data.get('margen_porcentaje') else None,
                    float(data['precio_ofertado']) if data.get('precio_ofertado') else None,
                    data.get('observaciones', '')
                ))
                alt_id = cursor.lastrowid
            return jsonify({'success': True, 'id': alt_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/alternativas/<int:producto_id>', methods=['DELETE'])
def eliminar_alternativas_producto(producto_id):
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("DELETE FROM alternativas_productos WHERE producto_id = %s", (producto_id,))
            else:
                cursor.execute("DELETE FROM alternativas_productos WHERE producto_id = ?", (producto_id,))
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/licitaciones-resumen', methods=['GET'])
def get_licitaciones_resumen():
    try:
        licitaciones = db.obtener_licitaciones_resumen()
        return jsonify([{
            'id': l[0],
            'numero': l[1],
            'cliente': l[2] or '-',
            'total_productos': l[3] or 0,
            'productos_ganados': l[4] or 0,
            'monto_cotizado': float(l[5]) if l[5] else 0.0,
            'monto_adjudicado': float(l[6]) if l[6] else 0.0
        } for l in licitaciones])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Ofertas Productos
@app.route('/api/ofertas/<int:producto_id>', methods=['GET'])
def get_ofertas_producto(producto_id):
    try:
        ofertas = db.obtener_ofertas_producto(producto_id)
        return jsonify([{
            'id': o[0],
            'producto_id': o[1],
            'oferente': o[2],
            'laboratorio': o[3],
            'precio': o[4]
        } for o in ofertas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ofertas/<int:producto_id>', methods=['POST'])
def guardar_ofertas_producto(producto_id):
    data = request.json
    try:
        ofertas = data.get('ofertas', [])
        db.guardar_ofertas_producto(producto_id, ofertas)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/licitaciones/<int:id>/exportar-excel', methods=['GET'])
def exportar_licitacion_excel(id):
    try:
        import pandas as pd
        from io import BytesIO
        from flask import send_file
        
        # Obtener licitación
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT numero_licitacion FROM licitaciones WHERE id = %s", (id,))
            else:
                cursor.execute("SELECT numero_licitacion FROM licitaciones WHERE id = ?", (id,))
            licitacion = cursor.fetchone()
            if not licitacion:
                return jsonify({'error': 'Licitación no encontrada'}), 404
        
        # Obtener productos con JOIN a celty para obtener laboratorio
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT p.id, p.monodroga, p.marca, p.presentacion, p.cantidad, p.precio_ofertado,
                           p.resultado, p.precio_ganador, p.oferente_ganador, c.laboratorio
                    FROM productos p
                    LEFT JOIN celty c ON LOWER(TRIM(p.monodroga)) = LOWER(TRIM(c.monodroga))
                                      AND LOWER(TRIM(p.marca)) = LOWER(TRIM(c.marca))
                                      AND LOWER(TRIM(p.presentacion)) = LOWER(TRIM(c.presentacion))
                    WHERE p.licitacion_id = %s
                """, (id,))
            else:
                cursor.execute("""
                    SELECT p.id, p.monodroga, p.marca, p.presentacion, p.cantidad, p.precio_ofertado,
                           p.resultado, p.precio_ganador, p.oferente_ganador, c.laboratorio
                    FROM productos p
                    LEFT JOIN celty c ON LOWER(TRIM(p.monodroga)) = LOWER(TRIM(c.monodroga))
                                      AND LOWER(TRIM(p.marca)) = LOWER(TRIM(c.marca))
                                      AND LOWER(TRIM(p.presentacion)) = LOWER(TRIM(c.presentacion))
                    WHERE p.licitacion_id = ?
                """, (id,))
            productos = cursor.fetchall()
        
        # Construir datos
        data = []
        for p in productos:
            row = {
                'Monodroga': p[1],
                'Laboratorio': p[9] or '',
                'Marca - Presentacion': f"{p[2]} - {p[3]}",
                'Cantidad': p[4],
                'Precio': p[5]
            }
            
            # Obtener ofertas
            ofertas = db.obtener_ofertas_producto(p[0])
            
            # Agregar ofertas dinámicamente
            for idx, oferta in enumerate(ofertas, 1):
                row[f'Oferente{idx}'] = oferta[2]
                row[f'Precio{idx}'] = oferta[4]
                row[f'Laboratorio {idx}'] = oferta[3]
            
            # Ganador
            if p[6] == 'Adjudicado':
                row['Ganador'] = 'Celtyc'
                row['Precio Ganador'] = p[5]
            elif p[6] == 'No Adjudicado' and p[8]:
                row['Ganador'] = p[8]
                row['Precio Ganador'] = p[7]
            else:
                row['Ganador'] = '-'
                row['Precio Ganador'] = '-'
            
            data.append(row)
        
        # Crear Excel
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Licitación')
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'licitacion_{licitacion[0]}.xlsx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Forzar SQLite en desarrollo
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
