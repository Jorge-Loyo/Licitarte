#!/bin/bash
set -e

echo "=== Limpiando clientes inactivos ==="
python limpiar_clientes.py

echo "=== Verificando columnas en PostgreSQL ==="
python prestart.py

echo "=== Iniciando aplicación ==="
exec gunicorn app:app
