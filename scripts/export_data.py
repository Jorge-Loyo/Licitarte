"""Script para exportar datos de PostgreSQL local a SQL"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.database.db_manager import DatabaseManager

def export_to_sql():
    """Exporta medicamentos, laboratorios y monodrogas a archivo SQL"""
    db = DatabaseManager()
    
    with open('export_medicamentos.sql', 'w', encoding='utf-8') as f:
        # Exportar laboratorios
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM laboratorios ORDER BY id")
            laboratorios = cursor.fetchall()
            
            f.write("-- Laboratorios\n")
            for lab in laboratorios:
                nombre = lab[0].replace("'", "''")
                f.write(f"INSERT INTO laboratorios (nombre) VALUES ('{nombre}') ON CONFLICT (nombre) DO NOTHING;\n")
            
            # Exportar monodrogas
            cursor.execute("SELECT nombre FROM monodrogas ORDER BY id")
            monodrogas = cursor.fetchall()
            
            f.write("\n-- Monodrogas\n")
            for mono in monodrogas:
                nombre = mono[0].replace("'", "''")
                f.write(f"INSERT INTO monodrogas (nombre) VALUES ('{nombre}') ON CONFLICT (nombre) DO NOTHING;\n")
            
            # Exportar medicamentos en lotes
            cursor.execute("SELECT COUNT(*) FROM medicamentos")
            total = cursor.fetchone()[0]
            
            f.write(f"\n-- Medicamentos ({total} registros)\n")
            
            batch_size = 1000
            for offset in range(0, total, batch_size):
                cursor.execute(f"""
                    SELECT numero_registro, troquel, cod_ab, troquel_ean, cod_monodroga,
                           monodroga, cod_laboratorio, laboratorio, marca, presentacion,
                           multidosis, precio_caja, precio_unitario, fecha
                    FROM medicamentos 
                    ORDER BY id 
                    LIMIT {batch_size} OFFSET {offset}
                """)
                
                medicamentos = cursor.fetchall()
                
                for med in medicamentos:
                    values = []
                    for val in med:
                        if val is None:
                            values.append('NULL')
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        else:
                            values.append(f"'{str(val).replace(chr(39), chr(39)+chr(39))}'")
                    
                    f.write(f"INSERT INTO medicamentos (numero_registro, troquel, cod_ab, troquel_ean, cod_monodroga, monodroga, cod_laboratorio, laboratorio, marca, presentacion, multidosis, precio_caja, precio_unitario, fecha) VALUES ({', '.join(values)}) ON CONFLICT (numero_registro) DO NOTHING;\n")
                
                print(f"Exportados {offset + len(medicamentos)} de {total} medicamentos")
    
    print(f"\n✓ Exportación completa: export_medicamentos.sql")
    print(f"  Total: {total} medicamentos")

if __name__ == '__main__':
    export_to_sql()
