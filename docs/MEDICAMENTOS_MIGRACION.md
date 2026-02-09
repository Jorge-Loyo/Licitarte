# Actualización de Estructura de Tabla Medicamentos - Resumen de Cambios

**Fecha:** 9 de febrero de 2026  
**Objetivo:** Alinear la estructura de la tabla `medicamentos` con el formato del Excel `Alfabeta_Febrero.xlsx`

## Resumen de Cambios

### 1. Nueva Estructura de la Tabla Medicamentos

Se agregaron las siguientes columnas a la tabla `medicamentos` para que coincida con el esquema del Excel:

#### Columnas Nuevas:

- `troquel` (TEXT) - Código troquel del medicamento
- `cod_ab` (INTEGER) - Código AB (Alfabeta)
- `troquel_ean` (TEXT) - Código EAN/Troquel.1
- `cod_monodroga` (INTEGER) - Código de la monodroga
- `cod_laboratorio` (INTEGER) - Código del laboratorio
- `multidosis` (INTEGER) - Cantidad de dosis múltiples

#### Columnas Existentes (Se Mantienen):

- `id` (INTEGER PRIMARY KEY)
- `numero_registro` (TEXT UNIQUE) - N de Registro del medicamento
- `monodroga` (TEXT) - Nombre de la monodroga
- `laboratorio` (TEXT) - Nombre del laboratorio
- `marca` (TEXT) - Marca del medicamento
- `presentacion` (TEXT) - Presentación del medicamento
- `precio_caja` (REAL) - Precio por caja
- `precio_unitario` (REAL) - Precio unitario
- `costo_unitario` (REAL) - Costo unitario
- `fecha` (TEXT) - Fecha del registro

### 2. Mapeo de Columnas Excel → BD

| Columna Excel   | Columna BD      | Tipo    | Notas                 |
| --------------- | --------------- | ------- | --------------------- |
| Troquel         | troquel         | TEXT    | Identificador troquel |
| Cod AB          | cod_ab          | INTEGER | Código Alfabeta       |
| Troquel.1       | troquel_ean     | TEXT    | Código EAN            |
| Fecha           | fecha           | TEXT    | Fecha de registro     |
| Cod Monodroga   | cod_monodroga   | INTEGER | Código monodroga      |
| Monodroga       | monodroga       | TEXT    | Nombre monodroga      |
| Cod Laboratorio | cod_laboratorio | INTEGER | Código laboratorio    |
| Laboratorio     | laboratorio     | TEXT    | Nombre laboratorio    |
| N de Registro   | numero_registro | TEXT    | Identificador único   |
| Marca           | marca           | TEXT    | Marca del medicamento |
| Presentacion    | presentacion    | TEXT    | Presentación          |
| Multidosis      | multidosis      | INTEGER | Cantidad dosis        |
| Precio x caja   | precio_caja     | REAL    | Precio por caja       |
| Precio unitario | precio_unitario | REAL    | Precio unitario       |

## Archivos Modificados

### 1. `shared/database/db_manager.py`

- Actualizada definición inicial de tabla `medicamentos` para PostgreSQL
- Actualizada definición inicial de tabla `medicamentos` para SQLite
- Agregado código de migración automática que agrega columnas faltantes si la tabla ya existe

### 2. `web/src/routes/uploads.py`

- Actualizada función `crear_producto_catalogo()` para incluir nuevos campos en INSERT
- Actualizada función `actualizar_producto_catalogo()` para incluir nuevos campos en UPDATE

### 3. `web/src/routes/catalogos.py`

- Actualizado query GET `/catalogo` para devolver todos los nuevos campos

### 4. `database/migrations/003_update_medicamentos_estructura.sql`

- Archivo SQL con instrucciones de migración para ambas bases de datos (PostgreSQL y SQLite)

## Scripts de Importación Nuevos

### 1. `database/import_medicamentos_alfabeta.py`

**Propósito:** Importación completa de medicamentos desde Excel

**Características:**

- Lee todos los registros del Excel Alfabeta_Febrero.xlsx
- Inserta nuevos medicamentos
- Actualiza medicamentos existentes (por número_registro)
- Valida datos antes de insertar
- Genera reporte de importación

**Uso:**

```bash
# Importación normal (actualiza existentes, agrega nuevos)
python database/import_medicamentos_alfabeta.py

# Importación limpia (vacía tabla y carga de cero)
python database/import_medicamentos_alfabeta.py --clean

# Especificar ruta alternativa del Excel
python database/import_medicamentos_alfabeta.py --excel-path "ruta/al/archivo.xlsx"
```

**Salida esperada:**

```
📂 Leyendo archivo Excel: Data/Alfabeta_Febrero.xlsx
✓ Se encontraron 1234 registros en el Excel
✓ Procesados 100/1234 registros...
...
==================================================
📊 RESUMEN DE IMPORTACIÓN
==================================================
✓ Insertados: 150
✓ Actualizados: 1084
📈 Total procesados: 1234
==================================================
```

### 2. `database/update_medicamentos_precios.py`

