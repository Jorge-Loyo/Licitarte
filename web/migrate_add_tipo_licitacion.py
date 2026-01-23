#!/usr/bin/env python
"""
Migración: Agregar columna tipo_licitacion_id a tabla licitaciones
"""
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from database.db_manager import DatabaseManager

def migrate():
    print("Iniciando migración...")
    db = DatabaseManager()
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            if db.USE_POSTGRES:
                # Verificar si la columna ya existe
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='licitaciones' AND column_name='tipo_licitacion_id'
                """)
                
                if cursor.fetchone() is None:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN tipo_licitacion_id INTEGER")
                    cursor.execute("ALTER TABLE licitaciones ADD CONSTRAINT fk_tipo_licitacion FOREIGN KEY (tipo_licitacion_id) REFERENCES tipos_licitacion(id)")
                    print("✓ Columna tipo_licitacion_id agregada a PostgreSQL")
                else:
                    print("✓ Columna tipo_licitacion_id ya existe")
            else:
                # SQLite
                cursor.execute("PRAGMA table_info(licitaciones)")
                columns = [col[1] for col in cursor.fetchall()]
                
                if 'tipo_licitacion_id' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN tipo_licitacion_id INTEGER")
                    print("✓ Columna tipo_licitacion_id agregada a SQLite")
                else:
                    print("✓ Columna tipo_licitacion_id ya existe")
        
        print("✓ Migración completada exitosamente")
    except Exception as e:
        print(f"✗ Error en migración: {e}")
        sys.exit(1)

if __name__ == '__main__':
    migrate()
