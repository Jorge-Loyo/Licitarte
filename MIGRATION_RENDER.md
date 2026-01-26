# Migración v1.1.0 en Render

## Ejecutar en Shell de Render

1. Ve a tu servicio en Render Dashboard
2. Click en "Shell" en el menú lateral
3. Ejecuta:

```bash
cd /opt/render/project/src
python database/migrate_v1_1_0.py
```

## Verificación

Deberías ver:
```
🚀 Iniciando migración v1.1.0...
📦 Agregando costo_unitario a celty...
✓ costo_unitario agregado
📦 Creando tabla portales_origen...
✓ 3 portales insertados
📦 Creando tabla modalidades_entrega...
✓ 3 modalidades insertadas
📦 Creando tabla formas_pago...
✓ 3 formas de pago insertadas
📦 Creando tabla organismos_jurisdiccion...
✓ 5 organismos insertados
📦 Creando tabla motivos_perdida...
✓ 5 motivos insertados
📦 Agregando columnas a licitaciones...
✓ portal_origen agregado a licitaciones
✓ modalidad_entrega agregado a licitaciones
✓ forma_pago agregado a licitaciones
✓ requiere_poliza agregado a licitaciones
✓ monto_poliza agregado a licitaciones
✓ observaciones agregado a licitaciones
📦 Agregando organismo_jurisdiccion a clientes...
✓ organismo_jurisdiccion agregado
📦 Agregando motivo_perdida a productos...
✓ motivo_perdida agregado

✅ Migración v1.1.0 completada exitosamente!
```

## Si hay errores

- Verifica que DATABASE_URL esté configurado
- Verifica que PostgreSQL esté accesible
- Revisa los logs para detalles del error

## Después de la migración

Reinicia el servicio en Render para aplicar cambios.