**Propósito:** Actualizar solo precios desde nuevas versiones del Excel

**Características:**

- Lee el Excel y busca medicamentos por número_registro
- Solo actualiza precios, multidosis, troquel y fecha
- No inserta nuevos registros
- Útil para importaciones recurrentes mensuales/quincenales

**Uso:**

```bash
# Actualizar precios (búsqueda automática en Data/)
python database/update_medicamentos_precios.py

# Especificar ruta alternativa del Excel
python database/update_medicamentos_precios.py --excel-path "Data/Alfabeta_Marzo.xlsx"
```

**Salida esperada:**

```
📂 Leyendo archivo Excel: Data/Alfabeta_Febrero.xlsx
✓ Se encontraron 1234 registros en el Excel

📝 Actualizando precios...
✓ Procesados 100/1234 registros...
...
==================================================
📊 RESUMEN DE ACTUALIZACIÓN DE PRECIOS
==================================================
✓ Actualizados: 1200
⚠️ No encontrados: 34
📈 Total procesados: 1234
==================================================
```

## Cómo Utilizar

### Primer Uso: Importación Inicial Completa

1. **Verificar que el archivo Excel existe:**

   ```bash
   ls Data/Alfabeta_Febrero.xlsx
   ```

2. **Ejecutar importación:**

   ```bash
   cd c:\git\Licitarte
   python database/import_medicamentos_alfabeta.py
   ```

3. **Verificar resultados** visitando el endpoint:
   ```
   GET /api/catalogos/catalogo?per_page=10
   ```

### Uso Recurrente: Actualización de Precios

Cuando recibas nuevas versiones del Excel con actualizaciones de precios:

```bash
# Opción 1: Actualizar solo precios (recomendado)
python database/update_medicamentos_precios.py --excel-path "Data/Alfabeta_Marzo.xlsx"

# Opción 2: Reimportar completamente (si hay cambios grandes)
python database/import_medicamentos_alfabeta.py --clean --excel-path "Data/Alfabeta_Marzo.xlsx"
```

### Usar desde la Aplicación Web

La aplicación web ya está actualizada. Puedes:

1. **Crear medicamento manualmente:**

   ```
   POST /api/catalogos/catalogo
   {
     "numero_registro": "123456",
     "monodroga": "Amoxicilina",
     "marca": "Amoxil",
     "laboratorio": "GSK",
     "presentacion": "500mg x 20 cápsulas",
     "precio_caja": 150.00,
     "precio_unitario": 7.50,
     "troquel": "4779441",
     "cod_ab": 1,
     "multidosis": 20
   }
   ```

2. **Actualizar medicamento:**

   ```
   PUT /api/catalogos/catalogo/123
   {
     "numero_registro": "123456",
     "precio_caja": 155.00,
     "precio_unitario": 7.75,
     ...
   }
   ```

3. **Listar medicamentos:**
   ```
   GET /api/catalogos/catalogo?search=amoxicilina&campo=monodroga&per_page=50
   ```

## Validaciones Incluidas

- ✓ Número de registro es requerido
- ✓ No permite duplicar número_registro
- ✓ Valida tipos de datos (integers para códigos, floats para precios)
- ✓ Maneja valores NULL/vacíos correctamente
- ✓ Genera reportes detallados de importación

## Base de Datos Soportadas

- ✓ SQLite (desarrollo local)
- ✓ PostgreSQL (producción)

Los scripts detectan automáticamente cuál está en uso y ajustan la sintaxis SQL.

## Consideraciones Importantes

1. **Número de Registro:** Es el identificador único del medicamento. Asegúrate de que sea consistente entre importaciones.

2. **Precios:** Se almacenan como REAL (decimales). Los scripts convierten automáticamente.

3. **Fechas:** Se importan como YYYY-MM-DD. El script usa la fecha actual si está vacía.

4. **Códigos:** cod_ab, cod_monodroga, cod_laboratorio son opcionales (pueden ser NULL).

5. **Respaldos:** Antes de ejecutar con `--clean`, considera hacer un backup de la BD.

## Troubleshooting

**Problema:** "El archivo no existe"

```bash
# Verificar ruta correcta
ls -la Data/Alfabeta_Febrero.xlsx
```

**Problema:** "Cannot read from database"

```bash
# Verificar conexión a BD
python -c "from shared.database.db_manager import DatabaseManager; print('OK')"
```

**Problema:** "Algunos registros no se importan"

```bash
# Ver logs detallados ejecutando con Python
python -u database/import_medicamentos_alfabeta.py 2>&1 | tee import.log
```

## Próximos Pasos Sugeridos

1. ✓ Ejecutar importación inicial con el Excel Alfabeta_Febrero.xlsx
2. ✓ Verificar cantidad de registros importados
3. ✓ Revisar algunos medicamentos en la aplicación web
4. ✓ Configurar importaciones automáticas mensualmente (CRON job)
5. ✓ Hacer backup regular de la tabla medicamentos

---

**Soporte:** Para dudas sobre la importación, revisar los logs de ejecución o contactar al desarrollador.
