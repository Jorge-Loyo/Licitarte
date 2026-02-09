#!/usr/bin/env python
"""Script para crear usuario admin con contraseña admin123"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from werkzeug.security import generate_password_hash
import psycopg

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Generar hash para admin123
password_hash = generate_password_hash('admin123')

print(f"Hash generado: {password_hash}")

# Actualizar o insertar usuario admin
with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO usuarios (username, email, password_hash) 
            VALUES ('admin', 'admin@licitarte.com', %s)
            ON CONFLICT (username) 
            DO UPDATE SET password_hash = EXCLUDED.password_hash
        """, (password_hash,))
        conn.commit()
        print("✅ Usuario admin creado/actualizado correctamente")
