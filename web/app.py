from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from database.db_manager import DatabaseManager, USE_POSTGRES
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

# Ejecutar migraciones v1.1.0 automáticamente
if USE_POSTGRES:
    print("🚀 Iniciando migraciones v1.1.0...")
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. costo_unitario en celty
            try:
                cursor.execute("ALTER TABLE celty ADD COLUMN costo_unitario REAL")
                conn.commit()
                print("✓ costo_unitario agregado")
            except:
                pass
            
            # 2. portales_origen
            try:
                cursor.execute("CREATE TABLE portales_origen (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Comprar', 'BAC', 'Otro']:
                    cursor.execute("INSERT INTO portales_origen (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ portales_origen creada")
            except:
                pass
            
            # 3. modalidades_entrega
            try:
                cursor.execute("CREATE TABLE modalidades_entrega (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Única', 'Múltiple', 'Programada']:
                    cursor.execute("INSERT INTO modalidades_entrega (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ modalidades_entrega creada")
            except:
                pass
            
            # 4. formas_pago
            try:
                cursor.execute("CREATE TABLE formas_pago (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Contado', '30 días', '60 días']:
                    cursor.execute("INSERT INTO formas_pago (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ formas_pago creada")
            except:
                pass
            
            # 5. organismos_jurisdiccion
            try:
                cursor.execute("CREATE TABLE organismos_jurisdiccion (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Nacional', 'Provincial', 'Municipal', 'CABA', 'Privado']:
                    cursor.execute("INSERT INTO organismos_jurisdiccion (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ organismos_jurisdiccion creada")
            except:
                pass
            
            # 6. motivos_perdida
            try:
                cursor.execute("CREATE TABLE motivos_perdida (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Precio más alto', 'Marca no priorizada', 'No cumplía especificación', 'Error administrativo', 'Otro']:
                    cursor.execute("INSERT INTO motivos_perdida (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ motivos_perdida creada")
            except:
                pass
            
            # 7. Columnas en licitaciones
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
            
            # 8. organismo_jurisdiccion en clientes
            try:
                cursor.execute("ALTER TABLE clientes ADD COLUMN organismo_jurisdiccion TEXT")
                conn.commit()
            except:
                pass
            
            # 9. motivo_perdida en productos
            try:
                cursor.execute("ALTER TABLE productos ADD COLUMN motivo_perdida TEXT")
                conn.commit()
            except:
                pass
            
            print("✅ Migraciones v1.1.0 completadas")
    except Exception as e:
        print(f"❌ Error en migraciones: {e}")
        import traceback
        traceback.print_exc()

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
        return jsonify({'success': True})
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
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/licitaciones', methods=['GET'])
def get_licitaciones():
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.id, l.numero_licitacion, l.fecha, l.oferente_ganador, l.marca_ganadora, l.precio_ganador,
                   c.nombre as cliente, t.nombre as tipo_licitacion
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
            data.get('observaciones', '')
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
                float(producto['precio_ganador']) if producto.get('precio_ganador') else None,
                producto.get('oferente_ganador', ''),
                producto.get('marca_ofrecida', ''),
                producto.get('marca_ganadora', ''),
                producto.get('motivo_perdida', '')
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

@app.route('/api/licitaciones/<int:id>', methods=['PUT'])
def actualizar_licitacion(id):
    data = request.json
    try:
        db.actualizar_licitacion(
            id,
            data['numero'],
            data['fecha'],
            '',
            '',
            None,
            int(data['cliente_id']) if data.get('cliente_id') else None
        )
        
        # Actualizar tipo_licitacion_id si se proporciona
        if 'tipo_licitacion_id' in data:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                tipo_id = int(data['tipo_licitacion_id']) if data['tipo_licitacion_id'] else None
                if db.USE_POSTGRES:
                    cursor.execute("UPDATE licitaciones SET tipo_licitacion_id = %s WHERE id = %s", (tipo_id, id))
                else:
                    cursor.execute("UPDATE licitaciones SET tipo_licitacion_id = ? WHERE id = ?", (tipo_id, id))
        
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
        'marca_ofrecida': p[10],
        'marca_ganadora': p[11] if len(p) > 11 else '',
        'motivo_perdida': p[12] if len(p) > 12 else ''
    } for p in productos])

@app.route('/api/productos', methods=['POST'])
def crear_producto():
    data = request.json
    try:
        db.agregar_producto(
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
            data.get('motivo_perdida', '')
        )
        return jsonify({'success': True})
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
            data.get('motivo_perdida', '')
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
    return jsonify([{
        'id': c[0],
        'nombre': c[1],
        'razon_social': c[2],
        'cuit': c[3],
        'direccion': c[4],
        'telefono': c[5],
        'email': c[6],
        'organismo_jurisdiccion': c[8] if len(c) > 8 else ''
    } for c in clientes])

@app.route('/api/clientes', methods=['POST'])
def crear_cliente():
    data = request.json
    print(f"DEBUG - Datos recibidos: {data}")
    
    if not data or not data.get('nombre'):
        print("DEBUG - Error: Nombre no proporcionado")
        return jsonify({'success': False, 'error': 'Nombre es obligatorio'}), 400
    
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
        print(f"DEBUG - Cliente creado con ID: {cliente_id}")
        return jsonify({'success': True, 'id': cliente_id})
    except ValueError as e:
        print(f"DEBUG - ValueError: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        print(f"DEBUG - Exception: {e}")
        import traceback
        traceback.print_exc()
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
        return jsonify({'success': True, 'id': oferente_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/oferentes/<int:id>', methods=['PUT'])
def actualizar_oferente(id):
    data = request.json
    try:
        db.actualizar_oferente(id, data['nombre'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/oferentes/<int:id>', methods=['DELETE'])
def eliminar_oferente(id):
    try:
        db.eliminar_oferente(id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

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
        return jsonify({'success': True, 'id': marca_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/marcas/<int:id>', methods=['PUT'])
def actualizar_marca(id):
    data = request.json
    try:
        db.actualizar_marca(id, data['nombre'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/marcas/<int:id>', methods=['DELETE'])
def eliminar_marca(id):
    try:
        db.eliminar_marca(id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

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
        return jsonify({'success': True, 'id': tipo_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/tipos-licitacion/<int:id>', methods=['PUT'])
def actualizar_tipo_licitacion(id):
    data = request.json
    try:
        db.actualizar_tipo_licitacion(id, data['nombre'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/tipos-licitacion/<int:id>', methods=['DELETE'])
def eliminar_tipo_licitacion(id):
    try:
        db.eliminar_tipo_licitacion(id)
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
        return jsonify({'success': True, 'id': portal_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/portales-origen/<int:id>', methods=['PUT'])
def actualizar_portal_origen(id):
    data = request.json
    try:
        db.actualizar_portal_origen(id, data['nombre'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/portales-origen/<int:id>', methods=['DELETE'])
def eliminar_portal_origen(id):
    try:
        db.eliminar_portal_origen(id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

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
        return jsonify({'success': True, 'id': modalidad_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/modalidades-entrega/<int:id>', methods=['PUT'])
def actualizar_modalidad_entrega(id):
    data = request.json
    try:
        db.actualizar_modalidad_entrega(id, data['nombre'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/modalidades-entrega/<int:id>', methods=['DELETE'])
def eliminar_modalidad_entrega(id):
    try:
        db.eliminar_modalidad_entrega(id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

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
        return jsonify({'success': True, 'id': forma_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/formas-pago/<int:id>', methods=['PUT'])
def actualizar_forma_pago(id):
    data = request.json
    try:
        db.actualizar_forma_pago(id, data['nombre'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/formas-pago/<int:id>', methods=['DELETE'])
def eliminar_forma_pago(id):
    try:
        db.eliminar_forma_pago(id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

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
        return jsonify({'success': True, 'id': organismo_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/organismos/<int:id>', methods=['PUT'])
def actualizar_organismo(id):
    data = request.json
    try:
        db.actualizar_organismo(id, data['nombre'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/organismos/<int:id>', methods=['DELETE'])
def eliminar_organismo(id):
    try:
        db.eliminar_organismo(id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

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
        return jsonify({'success': True, 'id': motivo_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/motivos-perdida/<int:id>', methods=['PUT'])
def actualizar_motivo_perdida(id):
    data = request.json
    try:
        db.actualizar_motivo_perdida(id, data['nombre'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/motivos-perdida/<int:id>', methods=['DELETE'])
def eliminar_motivo_perdida(id):
    try:
        db.eliminar_motivo_perdida(id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

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

if __name__ == '__main__':
    # Forzar SQLite en desarrollo
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
