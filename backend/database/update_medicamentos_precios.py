#!/usr/bin/env python3
"""
Script para actualizar precios de medicamentos desde un nuevo archivo Excel.

Este script es util para importaciones recurrentes cuando solo cambian los precios
pero la estructura de medicamentos permanece igual.

Uso: python update_medicamentos_precios.py [--excel-path PATH]

Opciones:
    --excel-path: Ruta al archivo Excel (por defecto: Data/Alfabeta_Febrero.xlsx)
"""

import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime

# Agregar ruta del proyecto
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.database.db_manager import DatabaseManager
from backend.database.connection_pool import USE_POSTGRES

def actualizar_precios_medicamentos(excel_path="Data/Alfabeta_Febrero.xlsx"):
    """
    Actualiza solo los precios de medicamentos desde un archivo Excel.
    
    Este script:
    1. Lee los precios del archivo Excel
    2. Busca el medicamento por numero de registro
    3. Actualiza los campos: precio_caja, precio_unitario, multidosis, troquel, fecha
    4. No inserta nuevos registros (solo actualiza existentes)
    
    Args:
        excel_path (str): Ruta al archivo Excel
    """
    
    # Verificar que el archivo Excel existe
    if not os.path.exists(excel_path):
        print(f"ERROR: El archivo {excel_path} no existe")
        return False
    
    print(f"Leyendo archivo Excel: {excel_path}")
    
    try:
        # Leer el Excel
        df = pd.read_excel(excel_path)
        print(f"Se encontraron {len(df)} registros en el Excel")
        
        # Inicializar DatabaseManager
        db = DatabaseManager()
        
        # Contadores
        total_actualizados = 0
        total_no_encontrados = 0
        total_errores = 0
        
        print("\nActualizando precios...")
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            for idx, row in df.iterrows():
                try:
                    # Mapear numero de registro
                    numero_registro = str(row.get('N de Registro', '')) if pd.notna(row.get('N de Registro')) else None
                    
                    if not numero_registro:
                        print(f"WARN - Fila {idx+2}: N de Registro vacio, saltando...")
                        continue
                    
                    # Preparar datos de precios
                    precio_caja = float(row['Precio x caja']) if pd.notna(row.get('Precio x caja')) else None
                    precio_unitario = float(row['Precio unitario']) if pd.notna(row.get('Precio unitario')) else None
                    multidosis = int(row['Multidosis']) if pd.notna(row.get('Multidosis')) else None
                    troquel = str(row.get('Troquel', '')) if pd.notna(row.get('Troquel')) else None
                    fecha = str(row['Fecha'].date()) if pd.notna(row.get('Fecha')) else datetime.now().strftime('%Y-%m-%d')
                    
                    # Verificar si el registro existe
                    if USE_POSTGRES:
                        cursor.execute("SELECT id FROM medicamentos WHERE numero_registro = %s", (numero_registro,))
                    else:
                        cursor.execute("SELECT id FROM medicamentos WHERE numero_registro = ?", (numero_registro,))
                    
                    existing = cursor.fetchone()
                    
                    if existing:
                        # Actualizar solo precios y fecha
                        if USE_POSTGRES:
                            cursor.execute("""
                                UPDATE medicamentos SET 
                                precio_caja=%s, precio_unitario=%s, multidosis=%s, 
                                troquel=%s, fecha=%s
                                WHERE numero_registro=%s
                            """, (
                                precio_caja, precio_unitario, multidosis,
                                troquel, fecha, numero_registro
                            ))
                        else:
                            cursor.execute("""
                                UPDATE medicamentos SET 
                                precio_caja=?, precio_unitario=?, multidosis=?, 
                                troquel=?, fecha=?
                                WHERE numero_registro=?
                            """, (
                                precio_caja, precio_unitario, multidosis,
                                troquel, fecha, numero_registro
                            ))
                        total_actualizados += 1
                    else:
                        print(f"WARN - Fila {idx+2}: Medicamento '{numero_registro}' no encontrado en BD")
                        total_no_encontrados += 1
                    
                    # Mostrar progreso cada 100 registros
                    if (idx + 1) % 100 == 0:
                        print(f"Procesados {idx + 1}/{len(df)} registros...")
                    
                except Exception as e:
                    print(f"ERROR en fila {idx+2}: {str(e)}")
                    total_errores += 1
                    continue
            
            # Confirmar cambios
            conn.commit()
        
        # Resumen
        print("\n" + "="*50)
        print("RESUMEN DE ACTUALIZACION DE PRECIOS")
        print("="*50)
        print(f"Actualizados: {total_actualizados}")
        if total_no_encontrados > 0:
            print(f"No encontrados: {total_no_encontrados}")
        if total_errores > 0:
            print(f"Errores: {total_errores}")
        print(f"Total procesados: {total_actualizados + total_no_encontrados + total_errores}")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"ERROR durante la actualizacion: {str(e)}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Actualizar precios de medicamentos desde Excel")
    parser.add_argument('--excel-path', default='Data/Alfabeta_Febrero.xlsx', 
                       help='Ruta al archivo Excel')
    
    args = parser.parse_args()
    
    success = actualizar_precios_medicamentos(excel_path=args.excel_path)
    sys.exit(0 if success else 1)
