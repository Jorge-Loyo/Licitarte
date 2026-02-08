"""Script de migraciones automáticas v1.1.0"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from shared.database.db_manager import DatabaseManager, USE_POSTGRES

def ejecutar_migraciones():
    """Ejecuta migraciones necesarias para v1.1.0"""
    db = DatabaseManager(os.path.abspath('../shared/database/licitaciones.db'))
    
    if not USE_POSTGRES:
        print("Migraciones solo necesarias en PostgreSQL")
        return
    
    print("Ejecutando migraciones v1.1.0...")
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Costo unitario en catálogo
            try:
                cursor.execute("ALTER TABLE celty ADD COLUMN costo_unitario REAL")
                conn.commit()
                print("✓ Agregada columna costo_unitario")
            except:
                print("- costo_unitario ya existe")
            
            # Portales origen
            try:
                cursor.execute("CREATE TABLE portales_origen (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Comprar', 'BAC', 'Otro']:
                    cursor.execute("INSERT INTO portales_origen (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ Tabla portales_origen creada")
            except:
                print("- portales_origen ya existe")
            
            # Modalidades entrega
            try:
                cursor.execute("CREATE TABLE modalidades_entrega (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Única', 'Múltiple', 'Programada']:
                    cursor.execute("INSERT INTO modalidades_entrega (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ Tabla modalidades_entrega creada")
            except:
                print("- modalidades_entrega ya existe")
            
            # Formas pago
            try:
                cursor.execute("CREATE TABLE formas_pago (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Contado', '30 días', '60 días']:
                    cursor.execute("INSERT INTO formas_pago (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ Tabla formas_pago creada")
            except:
                print("- formas_pago ya existe")
            
            # Organismos jurisdicción
            try:
                cursor.execute("CREATE TABLE organismos_jurisdiccion (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Nacional', 'Provincial', 'Municipal', 'CABA', 'Privado']:
                    cursor.execute("INSERT INTO organismos_jurisdiccion (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ Tabla organismos_jurisdiccion creada")
            except:
                print("- organismos_jurisdiccion ya existe")
            
            # Motivos pérdida
            try:
                cursor.execute("CREATE TABLE motivos_perdida (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Precio más alto', 'Marca no priorizada', 'No cumplía especificación', 'Error administrativo', 'Otro']:
                    cursor.execute("INSERT INTO motivos_perdida (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ Tabla motivos_perdida creada")
            except:
                print("- motivos_perdida ya existe")
            
            # Columnas en licitaciones
            for col in ['portal_origen', 'modalidad_entrega', 'forma_pago', 'observaciones']:
                try:
                    cursor.execute(f"ALTER TABLE licitaciones ADD COLUMN {col} TEXT")
                    conn.commit()
                    print(f"✓ Agregada columna {col}")
                except:
                    print(f"- {col} ya existe")
            
            try:
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN requiere_poliza BOOLEAN")
                conn.commit()
                print("✓ Agregada columna requiere_poliza")
            except:
                print("- requiere_poliza ya existe")
            
            try:
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN monto_poliza REAL")
                conn.commit()
                print("✓ Agregada columna monto_poliza")
            except:
                print("- monto_poliza ya existe")
            
            try:
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN tipo_licitacion_id INTEGER")
                conn.commit()
                print("✓ Agregada columna tipo_licitacion_id")
            except:
                print("- tipo_licitacion_id ya existe")
            
            # Columnas en clientes
            try:
                cursor.execute("ALTER TABLE clientes ADD COLUMN organismo_jurisdiccion TEXT")
                conn.commit()
                print("✓ Agregada columna organismo_jurisdiccion")
            except:
                print("- organismo_jurisdiccion ya existe")
            
            # Columnas en productos
            try:
                cursor.execute("ALTER TABLE productos ADD COLUMN motivo_perdida TEXT")
                conn.commit()
                print("✓ Agregada columna motivo_perdida")
            except:
                print("- motivo_perdida ya existe")
            
            try:
                cursor.execute("ALTER TABLE productos ADD COLUMN producto_cotizar TEXT DEFAULT 'principal'")
                conn.commit()
                print("✓ Agregada columna producto_cotizar")
            except:
                print("- producto_cotizar ya existe")
        
        print("\n✅ Migraciones completadas exitosamente")
    except Exception as e:
        print(f"\n❌ Error en migraciones: {e}")

if __name__ == '__main__':
    ejecutar_migraciones()
