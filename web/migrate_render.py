#!/usr/bin/env python
"""Migración manual para Render - agregar columnas faltantes"""
import os
import psycopg

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

def migrate():
    print("Ejecutando migraciones...")
    
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            # Agregar fecha_carga
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='licitaciones' AND column_name='fecha_carga'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                print("✓ fecha_carga agregada")
            else:
                print("✓ fecha_carga ya existe")
            
            # Agregar numero_presupuesto
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='licitaciones' AND column_name='numero_presupuesto'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN numero_presupuesto INTEGER")
                print("✓ numero_presupuesto agregada")
            else:
                print("✓ numero_presupuesto ya existe")
            
            conn.commit()
            print("\n✅ Migraciones completadas")

if __name__ == '__main__':
    migrate()
