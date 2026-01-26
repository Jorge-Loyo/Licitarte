# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.1.0] - 2025-01-26

### Agregado
- **Módulo Métricas**: Nuevo módulo con análisis avanzado
  - Ranking de causas de pérdidas con cantidad y porcentaje
  - Diferencia promedio en $ y % vs ganador
  - Análisis de competitividad
- **Análisis de Márgenes**: Sistema de alertas visuales al cotizar
  - Alerta roja: Precio por debajo o igual al costo
  - Alerta amarilla: Margen menor al 8%
  - Alerta verde: Margen igual o mayor al 8%
  - Cálculo automático en tiempo real
- **Gestión de Costos**: Campo costo_unitario en catálogo de productos
  - Edición manual desde Administración
  - No se sobrescribe con carga de Excel
  - Base para análisis de rentabilidad
- **Catálogos Dinámicos**: 5 nuevos catálogos configurables
  - Portales/Origen
  - Modalidades de Entrega
  - Formas de Pago
  - Organismos/Jurisdicción
  - Motivos de Pérdida (5 valores por defecto)
- **Diferencias vs Ganador**: Cálculo automático para productos no adjudicados
  - Columna Dif. $ (diferencia en pesos)
  - Columna Dif. % (diferencia porcentual)
  - Visible en tabla de productos de Gestión
  - Visible en modal de edición de producto
- **Dashboard Mejorado**: 6 indicadores en lugar de 4
  - Unidades Cotizadas
  - Unidades Ganadas
  - % Unidades Ganadas
  - Total Cotizado
  - Total Ganado
  - % Dinero Ganado
- **Formato MILL**: Montos ≥1M se muestran en formato millones
  - Ejemplo: $200.000.000,00 → $200,00 MILL
  - Aplicado en Dashboard y Gestión
- **Campos v2.0 en Licitaciones**:
  - portal_origen (catálogo)
  - modalidad_entrega (catálogo)
  - forma_pago (catálogo)
  - requiere_poliza (boolean)
  - monto_poliza (decimal)
  - observaciones (texto)
- **Organismo en Clientes**: Campo organismo_jurisdiccion
  - Catálogo configurable
  - Auto-completa en nueva licitación al seleccionar cliente
- **Total Cotizado**: Nueva columna en Gestión de Licitaciones
  - Suma de precio_ofertado × cantidad de todos los productos
  - Formato argentino con notación MILL
- **Total $ por Producto**: Nueva columna en detalle de productos
  - Muestra precio_ofertado × cantidad
  - Formato argentino con notación MILL
- **Agregar Productos**: Botón en modal de detalle de licitación
  - Permite agregar productos a licitaciones existentes
  - Modal reutiliza formulario de edición en modo "crear"
- **Notificaciones Custom**: Reemplazo de alert() nativo
  - Modal estilizado acorde al diseño
  - Títulos con íconos (✓ Éxito, ✗ Error)
  - Botón Aceptar centrado

### Mejorado
- **Modales Modernizados**: Rediseño completo de todos los modales
  - Secciones agrupadas con fondo var(--bg-dark)
  - Títulos centrados en color primario
  - Inputs más grandes (16px font, 12px padding)
  - Botones con flex y espaciado consistente
  - Modal de cliente ampliado a 800px
- **Scrollbars Personalizados**: Estilo moderno en toda la aplicación
  - Color primario en thumb
  - Bordes redondeados
  - Efecto hover
  - Aplicado globalmente
- **Formulario Nueva Licitación**: Rediseño completo
  - Secciones agrupadas con títulos
  - Productos en cards individuales
  - Botón eliminar en esquina superior derecha
  - Alerta de margen integrada por producto
  - Espaciado mejorado
- **Tabla Catálogo Productos**: Mejoras de usabilidad
  - Scroll lateral desde arriba (overflow-x)
  - Header sticky al hacer scroll vertical
  - Columna Costo Unitario
  - Columna Acciones con botón Editar
- **Lógica de Resultado**: Comportamiento mejorado
  - "Adjudicado": Auto-completa Oferente="Ganada", Marca=Marca Ofrecida, Precio=Precio Ofertado, deshabilita campos
  - "No Adjudicado": Habilita y requiere todos los campos, muestra dropdown Motivo Pérdida
  - "Parcial": Habilita campos sin requerirlos
  - Resultado por defecto cambiado a "Parcial"
- **Marca Ofrecida**: Valor por defecto "Celtyc" (marca del cliente)
- **Fecha en Catálogo**: Se mantiene al editar (no se reinicia)
  - Conversión automática dd/mm/yyyy ↔ yyyy-mm-dd
  - Campo habilitado para edición manual

### Corregido
- **Consolidación de Base de Datos**: Resuelto problema de múltiples archivos
  - Consolidado a database/licitaciones.db
  - Migrados todos los datos
  - Eliminados duplicados
- **Referencia USE_POSTGRES**: Corregido en endpoints de catálogo
  - Cambiado db.USE_POSTGRES a USE_POSTGRES
  - Endpoints POST y PUT de /api/catalogo
- **Endpoint Métricas**: Agregado en base.html
  - Enlace funcional en menú lateral
  - Template usando base.html correctamente
- **Motivos Pérdida**: Endpoints 404 resueltos
  - Métodos CRUD agregados en db_manager.py
  - Endpoints API agregados en app.py
  - Tabla motivos_perdida creada con 5 valores por defecto

### Seguridad
- Parametrización de todas las consultas SQL
- Validación de entrada en backend
- Sanitización de datos de usuario
- Manejo seguro de errores con try-catch
- Variables de entorno para credenciales

### Base de Datos
- **Nuevas Tablas**:
  - portales_origen (id, nombre, activo)
  - modalidades_entrega (id, nombre, activo)
  - formas_pago (id, nombre, activo)
  - organismos_jurisdiccion (id, nombre, activo)
  - motivos_perdida (id, nombre, activo)
- **Nuevas Columnas en licitaciones**:
  - portal_origen, modalidad_entrega, forma_pago
  - requiere_poliza, monto_poliza, observaciones
- **Nuevas Columnas en productos**:
  - motivo_perdida
- **Nuevas Columnas en clientes**:
  - organismo_jurisdiccion
- **Nuevas Columnas en celty**:
  - costo_unitario

## [1.0.0] - 2025-01-20

### Agregado
- Sistema completo de gestión de licitaciones farmacéuticas
- Dashboard con estadísticas en tiempo real
- Módulo de ingreso de nueva licitación
- Módulo de gestión de licitaciones existentes
- Módulo de administración (CRUD completo)
- Catálogo integrado de productos Celty
- Gestión de clientes, oferentes, marcas, tipos de licitación
- Carga masiva desde Excel
- Formato argentino de precios (punto miles, coma decimal)
- Paginación en todas las tablas
- Histórico de precios con filtros
- Tema claro/oscuro
- Soporte SQLite (local) y PostgreSQL (producción)
- Despliegue en Render.com

### Características Iniciales
- CRUD completo de licitaciones y productos
- Búsqueda y filtros avanzados
- Validación de datos
- Interfaz responsive
- API REST interna
- Manejo de errores robusto

[1.1.0]: https://github.com/Jorge-Loyo/Licitarte/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Jorge-Loyo/Licitarte/releases/tag/v1.0.0
