#!/usr/bin/env python3
"""Script para agregar columna porcentaje_poliza a tabla licitaciones"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

USE_POSTGRES = os.getenv('USE_POSTGRES', 'false').lower() == 'true'

if USE_POSTGRES:
    import psycopg
    from urllib.parse import urlparse
    
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("ERROR: DATABASE_URL no configurada")
        exit(1)
    
    print("Conectando a PostgreSQL...")
    result = urlparse(db_url)
    conn = psycopg.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
    cursor = conn.cursor()
    
    print("Verificando columna porcentaje_poliza...")
    cursor.execute("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name='licitaciones' AND column_name='porcentaje_poliza'
    """)
    if not cursor.fetchone():
        print("Agregando columna porcentaje_poliza...")
        cursor.execute("ALTER TABLE licitaciones ADD COLUMN porcentaje_poliza REAL")
        conn.commit()
        print("✓ Columna porcentaje_poliza agregada")
    else:
        print("✓ Columna porcentaje_poliza ya existe")
    
    cursor.close()
    conn.close()
else:
    import sqlite3
    
    db_path = Path(__file__).parent.parent / 'shared' / 'database' / 'licitaciones.db'
    print(f"Conectando a SQLite: {db_path}")
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    print("Verificando columna porcentaje_poliza...")
    cursor.execute("PRAGMA table_info(licitaciones)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'porcentaje_poliza' not in columns:
        print("Agregando columna porcentaje_poliza...")
        cursor.execute("ALTER TABLE licitaciones ADD COLUMN porcentaje_poliza REAL")
        conn.commit()
        print("✓ Columna porcentaje_poliza agregada")
    else:
        print("✓ Columna porcentaje_poliza ya existe")
    
    cursor.close()
    conn.close()

print("\n✅ Migración completada exitosamente")
