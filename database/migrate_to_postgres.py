import sqlite3
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('../web/.env')

# Conexiones
sqlite_conn = sqlite3.connect('../database/licitaciones.db')
pg_conn = psycopg2.connect(os.getenv('DATABASE_URL'))

print("✓ Conectado a ambas bases de datos")

# Crear tablas en PostgreSQL
with pg_conn.cursor() as cur:
    # Clientes
    cur.execute("""
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
    """)
    
    # Oferentes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS oferentes (
            id SERIAL PRIMARY KEY,
            nombre TEXT UNIQUE NOT NULL,
            activo BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Marcas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS marcas (
            id SERIAL PRIMARY KEY,
            nombre TEXT UNIQUE NOT NULL,
            activo BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Tipos Licitación
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tipos_licitacion (
            id SERIAL PRIMARY KEY,
            nombre TEXT UNIQUE NOT NULL,
            activo BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Catálogo Celty
    cur.execute("""
        CREATE TABLE IF NOT EXISTS celty (
            id SERIAL PRIMARY KEY,
            numero_registro TEXT UNIQUE NOT NULL,
            monodroga TEXT,
            marca TEXT,
            presentacion TEXT,
            laboratorio TEXT,
            precio_caja REAL,
            precio_unitario REAL,
            costo_unitario REAL,
            fecha TEXT
        )
    """)
    
    # Catálogos configurables
    for tabla in ['portales_origen', 'modalidades_entrega', 'formas_pago', 'organismos_jurisdiccion', 'motivos_perdida', 'mantenimientos_oferta']:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {tabla} (
                id SERIAL PRIMARY KEY,
                nombre TEXT UNIQUE NOT NULL,
                activo BOOLEAN DEFAULT TRUE
            )
        """)
    
    pg_conn.commit()
    print("✓ Tablas creadas en PostgreSQL")

# Migrar datos
tablas_a_migrar = [
    'clientes', 'oferentes', 'marcas', 'tipos_licitacion', 'celty',
    'portales_origen', 'modalidades_entrega', 'formas_pago',
    'organismos_jurisdiccion', 'motivos_perdida', 'mantenimientos_oferta'
]

for tabla in tablas_a_migrar:
    try:
        # Leer de SQLite
        sqlite_cur = sqlite_conn.cursor()
        sqlite_cur.execute(f"SELECT * FROM {tabla}")
        rows = sqlite_cur.fetchall()
        
        if not rows:
            print(f"⚠ {tabla}: Sin datos")
            continue
        
        # Obtener nombres de columnas
        columns = [desc[0] for desc in sqlite_cur.description]
        columns_str = ', '.join([c for c in columns if c != 'id'])
        placeholders = ', '.join(['%s'] * (len(columns) - 1))
        
        # Insertar en PostgreSQL
        pg_cur = pg_conn.cursor()
        count = 0
        for row in rows:
            try:
                values = list(row[1:])  # Excluir ID
                # Convertir INTEGER a BOOLEAN para columna 'activo'
                if 'activo' in columns:
                    activo_idx = columns.index('activo') - 1
                    if activo_idx < len(values) and isinstance(values[activo_idx], int):
                        values[activo_idx] = bool(values[activo_idx])
                
                pg_cur.execute(f"INSERT INTO {tabla} ({columns_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING", values)
                count += 1
            except Exception as e:
                print(f"  Error en fila: {e}")
                pg_conn.rollback()
                continue
        
        pg_conn.commit()
        print(f"✓ {tabla}: {count} registros migrados")
        
    except Exception as e:
        print(f"✗ {tabla}: {e}")
        continue

sqlite_conn.close()
pg_conn.close()

print("\n✅ Migración completada")
