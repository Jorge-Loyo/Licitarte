-- Script para limpiar la tabla de monodrogas antes de recargar el catálogo
-- Ejecutar en PostgreSQL o SQLite según corresponda

-- Para PostgreSQL:
TRUNCATE TABLE monodrogas RESTART IDENTITY CASCADE;

-- Para SQLite (comentar la línea de arriba y descomentar estas):
-- DELETE FROM monodrogas;
-- DELETE FROM sqlite_sequence WHERE name='monodrogas';
