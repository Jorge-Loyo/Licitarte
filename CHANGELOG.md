# Changelog - Licitarte

## [1.0.0] - 2025-01-XX

### ✨ Características Principales

#### Gestión de Licitaciones
- Crear licitaciones con múltiples productos
- Selección de productos desde catálogo Celty integrado
- Auto-completado de monodroga capitalizada
- Auto-completado de marca ofrecida desde laboratorio
- Editar licitaciones (N°, Cliente, Tipo, Fecha)
- Editar productos individuales
- Eliminar licitaciones completas
- Columna "Ganancia" muestra items adjudicados/total (ej: 3/5)

#### Dashboard
- Estadísticas en tiempo real:
  - Total licitaciones
  - Licitaciones ganadas
  - Total unidades
  - Precio promedio ponderado
- Histórico de precios con búsqueda por monodroga
- Productos adjudicados con paginación (5 por página)
- Histórico con paginación (5 por página)

#### Administración
- **Clientes**: CRUD completo con carga masiva Excel
  - Campos: nombre, razón social, CUIT, dirección, teléfono, email
- **Oferentes**: CRUD completo con carga masiva Excel
- **Marcas**: CRUD completo con carga masiva Excel
- **Tipos de Licitación**: CRUD completo con carga masiva Excel
- **Catálogo Celty**: Visualización y búsqueda completa
  - Carga masiva desde Excel
  - Agregar productos manualmente
  - Formato argentino de precios

#### Interfaz
- Tema claro/oscuro
- Diseño responsive
- Paginación en todas las tablas
- Búsqueda y filtros avanzados
- Formato argentino de precios (punto miles, coma decimal)

### 🗄️ Base de Datos
- Soporte SQLite (desarrollo local)
- Soporte PostgreSQL (producción)
- Migración automática en producción
- Tablas: clientes, oferentes, marcas, tipos_licitacion, licitaciones, productos, celty

### 🚀 Despliegue
- Configuración para Render.com
- Variables de entorno
- Script de inicialización para producción
- Gunicorn como servidor WSGI

### 🔒 Seguridad
- SECRET_KEY único por entorno
- Validación de datos de entrada
- Protección contra SQL injection
- Manejo seguro de errores

### 📚 Documentación
- README completo
- Manual de usuario integrado
- Guía de despliegue
- Changelog

---

## Notas de Versión

**Versión 1.0.0** es la primera versión estable de Licitarte, lista para uso en producción.

### Próximas Mejoras (v1.1.0)
- Exportación a Excel/PDF
- Reportes personalizados
- Gráficos y análisis avanzados
- Notificaciones
- Historial de cambios (audit log)

---

**Autor**: Jorge  
**Fecha**: Enero 2025  
**Licencia**: Propietario - Todos los derechos reservados
