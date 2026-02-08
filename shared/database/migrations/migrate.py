import sqlite3
from pathlib import Path

class MigrationManager:
    """Gestor de migraciones de base de datos"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.migrations_dir = Path(__file__).parent
        
    def init_migrations_table(self):
        """Crea tabla de control de migraciones"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def get_applied_migrations(self):
        """Obtiene migraciones ya aplicadas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT version FROM schema_migrations ORDER BY version')
        versions = [row[0] for row in cursor.fetchall()]
        conn.close()
        return versions
    
    def get_pending_migrations(self):
        """Obtiene migraciones pendientes"""
        applied = set(self.get_applied_migrations())
        all_migrations = sorted([
            int(f.stem.split('_')[0])
            for f in self.migrations_dir.glob('[0-9]*.sql')
        ])
        return [v for v in all_migrations if v not in applied]
    
    def apply_migration(self, version):
        """Aplica una migración específica"""
        files = list(self.migrations_dir.glob(f"{version:03d}_*.sql"))
        
        if not files:
            raise FileNotFoundError(f"Migración {version} no encontrada")
        
        with open(files[0], 'r', encoding='utf-8') as f:
            sql = f.read()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.executescript(sql)
            cursor.execute(
                'INSERT INTO schema_migrations (version) VALUES (?)',
                (version,)
            )
            conn.commit()
            print(f"✓ Migración {version} aplicada")
        except Exception as e:
            conn.rollback()
            print(f"✗ Error en migración {version}: {e}")
            raise
        finally:
            conn.close()
    
    def migrate(self):
        """Aplica todas las migraciones pendientes"""
        self.init_migrations_table()
        pending = self.get_pending_migrations()
        
        if not pending:
            print("✓ Base de datos actualizada")
            return
        
        print(f"Aplicando {len(pending)} migraciones...")
        for version in pending:
            self.apply_migration(version)
        
        print("✓ Todas las migraciones aplicadas")

if __name__ == '__main__':
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else '../licitaciones.db'
    manager = MigrationManager(db_path)
    manager.migrate()
