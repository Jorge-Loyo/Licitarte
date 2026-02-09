#!/usr/bin/env python
"""
Script para crear tabla laboratorios en PostgreSQL y importar datos desde Excel
"""

import os
import sys
from pathlib import Path

try:
    import pandas as pd
    import psycopg2
    from psycopg2.extras import execute_values
except ImportError:
    print("Instalando dependencias...")
    os.system("pip install pandas psycopg2-binary openpyxl")
    import pandas as pd
    import psycopg2
    from psycopg2.extras import execute_values

# Configuración de conexión PostgreSQL desde .env
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'licitarte123'),
    'database': os.environ.get('DB_NAME', 'licitarte')
}

BASE_DIR = Path(__file__).parent.parent
EXCEL_PATH = BASE_DIR / 'Data' / 'Laboratorio.xlsx'

def create_table(conn):
    """Crea la tabla laboratorios en PostgreSQL"""
    cursor = conn.cursor()
    
    try:
        # Crear tabla
        create_sql = """
        CREATE TABLE IF NOT EXISTS laboratorios (
            id SERIAL PRIMARY KEY,
            cod VARCHAR(50) NOT NULL,
            laboratorio VARCHAR(255) NOT NULL,
            UNIQUE(cod)
        );
        """
        cursor.execute(create_sql)
        
        # Crear índice
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_laboratorio_cod 
        ON laboratorios(cod);
        """)
        
        conn.commit()
        print("✅ Tabla 'laboratorios' creada exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error al crear tabla: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def import_data(conn):
    """Importa datos desde Excel a la tabla laboratorios"""
    
    if not EXCEL_PATH.exists():
        print(f"❌ Error: No se encontró el archivo {EXCEL_PATH}")
        return False
    
    try:
        # Leer Excel
        print(f"📄 Leyendo archivo Excel: {EXCEL_PATH}")
        df = pd.read_excel(EXCEL_PATH)
        
        # Limpiar nombres de columnas
        df.columns = [col.strip() for col in df.columns]
        
        print(f"   Columnas encontradas: {list(df.columns)}")
        print(f"   Total de laboratorios: {len(df)}")
        
        # Validar columnas
        if 'Cod Laboratorio' not in df.columns or 'Laboratorio' not in df.columns:
            print("❌ Error: No se encontraron las columnas esperadas")
            return False
        
        # Preparar datos
        data = []
        for idx, row in df.iterrows():
            cod = str(row['Cod Laboratorio']).strip()
            laboratorio = str(row['Laboratorio']).strip()
            
            # Validar datos no vacíos
            if cod and cod != 'nan' and laboratorio and laboratorio != 'nan':
                data.append((cod, laboratorio))
        
        # Limpiar tabla existente
        cursor = conn.cursor()
        print("\n🗑️  Limpiando tabla laboratorios existente...")
        cursor.execute("TRUNCATE TABLE laboratorios")
        conn.commit()
        
        # Insertar datos en lotes
        print("💾 Importando laboratorios...")
        batch_size = 100
        inserted = 0
        
        try:
            for i in range(0, len(data), batch_size):
                batch = data[i:i+batch_size]
                execute_values(
                    cursor,
                    "INSERT INTO laboratorios (cod, laboratorio) VALUES %s",
                    batch,
                    page_size=batch_size
                )
                conn.commit()
                inserted += len(batch)
                
                if inserted % 100 == 0:
                    print(f"   ✓ {inserted} registros insertados...")
            
            print(f"\n✅ Importación completada:")
            print(f"   - Registros insertados: {inserted}")
            print(f"   - Total leído: {len(df)}")
            return True
            
        except Exception as e:
            print(f"❌ Error durante la inserción: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            
    except Exception as e:
        print(f"❌ Error durante la importación: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("IMPORTADOR DE LABORATORIOS - POSTGRESQL")
    print("=" * 60)
    print(f"\nConexión: {DB_CONFIG['user']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}\n")
    
    try:
        # Conectar a la base de datos
        print("📡 Conectando a PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Conexión exitosa\n")
        
        # Crear tabla
        if not create_table(conn):
            return False
        
        # Importar datos
        print()
        if not import_data(conn):
            return False
        
        conn.close()
        print("\n✅ Todas las operaciones completadas exitosamente")
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error de base de datos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
