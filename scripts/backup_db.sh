#!/bin/bash
# Backup de base de datos - Licitarte

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="data/backups"
DB_FILE="shared/database/licitaciones.db"

mkdir -p $BACKUP_DIR

if [ -f "$DB_FILE" ]; then
    cp $DB_FILE "$BACKUP_DIR/licitaciones_$TIMESTAMP.db"
    echo "✅ Backup creado: $BACKUP_DIR/licitaciones_$TIMESTAMP.db"
else
    echo "❌ Base de datos no encontrada: $DB_FILE"
    exit 1
fi
