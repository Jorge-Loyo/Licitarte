"""Script para ejecutar todas las migraciones pendientes"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.database.migrations.migrate import MigrationManager

def run_all_migrations():
    """Ejecuta todas las migraciones pendientes"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'licitaciones.db')
    db_path = os.path.abspath(db_path)
    
    print(f"Base de datos: {db_path}")
    manager = MigrationManager(db_path)
    manager.migrate()

if __name__ == '__main__':
    run_all_migrations()
