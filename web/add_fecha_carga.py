import psycopg
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:licitarte123@localhost:5432/licitarte')

conn = psycopg.connect(DATABASE_URL)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE licitaciones ADD COLUMN IF NOT EXISTS fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    conn.commit()
    print("Columna fecha_carga agregada exitosamente")
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
