# Módulo Dashboard

## Descripción
Panel principal con estadísticas, métricas y análisis de licitaciones.

## Archivos
- `dashboard.html` - Vista con estadísticas y tablas
- `dashboard.js` - Lógica de carga y visualización

## Funcionalidades
- ✅ Estadísticas generales (unidades, montos, porcentajes)
- ✅ Histórico de productos con búsqueda
- ✅ Últimos productos adjudicados
- ✅ Paginación de resultados
- ✅ Formateo de moneda (millones)
- ✅ Actualización manual de datos

## Métricas Mostradas
- Unidades cotizadas vs ganadas
- Total cotizado vs ganado
- Porcentajes de éxito
- Histórico por monodroga
- Productos adjudicados recientes

## API Endpoints
- `GET /api/estadisticas`
- `GET /api/productos-adjudicados`
- `POST /api/historico`
