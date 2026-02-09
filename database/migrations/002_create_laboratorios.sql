-- Migración 002: Crear tabla laboratorios
-- Versión: 1.2.0
-- Fecha: 2025-02-08

CREATE TABLE IF NOT EXISTS laboratorios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cod TEXT NOT NULL,
    laboratorio TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_laboratorio_cod ON laboratorios (cod);