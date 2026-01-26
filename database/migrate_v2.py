"""
Script de Migración a Versión 2.0
Ejecutar: python database/migrate_v2.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from database.db_manager import DatabaseManager, USE_POSTGRES

def migrar_v2():
    print("=== MIGRACIÓN A VERSIÓN 2.0 ===\n")
    
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        print("1. Migrando tabla CLIENTES...")
        try:
            if USE_POSTGRES:
                cursor.execute("ALTER TABLE clientes ADD COLUMN IF NOT EXISTS organismo_jurisdiccion TEXT")
                cursor.execute("ALTER TABLE clientes ADD COLUMN IF NOT EXISTS provincia TEXT")
                cursor.execute("ALTER TABLE clientes ADD COLUMN IF NOT EXISTS localidad TEXT")
            else:
                cursor.execute("PRAGMA table_info(clientes)")
                columns = [col[1] for col in cursor.fetchall()]
                if 'organismo_jurisdiccion' not in columns:
                    cursor.execute("ALTER TABLE clientes ADD COLUMN organismo_jurisdiccion TEXT")
                if 'provincia' not in columns:
                    cursor.execute("ALTER TABLE clientes ADD COLUMN provincia TEXT")
                if 'localidad' not in columns:
                    cursor.execute("ALTER TABLE clientes ADD COLUMN localidad TEXT")
            print("   ✓ Clientes migrados")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        print("\n2. Migrando tabla LICITACIONES...")
        try:
            if USE_POSTGRES:
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN IF NOT EXISTS portal_origen TEXT")
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN IF NOT EXISTS modalidad_entrega TEXT")
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN IF NOT EXISTS forma_pago TEXT")
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN IF NOT EXISTS requiere_poliza BOOLEAN DEFAULT FALSE")
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN IF NOT EXISTS monto_poliza DECIMAL(15,2)")
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN IF NOT EXISTS observaciones TEXT")
            else:
                cursor.execute("PRAGMA table_info(licitaciones)")
                columns = [col[1] for col in cursor.fetchall()]
                if 'portal_origen' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN portal_origen TEXT")
                if 'modalidad_entrega' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN modalidad_entrega TEXT")
                if 'forma_pago' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN forma_pago TEXT")
                if 'requiere_poliza' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN requiere_poliza INTEGER DEFAULT 0")
                if 'monto_poliza' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN monto_poliza REAL")
                if 'observaciones' not in columns:
                    cursor.execute("ALTER TABLE licitaciones ADD COLUMN observaciones TEXT")
            print("   ✓ Licitaciones migradas")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        print("\n3. Migrando tabla PRODUCTOS...")
        try:
            if USE_POSTGRES:
                cursor.execute("ALTER TABLE productos ADD COLUMN IF NOT EXISTS precio_unitario DECIMAL(15,2)")
                cursor.execute("ALTER TABLE productos ADD COLUMN IF NOT EXISTS total_ofertado DECIMAL(15,2)")
                cursor.execute("ALTER TABLE productos ADD COLUMN IF NOT EXISTS motivo_perdida TEXT")
                cursor.execute("ALTER TABLE productos ADD COLUMN IF NOT EXISTS precio_ganador_unitario DECIMAL(15,2)")
                cursor.execute("ALTER TABLE productos ADD COLUMN IF NOT EXISTS diferencia_pesos DECIMAL(15,2)")
                cursor.execute("ALTER TABLE productos ADD COLUMN IF NOT EXISTS diferencia_porcentaje DECIMAL(10,2)")
                cursor.execute("ALTER TABLE productos ADD COLUMN IF NOT EXISTS costo_unitario DECIMAL(15,2)")
                cursor.execute("ALTER TABLE productos ADD COLUMN IF NOT EXISTS margen_unitario DECIMAL(15,2)")
                cursor.execute("ALTER TABLE productos ADD COLUMN IF NOT EXISTS margen_porcentaje DECIMAL(10,2)")
                cursor.execute("ALTER TABLE productos ADD COLUMN IF NOT EXISTS margen_total DECIMAL(15,2)")
                cursor.execute("ALTER TABLE productos ADD COLUMN IF NOT EXISTS alerta_margen BOOLEAN DEFAULT FALSE")
            else:
                cursor.execute("PRAGMA table_info(productos)")
                columns = [col[1] for col in cursor.fetchall()]
                nuevas_columnas = [
                    ('precio_unitario', 'REAL'),
                    ('total_ofertado', 'REAL'),
                    ('motivo_perdida', 'TEXT'),
                    ('precio_ganador_unitario', 'REAL'),
                    ('diferencia_pesos', 'REAL'),
                    ('diferencia_porcentaje', 'REAL'),
                    ('costo_unitario', 'REAL'),
                    ('margen_unitario', 'REAL'),
                    ('margen_porcentaje', 'REAL'),
                    ('margen_total', 'REAL'),
                    ('alerta_margen', 'INTEGER DEFAULT 0')
                ]
                for col_name, col_type in nuevas_columnas:
                    if col_name not in columns:
                        cursor.execute(f"ALTER TABLE productos ADD COLUMN {col_name} {col_type}")
            print("   ✓ Productos migrados")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        print("\n4. Migrando tabla CELTY (catálogo)...")
        try:
            if USE_POSTGRES:
                cursor.execute("ALTER TABLE celty ADD COLUMN IF NOT EXISTS costo_unitario DECIMAL(15,2)")
            else:
                cursor.execute("PRAGMA table_info(celty)")
                columns = [col[1] for col in cursor.fetchall()]
                if 'costo_unitario' not in columns:
                    cursor.execute("ALTER TABLE celty ADD COLUMN costo_unitario REAL")
            print("   ✓ Catálogo migrado")
        except Exception as e:
            print(f"   ✗ Error: {e}")
        
        print("\n5. Migrando datos existentes...")
        try:
            # Copiar precio_ofertado a precio_unitario si está vacío
            if USE_POSTGRES:
                cursor.execute("UPDATE productos SET precio_unitario = precio_ofertado WHERE precio_unitario IS NULL")
                cursor.execute("UPDATE productos SET total_ofertado = precio_ofertado * cantidad WHERE total_ofertado IS NULL")
            else:
                cursor.execute("UPDATE productos SET precio_unitario = precio_ofertado WHERE precio_unitario IS NULL")
                cursor.execute("UPDATE productos SET total_ofertado = precio_ofertado * cantidad WHERE total_ofertado IS NULL")
            print("   ✓ Datos migrados")
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    print("\n=== MIGRACIÓN COMPLETADA ===")
    print("\nNOTA: Los nuevos campos están disponibles pero vacíos.")
    print("Deberás completarlos manualmente en las nuevas licitaciones.")

if __name__ == "__main__":
    respuesta = input("¿Deseas ejecutar la migración a v2.0? (s/n): ")
    if respuesta.lower() == 's':
        migrar_v2()
    else:
        print("Migración cancelada")
