#!/usr/bin/env python
"""Script para sincronizar laboratorios y monodrogas desde medicamentos"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.database.db_manager import DatabaseManager
from shared.database.connection_pool import USE_POSTGRES

def sync_catalogos():
    print("Sincronizando laboratorios y monodrogas desde medicamentos...")
    
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Contar medicamentos
        cursor.execute("SELECT COUNT(*) FROM medicamentos")
        total_medicamentos = cursor.fetchone()[0]
        print(f"Total medicamentos: {total_medicamentos}")
        
        # Extraer y cargar monodrogas únicas
        print("\nExtrayendo monodrogas únicas...")
        cursor.execute("SELECT DISTINCT monodroga FROM medicamentos WHERE monodroga IS NOT NULL AND monodroga != '' ORDER BY monodroga")
        monodrogas = cursor.fetchall()
        
        count_mono = 0
        for (monodroga,) in monodrogas:
            try:
                if USE_POSTGRES:
                    cursor.execute("INSERT INTO monodrogas (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING", (monodroga,))
                else:
                    cursor.execute("INSERT OR IGNORE INTO monodrogas (nombre) VALUES (?)", (monodroga,))
                count_mono += 1
            except Exception as e:
                print(f"Error insertando monodroga {monodroga}: {e}")
        
        conn.commit()
        print(f"✓ {count_mono} monodrogas sincronizadas")
        
        # Extraer y cargar laboratorios únicos
        print("\nExtrayendo laboratorios únicos...")
        cursor.execute("SELECT DISTINCT laboratorio FROM medicamentos WHERE laboratorio IS NOT NULL AND laboratorio != '' ORDER BY laboratorio")
        laboratorios = cursor.fetchall()
        
        count_lab = 0
        for (laboratorio,) in laboratorios:
            try:
                if USE_POSTGRES:
                    cursor.execute("INSERT INTO laboratorios (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING", (laboratorio,))
                else:
                    cursor.execute("INSERT OR IGNORE INTO laboratorios (nombre) VALUES (?)", (laboratorio,))
                count_lab += 1
            except Exception as e:
                print(f"Error insertando laboratorio {laboratorio}: {e}")
        
        conn.commit()
        print(f"✓ {count_lab} laboratorios sincronizados")
        
        # Verificar resultados
        cursor.execute("SELECT COUNT(*) FROM monodrogas")
        total_mono = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM laboratorios")
        total_lab = cursor.fetchone()[0]
        
        print(f"\n✅ Sincronización completada:")
        print(f"   - Monodrogas: {total_mono}")
        print(f"   - Laboratorios: {total_lab}")

if __name__ == '__main__':
    sync_catalogos()
