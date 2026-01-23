import sqlite3
import os

# Backup de la base de datos actual
db_path = "database/licitaciones.db"
if os.path.exists(db_path):
    backup_path = "database/licitaciones_backup.db"
    import shutil
    shutil.copy2(db_path, backup_path)
    print(f"Backup creado: {backup_path}")
    
    # Eliminar base de datos actual
    os.remove(db_path)
    print(f"Base de datos eliminada: {db_path}")

# Crear nueva base de datos con schema actualizado
from database.db_manager import DatabaseManager
db = DatabaseManager()
print("Nueva base de datos creada con schema actualizado")
print("Campos actualizados:")
print("  - laboratorio_ganador -> oferente_ganador")
print("  - Agregado: marca_ofrecida")
