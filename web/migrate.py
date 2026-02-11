"""Script de migraciones automáticas v1.1.0"""
import sys
from pathlib import Path
from psycopg import sql

sys.path.insert(0, str(Path(__file__).parent.parent))
from shared.database.db_manager import DatabaseManager
from shared.database.connection_pool import USE_POSTGRES

def ejecutar_migraciones():
    """Ejecuta migraciones necesarias para v1.1.0"""
    db = DatabaseManager()
    
    if not USE_POSTGRES:
        print("Migraciones solo necesarias en PostgreSQL")
        return
    
    print("Ejecutando migraciones v1.1.0...")
    
    try:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Costo unitario en productos
            try:
                cursor.execute("ALTER TABLE productos ADD COLUMN costo_unitario REAL")
                conn.commit()
                print("✓ Agregada columna costo_unitario a productos")
            except Exception:
                print("- costo_unitario ya existe en productos")
            
            # Portales origen
            try:
                cursor.execute("CREATE TABLE portales_origen (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Comprar', 'BAC', 'Otro']:
                    cursor.execute("INSERT INTO portales_origen (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ Tabla portales_origen creada")
            except Exception:
                print("- portales_origen ya existe")
            
            # Modalidades entrega
            try:
                cursor.execute("CREATE TABLE modalidades_entrega (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Única', 'Múltiple', 'Programada']:
                    cursor.execute("INSERT INTO modalidades_entrega (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ Tabla modalidades_entrega creada")
            except Exception:
                print("- modalidades_entrega ya existe")
            
            # Formas pago
            try:
                cursor.execute("CREATE TABLE formas_pago (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Contado', '30 días', '60 días']:
                    cursor.execute("INSERT INTO formas_pago (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ Tabla formas_pago creada")
            except Exception:
                print("- formas_pago ya existe")
            
            # Organismos jurisdicción
            try:
                cursor.execute("CREATE TABLE organismos_jurisdiccion (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Nacional', 'Provincial', 'Municipal', 'CABA', 'Privado']:
                    cursor.execute("INSERT INTO organismos_jurisdiccion (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ Tabla organismos_jurisdiccion creada")
            except Exception:
                print("- organismos_jurisdiccion ya existe")
            
            # Motivos pérdida
            try:
                cursor.execute("CREATE TABLE motivos_perdida (id SERIAL PRIMARY KEY, nombre TEXT UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE)")
                for v in ['Precio más alto', 'Marca no priorizada', 'No cumplía especificación', 'Error administrativo', 'Otro']:
                    cursor.execute("INSERT INTO motivos_perdida (nombre) VALUES (%s)", (v,))
                conn.commit()
                print("✓ Tabla motivos_perdida creada")
            except Exception:
                print("- motivos_perdida ya existe")
            
            # Columnas en licitaciones
            columnas_licitaciones = ['portal_origen', 'modalidad_entrega', 'forma_pago', 'observaciones']
            for col in columnas_licitaciones:
                try:
                    query = sql.SQL("ALTER TABLE licitaciones ADD COLUMN {} TEXT").format(sql.Identifier(col))
                    cursor.execute(query)
                    conn.commit()
                    print(f"✓ Agregada columna {col}")
                except Exception:
                    print(f"- {col} ya existe")
            
            try:
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN requiere_poliza BOOLEAN")
                conn.commit()
                print("✓ Agregada columna requiere_poliza")
            except Exception:
                print("- requiere_poliza ya existe")
            
            try:
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN monto_poliza REAL")
                conn.commit()
                print("✓ Agregada columna monto_poliza")
            except Exception:
                print("- monto_poliza ya existe")
            
            try:
                cursor.execute("ALTER TABLE licitaciones ADD COLUMN tipo_licitacion_id INTEGER")
                conn.commit()
                print("✓ Agregada columna tipo_licitacion_id")
            except Exception:
                print("- tipo_licitacion_id ya existe")
            
            # Columnas en clientes
            try:
                cursor.execute("ALTER TABLE clientes ADD COLUMN organismo_jurisdiccion TEXT")
                conn.commit()
                print("✓ Agregada columna organismo_jurisdiccion")
            except Exception:
                print("- organismo_jurisdiccion ya existe")
            
            # Columnas en productos
            try:
                cursor.execute("ALTER TABLE productos ADD COLUMN motivo_perdida TEXT")
                conn.commit()
                print("✓ Agregada columna motivo_perdida")
            except Exception:
                print("- motivo_perdida ya existe")
            
            try:
                cursor.execute("ALTER TABLE productos ADD COLUMN producto_cotizar TEXT DEFAULT 'principal'")
                conn.commit()
                print("✓ Agregada columna producto_cotizar")
            except Exception:
                print("- producto_cotizar ya existe")
        
        print("\n✅ Migraciones completadas exitosamente")
    except Exception as e:
        print(f"\n❌ Error en migraciones: {e}")

if __name__ == '__main__':
    ejecutar_migraciones()
