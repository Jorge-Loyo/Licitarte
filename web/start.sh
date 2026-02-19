#!/bin/bash
set -e

echo "=== Verificando columnas en PostgreSQL ==="
python prestart.py

echo "=== Iniciando aplicación ==="
exec gunicorn app:app
