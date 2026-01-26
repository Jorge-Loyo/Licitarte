# ACTUALIZACIÓN A VERSIÓN 2.0

## ⚠️ IMPORTANTE: Backup de Base de Datos

Antes de ejecutar la migración, haz un backup de tu base de datos:

```bash
# Copiar base de datos actual
copy database\licitaciones.db database\licitaciones_backup.db
```

## 📋 Pasos para Actualizar

### 1. Ejecutar Migración de Base de Datos

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
cd database
python migrate_v2.py
```

Cuando te pregunte si deseas ejecutar la migración, escribe `s` y presiona Enter.

### 2. Verificar Migración

El script mostrará el progreso:
- ✓ = Migración exitosa
- ✗ = Error (revisar mensaje)

### 3. Reiniciar Aplicación Web

```bash
cd web
python app.py
```

## 🆕 Nuevos Campos Disponibles

### Clientes
- Organismo/Jurisdicción (Nacional, Provincial, Municipal, Hospital, OS)
- Provincia
- Localidad

### Licitaciones
- Portal/Origen (COMPR.AR, BAC, PBAC, Portal propio, Mail, Otro)
- Modalidad de Entrega (Total, Parciales, Abierto por demanda)
- Forma de Pago (30/60/90/120 días, Contra entrega, Tesorería pública)
- Requiere Póliza (Sí/No)
- Monto de Póliza
- Observaciones

### Productos
- Precio Unitario (reemplaza precio ofertado)
- Total Ofertado (calculado automáticamente)
- Motivo de Pérdida (si no adjudicado)
- Precio Ganador Unitario
- Diferencia $ (calculado)
- Diferencia % (calculado)
- Costo Unitario (uso interno)
- Margen Unitario (calculado)
- Margen % (calculado)
- Margen Total (calculado)
- Alerta de Margen (< 8%)

### Catálogo Celty
- Costo Unitario (base de costos)

## 📊 Cálculos Automáticos

Los siguientes campos se calculan automáticamente:

```
Total Ofertado = Cantidad × Precio Unitario
Margen Unitario = Precio Unitario - Costo Unitario
Margen % = ((Precio Unitario - Costo Unitario) / Precio Unitario) × 100
Margen Total = Margen Unitario × Cantidad
Diferencia $ = Precio Unitario - Precio Ganador Unitario
Diferencia % = ((Precio Unitario - Precio Ganador) / Precio Ganador) × 100
Alerta Margen = Margen % < 8%
```

## 🔄 Compatibilidad con Datos Existentes

- Los datos existentes se mantienen intactos
- Los nuevos campos estarán vacíos en licitaciones antiguas
- `precio_unitario` se copia automáticamente desde `precio_ofertado`
- `total_ofertado` se calcula automáticamente

## ❓ Solución de Problemas

### Error: "no se encontró Python"
Asegúrate de tener Python instalado y en el PATH del sistema.

### Error en la migración
1. Restaura el backup: `copy database\licitaciones_backup.db database\licitaciones.db`
2. Revisa el mensaje de error
3. Contacta soporte si persiste

## 📝 Notas

- La migración es segura y reversible (con el backup)
- Los campos nuevos son opcionales
- Puedes seguir usando la aplicación normalmente
- Los cálculos automáticos funcionan en tiempo real

## ✅ Verificación Post-Migración

1. Abre la aplicación web
2. Ve a "Nueva Licitación"
3. Verifica que aparezcan los nuevos campos
4. Crea una licitación de prueba
5. Verifica que los cálculos funcionen correctamente

---

**Versión:** 2.0.0  
**Fecha:** Enero 2025
