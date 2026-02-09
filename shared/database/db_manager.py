import os
from datetime import datetime
from contextlib import contextmanager
import pandas as pd
from .connection_pool import ConnectionPool, USE_POSTGRES

class DatabaseManager:
    _pool = None
    
    def __init__(self, db_path="database/licitaciones.db"):
        self.db_path = db_path
        
        if DatabaseManager._pool is None:
            DatabaseManager._pool = ConnectionPool()
        
        self.init_db()
        if not USE_POSTGRES and os.path.exists('Data/Medicamentos.xlsx'):
            self.cargar_catalogo_desde_excel()
    
    @contextmanager
    def get_connection(self):
        """Obtiene conexión del pool con transacción automática"""
        with DatabaseManager._pool.get_connection() as conn:
            yield conn
    
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
                        organismo_jurisdiccion TEXT,
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
                        portal_origen TEXT,
                        modalidad_entrega TEXT,
                        forma_pago TEXT,
                        requiere_poliza BOOLEAN DEFAULT FALSE,
                        monto_poliza REAL,
                        observaciones TEXT,
                        mantenimiento_oferta TEXT,
                        numero_presupuesto INTEGER,
                        tipo_adjudicacion TEXT DEFAULT 'Parcial',
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
                        motivo_perdida TEXT,
                        numero_renglon TEXT,
                        costo_unitario REAL,
                        margen_porcentaje REAL,
                        observaciones TEXT,
                        producto_cotizar TEXT DEFAULT 'principal',
                        FOREIGN KEY (licitacion_id) REFERENCES licitaciones (id) ON DELETE CASCADE
                    )
                ''')
                
                # Tabla Medicamentos con todas las columnas del Excel
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS medicamentos (
                        id SERIAL PRIMARY KEY,
                        troquel TEXT,
                        cod_ab INTEGER,
                        troquel_ean TEXT,
                        numero_registro TEXT UNIQUE NOT NULL,
                        cod_monodroga INTEGER,
                        monodroga TEXT,
                        cod_laboratorio INTEGER,
                        laboratorio TEXT,
                        marca TEXT,
                        presentacion TEXT,
                        multidosis INTEGER,
                        precio_caja REAL,
                        precio_unitario REAL,
                        costo_unitario REAL,
                        fecha TEXT
                    )
                ''')
                
                # Tablas de catálogos
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS portales_origen (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS modalidades_entrega (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS formas_pago (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS organismos_jurisdiccion (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS motivos_perdida (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS mantenimientos_oferta (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS laboratorios (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS monodrogas (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS presupuestos (
                        id SERIAL PRIMARY KEY,
                        numero INTEGER NOT NULL UNIQUE,
                        licitacion_id INTEGER NOT NULL,
                        fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (licitacion_id) REFERENCES licitaciones(id)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS alternativas_productos (
                        id SERIAL PRIMARY KEY,
                        producto_id INTEGER NOT NULL,
                        marca TEXT NOT NULL,
                        presentacion TEXT NOT NULL,
                        laboratorio TEXT,
                        costo_unitario REAL,
                        margen_porcentaje REAL,
                        precio_ofertado REAL,
                        observaciones TEXT,
                        FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ofertas_productos (
                        id SERIAL PRIMARY KEY,
                        producto_id INTEGER NOT NULL,
                        oferente TEXT NOT NULL,
                        laboratorio TEXT NOT NULL,
                        precio REAL NOT NULL,
                        FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
                    )
                ''')
                
                # Tabla Usuarios
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS usuarios (
                        id SERIAL PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        activo BOOLEAN DEFAULT TRUE,
                        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Insertar/actualizar usuario admin por defecto (password: admin123)
                from werkzeug.security import generate_password_hash
                admin_hash = generate_password_hash('admin123')
                cursor.execute("""
                    INSERT INTO usuarios (username, email, password_hash) 
                    VALUES (%s, %s, %s)
                    ON CONFLICT (username) 
                    DO UPDATE SET password_hash = EXCLUDED.password_hash
                """, ('admin', 'admin@licitarte.com', admin_hash))
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
                        organismo_jurisdiccion TEXT,
                        activo INTEGER DEFAULT 1
                    )
                ''')
                
                # Migración: Agregar organismo_jurisdiccion si no existe
                cursor.execute("PRAGMA table_info(clientes)")
                columns = [col[1] for col in cursor.fetchall()]
                if 'organismo_jurisdiccion' not in columns:
                    cursor.execute("ALTER TABLE clientes ADD COLUMN organismo_jurisdiccion TEXT")
                
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
                        portal_origen TEXT,
                        modalidad_entrega TEXT,
                        forma_pago TEXT,
                        requiere_poliza INTEGER DEFAULT 0,
                        monto_poliza REAL,
                        observaciones TEXT,
                        CHECK(length(numero_licitacion) > 0),
                        FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                        FOREIGN KEY (tipo_licitacion_id) REFERENCES tipos_licitacion (id)
                    )
                ''')
                
                # Migraciones para columnas faltantes
                cursor.execute("PRAGMA table_info(licitaciones)")
                columns = [col[1] for col in cursor.fetchall()]
                
                if 'portal_origen' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN portal_origen TEXT")
                if 'modalidad_entrega' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN modalidad_entrega TEXT")
                if 'forma_pago' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN forma_pago TEXT")
                if 'requiere_poliza' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN requiere_poliza INTEGER DEFAULT 0")
                if 'monto_poliza' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN monto_poliza REAL")
                if 'observaciones' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN observaciones TEXT")
                if 'mantenimiento_oferta' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN mantenimiento_oferta TEXT")
                if 'numero_presupuesto' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN numero_presupuesto INTEGER")
                
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
                        motivo_perdida TEXT,
                        FOREIGN KEY (licitacion_id) REFERENCES licitaciones (id) ON DELETE CASCADE
                    )
                ''')
                
                # Migraciones para columnas faltantes
                cursor.execute("PRAGMA table_info(productos)")
                columns = [col[1] for col in cursor.fetchall()]
                
                if 'marca_ganadora' not in columns:
                    cursor.execute("ALTER TABLE productos ADD COLUMN marca_ganadora TEXT")
                if 'motivo_perdida' not in columns:
                    cursor.execute("ALTER TABLE productos ADD COLUMN motivo_perdida TEXT")
                if 'numero_renglon' not in columns:
                    cursor.execute("ALTER TABLE productos ADD COLUMN numero_renglon TEXT")
                if 'costo_unitario' not in columns:
                    cursor.execute("ALTER TABLE productos ADD COLUMN costo_unitario REAL")
                if 'margen_porcentaje' not in columns:
                    cursor.execute("ALTER TABLE productos ADD COLUMN margen_porcentaje REAL")
                if 'observaciones' not in columns:
                    cursor.execute("ALTER TABLE productos ADD COLUMN observaciones TEXT")
                if 'producto_cotizar' not in columns:
                    cursor.execute("ALTER TABLE productos ADD COLUMN producto_cotizar TEXT DEFAULT 'principal'")
                
                # Tabla Medicamentos con todas las columnas del Excel
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS medicamentos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        troquel TEXT,
                        cod_ab INTEGER,
                        troquel_ean TEXT,
                        numero_registro TEXT UNIQUE NOT NULL,
                        cod_monodroga INTEGER,
                        monodroga TEXT,
                        cod_laboratorio INTEGER,
                        laboratorio TEXT,
                        marca TEXT,
                        presentacion TEXT,
                        multidosis INTEGER,
                        precio_caja REAL,
                        precio_unitario REAL,
                        costo_unitario REAL,
                        fecha TEXT
                    )
                ''')
                
                # Migraciones: Agregar columnas faltantes si no existen
                cursor.execute("PRAGMA table_info(medicamentos)")
                columns = [col[1] for col in cursor.fetchall()]
                
                columnas_faltantes = {
                    'costo_unitario': 'REAL',
                    'troquel': 'TEXT',
                    'cod_ab': 'INTEGER',
                    'troquel_ean': 'TEXT',
                    'cod_monodroga': 'INTEGER',
                    'cod_laboratorio': 'INTEGER',
                    'multidosis': 'INTEGER'
                }
                
                for col_name, col_type in columnas_faltantes.items():
                    if col_name not in columns:
                        cursor.execute(f"ALTER TABLE medicamentos ADD COLUMN {col_name} {col_type}")
                
                # Crear tablas de catálogos si no existen
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS portales_origen (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS modalidades_entrega (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS formas_pago (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS organismos_jurisdiccion (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS motivos_perdida (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS mantenimientos_oferta (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS laboratorios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS monodrogas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS presupuestos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        numero INTEGER NOT NULL UNIQUE,
                        licitacion_id INTEGER NOT NULL,
                        fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (licitacion_id) REFERENCES licitaciones(id)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS alternativas_productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        producto_id INTEGER NOT NULL,
                        marca TEXT NOT NULL,
                        presentacion TEXT NOT NULL,
                        laboratorio TEXT,
                        costo_unitario REAL,
                        margen_porcentaje REAL,
                        precio_ofertado REAL,
                        observaciones TEXT,
                        FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ofertas_productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        producto_id INTEGER NOT NULL,
                        oferente TEXT NOT NULL,
                        laboratorio TEXT NOT NULL,
                        precio REAL NOT NULL,
                        FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
                    )
                ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_licitacion_numero ON licitaciones(numero_licitacion)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_licitacion_cliente ON licitaciones(cliente_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_producto_licitacion ON productos(licitacion_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_producto_resultado ON productos(resultado)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_medicamentos_numero_registro ON medicamentos(numero_registro)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_medicamentos_monodroga ON medicamentos(monodroga)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_oferentes_nombre ON oferentes(nombre)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_marcas_nombre ON marcas(nombre)')
    
    def cargar_catalogo_desde_excel(self, excel_path='Data/Medicamentos.xlsx'):
        """Carga productos desde Excel a tabla medicamentos y sincroniza laboratorios/monodrogas"""
        try:
            df = pd.read_excel(excel_path)
            total_rows = len(df)
            batch_size = 1000
            
            for batch_start in range(0, total_rows, batch_size):
                batch_end = min(batch_start + batch_size, total_rows)
                df_batch = df.iloc[batch_start:batch_end]
                
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    for _, row in df_batch.iterrows():
                    try:
                        numero_registro = str(row.get('N de Registro', '')) if pd.notna(row.get('N de Registro')) else ''
                        troquel = str(row.get('Troquel', '')) if pd.notna(row.get('Troquel')) else None
                        cod_ab = int(row.get('Cod AB')) if pd.notna(row.get('Cod AB')) else None
                        troquel_ean = str(row.get('Troquel.1', '')) if pd.notna(row.get('Troquel.1')) else None
                        cod_monodroga = int(row.get('Cod Monodroga')) if pd.notna(row.get('Cod Monodroga')) else None
                        monodroga_excel = str(row.get('Monodroga', '')) if pd.notna(row.get('Monodroga')) else ''
                        cod_laboratorio = int(row.get('Cod Laboratorio')) if pd.notna(row.get('Cod Laboratorio')) else None
                        laboratorio_excel = str(row.get('Laboratorio', '')) if pd.notna(row.get('Laboratorio')) else ''
                        marca = str(row.get('Marca', '')) if pd.notna(row.get('Marca')) else ''
                        presentacion = str(row.get('Presentacion', '')) if pd.notna(row.get('Presentacion')) else ''
                        multidosis = int(row.get('Multidosis')) if pd.notna(row.get('Multidosis')) else None
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
                        
                        if not numero_registro or numero_registro == 'nan':
                            continue
                        
                        # Sincronizar monodroga: insertar solo si no existe
                        monodroga_final = monodroga_excel.strip()
                        if monodroga_excel and monodroga_excel.strip():
                            if USE_POSTGRES:
                                cursor.execute("INSERT INTO monodrogas (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING", (monodroga_excel.strip(),))
                                # Obtener nombre correcto de la tabla monodrogas
                                cursor.execute("SELECT nombre FROM monodrogas WHERE LOWER(nombre) = LOWER(%s)", (monodroga_excel.strip(),))
                            else:
                                cursor.execute("INSERT OR IGNORE INTO monodrogas (nombre) VALUES (?)", (monodroga_excel.strip(),))
                                cursor.execute("SELECT nombre FROM monodrogas WHERE LOWER(nombre) = LOWER(?)", (monodroga_excel.strip(),))
                            result = cursor.fetchone()
                            if result:
                                monodroga_final = result[0]
                        
                        # Sincronizar laboratorio: insertar solo si no existe
                        laboratorio_final = laboratorio_excel.strip()
                        if laboratorio_excel and laboratorio_excel.strip():
                            if USE_POSTGRES:
                                cursor.execute("INSERT INTO laboratorios (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING", (laboratorio_excel.strip(),))
                                # Obtener nombre correcto de la tabla laboratorios
                                cursor.execute("SELECT nombre FROM laboratorios WHERE LOWER(nombre) = LOWER(%s)", (laboratorio_excel.strip(),))
                            else:
                                cursor.execute("INSERT OR IGNORE INTO laboratorios (nombre) VALUES (?)", (laboratorio_excel.strip(),))
                                cursor.execute("SELECT nombre FROM laboratorios WHERE LOWER(nombre) = LOWER(?)", (laboratorio_excel.strip(),))
                            result = cursor.fetchone()
                            if result:
                                laboratorio_final = result[0]
                        
                        # Insertar/actualizar medicamento con nombres normalizados
                        if USE_POSTGRES:
                            cursor.execute("""
                                INSERT INTO medicamentos (numero_registro, troquel, cod_ab, troquel_ean, cod_monodroga,
                                monodroga, cod_laboratorio, laboratorio, marca, presentacion, multidosis,
                                precio_caja, precio_unitario, fecha) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (numero_registro) DO UPDATE SET
                                    troquel = EXCLUDED.troquel,
                                    cod_ab = EXCLUDED.cod_ab,
                                    troquel_ean = EXCLUDED.troquel_ean,
                                    cod_monodroga = EXCLUDED.cod_monodroga,
                                    monodroga = EXCLUDED.monodroga,
                                    cod_laboratorio = EXCLUDED.cod_laboratorio,
                                    laboratorio = EXCLUDED.laboratorio,
                                    marca = EXCLUDED.marca,
                                    presentacion = EXCLUDED.presentacion,
                                    multidosis = EXCLUDED.multidosis,
                                    precio_caja = EXCLUDED.precio_caja,
                                    precio_unitario = EXCLUDED.precio_unitario,
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
                            print(f"Error en fila: {e}")
                            continue
                    conn.commit()
                print(f"Procesado lote {batch_start}-{batch_end} de {total_rows}")
            return True
        except Exception as e:
            print(f"Error cargando catálogo: {e}")
            return False
    
    def obtener_catalogo_productos(self):
        """Obtiene lista de productos del catálogo de medicamentos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT numero_registro, monodroga, marca, presentacion FROM medicamentos ORDER BY monodroga, marca, presentacion")
            return cursor.fetchall()
    
    def obtener_producto_por_registro(self, numero_registro):
        """Obtiene producto completo por número de registro"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM medicamentos WHERE numero_registro = %s", (numero_registro,))
            else:
                cursor.execute("SELECT * FROM medicamentos WHERE numero_registro = ?", (numero_registro,))
            return cursor.fetchone()
    
    def crear_licitacion(self, numero, fecha, oferente_ganador="", marca_ganadora="", precio_ganador=None, cliente_id=None, tipo_licitacion_id=None, portal_origen="", modalidad_entrega="", forma_pago="", requiere_poliza=False, monto_poliza=None, observaciones="", mantenimiento_oferta=""):
        if not numero or not fecha:
            raise ValueError("Número y fecha son obligatorios")
        if len(numero.strip()) > 100:
            raise ValueError("Número de licitación demasiado largo")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""INSERT INTO licitaciones (numero_licitacion, cliente_id, tipo_licitacion_id, fecha, oferente_ganador, marca_ganadora, precio_ganador, portal_origen, modalidad_entrega, forma_pago, requiere_poliza, monto_poliza, observaciones, mantenimiento_oferta) 
                                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                              (numero.strip(), cliente_id, tipo_licitacion_id, fecha.strip(), oferente_ganador.strip(), marca_ganadora.strip(), precio_ganador, portal_origen, modalidad_entrega, forma_pago, requiere_poliza, monto_poliza, observaciones, mantenimiento_oferta))
                return cursor.fetchone()[0]
            else:
                cursor.execute("""INSERT INTO licitaciones (numero_licitacion, cliente_id, tipo_licitacion_id, fecha, oferente_ganador, marca_ganadora, precio_ganador, portal_origen, modalidad_entrega, forma_pago, requiere_poliza, monto_poliza, observaciones, mantenimiento_oferta) 
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                              (numero.strip(), cliente_id, tipo_licitacion_id, fecha.strip(), oferente_ganador.strip(), marca_ganadora.strip(), precio_ganador, portal_origen, modalidad_entrega, forma_pago, 1 if requiere_poliza else 0, monto_poliza, observaciones, mantenimiento_oferta))
                return cursor.lastrowid
    
    def agregar_producto(self, licitacion_id, monodroga, marca, presentacion, cantidad, precio_ofertado, resultado, precio_ganador=None, oferente_ganador="", marca_ofrecida="", marca_ganadora="", motivo_perdida="", numero_renglon="", costo_unitario=None, margen_porcentaje=None, observaciones="", producto_cotizar="principal"):
        if not monodroga or not marca or not presentacion or cantidad <= 0 or precio_ofertado < 0:
            raise ValueError("Datos de producto inválidos")
        if resultado == "Adjudicado":
            precio_ganador = precio_ofertado
        
        # Limpiar numero_renglon: si es string vacío o None, convertir a None
        if numero_renglon and str(numero_renglon).strip():
            numero_renglon_limpio = str(numero_renglon).strip()
        else:
            numero_renglon_limpio = None
            
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""INSERT INTO productos (licitacion_id, monodroga, marca, presentacion, cantidad, precio_ofertado, 
                                 resultado, precio_ganador, oferente_ganador, marca_ofrecida, marca_ganadora, motivo_perdida, numero_renglon, costo_unitario, margen_porcentaje, observaciones, producto_cotizar) 
                                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                              (licitacion_id, monodroga.strip(), marca.strip(), presentacion.strip(), cantidad, precio_ofertado, resultado, precio_ganador, oferente_ganador.strip(), marca_ofrecida.strip(), marca_ganadora.strip(), motivo_perdida.strip(), numero_renglon_limpio, costo_unitario, margen_porcentaje, observaciones.strip(), producto_cotizar))
                result = cursor.fetchone()[0]
            else:
                cursor.execute("""INSERT INTO productos (licitacion_id, monodroga, marca, presentacion, cantidad, precio_ofertado, 
                                 resultado, precio_ganador, oferente_ganador, marca_ofrecida, marca_ganadora, motivo_perdida, numero_renglon, costo_unitario, margen_porcentaje, observaciones, producto_cotizar) 
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                              (licitacion_id, monodroga.strip(), marca.strip(), presentacion.strip(), cantidad, precio_ofertado, resultado, precio_ganador, oferente_ganador.strip(), marca_ofrecida.strip(), marca_ganadora.strip(), motivo_perdida.strip(), numero_renglon_limpio, costo_unitario, margen_porcentaje, observaciones.strip(), producto_cotizar))
                result = cursor.lastrowid
            conn.commit()
            return result
    
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
    
    def actualizar_producto(self, producto_id, monodroga, marca, presentacion, cantidad, precio_ofertado, resultado, precio_ganador, oferente_ganador, marca_ofrecida, marca_ganadora="", motivo_perdida="", numero_renglon="", costo_unitario=None, margen_porcentaje=None, observaciones="", producto_cotizar="principal"):
        if not monodroga or not marca or not presentacion or cantidad <= 0 or precio_ofertado < 0:
            raise ValueError("Datos de producto inválidos")
        if resultado == "Adjudicado":
            precio_ganador = precio_ofertado
        
        # Limpiar numero_renglon: si es string vacío o None, convertir a None
        if numero_renglon and str(numero_renglon).strip():
            numero_renglon_limpio = str(numero_renglon).strip()
        else:
            numero_renglon_limpio = None
            
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""UPDATE productos SET monodroga=%s, marca=%s, presentacion=%s, cantidad=%s, precio_ofertado=%s, 
                                 resultado=%s, precio_ganador=%s, oferente_ganador=%s, marca_ofrecida=%s, marca_ganadora=%s, motivo_perdida=%s, numero_renglon=%s, costo_unitario=%s, margen_porcentaje=%s, observaciones=%s, producto_cotizar=%s WHERE id=%s""",
                              (monodroga.strip(), marca.strip(), presentacion.strip(), cantidad, precio_ofertado, resultado, precio_ganador, oferente_ganador.strip(), marca_ofrecida.strip(), marca_ganadora.strip(), motivo_perdida.strip(), numero_renglon_limpio, costo_unitario, margen_porcentaje, observaciones.strip(), producto_cotizar, producto_id))
            else:
                cursor.execute("""UPDATE productos SET monodroga=?, marca=?, presentacion=?, cantidad=?, precio_ofertado=?, 
                                 resultado=?, precio_ganador=?, oferente_ganador=?, marca_ofrecida=?, marca_ganadora=?, motivo_perdida=?, numero_renglon=?, costo_unitario=?, margen_porcentaje=?, observaciones=?, producto_cotizar=? WHERE id=?""",
                              (monodroga.strip(), marca.strip(), presentacion.strip(), cantidad, precio_ofertado, resultado, precio_ganador, oferente_ganador.strip(), marca_ofrecida.strip(), marca_ganadora.strip(), motivo_perdida.strip(), numero_renglon_limpio, costo_unitario, margen_porcentaje, observaciones.strip(), producto_cotizar, producto_id))
            
            conn.commit()
    
    def eliminar_licitacion(self, licitacion_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("DELETE FROM alternativas_productos WHERE producto_id IN (SELECT id FROM productos WHERE licitacion_id = %s)", (licitacion_id,))
                cursor.execute("DELETE FROM productos WHERE licitacion_id = %s", (licitacion_id,))
                cursor.execute("DELETE FROM presupuestos WHERE licitacion_id = %s", (licitacion_id,))
                cursor.execute("DELETE FROM licitaciones WHERE id = %s", (licitacion_id,))
            else:
                cursor.execute("DELETE FROM alternativas_productos WHERE producto_id IN (SELECT id FROM productos WHERE licitacion_id = ?)", (licitacion_id,))
                cursor.execute("DELETE FROM productos WHERE licitacion_id = ?", (licitacion_id,))
                cursor.execute("DELETE FROM presupuestos WHERE licitacion_id = ?", (licitacion_id,))
                cursor.execute("DELETE FROM licitaciones WHERE id = ?", (licitacion_id,))
    
    def obtener_estadisticas(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM licitaciones")
            total_licitaciones = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT COUNT(DISTINCT licitacion_id) FROM productos WHERE resultado = 'Adjudicado'")
            licitaciones_ganadas = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT SUM(cantidad) FROM productos")
            total_unidades = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT SUM(precio_ofertado * cantidad) / SUM(cantidad) FROM productos WHERE resultado = 'Adjudicado' AND cantidad > 0")
            precio_promedio = cursor.fetchone()[0] or 0
            
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
                'total_licitaciones': total_licitaciones,
                'licitaciones_ganadas': licitaciones_ganadas,
                'total_unidades': total_unidades,
                'precio_promedio_ponderado': precio_promedio,
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
    def crear_cliente(self, nombre, razon_social="", cuit="", direccion="", telefono="", email="", organismo_jurisdiccion=""):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("Nombre es obligatorio")
        if len(nombre.strip()) > 200:
            raise ValueError("Nombre demasiado largo")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                if USE_POSTGRES:
                    cursor.execute("INSERT INTO clientes (nombre, organismo_jurisdiccion, razon_social, cuit, direccion, telefono, email) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                                  (nombre.strip(), organismo_jurisdiccion.strip(), razon_social.strip(), cuit.strip(), direccion.strip(), telefono.strip(), email.strip()))
                    return cursor.fetchone()[0]
                else:
                    cursor.execute("INSERT INTO clientes (nombre, organismo_jurisdiccion, razon_social, cuit, direccion, telefono, email) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                  (nombre.strip(), organismo_jurisdiccion.strip(), razon_social.strip(), cuit.strip(), direccion.strip(), telefono.strip(), email.strip()))
                    return cursor.lastrowid
            except Exception as e:
                raise
    
    def obtener_clientes(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM clientes WHERE activo = TRUE ORDER BY nombre")
            else:
                cursor.execute("SELECT * FROM clientes WHERE activo = 1 ORDER BY nombre")
            return cursor.fetchall()
    
    def actualizar_cliente(self, cliente_id, nombre, razon_social, cuit, direccion, telefono, email, organismo_jurisdiccion=""):
        if not nombre:
            raise ValueError("Nombre es obligatorio")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE clientes SET nombre=%s, razon_social=%s, cuit=%s, direccion=%s, telefono=%s, email=%s, organismo_jurisdiccion=%s WHERE id=%s",
                              (nombre.strip(), razon_social.strip(), cuit.strip(), direccion.strip(), telefono.strip(), email.strip(), organismo_jurisdiccion.strip(), cliente_id))
            else:
                cursor.execute("UPDATE clientes SET nombre=?, razon_social=?, cuit=?, direccion=?, telefono=?, email=?, organismo_jurisdiccion=? WHERE id=?",
                              (nombre.strip(), razon_social.strip(), cuit.strip(), direccion.strip(), telefono.strip(), email.strip(), organismo_jurisdiccion.strip(), cliente_id))
    
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
    
    # CRUD Portales Origen
    def crear_portal_origen(self, nombre):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("INSERT INTO portales_origen (nombre) VALUES (%s) RETURNING id", (nombre.strip(),))
                return cursor.fetchone()[0]
            else:
                cursor.execute("INSERT INTO portales_origen (nombre) VALUES (?)", (nombre.strip(),))
                return cursor.lastrowid
    
    def obtener_portales_origen(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM portales_origen WHERE activo = TRUE ORDER BY nombre")
            else:
                cursor.execute("SELECT * FROM portales_origen WHERE activo = 1 ORDER BY nombre")
            return cursor.fetchall()
    
    def actualizar_portal_origen(self, portal_id, nombre):
        if not nombre:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE portales_origen SET nombre=%s WHERE id=%s", (nombre.strip(), portal_id))
            else:
                cursor.execute("UPDATE portales_origen SET nombre=? WHERE id=?", (nombre.strip(), portal_id))
    
    def eliminar_portal_origen(self, portal_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE portales_origen SET activo = FALSE WHERE id = %s", (portal_id,))
            else:
                cursor.execute("UPDATE portales_origen SET activo = 0 WHERE id = ?", (portal_id,))
    
    # CRUD Modalidades Entrega
    def crear_modalidad_entrega(self, nombre):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("INSERT INTO modalidades_entrega (nombre) VALUES (%s) RETURNING id", (nombre.strip(),))
                return cursor.fetchone()[0]
            else:
                cursor.execute("INSERT INTO modalidades_entrega (nombre) VALUES (?)", (nombre.strip(),))
                return cursor.lastrowid
    
    def obtener_modalidades_entrega(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM modalidades_entrega WHERE activo = TRUE ORDER BY nombre")
            else:
                cursor.execute("SELECT * FROM modalidades_entrega WHERE activo = 1 ORDER BY nombre")
            return cursor.fetchall()
    
    def actualizar_modalidad_entrega(self, modalidad_id, nombre):
        if not nombre:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE modalidades_entrega SET nombre=%s WHERE id=%s", (nombre.strip(), modalidad_id))
            else:
                cursor.execute("UPDATE modalidades_entrega SET nombre=? WHERE id=?", (nombre.strip(), modalidad_id))
    
    def eliminar_modalidad_entrega(self, modalidad_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE modalidades_entrega SET activo = FALSE WHERE id = %s", (modalidad_id,))
            else:
                cursor.execute("UPDATE modalidades_entrega SET activo = 0 WHERE id = ?", (modalidad_id,))
    
    # CRUD Formas Pago
    def crear_forma_pago(self, nombre):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("INSERT INTO formas_pago (nombre) VALUES (%s) RETURNING id", (nombre.strip(),))
                return cursor.fetchone()[0]
            else:
                cursor.execute("INSERT INTO formas_pago (nombre) VALUES (?)", (nombre.strip(),))
                return cursor.lastrowid
    
    def obtener_formas_pago(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM formas_pago WHERE activo = TRUE ORDER BY nombre")
            else:
                cursor.execute("SELECT * FROM formas_pago WHERE activo = 1 ORDER BY nombre")
            return cursor.fetchall()
    
    def actualizar_forma_pago(self, forma_id, nombre):
        if not nombre:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE formas_pago SET nombre=%s WHERE id=%s", (nombre.strip(), forma_id))
            else:
                cursor.execute("UPDATE formas_pago SET nombre=? WHERE id=?", (nombre.strip(), forma_id))
    
    def eliminar_forma_pago(self, forma_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE formas_pago SET activo = FALSE WHERE id = %s", (forma_id,))
            else:
                cursor.execute("UPDATE formas_pago SET activo = 0 WHERE id = ?", (forma_id,))
    
    # CRUD Organismos Jurisdiccion
    def crear_organismo(self, nombre):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("INSERT INTO organismos_jurisdiccion (nombre) VALUES (%s) RETURNING id", (nombre.strip(),))
                return cursor.fetchone()[0]
            else:
                cursor.execute("INSERT INTO organismos_jurisdiccion (nombre) VALUES (?)", (nombre.strip(),))
                return cursor.lastrowid
    
    def obtener_organismos(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM organismos_jurisdiccion WHERE activo = TRUE ORDER BY nombre")
            else:
                cursor.execute("SELECT * FROM organismos_jurisdiccion WHERE activo = 1 ORDER BY nombre")
            return cursor.fetchall()
    
    def actualizar_organismo(self, organismo_id, nombre):
        if not nombre:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE organismos_jurisdiccion SET nombre=%s WHERE id=%s", (nombre.strip(), organismo_id))
            else:
                cursor.execute("UPDATE organismos_jurisdiccion SET nombre=? WHERE id=?", (nombre.strip(), organismo_id))
    
    def eliminar_organismo(self, organismo_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE organismos_jurisdiccion SET activo = FALSE WHERE id = %s", (organismo_id,))
            else:
                cursor.execute("UPDATE organismos_jurisdiccion SET activo = 0 WHERE id = ?", (organismo_id,))
    
    # CRUD Motivos Perdida
    def crear_motivo_perdida(self, nombre):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("INSERT INTO motivos_perdida (nombre) VALUES (%s) RETURNING id", (nombre.strip(),))
                return cursor.fetchone()[0]
            else:
                cursor.execute("INSERT INTO motivos_perdida (nombre) VALUES (?)", (nombre.strip(),))
                return cursor.lastrowid
    
    def obtener_motivos_perdida(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM motivos_perdida WHERE activo = TRUE ORDER BY nombre")
            else:
                cursor.execute("SELECT * FROM motivos_perdida WHERE activo = 1 ORDER BY nombre")
            return cursor.fetchall()
    
    def actualizar_motivo_perdida(self, motivo_id, nombre):
        if not nombre:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE motivos_perdida SET nombre=%s WHERE id=%s", (nombre.strip(), motivo_id))
            else:
                cursor.execute("UPDATE motivos_perdida SET nombre=? WHERE id=?", (nombre.strip(), motivo_id))
    
    def eliminar_motivo_perdida(self, motivo_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE motivos_perdida SET activo = FALSE WHERE id = %s", (motivo_id,))
            else:
                cursor.execute("UPDATE motivos_perdida SET activo = 0 WHERE id = ?", (motivo_id,))

    # CRUD Mantenimientos Oferta
    def crear_mantenimiento_oferta(self, nombre):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("INSERT INTO mantenimientos_oferta (nombre) VALUES (%s) RETURNING id", (nombre.strip(),))
                return cursor.fetchone()[0]
            else:
                cursor.execute("INSERT INTO mantenimientos_oferta (nombre) VALUES (?)", (nombre.strip(),))
                return cursor.lastrowid
    
    def obtener_mantenimientos_oferta(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM mantenimientos_oferta WHERE activo = TRUE ORDER BY nombre")
            else:
                cursor.execute("SELECT * FROM mantenimientos_oferta WHERE activo = 1 ORDER BY nombre")
            return cursor.fetchall()
    
    def actualizar_mantenimiento_oferta(self, mantenimiento_id, nombre):
        if not nombre:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE mantenimientos_oferta SET nombre=%s WHERE id=%s", (nombre.strip(), mantenimiento_id))
            else:
                cursor.execute("UPDATE mantenimientos_oferta SET nombre=? WHERE id=?", (nombre.strip(), mantenimiento_id))
    
    def eliminar_mantenimiento_oferta(self, mantenimiento_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE mantenimientos_oferta SET activo = FALSE WHERE id = %s", (mantenimiento_id,))
            else:
                cursor.execute("UPDATE mantenimientos_oferta SET activo = 0 WHERE id = ?", (mantenimiento_id,))

    # CRUD Laboratorios
    def crear_laboratorio(self, nombre):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("INSERT INTO laboratorios (nombre) VALUES (%s) RETURNING id", (nombre.strip(),))
                return cursor.fetchone()[0]
            else:
                cursor.execute("INSERT INTO laboratorios (nombre) VALUES (?)", (nombre.strip(),))
                return cursor.lastrowid
    
    def obtener_laboratorios(self, pagina=1, por_pagina=50):
        """Obtiene laboratorios con paginación"""
        pagina = max(1, int(pagina))
        por_pagina = min(100, max(10, int(por_pagina)))
        offset = (pagina - 1) * por_pagina
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                # Total de registros
                cursor.execute("SELECT COUNT(*) FROM laboratorios WHERE activo = TRUE")
                total = cursor.fetchone()[0]
                # Registros de la página
                cursor.execute("SELECT id, cod, nombre, activo FROM laboratorios WHERE activo = TRUE ORDER BY nombre LIMIT %s OFFSET %s", (por_pagina, offset))
            else:
                cursor.execute("SELECT COUNT(*) FROM laboratorios WHERE activo = 1")
                total = cursor.fetchone()[0]
                cursor.execute("SELECT id, cod, nombre, activo FROM laboratorios WHERE activo = 1 ORDER BY nombre LIMIT ? OFFSET ?", (por_pagina, offset))
            
            datos = cursor.fetchall()
            return {
                'total': total,
                'pagina': pagina,
                'por_pagina': por_pagina,
                'total_paginas': (total + por_pagina - 1) // por_pagina,
                'datos': datos
            }
    
    def actualizar_laboratorio(self, laboratorio_id, nombre):
        if not nombre:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE laboratorios SET nombre=%s WHERE id=%s", (nombre.strip(), laboratorio_id))
            else:
                cursor.execute("UPDATE laboratorios SET nombre=? WHERE id=?", (nombre.strip(), laboratorio_id))
    
    def eliminar_laboratorio(self, laboratorio_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE laboratorios SET activo = FALSE WHERE id = %s", (laboratorio_id,))
            else:
                cursor.execute("UPDATE laboratorios SET activo = 0 WHERE id = ?", (laboratorio_id,))

    # CRUD Monodrogas
    def crear_monodroga(self, nombre):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("INSERT INTO monodrogas (nombre) VALUES (%s) RETURNING id", (nombre.strip(),))
                return cursor.fetchone()[0]
            else:
                cursor.execute("INSERT INTO monodrogas (nombre) VALUES (?)", (nombre.strip(),))
                return cursor.lastrowid
    
    def obtener_monodrogas(self, pagina=1, por_pagina=50):
        """Obtiene monodrogas con paginación"""
        pagina = max(1, int(pagina))
        por_pagina = min(100, max(10, int(por_pagina)))
        offset = (pagina - 1) * por_pagina
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                # Total de registros
                cursor.execute("SELECT COUNT(*) FROM monodrogas WHERE activo = TRUE")
                total = cursor.fetchone()[0]
                # Registros de la página
                cursor.execute("SELECT id, cod, nombre, activo FROM monodrogas WHERE activo = TRUE ORDER BY nombre LIMIT %s OFFSET %s", (por_pagina, offset))
            else:
                cursor.execute("SELECT COUNT(*) FROM monodrogas WHERE activo = 1")
                total = cursor.fetchone()[0]
                cursor.execute("SELECT id, cod, nombre, activo FROM monodrogas WHERE activo = 1 ORDER BY nombre LIMIT ? OFFSET ?", (por_pagina, offset))
            
            datos = cursor.fetchall()
            return {
                'total': total,
                'pagina': pagina,
                'por_pagina': por_pagina,
                'total_paginas': (total + por_pagina - 1) // por_pagina,
                'datos': datos
            }
    
    def actualizar_monodroga(self, monodroga_id, nombre):
        if not nombre:
            raise ValueError("Nombre es obligatorio")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE monodrogas SET nombre=%s WHERE id=%s", (nombre.strip(), monodroga_id))
            else:
                cursor.execute("UPDATE monodrogas SET nombre=? WHERE id=?", (nombre.strip(), monodroga_id))
    
    def eliminar_monodroga(self, monodroga_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("UPDATE monodrogas SET activo = FALSE WHERE id = %s", (monodroga_id,))
            else:
                cursor.execute("UPDATE monodrogas SET activo = 0 WHERE id = ?", (monodroga_id,))

    def obtener_siguiente_numero_presupuesto(self):
        """Obtiene el siguiente número de presupuesto disponible"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT COALESCE(MAX(numero), 0) + 1 FROM presupuestos")
            else:
                cursor.execute("SELECT COALESCE(MAX(numero), 0) + 1 FROM presupuestos")
            return cursor.fetchone()[0]
    
    def crear_presupuesto(self, licitacion_id):
        """Crea un nuevo presupuesto y retorna su número"""
        numero = self.obtener_siguiente_numero_presupuesto()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("INSERT INTO presupuestos (numero, licitacion_id) VALUES (%s, %s) RETURNING id", (numero, licitacion_id))
                cursor.execute("UPDATE licitaciones SET numero_presupuesto = %s WHERE id = %s", (numero, licitacion_id))
            else:
                cursor.execute("INSERT INTO presupuestos (numero, licitacion_id) VALUES (?, ?)", (numero, licitacion_id))
                cursor.execute("UPDATE licitaciones SET numero_presupuesto = ? WHERE id = ?", (numero, licitacion_id))
        return numero
    
    def obtener_presupuestos(self, limit=50, offset=0):
        """Obtiene lista de presupuestos con información de licitación"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT p.numero, p.fecha_generacion, l.numero_licitacion, c.nombre as cliente
                    FROM presupuestos p
                    JOIN licitaciones l ON p.licitacion_id = l.id
                    LEFT JOIN clientes c ON l.cliente_id = c.id
                    ORDER BY p.numero DESC
                    LIMIT %s OFFSET %s
                """, (limit, offset))
            else:
                cursor.execute("""
                    SELECT p.numero, p.fecha_generacion, l.numero_licitacion, c.nombre as cliente
                    FROM presupuestos p
                    JOIN licitaciones l ON p.licitacion_id = l.id
                    LEFT JOIN clientes c ON l.cliente_id = c.id
                    ORDER BY p.numero DESC
                    LIMIT ? OFFSET ?
                """, (limit, offset))
            return cursor.fetchall()
    
    def obtener_presupuesto_por_numero(self, numero):
        """Obtiene información completa de un presupuesto con productos y alternativas"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT p.numero, p.licitacion_id, l.numero_licitacion, c.nombre as cliente_nombre
                    FROM presupuestos p
                    JOIN licitaciones l ON p.licitacion_id = l.id
                    LEFT JOIN clientes c ON l.cliente_id = c.id
                    WHERE p.numero = %s
                """, (numero,))
            else:
                cursor.execute("""
                    SELECT p.numero, p.licitacion_id, l.numero_licitacion, c.nombre as cliente_nombre
                    FROM presupuestos p
                    JOIN licitaciones l ON p.licitacion_id = l.id
                    LEFT JOIN clientes c ON l.cliente_id = c.id
                    WHERE p.numero = ?
                """, (numero,))
            presupuesto = cursor.fetchone()
            
            if not presupuesto:
                return None
            
            # Obtener productos de la licitación
            licitacion_id = presupuesto[1]
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT id, monodroga, marca, presentacion, cantidad, precio_ofertado, producto_cotizar
                    FROM productos WHERE licitacion_id = %s
                """, (licitacion_id,))
            else:
                cursor.execute("""
                    SELECT id, monodroga, marca, presentacion, cantidad, precio_ofertado, producto_cotizar
                    FROM productos WHERE licitacion_id = ?
                """, (licitacion_id,))
            productos_raw = cursor.fetchall()
            
            productos = []
            for prod in productos_raw:
                producto_id = prod[0]
                producto_cotizar = prod[6] if len(prod) > 6 else 'principal'
                
                # Si es principal, agregar el producto
                if producto_cotizar == 'principal':
                    productos.append({
                        'id': producto_id,
                        'monodroga': prod[1],
                        'marca': prod[2],
                        'presentacion': prod[3],
                        'cantidad': prod[4],
                        'precio': prod[5]
                    })
                else:
                    # Si es alternativa, buscar la alternativa específica
                    if USE_POSTGRES:
                        cursor.execute("""
                            SELECT marca, presentacion, precio_ofertado
                            FROM alternativas_productos WHERE producto_id = %s
                        """, (producto_id,))
                    else:
                        cursor.execute("""
                            SELECT marca, presentacion, precio_ofertado
                            FROM alternativas_productos WHERE producto_id = ?
                        """, (producto_id,))
                    alternativas = cursor.fetchall()
                    
                    # Agregar la alternativa seleccionada
                    if alternativas:
                        # Extraer índice de alternativa del producto_cotizar (ej: "alt-1-0" -> 0)
                        try:
                            idx = int(producto_cotizar.split('-')[-1])
                            if idx < len(alternativas):
                                alt = alternativas[idx]
                                productos.append({
                                    'id': producto_id,
                                    'monodroga': prod[1],
                                    'marca': alt[0],
                                    'presentacion': alt[1],
                                    'cantidad': prod[4],
                                    'precio': alt[2]
                                })
                        except:
                            # Si falla, usar el producto principal
                            productos.append({
                                'id': producto_id,
                                'monodroga': prod[1],
                                'marca': prod[2],
                                'presentacion': prod[3],
                                'cantidad': prod[4],
                                'precio': prod[5]
                            })
            
            return {
                'numero': presupuesto[0],
                'licitacion': presupuesto[2],
                'cliente': presupuesto[3],
                'productos': productos
            }
    
    def obtener_licitaciones_resumen(self):
        """Obtiene listado de licitaciones con resumen de productos ganados/total y montos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT 
                        l.id,
                        l.numero_licitacion,
                        c.nombre as cliente,
                        COUNT(p.id) as total_productos,
                        SUM(CASE WHEN p.resultado = 'Adjudicado' THEN 1 ELSE 0 END) as productos_ganados,
                        COALESCE(SUM(p.precio_ofertado * p.cantidad), 0) as monto_cotizado,
                        COALESCE(SUM(CASE WHEN p.resultado = 'Adjudicado' THEN p.precio_ofertado * p.cantidad ELSE 0 END), 0) as monto_adjudicado
                    FROM licitaciones l
                    LEFT JOIN clientes c ON l.cliente_id = c.id
                    LEFT JOIN productos p ON l.id = p.licitacion_id
                    GROUP BY l.id, l.numero_licitacion, c.nombre
                    ORDER BY l.id DESC
                """)
            else:
                cursor.execute("""
                    SELECT 
                        l.id,
                        l.numero_licitacion,
                        c.nombre as cliente,
                        COUNT(p.id) as total_productos,
                        SUM(CASE WHEN p.resultado = 'Adjudicado' THEN 1 ELSE 0 END) as productos_ganados,
                        COALESCE(SUM(p.precio_ofertado * p.cantidad), 0) as monto_cotizado,
                        COALESCE(SUM(CASE WHEN p.resultado = 'Adjudicado' THEN p.precio_ofertado * p.cantidad ELSE 0 END), 0) as monto_adjudicado
                    FROM licitaciones l
                    LEFT JOIN clientes c ON l.cliente_id = c.id
                    LEFT JOIN productos p ON l.id = p.licitacion_id
                    GROUP BY l.id, l.numero_licitacion, c.nombre
                    ORDER BY l.id DESC
                """)
            return cursor.fetchall()
    
    # CRUD Ofertas Productos
    def obtener_ofertas_producto(self, producto_id):
        """Obtiene todas las ofertas de un producto"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute("SELECT * FROM ofertas_productos WHERE producto_id = %s ORDER BY id", (producto_id,))
            else:
                cursor.execute("SELECT * FROM ofertas_productos WHERE producto_id = ? ORDER BY id", (producto_id,))
            return cursor.fetchall()
    
    def guardar_ofertas_producto(self, producto_id, ofertas):
        """Guarda ofertas de un producto (elimina las anteriores y crea nuevas)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Eliminar ofertas anteriores
            if USE_POSTGRES:
                cursor.execute("DELETE FROM ofertas_productos WHERE producto_id = %s", (producto_id,))
            else:
                cursor.execute("DELETE FROM ofertas_productos WHERE producto_id = ?", (producto_id,))
            
            # Insertar nuevas ofertas
            for oferta in ofertas:
                if USE_POSTGRES:
                    cursor.execute(
                        "INSERT INTO ofertas_productos (producto_id, oferente, laboratorio, precio) VALUES (%s, %s, %s, %s)",
                        (producto_id, oferta['oferente'], oferta['laboratorio'], oferta['precio'])
                    )
                else:
                    cursor.execute(
                        "INSERT INTO ofertas_productos (producto_id, oferente, laboratorio, precio) VALUES (?, ?, ?, ?)",
                        (producto_id, oferta['oferente'], oferta['laboratorio'], oferta['precio'])
                    )
            conn.commit()
