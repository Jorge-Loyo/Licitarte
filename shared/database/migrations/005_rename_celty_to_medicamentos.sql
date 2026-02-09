-- Migración 005: Renombrar tabla celty a medicamentos
-- Versión: 1.2.0
-- Fecha: 2025-01-27

-- Renombrar tabla celty a medicamentos
ALTER TABLE celty RENAME TO medicamentos;

-- Recrear índices con nuevo nombre
DROP INDEX IF EXISTS idx_celty_numero_registro;
DROP INDEX IF EXISTS idx_celty_monodroga;

CREATE INDEX IF NOT EXISTS idx_medicamentos_numero_registro ON medicamentos(numero_registro);
CREATE INDEX IF NOT EXISTS idx_medicamentos_monodroga ON medicamentos(monodroga);
