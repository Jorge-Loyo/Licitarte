import sqlite3
import os

# Detectar si estamos en producción
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

if DATABASE_URL:
    try:
        import psycopg2
        USE_POSTGRES = True
    except ImportError:
        USE_POSTGRES = False
else:
    USE_POSTGRES = False

def migrate():
    if USE_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ofertas_productos (
                id SERIAL PRIMARY KEY,
                producto_id INTEGER NOT NULL,
                oferente TEXT NOT NULL,
                laboratorio TEXT NOT NULL,
                precio REAL NOT NULL,
                FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        conn.close()
    else:
        conn = sqlite3.connect('database/licitaciones.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ofertas_productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                oferente TEXT NOT NULL,
                laboratorio TEXT NOT NULL,
                precio REAL NOT NULL,
                FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        conn.close()

if __name__ == '__main__':
    migrate()
