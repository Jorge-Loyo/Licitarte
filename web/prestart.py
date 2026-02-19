#!/usr/bin/env python3
"""Script que se ejecuta antes de iniciar gunicorn para verificar columnas en PostgreSQL"""
import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv('USE_POSTGRES') == 'true':
    try:
        import psycopg
        from urllib.parse import urlparse
        
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            print("DATABASE_URL no configurada")
            exit(0)
        
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
        
        print("Verificando columna organismo_jurisdiccion en tabla clientes...")
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='clientes' AND column_name='organismo_jurisdiccion'
        """)
        if not cursor.fetchone():
            print("Agregando columna organismo_jurisdiccion...")
            cursor.execute("ALTER TABLE clientes ADD COLUMN organismo_jurisdiccion VARCHAR(200)")
            conn.commit()
            print("✓ Columna organismo_jurisdiccion agregada")
        else:
            print("✓ Columna organismo_jurisdiccion ya existe")
        
        print("Verificando columna numero_presupuesto en tabla licitaciones...")
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='licitaciones' AND column_name='numero_presupuesto'
        """)
        if not cursor.fetchone():
            print("Agregando columna numero_presupuesto...")
            cursor.execute("ALTER TABLE licitaciones ADD COLUMN numero_presupuesto INTEGER")
            conn.commit()
            print("✓ Columna numero_presupuesto agregada")
        else:
            print("✓ Columna numero_presupuesto ya existe")
        
        print("Verificando columna fecha_carga en tabla licitaciones...")
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='licitaciones' AND column_name='fecha_carga'
        """)
        if not cursor.fetchone():
            print("Agregando columna fecha_carga...")
            cursor.execute("ALTER TABLE licitaciones ADD COLUMN fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            conn.commit()
            print("✓ Columna fecha_carga agregada")
        else:
            print("✓ Columna fecha_carga ya existe")
        
        print("Verificando columna porcentaje_poliza en tabla licitaciones...")
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
        print("✓ Verificación de columnas completada exitosamente")
        
    except Exception as e:
        print(f"Error verificando columnas: {e}")
        exit(1)
else:
    print("SQLite detectado, no se requiere verificación de columnas")
