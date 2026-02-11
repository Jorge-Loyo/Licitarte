"""Script para agregar columnas faltantes en Render PostgreSQL"""
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("ERROR: DATABASE_URL no encontrada")
    exit(1)

print(f"Conectando a base de datos...")

try:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            print("Conexión exitosa")
            
            # Verificar si organismo_jurisdiccion existe en clientes
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'clientes' AND column_name = 'organismo_jurisdiccion'
            """)
            if not cursor.fetchone():
                print("Agregando columna organismo_jurisdiccion a tabla clientes...")
                cursor.execute("ALTER TABLE clientes ADD COLUMN organismo_jurisdiccion TEXT")
                conn.commit()
                print("✓ Columna organismo_jurisdiccion agregada")
            else:
                print("✓ Columna organismo_jurisdiccion ya existe")
            
            # Verificar si numero_presupuesto existe en licitaciones
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'licitaciones' AND column_name = 'numero_presupuesto'
            """)
            if not cursor.fetchone():
                print("Agregando columna numero_presupuesto a tabla licitaciones...")
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN numero_presupuesto INTEGER")
                conn.commit()
                print("✓ Columna numero_presupuesto agregada")
            else:
                print("✓ Columna numero_presupuesto ya existe")
            
            # Verificar si fecha_carga existe en licitaciones
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'licitaciones' AND column_name = 'fecha_carga'
            """)
            if not cursor.fetchone():
                print("Agregando columna fecha_carga a tabla licitaciones...")
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                conn.commit()
                print("✓ Columna fecha_carga agregada")
            else:
                print("✓ Columna fecha_carga ya existe")
            
            print("\n✓ Todas las columnas verificadas/agregadas correctamente")
            
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)
