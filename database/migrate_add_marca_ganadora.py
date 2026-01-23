"""
Script de migración para agregar columna marca_ganadora a tabla productos
"""
import sqlite3
import os
import sys

# Detectar si estamos en producción (Render)
DATABASE_URL = os.environ.get('DATABASE_URL')

# Render usa postgres:// pero psycopg2 necesita postgresql://
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

if DATABASE_URL:
    # Usar PostgreSQL en producción
    try:
        import psycopg2
        USE_POSTGRES = True
        print("✓ Migrando PostgreSQL")
    except ImportError as e:
        print(f"✗ Error importando psycopg2: {e}")
        sys.exit(1)
else:
    # Usar SQLite en local
    USE_POSTGRES = False
    print("Migrando SQLite (desarrollo local)")

def migrate():
    try:
        if USE_POSTGRES:
            conn = psycopg2.connect(DATABASE_URL)
            cursor = conn.cursor()
            
            # Verificar si la columna ya existe
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='productos' AND column_name='marca_ganadora'
            """)
            
            if cursor.fetchone() is None:
                cursor.execute("ALTER TABLE productos ADD COLUMN marca_ganadora TEXT")
                conn.commit()
                print("✓ Columna marca_ganadora agregada a PostgreSQL")
            else:
                print("✓ Columna marca_ganadora ya existe en PostgreSQL")
            
            conn.close()
        else:
            db_path = "licitaciones.db"
            if not os.path.exists(db_path):
                print(f"✗ Base de datos no encontrada: {db_path}")
                return
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Verificar si la columna ya existe
            cursor.execute("PRAGMA table_info(productos)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'marca_ganadora' not in columns:
                cursor.execute("ALTER TABLE productos ADD COLUMN marca_ganadora TEXT")
                conn.commit()
                print("✓ Columna marca_ganadora agregada a SQLite")
            else:
                print("✓ Columna marca_ganadora ya existe en SQLite")
            
            conn.close()
        
        print("✓ Migración completada exitosamente")
    except Exception as e:
        print(f"✗ Error en migración: {e}")
        sys.exit(1)

if __name__ == '__main__':
    migrate()
