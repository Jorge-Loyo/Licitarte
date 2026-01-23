import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager

# Detectar si estamos en producción (Render)
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Usar PostgreSQL en producción
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        USE_POSTGRES = True
    except ImportError:
        print("Warning: psycopg2 not installed, using SQLite")
        USE_POSTGRES = False
else:
    # Usar SQLite en local
    USE_POSTGRES = False

class DatabaseManager:
    def __init__(self, db_path="database/licitaciones.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        if USE_POSTGRES:
            conn = psycopg2.connect(DATABASE_URL)
        else:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON")
        
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if USE_POSTGRES:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS licitaciones (
                        id SERIAL PRIMARY KEY,
                        numero_licitacion TEXT UNIQUE NOT NULL,
                        fecha TEXT NOT NULL,
                        laboratorio_ganador TEXT,
                        CHECK(length(numero_licitacion) > 0)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS productos (
                        id SERIAL PRIMARY KEY,
                        licitacion_id INTEGER NOT NULL,
                        item_producto TEXT NOT NULL,
                        cantidad INTEGER NOT NULL CHECK(cantidad > 0),
                        precio_ofertado REAL NOT NULL CHECK(precio_ofertado >= 0),
                        resultado TEXT NOT NULL CHECK(resultado IN ('Adjudicado', 'Parcial', 'No Adjudicado')),
                        precio_ganador REAL CHECK(precio_ganador >= 0),
                        laboratorio_ganador TEXT,
                        FOREIGN KEY (licitacion_id) REFERENCES licitaciones (id) ON DELETE CASCADE
                    )
                ''')
            else:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS licitaciones (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        numero_licitacion TEXT UNIQUE NOT NULL,
                        fecha TEXT NOT NULL,
                        laboratorio_ganador TEXT,
                        CHECK(length(numero_licitacion) > 0)
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        licitacion_id INTEGER NOT NULL,
                        item_producto TEXT NOT NULL,
                        cantidad INTEGER NOT NULL CHECK(cantidad > 0),
                        precio_ofertado REAL NOT NULL CHECK(precio_ofertado >= 0),
                        resultado TEXT NOT NULL CHECK(resultado IN ('Adjudicado', 'Parcial', 'No Adjudicado')),
                        precio_ganador REAL CHECK(precio_ganador >= 0),
                        laboratorio_ganador TEXT,
                        FOREIGN KEY (licitacion_id) REFERENCES licitaciones (id) ON DELETE CASCADE
                    )
                ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_licitacion_numero ON licitaciones(numero_licitacion)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_producto_licitacion ON productos(licitacion_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_producto_resultado ON productos(resultado)')
    
    def crear_licitacion(self, numero, fecha, laboratorio_ganador=""):
        if not numero or not fecha:
            raise ValueError("Número y fecha son obligatorios")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO licitaciones (numero_licitacion, fecha, laboratorio_ganador) VALUES (?, ?, ?)",
                          (numero.strip(), fecha.strip(), laboratorio_ganador.strip()))
            return cursor.lastrowid
    
    def agregar_producto(self, licitacion_id, item, cantidad, precio_ofertado, resultado, precio_ganador=None, lab_ganador=""):
        if not item or cantidad <= 0 or precio_ofertado < 0:
            raise ValueError("Datos de producto inválidos")
        if resultado == "Adjudicado":
            precio_ganador = precio_ofertado
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO productos (licitacion_id, item_producto, cantidad, precio_ofertado, 
                             resultado, precio_ganador, laboratorio_ganador) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                          (licitacion_id, item.strip(), cantidad, precio_ofertado, resultado, precio_ganador, lab_ganador.strip()))
    
    def obtener_licitaciones(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM licitaciones ORDER BY fecha DESC")
            return cursor.fetchall()
    
    def obtener_productos_licitacion(self, licitacion_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE licitacion_id = ?", (licitacion_id,))
            return cursor.fetchall()
    
    def actualizar_licitacion(self, licitacion_id, numero, fecha, laboratorio_ganador):
        if not numero or not fecha:
            raise ValueError("Número y fecha son obligatorios")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE licitaciones SET numero_licitacion=?, fecha=?, laboratorio_ganador=? WHERE id=?",
                          (numero.strip(), fecha.strip(), laboratorio_ganador.strip(), licitacion_id))
    
    def actualizar_producto(self, producto_id, item, cantidad, precio_ofertado, resultado, precio_ganador, lab_ganador):
        if not item or cantidad <= 0 or precio_ofertado < 0:
            raise ValueError("Datos de producto inválidos")
        if resultado == "Adjudicado":
            precio_ganador = precio_ofertado
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE productos SET item_producto=?, cantidad=?, precio_ofertado=?, 
                             resultado=?, precio_ganador=?, laboratorio_ganador=? WHERE id=?""",
                          (item.strip(), cantidad, precio_ofertado, resultado, precio_ganador, lab_ganador.strip(), producto_id))
    
    def eliminar_licitacion(self, licitacion_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM licitaciones WHERE id = ?", (licitacion_id,))
    
    def obtener_estadisticas(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM licitaciones")
            total_licitaciones = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT licitacion_id) FROM productos WHERE resultado = 'Adjudicado'")
            licitaciones_ganadas = cursor.fetchone()[0]
            
            cursor.execute("SELECT SUM(cantidad) FROM productos")
            total_unidades = cursor.fetchone()[0] or 0
            
            cursor.execute("""SELECT SUM(precio_ofertado * cantidad), SUM(cantidad) 
                             FROM productos WHERE resultado = 'Adjudicado'""")
            resultado = cursor.fetchone()
            precio_promedio = (resultado[0] / resultado[1]) if resultado[1] else 0
            
            return {
                'total_licitaciones': total_licitaciones,
                'licitaciones_ganadas': licitaciones_ganadas,
                'total_unidades': total_unidades,
                'precio_promedio_ponderado': precio_promedio
            }
    
    def obtener_historico_producto(self, nombre_producto):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.precio_ganador, p.laboratorio_ganador, l.fecha, l.numero_licitacion
                FROM productos p
                JOIN licitaciones l ON p.licitacion_id = l.id
                WHERE p.item_producto LIKE ? AND p.precio_ganador IS NOT NULL
                ORDER BY l.fecha DESC
                LIMIT 1
            """, (f"%{nombre_producto.strip()}%",))
            return cursor.fetchone()
    
    def exportar_backup(self, backup_path):
        """Exporta backup de la base de datos"""
        import shutil
        shutil.copy2(self.db_path, backup_path)
