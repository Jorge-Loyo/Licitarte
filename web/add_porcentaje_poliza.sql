-- Agregar columna porcentaje_poliza a tabla licitaciones
ALTER TABLE licitaciones ADD COLUMN IF NOT EXISTS porcentaje_poliza REAL;
