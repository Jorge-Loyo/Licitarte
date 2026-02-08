import psycopg2
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:licitarte123@localhost:5432/licitarte')

if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    cur.execute("ALTER TABLE productos ADD COLUMN producto_cotizar TEXT DEFAULT 'principal'")
    conn.commit()
    
    print("✓ Columna producto_cotizar agregada exitosamente")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
