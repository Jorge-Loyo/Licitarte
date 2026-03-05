# Módulo Ingreso

## Descripción
Formulario completo para crear nuevas licitaciones con productos, alternativas y cálculos automáticos.

## Archivos
- `ingreso.html` - Formulario principal
- `ingreso.js` - Lógica principal (legacy)
- `ingreso-modular.js` - Versión modular
- `modules/` - Submódulos especializados

## Funcionalidades
- ✅ Datos de licitación (número, fecha, cliente, tipo)
- ✅ Gestión de productos con alternativas
- ✅ Búsqueda en catálogo
- ✅ Cálculo automático de márgenes
- ✅ Gestión de póliza de garantía
- ✅ Carga de pliegos (PDF, imágenes)
- ✅ Vista previa de oferta
- ✅ Descarga de PDF
- ✅ Modales para crear entidades rápidas

## Submódulos
- `alternativas-manager.js` - Gestión de alternativas
- `calculos.js` - Cálculos de precios y márgenes
- `data-loader.js` - Carga de datos maestros
- `producto-manager.js` - Gestión de productos
- `validaciones.js` - Validaciones de formulario

## Cálculos Automáticos
- Precio total por producto
- Margen de ganancia ($ y %)
- Monto de póliza según porcentaje
- Totales generales

## API Endpoints
- `POST /api/licitaciones`
- `GET /api/clientes`
- `GET /api/tipos-licitacion`
- `GET /api/catalogo`
