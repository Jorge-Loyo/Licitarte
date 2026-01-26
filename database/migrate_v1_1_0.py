#!/usr/bin/env python3
"""
Script de migración unificado para v1.1.0
Ejecutar en producción (Render) para crear tablas y columnas nuevas
"""

import os
import sys

# Agregar path del proyecto
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager, USE_POSTGRES

def migrate():
    print("🚀 Iniciando migración v1.1.0...")
    
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        try:
            # 1. Agregar costo_unitario a celty
            print("📦 Agregando costo_unitario a celty...")
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name='celty' AND column_name='costo_unitario'
                """)
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE celty ADD COLUMN costo_unitario REAL")
                    print("✓ costo_unitario agregado")
                else:
                    print("✓ costo_unitario ya existe")
            else:
                cursor.execute("PRAGMA table_info(celty)")
                columns = [col[1] for col in cursor.fetchall()]
                if 'costo_unitario' not in columns:
                    cursor.execute("ALTER TABLE celty ADD COLUMN costo_unitario REAL")
                    print("✓ costo_unitario agregado")
                else:
                    print("✓ costo_unitario ya existe")
            
            # 2. Crear tabla portales_origen
            print("📦 Creando tabla portales_origen...")
            if USE_POSTGRES:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS portales_origen (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS portales_origen (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                """)
            
            # Insertar valores por defecto
            cursor.execute("SELECT COUNT(*) FROM portales_origen")
            if cursor.fetchone()[0] == 0:
                valores = ['Comprar', 'BAC', 'Otro']
                for v in valores:
                    if USE_POSTGRES:
                        cursor.execute("INSERT INTO portales_origen (nombre) VALUES (%s)", (v,))
                    else:
                        cursor.execute("INSERT INTO portales_origen (nombre) VALUES (?)", (v,))
                print(f"✓ {len(valores)} portales insertados")
            else:
                print("✓ portales_origen ya tiene datos")
            
            # 3. Crear tabla modalidades_entrega
            print("📦 Creando tabla modalidades_entrega...")
            if USE_POSTGRES:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS modalidades_entrega (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS modalidades_entrega (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                """)
            
            cursor.execute("SELECT COUNT(*) FROM modalidades_entrega")
            if cursor.fetchone()[0] == 0:
                valores = ['Única', 'Múltiple', 'Programada']
                for v in valores:
                    if USE_POSTGRES:
                        cursor.execute("INSERT INTO modalidades_entrega (nombre) VALUES (%s)", (v,))
                    else:
                        cursor.execute("INSERT INTO modalidades_entrega (nombre) VALUES (?)", (v,))
                print(f"✓ {len(valores)} modalidades insertadas")
            else:
                print("✓ modalidades_entrega ya tiene datos")
            
            # 4. Crear tabla formas_pago
            print("📦 Creando tabla formas_pago...")
            if USE_POSTGRES:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS formas_pago (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS formas_pago (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                """)
            
            cursor.execute("SELECT COUNT(*) FROM formas_pago")
            if cursor.fetchone()[0] == 0:
                valores = ['Contado', '30 días', '60 días']
                for v in valores:
                    if USE_POSTGRES:
                        cursor.execute("INSERT INTO formas_pago (nombre) VALUES (%s)", (v,))
                    else:
                        cursor.execute("INSERT INTO formas_pago (nombre) VALUES (?)", (v,))
                print(f"✓ {len(valores)} formas de pago insertadas")
            else:
                print("✓ formas_pago ya tiene datos")
            
            # 5. Crear tabla organismos_jurisdiccion
            print("📦 Creando tabla organismos_jurisdiccion...")
            if USE_POSTGRES:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS organismos_jurisdiccion (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS organismos_jurisdiccion (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                """)
            
            cursor.execute("SELECT COUNT(*) FROM organismos_jurisdiccion")
            if cursor.fetchone()[0] == 0:
                valores = ['Nacional', 'Provincial', 'Municipal', 'CABA', 'Privado']
                for v in valores:
                    if USE_POSTGRES:
                        cursor.execute("INSERT INTO organismos_jurisdiccion (nombre) VALUES (%s)", (v,))
                    else:
                        cursor.execute("INSERT INTO organismos_jurisdiccion (nombre) VALUES (?)", (v,))
                print(f"✓ {len(valores)} organismos insertados")
            else:
                print("✓ organismos_jurisdiccion ya tiene datos")
            
            # 6. Crear tabla motivos_perdida
            print("📦 Creando tabla motivos_perdida...")
            if USE_POSTGRES:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS motivos_perdida (
                        id SERIAL PRIMARY KEY,
                        nombre TEXT UNIQUE NOT NULL,
                        activo BOOLEAN DEFAULT TRUE
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS motivos_perdida (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT UNIQUE NOT NULL,
                        activo INTEGER DEFAULT 1
                    )
                """)
            
            cursor.execute("SELECT COUNT(*) FROM motivos_perdida")
            if cursor.fetchone()[0] == 0:
                valores = ['Precio más alto', 'Marca no priorizada', 'No cumplía especificación', 'Error administrativo', 'Otro']
                for v in valores:
                    if USE_POSTGRES:
                        cursor.execute("INSERT INTO motivos_perdida (nombre) VALUES (%s)", (v,))
                    else:
                        cursor.execute("INSERT INTO motivos_perdida (nombre) VALUES (?)", (v,))
                print(f"✓ {len(valores)} motivos insertados")
            else:
                print("✓ motivos_perdida ya tiene datos")
            
            # 7. Agregar columnas a licitaciones
            print("📦 Agregando columnas a licitaciones...")
            columnas_licitaciones = [
                ('portal_origen', 'TEXT'),
                ('modalidad_entrega', 'TEXT'),
                ('forma_pago', 'TEXT'),
                ('requiere_poliza', 'BOOLEAN' if USE_POSTGRES else 'INTEGER'),
                ('monto_poliza', 'REAL'),
                ('observaciones', 'TEXT')
            ]
            
            for col_name, col_type in columnas_licitaciones:
                if USE_POSTGRES:
                    cursor.execute(f"""
                        SELECT column_name FROM information_schema.columns 
                        WHERE table_name='licitaciones' AND column_name='{col_name}'
                    """)
                    if not cursor.fetchone():
                        cursor.execute(f"ALTER TABLE licitaciones ADD COLUMN {col_name} {col_type}")
                        print(f"✓ {col_name} agregado a licitaciones")
                else:
                    cursor.execute("PRAGMA table_info(licitaciones)")
                    columns = [col[1] for col in cursor.fetchall()]
                    if col_name not in columns:
                        cursor.execute(f"ALTER TABLE licitaciones ADD COLUMN {col_name} {col_type}")
                        print(f"✓ {col_name} agregado a licitaciones")
            
            # 8. Agregar columnas a clientes
            print("📦 Agregando organismo_jurisdiccion a clientes...")
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name='clientes' AND column_name='organismo_jurisdiccion'
                """)
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE clientes ADD COLUMN organismo_jurisdiccion TEXT")
                    print("✓ organismo_jurisdiccion agregado")
            else:
                cursor.execute("PRAGMA table_info(clientes)")
                columns = [col[1] for col in cursor.fetchall()]
                if 'organismo_jurisdiccion' not in columns:
                    cursor.execute("ALTER TABLE clientes ADD COLUMN organismo_jurisdiccion TEXT")
                    print("✓ organismo_jurisdiccion agregado")
            
            # 9. Agregar motivo_perdida a productos
            print("📦 Agregando motivo_perdida a productos...")
            if USE_POSTGRES:
                cursor.execute("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name='productos' AND column_name='motivo_perdida'
                """)
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE productos ADD COLUMN motivo_perdida TEXT")
                    print("✓ motivo_perdida agregado")
            else:
                cursor.execute("PRAGMA table_info(productos)")
                columns = [col[1] for col in cursor.fetchall()]
                if 'motivo_perdida' not in columns:
                    cursor.execute("ALTER TABLE productos ADD COLUMN motivo_perdida TEXT")
                    print("✓ motivo_perdida agregado")
            
            conn.commit()
            print("\n✅ Migración v1.1.0 completada exitosamente!")
            
        except Exception as e:
            conn.rollback()
            print(f"\n❌ Error en migración: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    migrate()
