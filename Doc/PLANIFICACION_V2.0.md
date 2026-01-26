# PLANIFICACIÓN VERSIÓN 2.0 - Licitarte

## Nuevos Campos y Funcionalidades

### 1. DATOS DEL CLIENTE
**Agregar a tabla `clientes`:**
- `organismo_jurisdiccion` (Nacional / Provincial / Municipal / Hospital / OS)
- `provincia`
- `localidad`

### 2. DATOS DE LA LICITACIÓN
**Agregar a tabla `licitaciones`:**
- `portal_origen` (COMPR.AR / BAC / PBAC / Portal propio / Mail / Otro)
- `modalidad_entrega` (Entrega total / Entregas parciales / Abierto por demanda)
- `forma_pago` (30/60/90/120 días / Contra entrega / Tesorería pública)
- `requiere_poliza` (Sí / No)
- `monto_poliza` (DECIMAL)
- `observaciones` (TEXT)

### 3. DATOS DE PRODUCTOS
**Agregar a tabla `productos`:**
- `precio_unitario` (DECIMAL) - Input manual
- `total_ofertado` (DECIMAL) - Calculado: cantidad × precio_unitario
- `motivo_perdida` (Precio más alto / Marca no priorizada / No cumplía especificación / Error administrativo / Otro)
- `precio_ganador_unitario` (DECIMAL)
- `diferencia_pesos` (DECIMAL) - Calculado: precio_unitario - precio_ganador_unitario
- `diferencia_porcentaje` (DECIMAL) - Calculado: ((precio_unitario - precio_ganador_unitario) / precio_ganador_unitario) × 100

### 4. COSTOS Y RENTABILIDAD
**Agregar a tabla `productos`:**
- `costo_unitario` (DECIMAL) - Uso interno
- `margen_unitario` (DECIMAL) - Calculado: precio_unitario - costo_unitario
- `margen_porcentaje` (DECIMAL) - Calculado: ((precio_unitario - costo_unitario) / precio_unitario) × 100
- `margen_total` (DECIMAL) - Calculado: margen_unitario × cantidad
- `alerta_margen` (BOOLEAN) - Calculado: margen_porcentaje < 8%

**Agregar a tabla `celty` (catálogo):**
- `costo_unitario` (DECIMAL) - Base de costos

### 5. CAMPOS CALCULADOS AUTOMÁTICOS
**Nuevas vistas/consultas para:**
- `porcentaje_adjudicacion_producto` - Por monodroga/marca
- `porcentaje_adjudicacion_cliente` - Por cliente
- `precio_promedio_historico` - Por producto
- `ranking_producto` (Rentable / Competitivo / Descartable)

### 6. ALERTAS Y NOTIFICACIONES
**Sistema de alertas en Gestión:**
- Alerta amarilla: margen < 8%
- Alerta roja: margen < 5%
- Alerta de pólizas que atan capital en licitaciones pequeñas

---

## CAMBIOS EN LA BASE DE DATOS

### Migración SQL - Clientes
```sql
ALTER TABLE clientes ADD COLUMN organismo_jurisdiccion TEXT;
ALTER TABLE clientes ADD COLUMN provincia TEXT;
ALTER TABLE clientes ADD COLUMN localidad TEXT;
```

### Migración SQL - Licitaciones
```sql
ALTER TABLE licitaciones ADD COLUMN portal_origen TEXT;
ALTER TABLE licitaciones ADD COLUMN modalidad_entrega TEXT;
ALTER TABLE licitaciones ADD COLUMN forma_pago TEXT;
ALTER TABLE licitaciones ADD COLUMN requiere_poliza BOOLEAN DEFAULT FALSE;
ALTER TABLE licitaciones ADD COLUMN monto_poliza DECIMAL(15,2);
ALTER TABLE licitaciones ADD COLUMN observaciones TEXT;
```

### Migración SQL - Productos
```sql
ALTER TABLE productos ADD COLUMN precio_unitario DECIMAL(15,2);
ALTER TABLE productos ADD COLUMN total_ofertado DECIMAL(15,2);
ALTER TABLE productos ADD COLUMN motivo_perdida TEXT;
ALTER TABLE productos ADD COLUMN precio_ganador_unitario DECIMAL(15,2);
ALTER TABLE productos ADD COLUMN diferencia_pesos DECIMAL(15,2);
ALTER TABLE productos ADD COLUMN diferencia_porcentaje DECIMAL(10,2);
ALTER TABLE productos ADD COLUMN costo_unitario DECIMAL(15,2);
ALTER TABLE productos ADD COLUMN margen_unitario DECIMAL(15,2);
ALTER TABLE productos ADD COLUMN margen_porcentaje DECIMAL(10,2);
ALTER TABLE productos ADD COLUMN margen_total DECIMAL(15,2);
ALTER TABLE productos ADD COLUMN alerta_margen BOOLEAN DEFAULT FALSE;
```

### Migración SQL - Catálogo Celty
```sql
ALTER TABLE celty ADD COLUMN costo_unitario DECIMAL(15,2);
```

---

## CAMBIOS EN LA INTERFAZ

