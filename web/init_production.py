#!/usr/bin/env python
"""
Script de inicialización para producción
Carga el catálogo Celty en PostgreSQL
"""
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from database.db_manager import DatabaseManager

def init_production():
    print("Inicializando base de datos de producción...")
    
    # Verificar que DATABASE_URL esté configurado
    if not os.environ.get('DATABASE_URL'):
        print("ERROR: DATABASE_URL no está configurado")
        sys.exit(1)
    
    try:
        db = DatabaseManager()
        print("✓ Base de datos inicializada")
        
        # Cargar catálogo si existe el archivo
        if os.path.exists('../Data/Celty.xlsx'):
            print("Cargando catálogo desde Excel...")
            db.cargar_catalogo_desde_excel('../Data/Celty.xlsx')
            print("✓ Catálogo cargado")
        else:
            print("⚠ Archivo Celty.xlsx no encontrado, omitiendo carga de catálogo")
        
        print("\n✓ Inicialización completada exitosamente")
        
    except Exception as e:
        print(f"✗ Error durante la inicialización: {e}")
        sys.exit(1)

if __name__ == '__main__':
    init_production()
