#!/bin/bash
set -e

echo "Verificando columnas faltantes..."
python fix_render_columns.py

echo "Ejecutando migraciones..."
python migrate_render.py

echo "Creando usuario admin..."
python create_admin.py

echo "Cargando datos iniciales..."
python seed_database.py

echo "Iniciando gunicorn..."
exec gunicorn app:app -c gunicorn_config.py
