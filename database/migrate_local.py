"""
Script de migración para agregar columnas faltantes
"""
import sqlite3
import os

db_path = "licitaciones.db"

if not os.path.exists(db_path):
    print(f"ERROR - Base de datos no encontrada: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Verificar y agregar tipo_licitacion_id a licitaciones
    cursor.execute("PRAGMA table_info(licitaciones)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'tipo_licitacion_id' not in columns:
        cursor.execute("ALTER TABLE licitaciones ADD COLUMN tipo_licitacion_id INTEGER")
        print("OK - Columna tipo_licitacion_id agregada a licitaciones")
    else:
        print("OK - Columna tipo_licitacion_id ya existe")
    
    # Crear tabla tipos_licitacion si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tipos_licitacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            activo INTEGER DEFAULT 1
        )
    """)
    print("OK - Tabla tipos_licitacion verificada")
    
    # Crear tabla oferentes si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS oferentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            activo INTEGER DEFAULT 1
        )
    """)
    print("OK - Tabla oferentes verificada")
    
    # Crear tabla marcas si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marcas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            activo INTEGER DEFAULT 1
        )
    """)
    print("OK - Tabla marcas verificada")
    
    conn.commit()
    print("OK - Migracion completada exitosamente")
    
except Exception as e:
    print(f"ERROR - Error en migracion: {e}")
    conn.rollback()
finally:
    conn.close()
