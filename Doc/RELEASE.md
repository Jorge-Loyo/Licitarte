# Release v1.1.0 - Guía de Publicación

## Pre-requisitos

- [ ] Todos los cambios commiteados
- [ ] Base de datos migrada (migrate_v2.py, migrate_catalogos.py, migrate_organismos.py, add_motivo_perdida.py)
- [ ] Tests manuales completados
- [ ] README.md actualizado
- [ ] CHANGELOG.md actualizado
- [ ] ayuda.html actualizado

## Checklist de Seguridad

### Validación de Entrada
- [x] Parametrización de consultas SQL (prevención SQL injection)
- [x] Validación de tipos de datos en backend
- [x] Sanitización de strings en formularios
- [x] Validación de rangos numéricos (cantidad > 0, precio >= 0)
- [x] Validación de longitud de strings

### Manejo de Errores
- [x] Try-catch en todas las operaciones de DB
- [x] Mensajes de error genéricos al usuario
- [x] Logging de errores en servidor
- [x] Rollback de transacciones en caso de error

### Autenticación y Autorización
- [ ] ⚠️ NO IMPLEMENTADO - Sistema single-user local
- [ ] Considerar para v2.0 si se requiere multi-usuario

### Configuración
- [x] SECRET_KEY único por entorno
- [x] Variables de entorno para credenciales
- [x] DATABASE_URL para PostgreSQL en producción
- [x] Debug mode deshabilitado en producción

## Checklist de Escalabilidad

### Base de Datos
- [x] Índices en columnas frecuentes (numero_licitacion, cliente_id, licitacion_id, resultado)
- [x] Context managers para conexiones
- [x] Soporte PostgreSQL para producción
- [x] Paginación en todas las tablas
- [x] COALESCE para valores NULL

### Performance
- [x] Carga lazy de catálogos
- [x] Paginación frontend (10-5 items por página)
- [x] Queries optimizadas con JOINs
- [x] Caché de catálogos en memoria (JavaScript)

### Arquitectura
- [x] Separación frontend/backend
- [x] API REST interna
- [x] Modularización de código
- [x] Reutilización de componentes (modales, notificaciones)

## Pasos de Release

### 1. Preparación Local

```bash
# Verificar versión
cat VERSION  # Debe mostrar 1.1.0

# Verificar migraciones
cd database
python migrate_v2.py
python migrate_catalogos.py
python migrate_organismos.py
python add_motivo_perdida.py

# Verificar que no hay errores
cd ../web
python app.py
# Probar manualmente todas las funcionalidades
```

### 2. Git

```bash
# Commit final
git add .
git commit -m "Release v1.1.0 - Análisis de márgenes y métricas avanzadas"

# Tag
git tag -a v1.1.0 -m "Version 1.1.0

Novedades:
- Análisis de márgenes con alertas visuales
- Módulo de métricas con ranking de pérdidas
- Diferencias $ y % vs ganador
- Catálogos dinámicos configurables
- Dashboard con 6 indicadores
- Formato MILL para montos grandes
- Gestión de costos unitarios
- UI modernizada"

# Push
git push origin main
git push origin v1.1.0
```

### 3. Despliegue a Producción (Render.com)

```bash
# Render detectará el push y desplegará automáticamente

# Verificar variables de entorno en Render:
DATABASE_URL=postgresql://...
SECRET_KEY=...
FLASK_ENV=production
PORT=5000
```

### 4. Migraciones en Producción

```bash
# Conectar a shell de Render
# Ejecutar migraciones si es primera vez:
cd database
python migrate_v2.py
python migrate_catalogos.py
python migrate_organismos.py
python add_motivo_perdida.py
```

### 5. Verificación Post-Deploy

- [ ] Aplicación accesible en URL de producción
- [ ] Dashboard carga correctamente con 6 indicadores
- [ ] Nueva licitación muestra análisis de margen
- [ ] Gestión muestra diferencias $ y %
- [ ] Módulo Métricas funciona
- [ ] Administración muestra 9 catálogos
- [ ] Catálogo productos tiene costo_unitario
- [ ] Formato MILL funciona en montos grandes
- [ ] Notificaciones custom funcionan
- [ ] Scrollbars personalizados visibles

### 6. Comunicación

```markdown
# Anuncio v1.1.0

🎉 Nueva versión de Licitarte disponible!

## Novedades v1.1.0

### Análisis de Rentabilidad
- Alertas visuales al cotizar (rojo/amarillo/verde)
- Cálculo automático de margen vs costo
- Gestión de costos unitarios en catálogo

### Métricas Avanzadas
- Ranking de causas de pérdidas
- Diferencias promedio $ y % vs ganador
- Análisis de competitividad

### Mejoras de Gestión
- 6 indicadores en Dashboard
- Diferencias $ y % por producto no adjudicado
- Total cotizado por licitación
- Agregar productos a licitaciones existentes

### Catálogos Configurables
- Portales/Origen
- Modalidades de Entrega
- Formas de Pago
- Organismos/Jurisdicción
- Motivos de Pérdida

### Interfaz Modernizada
- Modales rediseñados con secciones
- Notificaciones custom
- Scrollbars personalizados
- Formato MILL para montos grandes

Ver CHANGELOG.md para detalles completos.
```

## Rollback (si es necesario)

```bash
# Revertir a v1.0.0
git checkout v1.0.0

# O revertir commit
git revert HEAD

# Push
git push origin main
```

## Notas Adicionales

### Compatibilidad
- Compatible con v1.0.0 (migraciones aditivas)
- No requiere borrar datos existentes
- Nuevos campos tienen valores por defecto

### Datos de Prueba
- 5 motivos de pérdida por defecto
- 5 organismos por defecto
- 3 portales por defecto
- 3 modalidades por defecto
- 3 formas de pago por defecto

### Limitaciones Conocidas
- Análisis de margen requiere costo_unitario cargado
- Excel no actualiza costo_unitario (solo manual)
- Sistema single-user (sin autenticación)

## Soporte

Para issues o preguntas:
- GitHub Issues: https://github.com/Jorge-Loyo/Licitarte/issues
- Email: soporte@licitarte.com

---

**Versión:** 1.1.0  
**Fecha:** 26 de Enero de 2025  
**Autor:** Jorge - Licitarte
