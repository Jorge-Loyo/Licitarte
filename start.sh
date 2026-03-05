#!/bin/bash

echo "Iniciando Licitarte..."
echo ""

cd "$(dirname "$0")"

if [ ! -f ".env" ]; then
    echo "Copiando .env.example a .env..."
    cp .env.example .env
fi

echo "Activando entorno virtual..."
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Creando entorno virtual..."
    python -m venv venv
    source venv/bin/activate
    echo "Instalando dependencias..."
    pip install -r requirements.txt
fi

echo ""
echo "Base de datos ya existe en licitarte-postgres (puerto 5433)"

sleep 1

echo ""
echo "Iniciando aplicacion Flask..."
cd backend
python app.py
