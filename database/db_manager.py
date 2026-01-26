import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager
import pandas as pd

# Detectar si estamos en producción (Render)
DATABASE_URL = os.environ.get('DATABASE_URL')

# Render usa postgres:// pero psycopg2 necesita postgresql://
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

if DATABASE_URL:
    # Usar PostgreSQL en producción
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        USE_POSTGRES = True
        print(f"✓ Conectado a PostgreSQL")
    except ImportError as e:
        print(f"✗ Error importando psycopg2: {e}")
        print("Usando SQLite como fallback")
        USE_POSTGRES = False
else:
    # Usar SQLite en local
    USE_POSTGRES = False
    print("Usando SQLite (desarrollo local)")

class DatabaseManager:
    def __init__(self, db_path="database/licitaciones.db"):
        self.db_path = db_path
        if not USE_POSTGRES:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()
        # Cargar catálogo desde Excel si existe y no es producción
        if not USE_POSTGRES and os.path.exists('Data/Celty.xlsx'):
            self.cargar_catalogo_desde_excel()
    
    @contextmanager
    def get_connection(self):
        if USE_POSTGRES:
            conn = psycopg2.connect(DATABASE_URL)
        else:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON")
        
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if USE_POSTGRES:
                # Tabla Clientes
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS clientes (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        razon_social TEXT,
                        cuit TEXT,
                        direccion TEXT,
                        telefono TEXT,
                        email TEXT,
                        activo BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                # Tabla Oferentes
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS oferentes (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                # Tabla Marcas
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS marcas (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                # Tabla Tipos de Licitación
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tipos_licitacion (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS licitaciones (
                        id SERIAL PRIMARY KEY,
                        numero_licitacion TEXT UNIQUE NOT NULL,
                        cliente_id INTEGER,
                        tipo_licitacion_id INTEGER,
                        fecha TEXT NOT NULL,
                        oferente_ganador TEXT,
                        marca_ganadora TEXT,
                        precio_ganador REAL,
                        CHECK(length(numero_licitacion) > 0),
                        FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                        FOREIGN KEY (tipo_licitacion_id) REFERENCES tipos_licitacion (id)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS productos (
                        id SERIAL PRIMARY KEY,
                        licitacion_id INTEGER NOT NULL,
                        monodroga TEXT NOT NULL,
                        marca TEXT NOT NULL,
                        presentacion TEXT NOT NULL,
                        cantidad INTEGER NOT NULL CHECK(cantidad > 0),
                        precio_ofertado REAL NOT NULL CHECK(precio_ofertado >= 0),
                        resultado TEXT NOT NULL CHECK(resultado IN ('Adjudicado', 'Parcial', 'No Adjudicado')),
                        precio_ganador REAL CHECK(precio_ganador >= 0),
                        oferente_ganador TEXT,
                        marca_ofrecida TEXT,
                        marca_ganadora TEXT,
                        FOREIGN KEY (licitacion_id) REFERENCES licitaciones (id) ON DELETE CASCADE
                    )
                ''')
                
                # Migración: Agregar marca_ganadora si no existe
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='productos' AND column_name='marca_ganadora'
                """)
                if cursor.fetchone() is None:
                    cursor.execute("ALTER TABLE productos ADD COLUMN marca_ganadora TEXT")
                    print("✓ Columna marca_ganadora agregada")
                
                # Tabla Celty con todas las columnas del Excel
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS celty (
                        id SERIAL PRIMARY KEY,
                        numero_registro TEXT UNIQUE NOT NULL,
                        monodroga TEXT,
                        marca TEXT,
                        presentacion TEXT,
                        laboratorio TEXT,
                        precio_caja REAL,
                        precio_unitario REAL,
                        fecha TEXT
                    )
                ''')
            else:
                # Tabla Clientes
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        razon_social TEXT,
                        cuit TEXT,
                        direccion TEXT,
                        telefono TEXT,
                        email TEXT,
                        activo INTEGER DEFAULT 1
                    )
                ''')
                
                # Tabla Oferentes
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS oferentes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                ''')
                
                # Tabla Marcas
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS marcas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                ''')
                
                # Tabla Tipos de Licitación
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tipos_licitacion (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS licitaciones (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        numero_licitacion TEXT UNIQUE NOT NULL,
                        cliente_id INTEGER,
                        tipo_licitacion_id INTEGER,
                        fecha TEXT NOT NULL,
                        oferente_ganador TEXT,
                        marca_ganadora TEXT,
                        precio_ganador REAL,
                        CHECK(length(numero_licitacion) > 0),
                        FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                        FOREIGN KEY (tipo_licitacion_id) REFERENCES tipos_licitacion (id)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        licitacion_id INTEGER NOT NULL,
                        monodroga TEXT NOT NULL,
                        marca TEXT NOT NULL,
                        presentacion TEXT NOT NULL,
                        cantidad INTEGER NOT NULL CHECK(cantidad > 0),
                        precio_ofertado REAL NOT NULL CHECK(precio_ofertado >= 0),
                        resultado TEXT NOT NULL CHECK(resultado IN ('Adjudicado', 'Parcial', 'No Adjudicado')),
                        precio_ganador REAL CHECK(precio_ganador >= 0),
                        oferente_ganador TEXT,
                        marca_ofrecida TEXT,
                        marca_ganadora TEXT,
                        FOREIGN KEY (licitacion_id) REFERENCES licitaciones (id) ON DELETE CASCADE
                    )
                ''')
                
                # Migración: Agregar marca_ganadora si no existe
                cursor.execute("PRAGMA table_info(productos)")
                columns = [col[1] for col in cursor.fetchall()]
                if 'marca_ganadora' not in columns:
                    cursor.execute("ALTER TABLE productos ADD COLUMN marca_ganadora TEXT")
                    print("✓ Columna marca_ganadora agregada")
                
                # Tabla Celty con todas las columnas del Excel
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS celty (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        numero_registro TEXT UNIQUE NOT NULL,
                        monodroga TEXT,
                        marca TEXT,
                        presentacion TEXT,
                        laboratorio TEXT,
                        precio_caja REAL,
                        precio_unitario REAL,
                        fecha TEXT
                    )
                ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_licitacion_numero ON licitaciones(numero_licitacion)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_licitacion_cliente ON licitaciones(cliente_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_producto_licitacion ON productos(licitacion_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_producto_resultado ON productos(resultado)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_celty_numero_registro ON celty(numero_registro)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_celty_monodroga ON celty(monodroga)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_oferentes_nombre ON oferentes(nombre)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_marcas_nombre ON marcas(nombre)')
    
    def cargar_catalogo_desde_excel(self, excel_path='Data/Celty.xlsx'):
        """Carga productos desde Excel a tabla celty"""
        try:
            df = pd.read_excel(excel_path)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                for _, row in df.iterrows():
                    try:
                        numero_registro = str(row.get('Numero de Registro', ''))
                        monodroga = str(row.get('Monodroga', ''))
                        marca = str(row.get('Marca', ''))
                        presentacion = str(row.get('Presentacion', ''))
                        laboratorio = str(row.get('Laboratorio', ''))
                        precio_caja = float(row.get('Precio por Caja', 0)) if pd.notna(row.get('Precio por Caja', 0)) else 0
                        precio_unitario = float(row.get('Presio unitario', 0)) if pd.notna(row.get('Presio unitario', 0)) else 0
                        
                        # Formatear fecha a dd/mm/aaaa
                        fecha_raw = row.get('Fecha')
                        if pd.notna(fecha_raw):
                            if isinstance(fecha_raw, str):
                                fecha = fecha_raw.split()[0] if ' ' in fecha_raw else fecha_raw
                            else:
                                fecha = fecha_raw.strftime('%d/%m/%Y')
                        else:
                            fecha = ''
                        
                        if not numero_registro or numero_registro == 'nan':
                            continue
                        
                        if USE_POSTGRES:
                            cursor.execute("""
                                INSERT INTO celty (numero_registro, monodroga, marca, presentacion, laboratorio, 
                                                  precio_caja, precio_unitario, fecha) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (numero_registro) DO UPDATE SET
                                    monodroga = EXCLUDED.monodroga,
                                    marca = EXCLUDED.marca,
                                    presentacion = EXCLUDED.presentacion,
                                    laboratorio = EXCLUDED.laboratorio,
                                    precio_caja = EXCLUDED.precio_caja,
                                    precio_unitario = EXCLUDED.precio_unitario,
                                    fecha = EXCLUDED.fecha
                            """, (numero_registro, monodroga, marca, presentacion, laboratorio, precio_caja, precio_unitario, fecha))
                        else:
                            cursor.execute("""
                                INSERT OR REPLACE INTO celty (numero_registro, monodroga, marca, presentacion, laboratorio, 
                                                            precio_caja, precio_unitario, fecha) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, (numero_registro, monodroga, marca, presentacion, laboratorio, precio_caja, precio_unitario, fecha))
                    except Exception as e:
                        print(f"Error en fila: {e}")
                        continue
            return True
        except Exception as e:
            print(f"Error cargando catálogo: {e}")
            return False
    
    def obtener_catalogo_productos(self):
        """Obtiene lista de productos del catálogo Celty"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT numero_registro, monodroga, marca, presentacion FROM celty ORDER BY monodroga, marca, presentacion")
            return cursor.fetchall()
    
    def obtener_producto_por_registro(self, numero_registro):
        """Obtiene producto completo por número de registro"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM celty WHERE numero_registro = %s", (numero_registro,))
            else:
                cursor.execute("SELECT * FROM celty WHERE numero_registro = ?", (numero_registro,))
            return cursor.fetchone()
    
    def crear_licitacion(self, numero, fecha, oferente_ganador="", marca_ganadora="", precio_ganador=None, cliente_id=None, tipo_licitacion_id=None):
        if not numero or not fecha:
            raise ValueError("Número y fecha son obligatorios")
        if len(numero.strip()) > 100:
            raise ValueError("Número de licitación demasiado largo")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("INSERT INTO licitaciones (numero_licitacion, cliente_id, tipo_licitacion_id, fecha, oferente_ganador, marca_ganadora, precio_ganador) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                              (numero.strip(), cliente_id, tipo_licitacion_id, fecha.strip(), oferente_ganador.strip(), marca_ganadora.strip(), precio_ganador))
                return cursor.fetchone()[0]
            else:
                cursor.execute("INSERT INTO licitaciones (numero_licitacion, cliente_id, tipo_licitacion_id, fecha, oferente_ganador, marca_ganadora, precio_ganador) VALUES (?, ?, ?, ?, ?, ?, ?)",
                              (numero.strip(), cliente_id, tipo_licitacion_id, fecha.strip(), oferente_ganador.strip(), marca_ganadora.strip(), precio_ganador))
                return cursor.lastrowid
    
    def agregar_producto(self, licitacion_id, monodroga, marca, presentacion, cantidad, precio_ofertado, resultado, precio_ganador=None, oferente_ganador="", marca_ofrecida="", marca_ganadora=""):
        if not monodroga or not marca or not presentacion or cantidad <= 0 or precio_ofertado < 0:
            raise ValueError("Datos de producto inválidos")
        if resultado == "Adjudicado":
            precio_ganador = precio_ofertado
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""INSERT INTO productos (licitacion_id, monodroga, marca, presentacion, cantidad, precio_ofertado, 
                                 resultado, precio_ganador, oferente_ganador, marca_ofrecida, marca_ganadora) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                              (licitacion_id, monodroga.strip(), marca.strip(), presentacion.strip(), cantidad, precio_ofertado, resultado, precio_ganador, oferente_ganador.strip(), marca_ofrecida.strip(), marca_ganadora.strip()))
            else:
                cursor.execute("""INSERT INTO productos (licitacion_id, monodroga, marca, presentacion, cantidad, precio_ofertado, 
                                 resultado, precio_ganador, oferente_ganador, marca_ofrecida, marca_ganadora) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                              (licitacion_id, monodroga.strip(), marca.strip(), presentacion.strip(), cantidad, precio_ofertado, resultado, precio_ganador, oferente_ganador.strip(), marca_ofrecida.strip(), marca_ganadora.strip()))
    
    def obtener_licitaciones(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM licitaciones ORDER BY fecha DESC")
            return cursor.fetchall()
    
    def obtener_productos_licitacion(self, licitacion_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM productos WHERE licitacion_id = %s", (licitacion_id,))
            else:
                cursor.execute("SELECT * FROM productos WHERE licitacion_id = ?", (licitacion_id,))
            return cursor.fetchall()
    
    def actualizar_licitacion(self, licitacion_id, numero, fecha, oferente_ganador, marca_ganadora, precio_ganador, cliente_id):
        if not numero or not fecha:
            raise ValueError("Número y fecha son obligatorios")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE licitaciones SET numero_licitacion=%s, cliente_id=%s, fecha=%s, oferente_ganador=%s, marca_ganadora=%s, precio_ganador=%s WHERE id=%s",
                              (numero.strip(), cliente_id, fecha.strip(), oferente_ganador.strip(), marca_ganadora.strip(), precio_ganador, licitacion_id))
            else:
                cursor.execute("UPDATE licitaciones SET numero_licitacion=?, cliente_id=?, fecha=?, oferente_ganador=?, marca_ganadora=?, precio_ganador=? WHERE id=?",
                              (numero.strip(), cliente_id, fecha.strip(), oferente_ganador.strip(), marca_ganadora.strip(), precio_ganador, licitacion_id))
    
    def actualizar_producto(self, producto_id, monodroga, marca, presentacion, cantidad, precio_ofertado, resultado, precio_ganador, oferente_ganador, marca_ofrecida, marca_ganadora=""):
        if not monodroga or not marca or not presentacion or cantidad <= 0 or precio_ofertado < 0:
            raise ValueError("Datos de producto inválidos")
        if resultado == "Adjudicado":
            precio_ganador = precio_ofertado
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""UPDATE productos SET monodroga=%s, marca=%s, presentacion=%s, cantidad=%s, precio_ofertado=%s, 
                                 resultado=%s, precio_ganador=%s, oferente_ganador=%s, marca_ofrecida=%s, marca_ganadora=%s WHERE id=%s""",
                              (monodroga.strip(), marca.strip(), presentacion.strip(), cantidad, precio_ofertado, resultado, precio_ganador, oferente_ganador.strip(), marca_ofrecida.strip(), marca_ganadora.strip(), producto_id))
            else:
                cursor.execute("""UPDATE productos SET monodroga=?, marca=?, presentacion=?, cantidad=?, precio_ofertado=?, 
                                 resultado=?, precio_ganador=?, oferente_ganador=?, marca_ofrecida=?, marca_ganadora=? WHERE id=?""",
                              (monodroga.strip(), marca.strip(), presentacion.strip(), cantidad, precio_ofertado, resultado, precio_ganador, oferente_ganador.strip(), marca_ofrecida.strip(), marca_ganadora.strip(), producto_id))
    
    def eliminar_licitacion(self, licitacion_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("DELETE FROM licitaciones WHERE id = %s", (licitacion_id,))
            else:
                cursor.execute("DELETE FROM licitaciones WHERE id = ?", (licitacion_id,))
    
    def obtener_estadisticas(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT SUM(cantidad) FROM productos")
            unidades_cotizadas = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT SUM(cantidad) FROM productos WHERE resultado = 'Adjudicado'")
            unidades_ganadas = cursor.fetchone()[0] or 0
            
            porcentaje_unidades = (unidades_ganadas / unidades_cotizadas * 100) if unidades_cotizadas > 0 else 0
            
            cursor.execute("SELECT SUM(precio_ofertado * cantidad) FROM productos")
            total_cotizado = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT SUM(precio_ofertado * cantidad) FROM productos WHERE resultado = 'Adjudicado'")
            total_ganado = cursor.fetchone()[0] or 0
            
            porcentaje_dinero = (total_ganado / total_cotizado * 100) if total_cotizado > 0 else 0
            
            return {
                'unidades_cotizadas': unidades_cotizadas,
                'unidades_ganadas': unidades_ganadas,
                'porcentaje_unidades': porcentaje_unidades,
                'total_cotizado': total_cotizado,
                'total_ganado': total_ganado,
                'porcentaje_dinero': porcentaje_dinero
            }
    
    def obtener_historico_producto(self, monodroga, marca, presentacion):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT p.precio_ganador, p.oferente_ganador, p.marca_ofrecida, l.fecha, l.numero_licitacion
                    FROM productos p
                    JOIN licitaciones l ON p.licitacion_id = l.id
                    WHERE p.monodroga LIKE %s AND p.marca LIKE %s AND p.presentacion LIKE %s AND p.precio_ganador IS NOT NULL
                    ORDER BY l.fecha DESC
                    LIMIT 1
                """, (f"%{monodroga.strip()}%", f"%{marca.strip()}%", f"%{presentacion.strip()}%"))
            else:
                cursor.execute("""
                    SELECT p.precio_ganador, p.oferente_ganador, p.marca_ofrecida, l.fecha, l.numero_licitacion
                    FROM productos p
                    JOIN licitaciones l ON p.licitacion_id = l.id
                    WHERE p.monodroga LIKE ? AND p.marca LIKE ? AND p.presentacion LIKE ? AND p.precio_ganador IS NOT NULL
                    ORDER BY l.fecha DESC
                    LIMIT 1
                """, (f"%{monodroga.strip()}%", f"%{marca.strip()}%", f"%{presentacion.strip()}%"))
            return cursor.fetchone()
    
    def exportar_backup(self, backup_path):
        """Exporta backup de la base de datos"""
        import shutil
        shutil.copy2(self.db_path, backup_path)
    
    # CRUD Clientes
    def crear_cliente(self, nombre, razon_social="", cuit="", direccion="", telefono="", email=""):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("Nombre es obligatorio")
        if len(nombre.strip()) > 200:
            raise ValueError("Nombre demasiado largo")
        
        print(f"DEBUG - Creando cliente: {nombre}")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if USE_POSTGRES:
                    cursor.execute("INSERT INTO clientes (nombre, razon_social, cuit, direccion, telefono, email) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                                  (nombre.strip(), razon_social.strip(), cuit.strip(), direccion.strip(), telefono.strip(), email.strip()))
                    result = cursor.fetchone()[0]
                    print(f"DEBUG - Cliente creado en PostgreSQL con ID: {result}")
                    return result
                else:
                    cursor.execute("INSERT INTO clientes (nombre, razon_social, cuit, direccion, telefono, email) VALUES (?, ?, ?, ?, ?, ?)",
                                  (nombre.strip(), razon_social.strip(), cuit.strip(), direccion.strip(), telefono.strip(), email.strip()))
                    result = cursor.lastrowid
                    print(f"DEBUG - Cliente creado en SQLite con ID: {result}")
                    return result
            except Exception as e:
                print(f"DEBUG - Error en crear_cliente: {e}")
                import traceback
                traceback.print_exc()
                raise
    
    def obtener_clientes(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM clientes WHERE activo = TRUE ORDER BY nombre")
            else:
                cursor.execute("SELECT * FROM clientes WHERE activo = 1 ORDER BY nombre")
            return cursor.fetchall()
    
    def actualizar_cliente(self, cliente_id, nombre, razon_social, cuit, direccion, telefono, email):
        if not nombre:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE clientes SET nombre=%s, razon_social=%s, cuit=%s, direccion=%s, telefono=%s, email=%s WHERE id=%s",
                              (nombre.strip(), razon_social.strip(), cuit.strip(), direccion.strip(), telefono.strip(), email.strip(), cliente_id))
            else:
                cursor.execute("UPDATE clientes SET nombre=?, razon_social=?, cuit=?, direccion=?, telefono=?, email=? WHERE id=?",
                              (nombre.strip(), razon_social.strip(), cuit.strip(), direccion.strip(), telefono.strip(), email.strip(), cliente_id))
    
    def eliminar_cliente(self, cliente_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE clientes SET activo = FALSE WHERE id = %s", (cliente_id,))
            else:
                cursor.execute("UPDATE clientes SET activo = 0 WHERE id = ?", (cliente_id,))
    
    # CRUD Oferentes
    def crear_oferente(self, nombre):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("INSERT INTO oferentes (nombre) VALUES (%s) RETURNING id", (nombre.strip(),))
                return cursor.fetchone()[0]
            else:
                cursor.execute("INSERT INTO oferentes (nombre) VALUES (?)", (nombre.strip(),))
                return cursor.lastrowid
    
    def obtener_oferentes(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM oferentes WHERE activo = TRUE ORDER BY nombre")
            else:
                cursor.execute("SELECT * FROM oferentes WHERE activo = 1 ORDER BY nombre")
            return cursor.fetchall()
    
    def actualizar_oferente(self, oferente_id, nombre):
        if not nombre:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE oferentes SET nombre=%s WHERE id=%s", (nombre.strip(), oferente_id))
            else:
                cursor.execute("UPDATE oferentes SET nombre=? WHERE id=?", (nombre.strip(), oferente_id))
    
    def eliminar_oferente(self, oferente_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE oferentes SET activo = FALSE WHERE id = %s", (oferente_id,))
            else:
                cursor.execute("UPDATE oferentes SET activo = 0 WHERE id = ?", (oferente_id,))
    
    # CRUD Marcas
    def crear_marca(self, nombre):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("INSERT INTO marcas (nombre) VALUES (%s) RETURNING id", (nombre.strip(),))
                return cursor.fetchone()[0]
            else:
                cursor.execute("INSERT INTO marcas (nombre) VALUES (?)", (nombre.strip(),))
                return cursor.lastrowid
    
    def obtener_marcas(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM marcas WHERE activo = TRUE ORDER BY nombre")
            else:
                cursor.execute("SELECT * FROM marcas WHERE activo = 1 ORDER BY nombre")
            return cursor.fetchall()
    
    def actualizar_marca(self, marca_id, nombre):
        if not nombre:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE marcas SET nombre=%s WHERE id=%s", (nombre.strip(), marca_id))
            else:
                cursor.execute("UPDATE marcas SET nombre=? WHERE id=?", (nombre.strip(), marca_id))
    
    def eliminar_marca(self, marca_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE marcas SET activo = FALSE WHERE id = %s", (marca_id,))
            else:
                cursor.execute("UPDATE marcas SET activo = 0 WHERE id = ?", (marca_id,))
    
    # CRUD Tipos de Licitación
    def crear_tipo_licitacion(self, nombre):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("INSERT INTO tipos_licitacion (nombre) VALUES (%s) RETURNING id", (nombre.strip(),))
                return cursor.fetchone()[0]
            else:
                cursor.execute("INSERT INTO tipos_licitacion (nombre) VALUES (?)", (nombre.strip(),))
                return cursor.lastrowid
    
    def obtener_tipos_licitacion(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM tipos_licitacion WHERE activo = TRUE ORDER BY nombre")
            else:
                cursor.execute("SELECT * FROM tipos_licitacion WHERE activo = 1 ORDER BY nombre")
            return cursor.fetchall()
    
    def actualizar_tipo_licitacion(self, tipo_id, nombre):
        if not nombre:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE tipos_licitacion SET nombre=%s WHERE id=%s", (nombre.strip(), tipo_id))
            else:
                cursor.execute("UPDATE tipos_licitacion SET nombre=? WHERE id=?", (nombre.strip(), tipo_id))
    
    def eliminar_tipo_licitacion(self, tipo_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE tipos_licitacion SET activo = FALSE WHERE id = %s", (tipo_id,))
            else:
                cursor.execute("UPDATE tipos_licitacion SET activo = 0 WHERE id = ?", (tipo_id,))
