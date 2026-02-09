#!/usr/bin/env python3
"""
Script para importar medicamentos desde el archivo Alfabeta_Febrero.xlsx
a la tabla medicamentos de la base de datos.

Uso: python import_medicamentos_alfabeta.py [--clean] [--excel-path PATH]

Opciones:
    --clean: Vaciar la tabla medicamentos antes de importar
    --excel-path: Ruta al archivo Excel (por defecto: Data/Alfabeta_Febrero.xlsx)
"""

import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime

# Agregar ruta del proyecto
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.database.db_manager import DatabaseManager
from shared.database.connection_pool import USE_POSTGRES

def importar_medicamentos(excel_path="Data/Alfabeta_Febrero.xlsx", clean=False):
    """
    Importa medicamentos desde Excel a la tabla medicamentos.
    
    Args:
        excel_path (str): Ruta al archivo Excel
        clean (bool): Si True, vacía la tabla antes de importar
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
        
        # Mostrar las columnas encontradas
        print(f"Columnas: {list(df.columns)}")
        
        # Inicializar DatabaseManager
        db = DatabaseManager()
        
        # Limpiar tabla si está especificado
        if clean:
            print("Limpiando tabla medicamentos...")
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM medicamentos")
                conn.commit()
            print("Tabla medicamentos vaciada")
        
        # Preparar datos para inserción
        total_insertados = 0
        total_actualizados = 0
        total_errores = 0
        
        print("\nImportando medicamentos...")
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            for idx, row in df.iterrows():
                try:
                    # Mapear columnas del Excel a campos de BD
                    numero_registro = str(row.get('N de Registro', '')) if pd.notna(row.get('N de Registro')) else None
                    
                    if not numero_registro:
                        print(f"WARN - Fila {idx+2}: N de Registro vacio, saltando...")
                        continue
                    
                    # Preparar datos
                    datos = {
                        'numero_registro': numero_registro,
                        'troquel': str(row.get('Troquel', '')) if pd.notna(row.get('Troquel')) else None,
                        'cod_ab': int(row['Cod AB']) if pd.notna(row.get('Cod AB')) else None,
                        'troquel_ean': str(row.get('Troquel.1', '')) if pd.notna(row.get('Troquel.1')) else None,
                        'fecha': str(row['Fecha'].date()) if pd.notna(row.get('Fecha')) else datetime.now().strftime('%Y-%m-%d'),
                        'cod_monodroga': int(row['Cod Monodroga']) if pd.notna(row.get('Cod Monodroga')) else None,
                        'monodroga': str(row.get('Monodroga', '')) if pd.notna(row.get('Monodroga')) else '',
                        'cod_laboratorio': int(row['Cod Laboratorio']) if pd.notna(row.get('Cod Laboratorio')) else None,
                        'laboratorio': str(row.get('Laboratorio', '')) if pd.notna(row.get('Laboratorio')) else '',
                        'marca': str(row.get('Marca', '')) if pd.notna(row.get('Marca')) else '',
                        'presentacion': str(row.get('Presentacion', '')) if pd.notna(row.get('Presentacion')) else '',
                        'multidosis': int(row['Multidosis']) if pd.notna(row.get('Multidosis')) else None,
                        'precio_caja': float(row['Precio x caja']) if pd.notna(row.get('Precio x caja')) else None,
                        'precio_unitario': float(row['Precio unitario']) if pd.notna(row.get('Precio unitario')) else None,
                    }
                    
                    # Verificar si el registro ya existe
                    if USE_POSTGRES:
                        cursor.execute("SELECT id FROM medicamentos WHERE numero_registro = %s", (numero_registro,))
                    else:
                        cursor.execute("SELECT id FROM medicamentos WHERE numero_registro = ?", (numero_registro,))
                    
                    existing = cursor.fetchone()
                    
                    if existing:
                        # Actualizar registro existente
                        if USE_POSTGRES:
                            cursor.execute("""
                                UPDATE medicamentos SET 
                                troquel=%s, cod_ab=%s, troquel_ean=%s, fecha=%s,
                                cod_monodroga=%s, monodroga=%s, cod_laboratorio=%s, laboratorio=%s,
                                marca=%s, presentacion=%s, multidosis=%s, precio_caja=%s, precio_unitario=%s
                                WHERE numero_registro=%s
                            """, (
                                datos['troquel'], datos['cod_ab'], datos['troquel_ean'], datos['fecha'],
                                datos['cod_monodroga'], datos['monodroga'], datos['cod_laboratorio'], datos['laboratorio'],
                                datos['marca'], datos['presentacion'], datos['multidosis'], 
                                datos['precio_caja'], datos['precio_unitario'], numero_registro
                            ))
                        else:
                            cursor.execute("""
                                UPDATE medicamentos SET 
                                troquel=?, cod_ab=?, troquel_ean=?, fecha=?,
                                cod_monodroga=?, monodroga=?, cod_laboratorio=?, laboratorio=?,
                                marca=?, presentacion=?, multidosis=?, precio_caja=?, precio_unitario=?
                                WHERE numero_registro=?
                            """, (
                                datos['troquel'], datos['cod_ab'], datos['troquel_ean'], datos['fecha'],
                                datos['cod_monodroga'], datos['monodroga'], datos['cod_laboratorio'], datos['laboratorio'],
                                datos['marca'], datos['presentacion'], datos['multidosis'],
                                datos['precio_caja'], datos['precio_unitario'], numero_registro
                            ))
                        total_actualizados += 1
                    else:
                        # Insertar nuevo registro
                        if USE_POSTGRES:
                            cursor.execute("""
                                INSERT INTO medicamentos (numero_registro, troquel, cod_ab, troquel_ean, fecha,
                                cod_monodroga, monodroga, cod_laboratorio, laboratorio, marca, presentacion,
                                multidosis, precio_caja, precio_unitario)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (
                                numero_registro, datos['troquel'], datos['cod_ab'], datos['troquel_ean'],
                                datos['fecha'], datos['cod_monodroga'], datos['monodroga'],
                                datos['cod_laboratorio'], datos['laboratorio'], datos['marca'],
                                datos['presentacion'], datos['multidosis'], datos['precio_caja'],
                                datos['precio_unitario']
                            ))
                        else:
                            cursor.execute("""
                                INSERT INTO medicamentos (numero_registro, troquel, cod_ab, troquel_ean, fecha,
                                cod_monodroga, monodroga, cod_laboratorio, laboratorio, marca, presentacion,
                                multidosis, precio_caja, precio_unitario)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                numero_registro, datos['troquel'], datos['cod_ab'], datos['troquel_ean'],
                                datos['fecha'], datos['cod_monodroga'], datos['monodroga'],
                                datos['cod_laboratorio'], datos['laboratorio'], datos['marca'],
                                datos['presentacion'], datos['multidosis'], datos['precio_caja'],
                                datos['precio_unitario']
                            ))
                        total_insertados += 1
                    
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
        print("RESUMEN DE IMPORTACION")
        print("="*50)
        print(f"Insertados: {total_insertados}")
        print(f"Actualizados: {total_actualizados}")
        if total_errores > 0:
            print(f"Errores: {total_errores}")
        print(f"Total procesados: {total_insertados + total_actualizados}")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"ERROR durante la importacion: {str(e)}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Importar medicamentos desde Excel a la BD")
    parser.add_argument('--clean', action='store_true', help='Vaciar tabla antes de importar')
    parser.add_argument('--excel-path', default='Data/Alfabeta_Febrero.xlsx', 
                       help='Ruta al archivo Excel')
    
    args = parser.parse_args()
    
    success = importar_medicamentos(excel_path=args.excel_path, clean=args.clean)
    sys.exit(0 if success else 1)
