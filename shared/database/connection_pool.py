import os
from contextlib import contextmanager
import psycopg
from psycopg.pool import ConnectionPool as PsycopgPool

USE_POSTGRES = True

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no configurado. Inicia PostgreSQL con: docker-compose up -d")

if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

class ConnectionPool:
    """Pool de conexiones para PostgreSQL"""
    
    def __init__(self, min_conn=2, max_conn=10):
        try:
            self.pool = PsycopgPool(
                DATABASE_URL, min_size=min_conn, max_size=max_conn
            )
        except psycopg.OperationalError as e:
            raise RuntimeError(f"No se pudo conectar a PostgreSQL. Verifica que Docker esté corriendo: {e}")
    
    @contextmanager
    def get_connection(self):
        """Obtiene conexión del pool con transacción automática"""
        conn = self.pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self.pool.putconn(conn)
    
    def close_all(self):
        """Cierra todas las conexiones"""
        self.pool.closeall()
