"""Migración: Crear tabla usuarios en PostgreSQL"""
import sys
import os
from pathlib import Path
from werkzeug.security import generate_password_hash

sys.path.insert(0, str(Path(__file__).parent.parent))
from shared.database.db_manager import DatabaseManager

def crear_tabla_usuarios():
    """Crear tabla usuarios y usuario admin por defecto"""
    print("Creando tabla usuarios en PostgreSQL...")
    
    try:
        db = DatabaseManager()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    activo BOOLEAN DEFAULT TRUE,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            admin_hash = generate_password_hash('admin123')
            
            try:
                cursor.execute("""
                    INSERT INTO usuarios (username, email, password_hash)
                    VALUES (%s, %s, %s)
                """, ('admin', 'admin@licitarte.com', admin_hash))
                print("✓ Usuario admin creado (username: admin, password: admin123)")
            except Exception:
                print("- Usuario admin ya existe")
        
        print("✓ Tabla usuarios creada exitosamente")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    crear_tabla_usuarios()
