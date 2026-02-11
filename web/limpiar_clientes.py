#!/usr/bin/env python3
"""Script para limpiar clientes inactivos en PostgreSQL"""
import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv('USE_POSTGRES') == 'true':
    import psycopg
    from urllib.parse import urlparse
    
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        result = urlparse(db_url)
        conn = psycopg.connect(
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        cursor = conn.cursor()
        
        # Eliminar físicamente todos los clientes inactivos
        cursor.execute("DELETE FROM clientes WHERE activo = FALSE")
        conn.commit()
        print(f"✓ Clientes inactivos eliminados")
        
        cursor.close()
        conn.close()
else:
    print("Este script solo funciona con PostgreSQL")
