import sqlite3

conn = sqlite3.connect('licitaciones.db')
cursor = conn.cursor()

cursor.execute('PRAGMA table_info(productos)')
columns = [col[1] for col in cursor.fetchall()]

if 'motivo_perdida' not in columns:
    cursor.execute('ALTER TABLE productos ADD COLUMN motivo_perdida TEXT')
    conn.commit()
    print('✓ Columna motivo_perdida agregada')
else:
    print('Columna motivo_perdida ya existe')

conn.close()
