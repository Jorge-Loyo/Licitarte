#!/bin/bash
# Ejecutar migraciones - Licitarte

echo "🔄 Ejecutando migraciones..."

cd shared/database/migrations
python migrate.py ../licitaciones.db

if [ $? -eq 0 ]; then
    echo "✅ Migraciones completadas"
else
    echo "❌ Error en migraciones"
    exit 1
fi
