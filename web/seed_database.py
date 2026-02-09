"""Script para cargar datos iniciales si la BD está vacía"""
import os
import sys
import gzip
import subprocess
from pathlib import Path

# Agregar directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def seed_database():
    """Carga datos iniciales si la base de datos está vacía"""
    try:
        # Verificar si hay medicamentos
        from shared.database.db_manager import DatabaseManager
        db = DatabaseManager()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM medicamentos")
            count = cursor.fetchone()[0]
            
            if count > 0:
                print(f"✓ Base de datos ya tiene {count} medicamentos")
                return
        
        print("Base de datos vacía, cargando datos iniciales...")
        
        # Descomprimir y ejecutar SQL
        seed_file = Path(__file__).parent.parent / "Data" / "medicamentos_seed.sql.gz"
        
        if not seed_file.exists():
            print("⚠ Archivo de seed no encontrado")
            return
        
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("⚠ DATABASE_URL no configurado")
            return
        
        # Descomprimir y ejecutar
        with gzip.open(seed_file, 'rt', encoding='utf-8') as f:
            sql_content = f.read()
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            # Ejecutar en lotes para evitar timeout
            statements = sql_content.split(';')
            total = len(statements)
            
            for i, statement in enumerate(statements):
                if statement.strip():
                    try:
                        cursor.execute(statement)
                        if i % 1000 == 0:
                            conn.commit()
                            print(f"Procesado {i}/{total} statements...")
                    except Exception as e:
                        print(f"Error en statement {i}: {e}")
                        continue
            
            conn.commit()
        
        # Verificar
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM medicamentos")
            count = cursor.fetchone()[0]
            print(f"✓ Cargados {count} medicamentos exitosamente")
    
    except Exception as e:
        print(f"Error cargando seed: {e}")

if __name__ == '__main__':
    seed_database()
