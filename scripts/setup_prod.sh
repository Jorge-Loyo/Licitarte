#!/bin/bash
# Setup ambiente de producción - Licitarte

echo "🚀 Configurando ambiente de producción..."

cd web
pip install -r requirements.txt
pip install gunicorn

echo "✅ Setup completado"
echo ""
echo "Para iniciar:"
echo "  gunicorn app:app"