### Módulo: Nueva Licitación
**Sección Datos de Licitación:**
- Agregar select: Portal/Origen
- Agregar select: Modalidad de Entrega
- Agregar select: Forma de Pago

**Sección Póliza:**
- Checkbox: Requiere Póliza
- Input: Monto de Póliza (si requiere)

**Sección Productos:**
- Cambiar "Precio Ofertado" por "Precio Unitario"
- Mostrar "Total Ofertado" (calculado automáticamente)
- Agregar: Costo Unitario (opcional, uso interno)
- Mostrar: Margen % (calculado)
- Alerta visual si margen < 8%

**Sección Resultado (si No Adjudicado):**
- Select: Motivo de Pérdida
- Input: Precio Ganador Unitario
- Mostrar: Diferencia $ (calculado)
- Mostrar: Diferencia % (calculado)

**Sección Observaciones:**
- Textarea: Observaciones generales

### Módulo: Gestión
**Vista de Licitación:**
- Mostrar alertas de margen bajo
- Mostrar total de margen de la licitación
- Indicador visual de rentabilidad

**Edición de Productos:**
- Todos los campos nuevos editables
- Cálculos automáticos en tiempo real

### Módulo: Administración - Clientes
**Formulario de Cliente:**
- Select: Organismo/Jurisdicción
- Input: Provincia
- Input: Localidad

### Módulo: Administración - Catálogo
**Tabla Celty:**
- Agregar columna: Costo Unitario
- Permitir edición de costos

### Módulo: Dashboard
**Nuevas Estadísticas:**
- Ranking de motivos de pérdida (gráfico)
- Productos más rentables
- Productos con mayor competitividad
- Clientes con mejor % de adjudicación
- Análisis de márgenes promedio

---

## CÁLCULOS AUTOMÁTICOS

### JavaScript - Cálculos en Tiempo Real
```javascript
// Total Ofertado
total_ofertado = cantidad × precio_unitario

// Margen Unitario
margen_unitario = precio_unitario - costo_unitario

// Margen Porcentaje
margen_porcentaje = ((precio_unitario - costo_unitario) / precio_unitario) × 100

// Margen Total
margen_total = margen_unitario × cantidad

// Diferencia vs Ganador (Pesos)
diferencia_pesos = precio_unitario - precio_ganador_unitario

// Diferencia vs Ganador (Porcentaje)
diferencia_porcentaje = ((precio_unitario - precio_ganador_unitario) / precio_ganador_unitario) × 100

// Alerta de Margen
alerta_margen = margen_porcentaje < 8
```

### Backend - Consultas Analíticas
```python
# % Adjudicación por Producto
SELECT monodroga, marca, 
       COUNT(CASE WHEN resultado = 'Adjudicado' THEN 1 END) * 100.0 / COUNT(*) as porcentaje
FROM productos
GROUP BY monodroga, marca

# % Adjudicación por Cliente
SELECT cliente_id, 
       COUNT(CASE WHEN tiene_adjudicados THEN 1 END) * 100.0 / COUNT(*) as porcentaje
FROM licitaciones
GROUP BY cliente_id

# Precio Promedio Histórico
SELECT monodroga, marca, AVG(precio_unitario) as precio_promedio
FROM productos
WHERE resultado = 'Adjudicado'
GROUP BY monodroga, marca

# Ranking de Productos
SELECT monodroga, marca,
       AVG(margen_porcentaje) as margen_promedio,
       COUNT(CASE WHEN resultado = 'Adjudicado' THEN 1 END) * 100.0 / COUNT(*) as tasa_adjudicacion,
       CASE 
           WHEN AVG(margen_porcentaje) > 15 AND tasa_adjudicacion > 50 THEN 'Rentable'
           WHEN tasa_adjudicacion > 30 THEN 'Competitivo'
           ELSE 'Descartable'
       END as ranking
FROM productos
GROUP BY monodroga, marca
```

---

## PRIORIDADES DE IMPLEMENTACIÓN

### FASE 1 - Campos Básicos
1. Migración de base de datos
2. Actualizar formularios de ingreso
3. Cálculos automáticos básicos (precio unitario, total ofertado)

### FASE 2 - Análisis de Competencia
1. Motivo de pérdida
2. Diferencia vs ganador
3. Ranking de causas de pérdida

### FASE 3 - Costos y Rentabilidad
1. Costo unitario en catálogo
2. Cálculo de márgenes
3. Alertas de margen bajo

### FASE 4 - Análisis Avanzado
1. Campos calculados automáticos
2. Dashboard con nuevas estadísticas
3. Reportes de rentabilidad

### FASE 5 - Pólizas y Documentación
1. Gestión de pólizas
2. Alertas de capital atado
3. Sistema de observaciones

---

## NOTAS IMPORTANTES

- Mantener compatibilidad con datos existentes
- Los campos nuevos deben ser opcionales inicialmente
- Implementar validaciones de datos
- Agregar tooltips explicativos en la interfaz
- Considerar permisos de usuario para campos sensibles (costos)
- Backup de base de datos antes de cada migración

---

**Fecha de Planificación:** Enero 2025
**Versión Objetivo:** 2.0.0
**Estado:** Planificado
