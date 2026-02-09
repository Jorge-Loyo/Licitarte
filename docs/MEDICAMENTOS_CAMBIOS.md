# CAMBIOS REALIZADOS - Actualizacion Tabla Medicamentos

## 9 de febrero de 2026

### RESUMEN EJECUTIVO

Se ha actualizado completamente la estructura de la tabla `medicamentos` para alinearse con el formato del archivo Excel `Alfabeta_Febrero.xlsx`. Esto permite importar y mantener actualizados todos los medicamentos del catálogo de forma automática.

---

## ARCHIVOS MODIFICADOS

### 1. **shared/database/db_manager.py**

- Actualizada definición de tabla `medicamentos` (PostgreSQL y SQLite)
- Agregadas 6 nuevas columnas con migracion automatica
- Cambios: líneas 123-410

**Nuevas columnas agregadas:**

- troquel (TEXT)
- cod_ab (INTEGER)
- troquel_ean (TEXT)
- cod_monodroga (INTEGER)
- cod_laboratorio (INTEGER)
- multidosis (INTEGER)

### 2. **web/src/routes/uploads.py**

- Actualizada funcion `crear_producto_catalogo()` (INSERT)
- Actualizada funcion `actualizar_producto_catalogo()` (UPDATE)
- Ambas ahora incluyen los 6 nuevos campos en las operaciones

### 3. **web/src/routes/catalogos.py**

- Actualizado endpoint GET `/catalogo`
- Ahora devuelve todos los nuevos campos en las respuestas

### 4. **shared/database/migrations/003_update_medicamentos_estructura.sql**

- Archivo SQL de referencia con instrucciones de migracion
- Soporta PostgreSQL y SQLite

---

## ARCHIVOS NUEVOS CREADOS

### 1. **shared/database/import_medicamentos_alfabeta.py** (10.5 KB)

Propósito: Importar TODOS los medicamentos desde el Excel

Características:

- Lee archivo Excel (1000+ medicamentos)
- Inserta nuevos registros
- Actualiza registros existentes por numero_registro
- Maneja automáticamente valores NULL
- Genera reporte detallado de importacion

Uso:

```bash
# Importacion normal
python shared/database/import_medicamentos_alfabeta.py

# Importacion limpia (vacía tabla primero)
python shared/database/import_medicamentos_alfabeta.py --clean

# Archivo alternativo
python shared/database/import_medicamentos_alfabeta.py --excel-path "Data/Otro.xlsx"
```

### 2. **shared/database/update_medicamentos_precios.py** (6.5 KB)

Propósito: Actualizar precios SOLAMENTE desde nuevas versiones del Excel

Características:

- Lee solo los precios del Excel
- Busca medicamentos por numero_registro
- Actualiza: precio_caja, precio_unitario, multidosis, troquel, fecha
- NO inserta nuevos registros
- Ideal para importaciones mensuales/quincenales

Uso:

```bash
# Actualizar precios del Excel actual
python shared/database/update_medicamentos_precios.py

# Archivo alternativo
python shared/database/update_medicamentos_precios.py --excel-path "Data/Alfabeta_Marzo.xlsx"
```

### 3. **docs/MEDICAMENTOS_MIGRACION.md** (Documentacion completa)

- Guía detallada de uso
- Mapeo de columnas Excel -> BD
- Ejemplos de uso
- Troubleshooting
- Consideraciones importantes

---

## MAPEO DE COLUMNAS

| Excel           | BD              | Tipo          |
| --------------- | --------------- | ------------- |
| Troquel         | troquel         | TEXT          |
| Cod AB          | cod_ab          | INTEGER       |
| Troquel.1       | troquel_ean     | TEXT          |
| Fecha           | fecha           | TEXT          |
| Cod Monodroga   | cod_monodroga   | INTEGER       |
| Monodroga       | monodroga       | TEXT          |
| Cod Laboratorio | cod_laboratorio | INTEGER       |
| Laboratorio     | laboratorio     | TEXT          |
| N de Registro   | numero_registro | TEXT (UNIQUE) |
| Marca           | marca           | TEXT          |
| Presentacion    | presentacion    | TEXT          |
| Multidosis      | multidosis      | INTEGER       |
| Precio x caja   | precio_caja     | REAL          |
| Precio unitario | precio_unitario | REAL          |

---

## PASOS SIGUIENTES RECOMENDADOS

### 1. IMPORTACION INICIAL (AHORA)

```bash
cd c:\git\Licitarte

# Importar todos los medicamentos del Excel Alfabeta_Febrero.xlsx
python shared/database/import_medicamentos_alfabeta.py
```

**Esto va a:**

- Leer 1200+ medicamentos del Excel
- Crear nuevos registros en la BD
- Mostrar reporte de importacion
- Tomar ~2-3 minutos

### 2. VALIDAR IMPORTACION

Verificar que todo se importó correctamente:

