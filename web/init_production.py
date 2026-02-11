#!/usr/bin/env python
"""
Script de inicialización para producción
Ejecuta migraciones v1.1.0 y carga catálogo
"""
import sys
import os
from pathlib import Path

# Agregar directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.database.db_manager import DatabaseManager
from shared.database.connection_pool import USE_POSTGRES

def run_migrations(db):
    """Ejecutar migraciones v1.1.0"""
    print("\n🚀 Ejecutando migraciones v1.1.0...")
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        try:
            # 1. costo_unitario en productos
            if USE_POSTGRES:
                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='productos' AND column_name='costo_unitario'")
                if not cursor.fetchone():
                    cursor.execute("ALTER TABLE productos ADD COLUMN costo_unitario REAL")
                    print("✓ costo_unitario agregado a productos")
            
            # 2. portales_origen
            cursor.execute("CREATE TABLE IF NOT EXISTS portales_origen (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
            cursor.execute("SELECT COUNT(*) FROM portales_origen")
            if cursor.fetchone()[0] == 0:
                for v in ['Comprar', 'BAC', 'Otro']:
                    cursor.execute("INSERT INTO portales_origen (nombre) VALUES (%s)", (v,))
                print("✓ portales_origen creada")
            
            # 3. modalidades_entrega
            cursor.execute("CREATE TABLE IF NOT EXISTS modalidades_entrega (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
            cursor.execute("SELECT COUNT(*) FROM modalidades_entrega")
            if cursor.fetchone()[0] == 0:
                for v in ['Única', 'Múltiple', 'Programada']:
                    cursor.execute("INSERT INTO modalidades_entrega (nombre) VALUES (%s)", (v,))
                print("✓ modalidades_entrega creada")
            
            # 4. formas_pago
            cursor.execute("CREATE TABLE IF NOT EXISTS formas_pago (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
            cursor.execute("SELECT COUNT(*) FROM formas_pago")
            if cursor.fetchone()[0] == 0:
                for v in ['Contado', '30 días', '60 días']:
                    cursor.execute("INSERT INTO formas_pago (nombre) VALUES (%s)", (v,))
                print("✓ formas_pago creada")
            
            # 5. organismos_jurisdiccion
            cursor.execute("CREATE TABLE IF NOT EXISTS organismos_jurisdiccion (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
            cursor.execute("SELECT COUNT(*) FROM organismos_jurisdiccion")
            if cursor.fetchone()[0] == 0:
                for v in ['Nacional', 'Provincial', 'Municipal', 'CABA', 'Privado']:
                    cursor.execute("INSERT INTO organismos_jurisdiccion (nombre) VALUES (%s)", (v,))
                print("✓ organismos_jurisdiccion creada")
            
            # 6. motivos_perdida
            cursor.execute("CREATE TABLE IF NOT EXISTS motivos_perdida (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
            cursor.execute("SELECT COUNT(*) FROM motivos_perdida")
            if cursor.fetchone()[0] == 0:
                for v in ['Precio más alto', 'Marca no priorizada', 'No cumplía especificación', 'Error administrativo', 'Otro']:
                    cursor.execute("INSERT INTO motivos_perdida (nombre) VALUES (%s)", (v,))
                print("✓ motivos_perdida creada")
            
            # 7. Columnas en licitaciones
            for col in ['portal_origen', 'modalidad_entrega', 'forma_pago', 'observaciones']:
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='licitaciones' AND column_name='{col}'")
                if not cursor.fetchone():
                    cursor.execute(f"ALTER TABLE licitaciones ADD COLUMN {col} TEXT")
            
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='licitaciones' AND column_name='requiere_poliza'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN requiere_poliza BOOLEAN")
            
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='licitaciones' AND column_name='monto_poliza'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN monto_poliza REAL")
            
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='licitaciones' AND column_name='fecha_carga'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='licitaciones' AND column_name='numero_presupuesto'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN numero_presupuesto INTEGER")
            
            print("✓ Columnas agregadas a licitaciones")
            
            # 8. organismo_jurisdiccion en clientes
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='clientes' AND column_name='organismo_jurisdiccion'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE clientes ADD COLUMN organismo_jurisdiccion TEXT")
                print("✓ organismo_jurisdiccion agregado a clientes")
            
            # 9. motivo_perdida en productos
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='productos' AND column_name='motivo_perdida'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE productos ADD COLUMN motivo_perdida TEXT")
                print("✓ motivo_perdida agregado a productos")
            
            conn.commit()
            print("✅ Migraciones v1.1.0 completadas")
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Error en migraciones: {e}")
            raise

def init_production():
    print("Inicializando base de datos de producción...")
    
    if not os.environ.get('DATABASE_URL'):
        print("ERROR: DATABASE_URL no está configurado")
        sys.exit(1)
    
    try:
        db = DatabaseManager()
        print("✓ Base de datos inicializada")
        
        # Ejecutar migraciones
        if USE_POSTGRES:
            run_migrations(db)
        
        # Cargar catálogo (esto también llena laboratorios y monodrogas)
        excel_path = Path(__file__).parent.parent / 'Data' / 'Alfabeta_Febrero.xlsx'
        if not excel_path.exists():
            excel_path = Path(__file__).parent.parent / 'Data' / 'Medicamentos.xlsx'
        
        if excel_path.exists():
            print(f"\nCargando catálogo desde {excel_path.name}...")
            resultado = db.cargar_catalogo_desde_excel(str(excel_path))
            if resultado:
                print("✓ Catálogo cargado (medicamentos, laboratorios y monodrogas sincronizados)")
            else:
                print("⚠ Error al cargar catálogo")
        else:
            print("⚠ Archivo de catálogo no encontrado en Data/")
        
        print("\n✅ Inicialización completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    init_production()
