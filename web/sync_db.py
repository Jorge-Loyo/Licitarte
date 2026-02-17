#!/usr/bin/env python3
"""Script para sincronizar base de datos SQLite local a PostgreSQL en Render"""
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

# Solo ejecutar en PostgreSQL (Render)
if os.getenv('USE_POSTGRES') != 'true':
    print("Este script solo se ejecuta en PostgreSQL")
    exit(0)

try:
    import psycopg
    from urllib.parse import urlparse
    
    # Conectar a PostgreSQL
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("DATABASE_URL no configurada")
        exit(1)
    
    result = urlparse(db_url)
    pg_conn = psycopg.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
    pg_cursor = pg_conn.cursor()
    
    # Conectar a SQLite local (debe estar en el repo)
    sqlite_path = '../shared/database/licitaciones.db'
    if not os.path.exists(sqlite_path):
        print(f"Base de datos local no encontrada: {sqlite_path}")
        exit(1)
    
    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_cursor = sqlite_conn.cursor()
    
    print("=== Sincronizando base de datos local a Render ===")
    
    # Tablas a sincronizar en orden (respetando foreign keys)
    tablas = [
        'organismos_jurisdiccion',
        'clientes',
        'oferentes',
        'marcas',
        'tipos_licitacion',
        'portales_origen',
        'modalidades_entrega',
        'formas_pago',
        'motivos_perdida',
        'mantenimientos_oferta',
        'laboratorios',
        'monodrogas',
        'medicamentos',
        'licitaciones',
        'productos',
        'alternativas_productos',
        'presupuestos'
    ]
    
    for tabla in tablas:
        try:
            # Limpiar tabla en PostgreSQL
            pg_cursor.execute(f"TRUNCATE TABLE {tabla} RESTART IDENTITY CASCADE")
            
            # Obtener datos de SQLite
            sqlite_cursor.execute(f"SELECT * FROM {tabla}")
            rows = sqlite_cursor.fetchall()
            
            if not rows:
                print(f"✓ {tabla}: 0 registros")
                continue
            
            # Obtener nombres de columnas
            sqlite_cursor.execute(f"PRAGMA table_info({tabla})")
            columns = [col[1] for col in sqlite_cursor.fetchall()]
            
            # Insertar en PostgreSQL
            placeholders = ','.join(['%s'] * len(columns))
            columns_str = ','.join(columns)
            
            for row in rows:
                pg_cursor.execute(
                    f"INSERT INTO {tabla} ({columns_str}) VALUES ({placeholders})",
                    row
                )
            
            pg_conn.commit()
            print(f"✓ {tabla}: {len(rows)} registros sincronizados")
            
        except Exception as e:
            print(f"✗ Error en {tabla}: {e}")
            continue
    
    sqlite_conn.close()
    pg_cursor.close()
    pg_conn.close()
    
    print("=== Sincronización completada ===")
    
except Exception as e:
    print(f"Error general: {e}")
    exit(1)
