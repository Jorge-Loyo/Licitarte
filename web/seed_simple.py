"""Seed simple con datos de prueba"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.database.db_manager import DatabaseManager

# Datos de prueba mínimos
LABORATORIOS = [
    (1, '1', 'Abbott', 'Abbott'),
    (2, '2', 'Geminis', 'Geminis'),
    (3, '4', 'Roemmers', 'Roemmers'),
]

MONODROGAS = [
    (1, 'PARACETAMOL', 'Paracetamol'),
    (2, 'IBUPROFENO', 'Ibuprofeno'),
    (3, 'AMOXICILINA', 'Amoxicilina'),
]

MEDICAMENTOS = [
    (1, '12345', 'REG001', 1, 1, 'TAFIROL 500MG', 'Comprimidos x 20', False, 150.00, 180.00, 200.00, 220.00, 250.00, None),
    (2, '12346', 'REG002', 2, 2, 'IBUPIRAC 400MG', 'Comprimidos x 30', False, 200.00, 240.00, 280.00, 320.00, 350.00, None),
    (3, '12347', 'REG003', 3, 3, 'AMOXIDAL 500MG', 'Cápsulas x 16', False, 300.00, 360.00, 420.00, 480.00, 550.00, None),
]

def seed():
    try:
        db = DatabaseManager()
        with db.get_connection() as conn:
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Verificar si ya hay datos
            cursor.execute("SELECT COUNT(*) FROM medicamentos")
            if cursor.fetchone()[0] > 0:
                print("✓ Ya hay datos en la BD")
                return
            
            print("Cargando datos de prueba...")
            
            # Laboratorios
            for lab in LABORATORIOS:
                try:
                    cursor.execute(
                        "INSERT INTO laboratorios (id, cod, laboratorio, nombre, activo) VALUES (%s, %s, %s, %s, true)",
                        lab
                    )
                except:
                    pass
            
            # Monodrogas
            for mono in MONODROGAS:
                try:
                    cursor.execute(
                        "INSERT INTO monodrogas (id, monodroga, nombre, activo) VALUES (%s, %s, %s, true)",
                        mono
                    )
                except:
                    pass
            
            # Medicamentos
            for med in MEDICAMENTOS:
                try:
                    cursor.execute(
                        """INSERT INTO medicamentos 
                        (id, troquel, cod_ab, numero_registro, monodroga_id, laboratorio_id, marca, presentacion, 
                        multidosis, precio_alfabeta, precio_kairos, precio_vademecum, precio_msd, precio_alfabeta_iva, observaciones)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        med
                    )
                except:
                    pass
            
            cursor.execute("SELECT COUNT(*) FROM medicamentos")
            count = cursor.fetchone()[0]
            print(f"✓ Cargados {count} medicamentos de prueba")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    seed()
