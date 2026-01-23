# 📘 MANUAL DE USUARIO - LICITARTE

## Sistema de Gestión de Licitaciones Farmacéuticas

---

## 📋 ÍNDICE

1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Inicio de la Aplicación](#inicio-de-la-aplicación)
4. [Módulos del Sistema](#módulos-del-sistema)
5. [Guía de Uso Paso a Paso](#guía-de-uso-paso-a-paso)
6. [Preguntas Frecuentes](#preguntas-frecuentes)
7. [Solución de Problemas](#solución-de-problemas)
8. [Respaldo de Datos](#respaldo-de-datos)

---

## 🎯 INTRODUCCIÓN

**Licitarte** es una aplicación de escritorio diseñada para gestionar y analizar licitaciones farmacéuticas de manera eficiente. Permite:

- ✅ Registrar licitaciones con múltiples productos
- ✅ Gestionar y editar información de licitaciones
- ✅ Analizar resultados y estadísticas
- ✅ Consultar histórico de precios y ganadores
- ✅ Generar reportes de licitaciones adjudicadas

---

## 💻 INSTALACIÓN

### Requisitos del Sistema

- **Sistema Operativo:** Windows 10/11, macOS, Linux
- **Python:** Versión 3.8 o superior
- **Espacio en Disco:** 50 MB mínimo

### Pasos de Instalación

1. **Verificar Python instalado:**
   ```bash
   python --version
   ```
   Si no está instalado, descargue desde: https://www.python.org/downloads/

2. **Navegar a la carpeta de la aplicación:**
   ```bash
   cd C:\git\Licitarte
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verificar instalación:**
   La aplicación creará automáticamente la carpeta `database` al iniciar.

---

## 🚀 INICIO DE LA APLICACIÓN

### Ejecutar Licitarte

```bash
python main.py
```

### Primera Vez

Al iniciar por primera vez:
- Se creará automáticamente la base de datos en `database/licitaciones.db`
- La interfaz mostrará el Dashboard vacío
- Todos los módulos estarán disponibles en el menú lateral

---

## 📂 MÓDULOS DEL SISTEMA

### 1. 📊 DASHBOARD (Análisis)

**Función:** Visualizar estadísticas y métricas de licitaciones.

**Elementos:**

- **Tarjetas de Estadísticas:**
  - Total Licitaciones: Cantidad total registrada
  - Licitaciones Ganadas: Cantidad con productos adjudicados
  - Total Unidades: Suma de todas las cantidades licitadas
  - Precio Promedio Ponderado: Promedio de precios ganados

- **Búsqueda de Histórico:**
  - Buscar productos específicos
  - Ver último precio ganador
  - Identificar laboratorio ganador anterior
  - Consultar fecha de última adjudicación

- **Tabla de Productos Adjudicados:**
  - Lista completa de productos ganados
  - Información de licitación, cantidad y precio

**Botones:**
- 🔄 Actualizar: Refresca las estadísticas

---

### 2. ➕ NUEVA LICITACIÓN (Ingreso)

**Función:** Registrar nuevas licitaciones con sus productos.

#### Campos de Licitación

| Campo | Descripción | Obligatorio |
|-------|-------------|-------------|
| N° Licitación | Número único identificador | ✅ Sí |
| Fecha | Fecha de la licitación (YYYY-MM-DD) | ✅ Sí |
| Lab. Ganador | Laboratorio ganador general | ❌ No |

#### Campos de Producto

| Campo | Descripción | Obligatorio | Validación |
|-------|-------------|-------------|------------|
| Ítem/Producto | Nombre del producto | ✅ Sí | Texto |
| Cantidad | Unidades licitadas | ✅ Sí | Número > 0 |
| Precio Ofertado | Precio ofrecido | ✅ Sí | Número ≥ 0 |
| Resultado | Estado del producto | ✅ Sí | Lista desplegable |
| Lab. Ganador | Laboratorio ganador del ítem | ❌ No | Texto |

**Opciones de Resultado:**
- **Adjudicado:** Producto ganado (precio ganador = precio ofertado)
- **Parcial:** Adjudicación parcial
- **No Adjudicado:** Producto no ganado

**Botones:**
- ➕ Agregar Producto: Añade un nuevo producto a la licitación
- ✕ (en cada producto): Elimina ese producto
- Guardar Licitación: Guarda toda la información

---

### 3. 📋 GESTIÓN (Administración)

**Función:** Ver, editar y eliminar licitaciones existentes.

#### Funcionalidades

**Búsqueda:**
- Buscar por N° de Licitación
- Buscar por Laboratorio Ganador
- Búsqueda en tiempo real

**Tabla de Licitaciones:**
- ID: Identificador interno
- N° Licitación: Número de licitación
- Fecha: Fecha de registro
- Lab. Ganador: Laboratorio ganador

**Acciones:**
- **Doble clic** en una fila: Abre detalle de productos
- **Ver Detalle:** Muestra productos de la licitación seleccionada
- **Eliminar:** Borra la licitación y todos sus productos

#### Ventana de Detalle

Muestra todos los productos de una licitación:
- ID del producto
- Ítem/Producto
- Cantidad
- Precio Ofertado
- Resultado
- Precio Ganador
- Lab. Ganador

**Editar Producto:**
1. Seleccionar producto en la tabla
2. Clic en "Editar Producto"
3. Modificar campos necesarios
4. Guardar cambios

---

## 📖 GUÍA DE USO PASO A PASO

### CASO 1: Registrar una Nueva Licitación

**Escenario:** Participó en la licitación N° 2024-001 con 3 productos.

**Pasos:**

1. **Ir al módulo "Nueva Licitación"**
   - Clic en "➕ Nueva Licitación" en el menú lateral

2. **Completar datos de la licitación:**
   - N° Licitación: `2024-001`
   - Fecha: `2024-01-15` (o usar fecha actual)
   - Lab. Ganador: `Laboratorio ABC` (opcional)

3. **Agregar primer producto:**
   - Ítem/Producto: `Paracetamol 500mg`
   - Cantidad: `10000`
   - Precio Ofertado: `0.50`
   - Resultado: Seleccionar `Adjudicado`
   - Lab. Ganador: (se completa automáticamente si es adjudicado)

4. **Agregar más productos:**
   - Clic en "➕ Agregar Producto"
   - Repetir el proceso para cada producto

5. **Guardar:**
   - Clic en "Guardar Licitación"
   - Confirmar mensaje de éxito

6. **Verificar:**
   - Ir al Dashboard para ver estadísticas actualizadas

---

### CASO 2: Consultar Histórico de un Producto

**Escenario:** Quiere saber el último precio ganador del Paracetamol.

**Pasos:**

1. **Ir al Dashboard**
   - Clic en "📊 Dashboard"

2. **Buscar producto:**
   - En "Histórico de Producto"
   - Escribir: `Paracetamol`
   - Clic en "Buscar"

3. **Ver resultados:**
   - N° Licitación donde se ganó
   - Precio Ganador
   - Laboratorio Ganador
   - Fecha de adjudicación

---

### CASO 3: Editar un Producto Existente

**Escenario:** Necesita corregir el precio de un producto.

**Pasos:**

1. **Ir a Gestión**
   - Clic en "📋 Gestión"

2. **Buscar licitación:**
   - Usar el campo de búsqueda
   - O buscar en la tabla

3. **Abrir detalle:**
   - Doble clic en la licitación
   - O seleccionar y clic en "Ver Detalle"

4. **Editar producto:**
   - Seleccionar el producto a editar
   - Clic en "Editar Producto"
   - Modificar campos necesarios
   - Clic en "Guardar"

5. **Verificar cambios:**
   - Los cambios se reflejan inmediatamente

---

### CASO 4: Eliminar una Licitación

**Escenario:** Registró una licitación por error.

**Pasos:**

1. **Ir a Gestión**
   - Clic en "📋 Gestión"

2. **Seleccionar licitación:**
   - Clic en la fila de la licitación a eliminar

3. **Eliminar:**
   - Clic en botón "Eliminar"
   - Confirmar en el diálogo

4. **Resultado:**
   - La licitación y todos sus productos se eliminan permanentemente

⚠️ **ADVERTENCIA:** Esta acción no se puede deshacer.

---

## ❓ PREGUNTAS FRECUENTES

### ¿Qué significa "Precio Promedio Ponderado"?

Es el promedio de precios considerando las cantidades. Se calcula:
```
Suma(Precio × Cantidad) / Suma(Cantidad)
```
Solo incluye productos adjudicados.

---

### ¿Puedo usar el mismo N° de Licitación dos veces?

No. El sistema no permite números de licitación duplicados. Recibirá un mensaje de error si intenta registrar un número existente.

---

### ¿Qué pasa si marco un producto como "Adjudicado"?

El sistema automáticamente:
- Copia el "Precio Ofertado" al "Precio Ganador"
- Lo incluye en las estadísticas del Dashboard
- Lo muestra en la tabla de productos adjudicados

---

### ¿Cómo busco productos en el histórico?

La búsqueda es flexible:
- Puede escribir parte del nombre
- No distingue mayúsculas/minúsculas
- Ejemplo: buscar "para" encontrará "Paracetamol"

---

### ¿Puedo exportar los datos?

Actualmente, los datos se almacenan en SQLite. Para exportar:
1. Copie el archivo `database/licitaciones.db`
2. Use herramientas como DB Browser for SQLite para exportar a Excel/CSV

---

### ¿Dónde se guardan los datos?

En la carpeta `database/licitaciones.db` dentro de la aplicación.

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Error: "No se puede conectar a la base de datos"

**Solución:**
1. Verificar que existe la carpeta `database`
2. Verificar permisos de escritura
3. Reiniciar la aplicación

---

### Error: "El número de licitación ya existe"

**Causa:** Intenta registrar un N° de licitación duplicado.

**Solución:**
- Use un número diferente
- O edite la licitación existente en lugar de crear una nueva

---

### Error: "Cantidad y precio deben ser números válidos"

**Causa:** Ingresó texto en campos numéricos.

**Solución:**
- Cantidad: Solo números enteros positivos (ej: 1000)
- Precio: Números decimales con punto (ej: 10.50)

---

### La aplicación no inicia

**Soluciones:**

1. **Verificar Python:**
   ```bash
   python --version
   ```

2. **Reinstalar dependencias:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Verificar errores:**
   ```bash
   python main.py
   ```
   Leer mensajes de error en la consola

---

### Las estadísticas no se actualizan

**Solución:**
- Clic en el botón "🔄 Actualizar" en el Dashboard
- O cambiar de módulo y volver al Dashboard

---

## 💾 RESPALDO DE DATOS

### Crear Respaldo Manual

**Método 1: Copiar archivo**
1. Cerrar la aplicación
2. Copiar `database/licitaciones.db`
3. Guardar en ubicación segura con fecha:
   - Ejemplo: `licitaciones_backup_2024-01-15.db`

**Método 2: Programático**
```python
from database.db_manager import DatabaseManager
db = DatabaseManager()
db.exportar_backup("backup/licitaciones_backup.db")
```

---

### Restaurar Respaldo

1. Cerrar la aplicación
2. Reemplazar `database/licitaciones.db` con el archivo de respaldo
3. Reiniciar la aplicación

---

### Recomendaciones de Respaldo

- ✅ Hacer respaldo semanal
- ✅ Guardar en ubicación diferente (USB, nube)
- ✅ Mantener múltiples versiones
- ✅ Etiquetar con fecha

---

## 📊 MEJORES PRÁCTICAS

### Ingreso de Datos

1. **Usar formato consistente:**
   - Fechas: YYYY-MM-DD
   - Nombres de productos: Capitalizar correctamente
   - Laboratorios: Usar nombres completos

2. **Verificar antes de guardar:**
   - Revisar todos los campos
   - Confirmar cantidades y precios
   - Verificar resultado correcto

3. **Documentar información completa:**
   - Llenar campos opcionales cuando sea relevante
   - Agregar laboratorio ganador en productos

---

### Gestión de Licitaciones

1. **Búsqueda eficiente:**
   - Usar el campo de búsqueda
   - Buscar por número o laboratorio

2. **Edición cuidadosa:**
   - Verificar que está editando el producto correcto
   - Confirmar cambios antes de guardar

3. **Eliminación responsable:**
   - Verificar dos veces antes de eliminar
   - Considerar hacer respaldo antes de eliminar datos importantes

---

## 📞 SOPORTE

### Información del Sistema

- **Versión:** 1.0
- **Base de Datos:** SQLite 3
- **Framework UI:** CustomTkinter

### Logs y Diagnóstico

Los errores se muestran en:
- Mensajes emergentes en la aplicación
- Consola de Python (si se ejecuta desde terminal)

---

## 🔐 SEGURIDAD Y PRIVACIDAD

### Datos Locales

- Todos los datos se almacenan localmente
- No hay conexión a internet
- No se comparte información con terceros

### Validaciones Implementadas

- ✅ Números de licitación únicos
- ✅ Cantidades positivas
- ✅ Precios no negativos
- ✅ Campos obligatorios validados
- ✅ Integridad referencial en base de datos

---

## 📈 INTERPRETACIÓN DE ESTADÍSTICAS

### Total Licitaciones
Cuenta todas las licitaciones registradas, independientemente del resultado.

### Licitaciones Ganadas
Cuenta licitaciones que tienen al menos un producto adjudicado.

### Total Unidades
Suma de todas las cantidades de todos los productos (ganados o no).

### Precio Promedio Ponderado
Promedio de precios de productos adjudicados, ponderado por cantidad:
- Útil para análisis de rentabilidad
- Solo considera productos ganados
- Refleja el valor real de las adjudicaciones

---

## 🎓 GLOSARIO

- **Licitación:** Proceso de compra pública de productos farmacéuticos
- **Adjudicado:** Producto ganado en la licitación
- **Parcial:** Adjudicación de solo parte de la cantidad solicitada
- **No Adjudicado:** Producto no ganado
- **Precio Ofertado:** Precio que usted ofreció
- **Precio Ganador:** Precio del laboratorio que ganó el producto
- **Precio Promedio Ponderado:** Promedio considerando cantidades

---

## ✅ CHECKLIST DE USO DIARIO

### Al Registrar Licitación Nueva
- [ ] Verificar N° de licitación único
- [ ] Ingresar fecha correcta
- [ ] Agregar todos los productos
- [ ] Verificar cantidades y precios
- [ ] Seleccionar resultado correcto
- [ ] Guardar y confirmar

### Al Finalizar el Día
- [ ] Revisar Dashboard
- [ ] Verificar estadísticas
- [ ] Hacer respaldo si es necesario

### Semanalmente
- [ ] Crear respaldo de base de datos
- [ ] Revisar licitaciones pendientes
- [ ] Analizar tendencias en Dashboard

---

## 📝 NOTAS FINALES

Este manual cubre todas las funcionalidades principales de Licitarte v1.0. Para funcionalidades adicionales o personalizaciones, consulte con el desarrollador.

**Última actualización:** Enero 2024

---

**¡Gracias por usar Licitarte!** 🎉
