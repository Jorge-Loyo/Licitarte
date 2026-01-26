"""
Migración: Agregar tabla organismos_jurisdiccion
"""
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from database.db_manager import DatabaseManager, USE_POSTGRES

def migrar_organismos():
    print("=== AGREGANDO TABLA ORGANISMOS ===\n")
    
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        print("Creando tabla organismos_jurisdiccion...")
        try:
            if USE_POSTGRES:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS organismos_jurisdiccion (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS organismos_jurisdiccion (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                """)
            
            valores = ['Nacional', 'Provincial', 'Municipal', 'Hospital', 'OS']
            for val in valores:
                try:
                    if USE_POSTGRES:
                        cursor.execute("INSERT INTO organismos_jurisdiccion (nombre) VALUES (%s) ON CONFLICT DO NOTHING", (val,))
                    else:
                        cursor.execute("INSERT OR IGNORE INTO organismos_jurisdiccion (nombre) VALUES (?)", (val,))
                except:
                    pass
            print("   OK Tabla organismos_jurisdiccion creada")
        except Exception as e:
            print(f"   ERROR: {e}")
    
    print("\n=== MIGRACION COMPLETADA ===")

if __name__ == "__main__":
    migrar_organismos()
