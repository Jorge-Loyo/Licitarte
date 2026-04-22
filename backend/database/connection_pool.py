import os
from contextlib import contextmanager
from pathlib import Path
from dotenv import load_dotenv
import psycopg
from psycopg_pool import ConnectionPool as PsycopgPool

# Cargar .env desde la raíz del proyecto (dos niveles arriba de este archivo)
load_dotenv(Path(__file__).parent.parent.parent / '.env')

USE_POSTGRES = True

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no configurado. Inicia PostgreSQL con: docker-compose up -d")

if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

class ConnectionPool:
    """Pool de conexiones para PostgreSQL con reconexión automática"""
    
    def __init__(self, min_conn=2, max_conn=10):
        if not DATABASE_URL:
            raise RuntimeError("DATABASE_URL no está configurado")
        try:
            self.pool = PsycopgPool(
                DATABASE_URL, 
                min_size=min_conn, 
                max_size=max_conn,
                kwargs={
                    'autocommit': False,
                    'prepare_threshold': None,
                    'options': '-c statement_timeout=300000'  # 5 minutos
                }
            )
        except psycopg.OperationalError as e:
            raise RuntimeError(f"No se pudo conectar a PostgreSQL. Verifica que Docker esté corriendo: {e}")
    
    @contextmanager
    def get_connection(self):
        """Obtiene conexión del pool con transacción automática y reconexión"""
        conn = self.pool.getconn()
        try:
            # Verificar si la conexión está viva
            if conn.closed or conn.info.transaction_status == psycopg.pq.TransactionStatus.UNKNOWN:
                conn.close()
                self.pool.putconn(conn)
                conn = self.pool.getconn()
            
            yield conn
            conn.commit()
        except (psycopg.OperationalError, psycopg.InterfaceError) as e:
            # Conexión perdida, cerrar y obtener nueva
            try:
                conn.rollback()
            except:
                pass
            try:
                conn.close()
            except:
                pass
            self.pool.putconn(conn)
            raise
        except Exception:
            conn.rollback()
            raise
        finally:
            try:
                self.pool.putconn(conn)
            except:
                pass
    
    def close_all(self):
        """Cierra todas las conexiones"""
        self.pool.close()
