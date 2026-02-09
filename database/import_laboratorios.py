#!/usr/bin/env python
"""
Script para importar laboratorios desde Laboratorio.xlsx a la base de datos
"""

import sqlite3
import os
import sys
from pathlib import Path

try:
    import pandas as pd
    import openpyxl
except ImportError:
    print("Instalando dependencias...")
    os.system("pip install pandas openpyxl")
    import pandas as pd
    import openpyxl

# Obtener la ruta de la base de datos
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / 'database' / 'licitaciones.db'
EXCEL_PATH = BASE_DIR / 'Data' / 'Laboratorio.xlsx'

def import_laboratorios():
    """Importa laboratorios desde el archivo Excel a la base de datos"""
    
    if not EXCEL_PATH.exists():
        print(f"❌ Error: No se encontró el archivo {EXCEL_PATH}")
        return False
    
    if not DB_PATH.exists():
        print(f"❌ Error: No se encontró la base de datos {DB_PATH}")
        return False
    
    try:
        # Leer el Excel
        print(f"📄 Leyendo archivo Excel: {EXCEL_PATH}")
        df = pd.read_excel(EXCEL_PATH)
        
        print(f"   Columnas encontradas: {list(df.columns)}")
        print(f"   Total de laboratorios: {len(df)}")
        
        # Renombrar columnas para que coincidan con la estructura esperada
        # Esperamos: 'Cod Laboratorio' y 'Laboratorio'
        df.columns = [col.strip() for col in df.columns]
        
        if 'Cod Laboratorio' not in df.columns:
            print("❌ Error: No se encontró la columna 'Cod Laboratorio'")
            return False
        
        if 'Laboratorio' not in df.columns:
            print("❌ Error: No se encontró la columna 'Laboratorio'")
            return False
        
        # Conectar a la base de datos
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Limpiar tabla existente (opcional, comentar si no se desea)
        print("\n🗑️  Limpiando tabla laboratorios existente...")
        cursor.execute("DELETE FROM laboratorios")
        
        # Insertar datos
        print("💾 Importando laboratorios...")
        inserted = 0
        errors = 0
        
        for idx, row in df.iterrows():
            try:
                cod = str(row['Cod Laboratorio']).strip()
                laboratorio = str(row['Laboratorio']).strip()
                
                # Validar datos no vacíos
                if not cod or cod == 'nan':
                    continue
                if not laboratorio or laboratorio == 'nan':
                    continue
                
                cursor.execute(
                    "INSERT INTO laboratorios (cod, laboratorio) VALUES (?, ?)",
                    (cod, laboratorio)
                )
                inserted += 1
                
                if inserted % 10 == 0:
                    print(f"   ✓ {inserted} registros insertados...")
                    
            except Exception as e:
                errors += 1
                print(f"   ❌ Error en fila {idx + 2}: {e}")
        
        # Confirmar cambios
        conn.commit()
        conn.close()
        
        print(f"\n✅ Importación completada:")
        print(f"   - Registros insertados: {inserted}")
        print(f"   - Errores: {errors}")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la importación: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("IMPORTADOR DE LABORATORIOS")
    print("=" * 60)
    
    success = import_laboratorios()
    
    if success:
        print("\n✅ Los laboratorios fueron importados exitosamente")
        sys.exit(0)
    else:
        print("\n❌ Hubo errores durante la importación")
        sys.exit(1)