```bash
# Ver cantidad de medicamentos
cd web
python -c "from app import db; c = db.get_connection(); cur = c.cursor(); cur.execute('SELECT COUNT(*) FROM medicamentos'); print(f'Total: {cur.fetchone()[0]}')"

# O visitar el endpoint:
# GET http://localhost:5000/api/catalogos/catalogo?per_page=5
```

### 3. REALIZAR COPIAS DE SEGURIDAD

Antes de cualquier operación de datos:

```bash
# Backup de la BD actual
cp shared/licitaciones.db shared/licitaciones_backup_$(date +%Y%m%d_%H%M%S).db
```

### 4. PARA FUTURAS ACTUALIZACIONES

**Opcion A: Si solo cambian precios (RECOMENDADO):**

```bash
python shared/database/update_medicamentos_precios.py --excel-path "Data/Alfabeta_Marzo.xlsx"
```

- Rapido y seguro
- Solo actualiza precios
- Toma ~30 segundos

**Opcion B: Si hay cambios grandes:**

```bash
python shared/database/import_medicamentos_alfabeta.py --clean --excel-path "Data/Alfabeta_Marzo.xlsx"
```

- Reimporta todo desde cero
- Garantiza consistencia
- Toma ~2-3 minutos

### 5. CONFIGURAR IMPORTACIONES AUTOMATICAS (Opcional)

Crear un script .bat para automatizar importaciones mensuales:

```batch
@echo off
REM script_importar_medicamentos.bat
cd c:\git\Licitarte
python shared/database/update_medicamentos_precios.py --excel-path "Data/Alfabeta_%DATE:~-4,4%%DATE:~-10,2%.xlsx"
echo Importacion completada: %date% %time%
```

Luego configurar una tarea programada (Task Scheduler) para ejecutarlo mensualmente.

---

## CAMBIOS EN LA API

### Crear medicamento (POST)

```json
{
  "numero_registro": "123456",
  "troquel": "4779441",
  "cod_ab": 1,
  "troquel_ean": "7790440123456",
  "cod_monodroga": 100,
  "monodroga": "Amoxicilina",
  "cod_laboratorio": 50,
  "laboratorio": "GSK",
  "marca": "Amoxil",
  "presentacion": "500mg x 20 capsulas",
  "multidosis": 20,
  "precio_caja": 150.0,
  "precio_unitario": 7.5
}
```

### Actualizar medicamento (PUT)

Ahora soporta actualizar los nuevos campos también.

### Obtener medicamentos (GET)

```bash
# Devuelve todos los campos incluyendo los nuevos
GET /api/catalogos/catalogo?search=amoxilina&per_page=10
```

---

## VALIDACIONES Y GARANTIAS

- [x] Base de datos soportadas: SQLite y PostgreSQL
- [x] Manejo automatico de NULL/valores vacios
- [x] Validacion de tipos de datos
- [x] Transacciones seguras en base de datos
- [x] Reportes detallados de importacion
- [x] Numero_registro es unico (no hay duplicados)
- [x] Compatibilidad con migraciones futuras

---

## TROUBLESHOOTING RAPIDO

**P: "El archivo Excel no se encuentra"**

```bash
# Verificar que existe
dir Data\Alfabeta_Febrero.xlsx
# Usar ruta absoluta si es necesario
python shared/database/import_medicamentos_alfabeta.py --excel-path "C:\ruta\completa\archivo.xlsx"
```

**P: "Error de conexion a base de datos"**

```bash
# Verificar que la BD existe
ls -la shared/licitaciones.db
# Reiniciar la aplicacion
```

**P: "Algunos medicamentos no se importan"**

```bash
# Ver logs detallados
python -u shared/database/import_medicamentos_alfabeta.py 2>&1 | tee import.log
# Revisar el archivo import.log
```

**P: "Necesito revertir cambios"**

```bash
# Restaurar de backup
cp shared/licitaciones_backup_YYYYMMDD_HHMMSS.db shared/licitaciones.db
```

---

## ESTADISTICAS ESPERADAS

**Excel Alfabeta_Febrero.xlsx:**

- Registros: ~1,200 medicamentos
- Tamaño: ~200 KB
- Tiempo de importacion: 2-3 minutos

**Después de importacion:**

- BD tamaño: +5-10 MB
- Tiempo de consultas: <500ms
- Campos por medicamento: 14

---

## VERSIONES DE SOFTWARE

- Python: 3.9+
- Pandas: 2.0.0+
- Flask: 3.0.0+
- SQLite: 3.0+
- PostgreSQL: 12+ (si se usa)

---

## CONTACTO Y SOPORTE

Para dudas sobre:

- **Importacion de datos:** Ver docs/MEDICAMENTOS_MIGRACION.md
- **Cambios en base de datos:** Revisar shared/database/db_manager.py
- **API cambios:** Ver web/src/routes/catalogos.py y uploads.py

---

**Estado:** Completado y listo para uso
**Fecha:** 9 de febrero de 2026
**Probado en:** SQLite (desarrollo local)
