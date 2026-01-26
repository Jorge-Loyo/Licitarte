"""
Migración: Agregar tablas de catálogos
"""
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from database.db_manager import DatabaseManager, USE_POSTGRES

def migrar_catalogos():
    print("=== AGREGANDO TABLAS DE CATÁLOGOS ===\n")
    
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        print("1. Creando tabla portales_origen...")
        try:
            if USE_POSTGRES:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS portales_origen (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS portales_origen (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                """)
            
            # Insertar valores por defecto
            valores = ['COMPR.AR', 'BAC', 'PBAC', 'Portal propio', 'Mail', 'Otro']
            for val in valores:
                try:
                    if USE_POSTGRES:
                        cursor.execute("INSERT INTO portales_origen (nombre) VALUES (%s) ON CONFLICT DO NOTHING", (val,))
                    else:
                        cursor.execute("INSERT OR IGNORE INTO portales_origen (nombre) VALUES (?)", (val,))
                except:
                    pass
            print("   OK Tabla portales_origen creada")
        except Exception as e:
            print(f"   ERROR: {e}")
        
        print("\n2. Creando tabla modalidades_entrega...")
        try:
            if USE_POSTGRES:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS modalidades_entrega (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS modalidades_entrega (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                """)
            
            valores = ['Entrega total', 'Entregas parciales', 'Abierto por demanda']
            for val in valores:
                try:
                    if USE_POSTGRES:
                        cursor.execute("INSERT INTO modalidades_entrega (nombre) VALUES (%s) ON CONFLICT DO NOTHING", (val,))
                    else:
                        cursor.execute("INSERT OR IGNORE INTO modalidades_entrega (nombre) VALUES (?)", (val,))
                except:
                    pass
            print("   OK Tabla modalidades_entrega creada")
        except Exception as e:
            print(f"   ERROR: {e}")
        
        print("\n3. Creando tabla formas_pago...")
        try:
            if USE_POSTGRES:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS formas_pago (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS formas_pago (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                """)
            
            valores = ['30 días', '60 días', '90 días', '120 días', 'Contra entrega', 'Tesorería pública']
            for val in valores:
                try:
                    if USE_POSTGRES:
                        cursor.execute("INSERT INTO formas_pago (nombre) VALUES (%s) ON CONFLICT DO NOTHING", (val,))
                    else:
                        cursor.execute("INSERT OR IGNORE INTO formas_pago (nombre) VALUES (?)", (val,))
                except:
                    pass
            print("   OK Tabla formas_pago creada")
        except Exception as e:
            print(f"   ERROR: {e}")
    
    print("\n=== MIGRACIÓN COMPLETADA ===")

if __name__ == "__main__":
    migrar_catalogos()
