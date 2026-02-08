import sqlite3
import os

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), 'licitaciones.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Crear tabla alternativas_productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alternativas_productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                marca TEXT NOT NULL,
                presentacion TEXT NOT NULL,
                laboratorio TEXT,
                costo_unitario REAL,
                margen_porcentaje REAL,
                precio_ofertado REAL,
                observaciones TEXT,
                FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        print("✓ Tabla alternativas_productos creada")
        
    except Exception as e:
        print(f"Error en migración: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
