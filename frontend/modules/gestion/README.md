# Módulo Gestión

## Descripción
Listado y gestión de licitaciones existentes con filtros y acciones.

## Archivos
- `gestion.html` - Vista de listado
- `gestion.js` - Lógica de gestión
- `gestion_nueva.html` - Vista alternativa
- `gestion_nueva.js` - Lógica alternativa

## Funcionalidades
- ✅ Listado de licitaciones
- ✅ Filtros por estado, fecha, cliente
- ✅ Búsqueda por número
- ✅ Editar licitación
- ✅ Ver resultado
- ✅ Eliminar licitación
- ✅ Exportar datos

## Estados de Licitación
- Pendiente
- En proceso
- Adjudicada
- Perdida
- Cancelada

## API Endpoints
- `GET /api/licitaciones`
- `DELETE /api/licitaciones/:id`
